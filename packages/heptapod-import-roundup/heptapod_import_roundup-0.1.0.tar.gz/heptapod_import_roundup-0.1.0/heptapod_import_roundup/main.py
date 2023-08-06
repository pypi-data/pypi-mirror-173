# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import argparse
import logging
from pathlib import Path
import pdb
import sys

from .importer import RoundupImporter

API_MODES = ('sudo',
             )


def add_src_target_args(argparser):
    grp = argparser.add_argument_group("Source and target arguments")
    grp.add_argument("dsn", help="PostgreSQL DSN (connection string) to "
                     "the roundup database. Full read-only access is "
                     "required.")
    grp.add_argument("files_path", help="Path to the Roundup files "
                     "hierarchy "
                     "(typically the files/home/roundup/db/files "
                     "subdirectory of a backup)"
                     )
    grp.add_argument("project_url", help="URL of the Heptapod project "
                     "to import into.")
    return grp


def add_running_args(argparser):
    grp = argparser.add_argument_group("Running options")
    grp.add_argument("--logging-level", default='INFO')
    grp.add_argument("--pdb", action="store_true",
                     help="Invoke a pdb post-mortem debugger on uncatched "
                     "exceptions.")
    return grp


def add_issue_selection_args(argparser):
    grp = argparser.add_argument_group("Issue selection options")
    grp.add_argument('--start', type=int, default=1,
                     help="First issue to start at")
    grp.add_argument('--stop', type=int,
                     help="Last issue to import")
    return grp


def add_user_args(argparser):
    grp = argparser.add_argument_group("Users and project membership options")
    grp.add_argument('--users-create', action="store_true",
                     help="Create missing users. "
                     "Roundup users are identified by comparing their "
                     "email addresses with all primary and secondary "
                     "addresses in the Heptapod database.")
    grp.add_argument('--initial-labels-fallback-user',
                     help="(email). If issue creator does not have "
                     "the access level to set labels, use this user "
                     "instead. If this option is not set, "
                     "creators of issues with labels will be given "
                     "explicit membership, at the Reporter role")
    return grp


def add_api_args(argparser):
    grp = argparser.add_argument_group("Heptapod API options")
    grp.add_argument("--api-mode", default="sudo", choices=API_MODES,
                     help="Heptapod API mode, one of %r" % API_MODES)
    grp.add_argument('--sudo-token', help="Personal access token "
                     "of an Administrator of the Heptapod instance, "
                     "having the `sudo` and `api` API scopes")


def setup_logging(cl_args):
    logging.basicConfig(
        level=getattr(logging, cl_args.logging_level.upper()),
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )


def do_import(importer, with_pdb=False):
    try:
        importer.validate_pg_connection()
        importer.import_project_labels()
        importer.import_issues()
    except Exception:
        if with_pdb:
            pdb.post_mortem(sys.exc_info()[2])
        raise


def main():
    parser = argparse.ArgumentParser()
    add_src_target_args(parser)
    add_api_args(parser)
    add_issue_selection_args(parser)
    add_user_args(parser)
    add_running_args(parser)
    cl_args = parser.parse_args()

    setup_logging(cl_args)
    if cl_args.api_mode == 'sudo':
        importer = RoundupImporter.sudo_importer(
            postgresql_dsn=cl_args.dsn,
            files_path=Path(cl_args.files_path),
            project_url=cl_args.project_url,
            sudo_token=cl_args.sudo_token,
            auto_create_users=bool(cl_args.users_create),
            start=cl_args.start,
            stop=cl_args.stop,
        )
    do_import(importer, with_pdb=cl_args.pdb)
