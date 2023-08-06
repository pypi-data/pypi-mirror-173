# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import ast
from contextlib import contextmanager
from functools import cached_property
import itertools
import logging
from urllib.parse import (
    urlparse,
    urlunparse,
)

import psycopg

from gitlab.const import AccessLevel
from heptapod_api_import.api import (
    GitLab,
    GitLabSudoAPI,
)
from heptapod_api_import.issues import IssuesImporter
from heptapod_api_import.labels import LabelsImporter
from heptapod_api_import.objects import GitLabObjectHandle
from heptapod_api_import.user_mapping import EmailUserMapping

logger = logging.getLogger(__name__)

REPORTER = AccessLevel.REPORTER

_missing = object()  # marker for get, pop etc.


def format_escape(s):
    """Escaping for Python's string format() method.

    Quoting the official doc at
      https://docs.python.org/3.8/library/string.html#format-string-syntax:

    Anything that is not contained in braces is considered literal text,
    which is copied unchanged to the output. If you need to include a brace
    character in the literal text, it can be escaped by doubling: {{ and }}.
    """
    return s.replace('{', '{{').replace('}', '}}')


class RoundupImporter:
    """Main export/import class from Roundup

    Remarks and TODOs

    - special accounts: they have their own dedicated addresses:
        + Roundup admin
        + various bots (including CI)
      in all cases, they can be mapped either by using secondary Heptapod
      emails of human users, or by pre-creating them in the Heptapod instance.
    - datetimes: it seems that the `_creation` column is more or less
      automatic, so we can hope for a uniform behaviour.
      After a quick inspection (https://bugs.tryton.org/issue11212) it seems
      that the timestamp without timezone stored in the DB is in UTC. TODO
      check that more seriously.
    """

    # TODO make configurable etc.
    anonymous_user_email = 'anonymous.roundup@heptapod.example'
    anonymous_user_nickname = anonymous_user_email.split('@')[0]

    def __init__(self, api_cls, postgresql_dsn, files_path,
                 project_url, start=1, stop=None,
                 labels_fallback_user_email=None):
        self.postgresql_dsn = postgresql_dsn
        self.files_path = files_path
        parsed = urlparse(project_url)
        self.project_full_path = parsed.path.lstrip('/')
        heptapod_url = urlunparse((parsed.scheme, parsed.netloc, '',
                                   '', '', ''))
        self.gitlab = GitLab(heptapod_url)
        self.gitlab_multiple_api = api_cls(self.gitlab)
        self.labels_fallback_user_email = labels_fallback_user_email
        self.start = start
        self.stop = stop

        # TODO it can vary from one instance of roundup to the other
        # and seems to be defined in the "Open issues" query (`_url` column,
        # storing an URI query string). In my example:
        # "@columns=title,id,creation,creator,activity,actor,status,"
        # "assignedto,type&@sort=-type&@group=creation&"
        # "@filter=status,type&@pagesize=50&@startwith=0"
        # "&status=-1,1,2,3,4,5,6,7&type=1"
        self.open_statuses = (None, 1, 2, 3, 4, 5, 6, 7)
        self.user_emails = {}  # cache roundup user_id -> email address

    @classmethod
    def sudo_importer(cls, sudo_token, auto_create_users=False, **kwargs):
        importer = cls(api_cls=GitLabSudoAPI, **kwargs)
        importer.gitlab_multiple_api.gitlab.init_admin(sudo_token)
        importer.users_map = EmailUserMapping(
            admin_api=importer.gitlab.admin_api,
            create_missing=auto_create_users,
            src_user_exporter=importer.export_user,
            testing_mode=True,
        )
        return importer

    def export_user(self, email):
        if email == self.anonymous_user_email:
            nick = self.anonymous_user_nickname
            return dict(nickname=nick, fullname=nick)

        with self.pg_connection.cursor() as cr:
            cr.execute("SELECT _username, _realname, _creation "
                       "FROM _user "
                       "WHERE _address=%s", [email])
            row = cr.fetchone()
            # TODO handle nickname collisions (should be done in generic part)
            data = dict(nickname=row[0],
                        fullname=row[1],
                        )
            # TODO another chapter in the problems with the admin account
            # (the `admin` username is reserved in GitLab, and indeed
            # unacceptable in this case)
            if data['nickname'] == 'admin' and data['fullname'] is None:
                data['nickname'] = 'roundup-admin'
                data['fullname'] = "Roundup Admin"
            if data['fullname'] is None:
                data['fullname'] = data['nickname']
            return data

    @cached_property
    def pg_connection(self):
        return psycopg.connect(self.postgresql_dsn)

    @cached_property
    def project_id(self):
        # TODO should not need an admin connection to do that
        # but we cannot assume anything to be in :attr:`users_map` yet
        return self.gitlab.admin_api.projects.get(self.project_full_path).id

    @property
    def project_handle(self):
        return GitLabObjectHandle('project', self.project_id)

    @property
    def labels_fallback_user(self):
        email = self.labels_fallback_user_email
        return None if email is None else self.users_map.get(email)

    def validate_pg_connection(self):
        with self.pg_connection.cursor() as cr:
            cr.execute("SELECT count(*) FROM _issue")
            logger.info("Connection to roundup PostgreSQL database ok. "
                        "Total number of issues: %d", cr.fetchone()[0])

    def import_project_labels(self):
        importer = LabelsImporter(self.gitlab_multiple_api,
                                  roles_manager=lambda handle: 'root')  # TODO
        logger.info("Importing missing labels for project %s",
                    self.project_full_path)
        self.extract_roundup_components()
        logger.info("Found %d Roundup components to map as GitLab labels.",
                    len(self.component2label))
        self.extract_roundup_statuses()
        logger.info("Found %d Roundup status values to map as GitLab labels.",
                    len(self.status2label))

        labels = []

        for lab in itertools.chain(self.status2label.values(),
                                   self.component2label.values(),
                                   ):
            lab = lab.copy()
            lab['username'] = self.users_map.get(lab.pop('creator_email'))
            labels.append(lab)

        importer.ensure_project_labels(self.gitlab.admin_username,
                                       self.project_id,
                                       labels)

    def import_issues(self):
        importer = IssuesImporter(self.gitlab_multiple_api,
                                  roles_manager=lambda handle: 'root')  # TODO

        importer.start(self.project_id)
        for issue, properties in self.extract_issues():
            logger.info("Import issue %d" % issue['iid'])
            issue['project_id'] = self.project_id
            username = self.users_map.get(issue.pop('creator_email'))
            issue['username'] = username
            # TODO issue type (crash, security, behavior, performance,
            #                  feature request)
            issue['events'] = []
            # Roundup issues have no initial labels, everything
            # happens in subsequent events. Erm no!

            events = self.extract_issue_events(importer, issue['iid'],
                                               properties)

            event_msgids = set(event['data'].pop('msg_id')
                               for event in events
                               if event['type'] == 'comment')
            creation_msgids = [i for i in issue.pop('message_ids')
                               # current query gives [None] if there are
                               # no messages
                               if i not in event_msgids and i is not None]
            if len(creation_msgids) > 1:
                raise RuntimeError("Issue %d has more that one message "
                                   "outside of events." % issue['iid'])

            if creation_msgids:
                issue['description'] = self.extract_message(
                    creation_msgids[0])['body']
            else:
                issue['description'] = ''

            assigned_id = properties['assignedto']
            if assigned_id is not None:
                issue['assignees'] = [self.gitlab_username(assigned_id)]

            issue['events'] = events
            issue['attachments'] = self.extract_attachments(issue['iid'])
            importer.import_issue(issue,
                                  attachments_header=(
                                      '\n\n'
                                      '## Files\n'
                                      'Download|Creator|Timestamp|Type\n'
                                      '---|---|---|---\n'
                                      ))

    def extract_roundup_components(self):
        self.component2label = {}
        with self.pg_connection.cursor() as cr:
            # as of Roundup 2.1.0, `(__retired__, _name)` is unique,
            # but `_name` itself is not, hence there can be at most two
            # occurrences, if component was retired and then created again.
            # Of course `id` is primary key.
            cr.execute("SELECT c.id, c._name, c.__retired__, c._creation, "
                       "       u._address "
                       "FROM _component c, _user u "
                       "WHERE u.id=c._creator "
                       "ORDER BY c.__retired__ ASC "
                       )
            seen = set()
            for row in cr.fetchall():
                comp_id, name, retired, creation_dt, creator_email = row
                if retired and name in seen:
                    name = name + '_retired'

                label_name, label_color = self.component_label_name_color(name)
                self.component2label[comp_id] = dict(
                    name=label_name,
                    color=label_color,
                    creator_email=creator_email,
                    created_at=creation_dt)

    def component_label_name_color(self, component):
        """Return name and color of label for a component.

        Can be overridden by project-specific importers
        """
        return 'component::' + component, 'green'

    def extract_roundup_statuses(self):
        self.status2label = {}
        with self.pg_connection.cursor() as cr:
            # see comment about __retired__ in extract_roundup_components()
            # TODO factorization of this logic?
            cr.execute("SELECT s.id, s._name, s.__retired__, s._creation, "
                       "       u._address "
                       "FROM _status s, _user u "
                       "WHERE u.id=s._creator "
                       "ORDER BY s.__retired__ ASC"
                       )
            seen = set()
            for row in cr.fetchall():
                status_id, name, retired, creation_dt, creator_email = row
                if retired and name in seen:
                    name = name + '_retired'

                self.status2label[status_id] = dict(
                    name='status::' + name,
                    # TODO validate same color for all statuses? And
                    # (really) choose it.
                    color='blue',
                    creator_email=creator_email,
                    created_at=creation_dt)

    def extract_issues(self):
        # TODO batching
        with self.pg_connection.cursor() as cr:
            # TODO priority
            # TODO type
            # TODO there were creation labels, but they don't show up
            # in the journal, they have to be inferred (yay)
            i_query = ("SELECT u._address, "
                       "       i.id, i._title, "
                       "       i._creation, i._activity, "
                       "       array_agg(i2comp.linkid), "
                       "       array_agg(i2msg.linkid), "
                       "       i._status, "
                       # not resolving _assignedto as email address because
                       # we'll have (non joinable) numeric ids in the journal
                       # anyway
                       "       i._assignedto, "
                       "       i._priority "
                       "FROM _issue i "
                       "LEFT JOIN issue_component i2comp "
                       "       ON i2comp.nodeid=i.id "
                       "LEFT JOIN issue_messages i2msg "
                       "       ON i2msg.nodeid=i.id "
                       "     JOIN _user u ON u.id = i._creator "
                       "WHERE i.id >= %s "
                       "GROUP BY i._creation, i._activity, "
                       "         u._address, i.id, i._title, i._creation "
                       "ORDER BY i.id "
                       )
            query_args = [self.start]
            if self.stop is not None:
                i_query += "LIMIT %s"
                query_args.append(self.stop - self.start + 1)
            cr.execute(i_query, query_args)

            rows = cr.fetchall()
        return [(dict(creator_email=row[0],
                      iid=row[1],
                      title=row[2],
                      created_at=row[3],
                      updated_at=row[4],
                      # TODO better query, curently multiple components
                      # give multiple lines to left join with messages, before
                      # the GROUP BY, hence it repeats message ids.
                      message_ids=set(row[6]),
                      ),
                 dict(component=set(row[5]),
                      status=row[7],
                      assignedto=row[8],
                      priority=row[9],
                      ),
                 ) for row in rows]

    @contextmanager
    def db_user_email_roles(self, user_id):
        with self.pg_connection.cursor() as cr:
            cr.execute("SELECT _address, _roles FROM _user WHERE id=%s",
                       [user_id])
            yield cr.fetchone()

    def user_email(self, user_id):
        if user_id is None:
            return None

        email = self.user_emails.get(user_id)
        if email is not None:
            return email

        with self.db_user_email_roles(user_id) as (email, roles):
            if email is None and roles == 'Anonymous':
                email = self.anonymous_user_email

            self.user_emails[user_id] = email
            return email

    def gitlab_username(self, roundup_user_id):
        return self.users_map.get(self.user_email(roundup_user_id))

    def extract_issue_events(self, importer, iid, properties):
        """Read the journal backwards.

        :param properties: the final values of properties, will be holding
          the initial values at the end of the process
        :return: Heptapod events
        """
        events = []
        with self.pg_connection.cursor() as cr:
            # tag is actually the id of the user responsible for the event (!)
            cr.execute("SELECT u._address, j.params, j.date "
                       "FROM issue__journal j, _user u "
                       "WHERE nodeid=%s AND action='set' "
                       "  AND u.id = j.tag::int "
                       "ORDER BY j.date DESC", [iid])
            journal = cr.fetchall()
            roundup_events = self.rewind_journal(journal, properties)
            for event_nr, roundup_event in enumerate(roundup_events):
                changes = roundup_event['changes']
                username = roundup_event['username']
                event_dt = roundup_event['event_dt']

                for msg_change in changes.get('messages', ()):
                    if msg_change[0] == '+':
                        for msg_id in msg_change[1]:
                            # message extraction is postponed at the end
                            # TODO events can perform several actions,
                            # such as adding a message and an attachment
                            events.append(dict(type='comment',
                                               datetime=event_dt,
                                               data=int(msg_id)))

                add_labels = []
                remove_labels = []
                for comp_change in changes.get('component', ()):
                    change_labels = (self.component2label[int(cid)]['name']
                                     for cid in comp_change[1])
                    if comp_change[0] == '+':
                        dest = add_labels
                    elif comp_change[0] == '-':
                        dest = remove_labels
                    dest.extend(change_labels)

                old_open = new_open = None
                status_change = changes.get('status')
                if status_change is not None:
                    old_status, new_status = status_change
                    old_open = old_status in self.open_statuses
                    new_open = new_status in self.open_statuses
                    if old_status is not None:
                        old_status_label = (
                            self.status2label[old_status]['name'])
                        remove_labels.append(old_status_label)
                    if new_status is not None:  # yes it happens
                        new_status_label = (
                            self.status2label[new_status]['name'])
                        add_labels.append(new_status_label)

                assign_change = changes.get('assignedto')
                if assign_change is None:
                    assignees = None
                else:
                    new_assignee = assign_change[1]
                    if new_assignee is None:
                        assignees = ()
                    else:
                        assignees = [self.gitlab_username(new_assignee)]

                # TODO general props_change event
                if add_labels or remove_labels or assignees is not None:
                    importer.ensure_role(username, REPORTER,
                                         self.project_handle)
                    if old_open and not new_open:
                        state_change = 'close'
                    elif new_open and not old_open:
                        state_change = 'reopen'
                    else:
                        state_change = None

                    events.append(
                        dict(type='change_labels',
                             data=dict(add_labels=add_labels,
                                       remove_labels=remove_labels,
                                       assignees=assignees,
                                       state_change=state_change,
                                       username=username,
                                       datetime=event_dt)))

        for event in events:
            if event['type'] == 'comment':
                event['data'] = self.extract_message(event['data'])
        return events

    def rewind_journal(self, journal, properties):
        """Read the journal backwards and rewind properties to initial values.

        :return: an iterable of events in order from the oldest to the latest.

        The properties are updated in place to their initial values.
        The returned events have pairs of values `(old, new)` for each
        univalued property.
        """
        events = []
        for event_nr, row in enumerate(journal):
            username = self.users_map.get(row[0])
            # Roundup uses eval(), see roundup.anypy.strings.eval_import()
            # literal_eval is less of a security nightmare, but can still
            # crash the interpreter.
            params = ast.literal_eval(row[1])

            # univalued properties
            for prop in ('status', 'assignedto', 'priority'):
                prev = params.pop(prop, _missing)
                if prev is _missing:
                    continue

                if prev is not None:
                    prev = int(prev)
                params[prop] = (prev, properties[prop])
                properties[prop] = prev

            # mutivalued properties
            for prop in ('component',
                         ):
                changes = params.get(prop)
                if changes is None:
                    continue

                values = properties[prop]
                for change in changes:
                    ids = (int(cid) for cid in change[1])
                    if change[0] == '+':
                        values.difference_update(ids)
                    if change[0] == '-':
                        values.update(ids)

            events.append(dict(username=username,
                               changes=params,
                               event_dt=row[2],
                               ))

        events.reverse()
        return events

    def extract_message(self, msg_id):
        with self.pg_connection.cursor() as cr:
            # tag is actually the id of the user responsible for the event (!)
            # TODO _inreplyto
            # TODO actual content: _summary is the first line and
            # the _content column is null. Message content is actually on disk
            # (/home/roundup/db/files/msg in our test data backup)
            cr.execute("SELECT u._address, m._date "
                       "FROM _msg  m, _user u "
                       "WHERE m.id=%s "
                       "  AND u.id = m._author ",
                       [msg_id])
            row = cr.fetchone()
            # TODO actual content mapping (conversion to Markdown?
            # keep changeset crossrefs in any case)
            return dict(
                # used for internal references, will be removed before
                # sending to the GitLab API
                msg_id=msg_id,
                username=self.users_map.get(row[0]),
                created_at=row[1],
                # TODO format conversion
                body=self.message_path(msg_id).read_text()
            )

    def message_path(self, msg_id):
        return self.files_path / 'msg' / str(msg_id // 1000) / f'msg{msg_id}'

    def extract_attachments(self, issue_id):
        # TODO attachments are created by events, which can also add
        # a message, hence we could turn them into Note attachments,
        # but it's dubious it would be much clearer because it is not
        # the way roundup presents them, hence it would look more different
        # from the original. Also there is a possibility to upload a file
        # and then withdraw it, which would be more complicated to
        with self.pg_connection.cursor() as cr:
            # TODO files can also be modified (date is _activity),
            # potentially by someone else (_actor)
            cr.execute("SELECT f.id, creator._address, "
                       "f._type, f._name, f._creation "
                       "FROM _file f, issue_files link, _user creator "
                       "WHERE link.linkid=f.id "
                       "  AND link.nodeid=%s "
                       "  AND creator.id=f._creator ",
                       [issue_id])
            attachments = []
            for row in cr.fetchall():
                path = self.file_path(row[0])
                creator = self.users_map.get(row[1])
                mime_type = row[2]
                file_name = row[3]
                creation_utc = row[4]
                renderer = "[%s]({url})|@%s|%s UTC|%s\n" % (
                    format_escape(file_name),
                    format_escape(creator), creation_utc, mime_type)
                attachments.append(dict(path=path,
                                        file_name=file_name,
                                        creator=creator,
                                        download_renderer=renderer,
                                        ))
            return attachments

    def file_path(self, file_id):
        return (self.files_path / 'file'
                / str(file_id // 1000)
                / f'file{file_id}')
