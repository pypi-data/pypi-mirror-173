from setuptools import setup, find_packages
from setuptools.command.install import install
import atexit
import os
import sys
from subprocess import check_call

VERSION = '1.3.0'
DESCRIPTION = 'PyGeBR - Processing flows made easy'
LONG_DESCRIPTION = 'Assemble, inspect, edit and run processing flows'

def _post_install():
    menusdir = './pygebr/menus'
    for sub in os.listdir(menusdir):
        menuspy = os.path.join(menusdir, sub, "menus.py")
        check_call(menuspy)

class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)

# Setting up
setup(
        name="pygebr",
        version=VERSION,
        author="Ricardo Biloti",
        author_email="<biloti@unicamp.br>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        cmdclass={'install': new_install},
        packages=find_packages(),
        include_packages_data=True,
        python_requires=">= 3.7.0",
        install_requires=[
            "colorama",
            "ipywidgets",
            "jsonschema >= 4.16",
            ],
        package_data={
            'pygebr': ['schema/*.schema',
                       'menus/*/menus.py',
                       'menus/*/*.json',
                       'docs/*'],
            },
        keywords=['seismic', 'processing flow'],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering",
            ])
