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

import ipywidgets as W

#-------------------------------------------------------------------------------
class Person:
    """Class used to represent someone to credit for.

Any program, flow or menu in PyGeBR may have authors, which
are represented as a list of Person.

Attributes
----------

json: dict
    Dictionary representing a person

widget: dict
    Dictionary holding an widget to edit person's attributes

name: str
    Person's name

email: str
    Person's email

institution: str
    Person's affiliation

homepage: str
    Person's or institution's website
"""

    def __init__ (self, json=None, name=None, email=None,
        institution=None, homepage=None):
        """
        Parameters
        ----------

        json: dictionary (optional)
            A dictionary to represent a person.

        name: str (optional)
            Person's name

        email: str (optional)
            Person's email

        institution: str (optional)
            Person's affiliation

        homepage: str (optional)
            Person's or institution's website
        """

        if json is None:
            self.json = {}
        else:
            if not isinstance(json, dict):
                raise Exception("Argument should be a dictionary")
            self.json = json

        self.widget = {}

        if not name is None:
            self.name(name)
        if not email is None:
            self.email(email)
        if not institution is None:
            self.institution(institution)
        if not homepage is None:
            self.homepage(homepage)

    def has_name (self):
        """
        Return whether a pearson has name set
        """

        return 'name' in self.json

    def name(self, value=None):
        """
        Set or return person's name

        Parameter
        ---------

        value: str (optional)
            value to set as person's name
        """
        if value is None:
            return self.json['name'] if self.has_name() else ""

        if not isinstance(value, str):
            raise Exception("Argument should be a string")

        if (not value) and 'name' in self.json:
            del self.json['name']
        else:
            self.json['name'] = value

    def has_email(self):
        """
        Return whether a pearson has email set
        """
        return 'email' in self.json

    def email(self, value=None):
        """
        Set or return person's email

        Parameter
        ---------

        value: str (optional)
            value to set as person's email
        """
        if value is None:
            return self.json['email'] if self.has_email() else ""

        if not isinstance(value, str):
            raise Exception("Argument should be a string")

        if (not value) and 'email' in self.json:
            del self.json['email']
        else:
            self.json['email'] = value

    def has_institution (self):
        """
        Return whether a pearson has institution set
        """
        return 'institution' in self.json

    def institution(self, value=None):
        """
        Set or return person's affiliation

        Parameter
        ---------

        value: str (optional)
            value to set as person's affiliation
        """
        if value is None:
            return self.json['institution'] if self.has_institution() else ""

        if not isinstance(value, str):
            raise Exception("Argument should be a string")

        if (not value) and 'institution' in self.json:
            del self.json['institution']
        else:
            self.json['institution'] = value

    def has_homepage (self):
        """
        Return whether a pearson has homepage set
        """
        return 'homepage' in self.json

    def homepage(self, value=None):
        """
        Set or return person's or institutions' website

        Parameter
        ---------

        value: str (optional)
            value to set as website
        """
        if value is None:
            return self.json['homepage'] if self.has_homepage() else ""

        if not isinstance(value, str):
            raise Exception("Argument should be a string")

        if (not value) and 'homepage' in self.json:
            del self.json['homepage']
        else:
            self.json['homepage'] = value

    def __str__(self):
        """
        Returns a multiline string, descring the person.
        """
        line = self.name()

        if self.has_email():
            if line:
                line = line + " "

            line = line + "<" + self.json['email'] +">"

        if line:
            line = line + "\n"

        if self.has_institution():
            line = line + self.institution() + "\n"

        if self.has_homepage():
            line = line + self.homepage() + "\n"

        return line[0:-1]

    def widget_construct(self):
        """
        Construct widget to edit person's attributes
        """

        if self.widget != {}:
            return

        self.widget['name'] = W.Text(placeholder="Name", value=self.name())
        self.widget['email'] = W.Text(placeholder="Email address", value=self.email())
        self.widget['institution'] = W.Text(placeholder="Institution", value=self.institution())
        self.widget['homepage'] = W.Text(placeholder="Homepage",value=self.homepage())

        self.widget['line'] = W.VBox([W.HBox([self.widget['name'],self.widget['email']]),
                         W.HBox([self.widget['institution'],self.widget['homepage']])],
                         layout=W.Layout(margin="0px 0px 10px 0px"))

    def w_get(self):
        """
        Set person's attributes from widget entries' value
        """

        self.name(self.widget['name'].value)
        self.email(self.widget['email'].value)
        self.institution(self.widget['institution'].value)
        self.homepage(self.widget['homepage'].value)

    def w_set(self):
        """
        Set widget entries' value from person's attributes
        """

        self.widget['name'].value = self.name()
        self.widget['email'].value = self.email()
        self.widget['institution'].value = self.institution()
        self.widget['homepage'].value = self.homepage()

    def w_line(self):
        """
        Return a widget to edit the person's attributes.
        The widget is meant to be included into a VBox.
        """
        if self.widget == {}:
            self.widget_construct()

        return self.widget['line']
