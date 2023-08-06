from pathlib import Path
from setuptools import setup

MAIN_PACKAGE = 'heptapod_import_roundup'
VERSION_FILE = 'VERSION'
REQUIREMENTS_FILE = 'install-requirements.txt'


scripts = {  # name to (module in main package, function)
    'import-roundup': ('main', 'main'),
}


setup(
    name='heptapod_import_roundup',
    version=Path(MAIN_PACKAGE, VERSION_FILE).read_text().strip(),
    author='Georges Racinet',
    author_email='georges.racinet@octobus.net',
    url='https://foss.heptapod.net/heptapod/heptapod-api-import',
    description="Toolbox library for using the GitLab/Heptapod API for "
    "import use cases",
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    keywords='hg mercurial git heptapod gitlab',
    license='GPL3+',
    # do not use find_packages, as it could recurse into the Git and
    # Mercurial repositories
    packages=[MAIN_PACKAGE],
    package_data={MAIN_PACKAGE: [VERSION_FILE]},
    entry_points=dict(
        console_scripts=[
            '{name}={pkg}.{mod}:{fun}'.format(
                pkg=MAIN_PACKAGE, name=name, mod=mod, fun=fun)
            for name, (mod, fun) in scripts.items()],
    ),
    install_requires=Path(REQUIREMENTS_FILE).read_text().splitlines(),
)
