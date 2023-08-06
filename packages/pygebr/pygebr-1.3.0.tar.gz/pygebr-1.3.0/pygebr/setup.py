# This file is part of PyGeBR library.
#
# PyGeBR is a library to create, merge, edit, inspect and run
# processing flows. It was originally designed for seismic
# data processing, but it extends to other data as well.
#
# PyGeBR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyGeBR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyGeBR.  If not, see <https://www.gnu.org/licenses/>
#
# Copyright 2021-2022 Ricardo Biloti <biloti@unicamp.br>
#                     Eduardo Filpo <efilpo@gmail.com>
#

import os
import json as JSON
from .person import Person

class Setup:
    """A class used to setup basic configuration parameters for PyGeBR

An instance for this class can setup or query basic parameters
for PyGeBR, like the default author for new flows made from
menus as well as search path for menus.
"""

    def __init__ (self, authors = None, menudirs = None):
        """
        Loads a setup saved on $HOME/.config/pygebr/config.json
        or instantiate a new one.

        Parameters
        ---------
        authors: Person or list of Person (optional)
            When provided set the list of author.

        menudirs: str or list of str (optional)
            When provided set the list of search paths.
        """

        self.configDir = os.path.join(os.environ['HOME'],'.config/pygebr')
        if not os.path.isdir(self.configDir):
            os.mkdir(self.configDir)

        self.configFile = os.path.join(self.configDir,'config.json')
        if os.path.isfile(self.configFile):
            with open(self.configFile) as fp:
                self.config = JSON.loads(fp.read())
        else:
            self.config = {"authors": [], "menudirs": []}

        if authors is not None:
            self.authors(authors)

        if menudirs is not None:
            self.menudirs(menudirs)

    def __str__(self):
        """
        Print the setup.
        """

        output = ""
        for person in self.authors():
            output = output + str(person) + "\n"

        output = output + "\nLook up for menus in:\n"
        for path in self.menudirs():
            output = output + path + "\n"

        return output

    def authors(self, authors=None):
        """
        Set or returns default authors for new flows.

        Parameter
        ---------
        authors: Person or list of Person
        When provided, set default authors.
        """

        if authors is None:
            alist = []
            for p in self.config['authors']:
                alist.append(Person(json=p))
            return alist

        if isinstance(authors, list):
            people = []
            for person in authors:
                if isinstance(person, Person):
                    people.append(person.json)
                else:
                    raise TypeError("authors is not of type list of Person")

            self.config['authors'] = people
        else:
            if isinstance(authors, Person):
                self.config['authors'] = [authors.json]
            else:
                raise TypeError("authors is not of type Person")

    def menudirs(self, menudirs=None):
        """
        Set or returns default search paths for looking for menus.

        Parameter
        ----------
        menudirs: str or list of str
        When provided, set default search paths.
        """

        if menudirs is None:
            return self.config["menudirs"]

        if not isinstance(menudirs, list):
            raise TypeError("menudirs is not a list of path's")

        sysmenusdir = os.path.join(os.path.dirname(__file__),"menus")

        dirs = []

        for p in menudirs:
            dirs.append(p)

        for sub in os.listdir(sysmenusdir):
            dirs.append(os.path.join(sysmenusdir, sub))

        self.config['menudirs'] = dirs

    def save(self):
        """
        Save and apply the setup.

        The setup is save in $HOME/.config/pygebr/config.json.
        """
        with open(self.configFile,'w') as fp:
            fp.write(JSON.dumps(self.config))
