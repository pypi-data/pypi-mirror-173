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

import re
import ipywidgets as W
from .person import Person
from .param  import Param

#-------------------------------------------------------------------------------
class Prog:
    """Class used to represent a command line program

Attributes
----------

json: dict
    Dictionary representing a parameter

w: dict
    Dictionary holding an widget to edit programs's parameters

parlist: list of Param
    List of parameters which control the program behavior

authors: List of Person
    List of program's authors

title: str
    Program's title

description: str
    One-line description for the parameter purpose

executable: str
    Command to execute the program

stdin: boolean
    True if program reads from standar input

stdout: boolean
    True if program writes to standar output

stderr: boolean
    True if program writes to standar error

Below, in setter methods, providing "" as value has the effect to delete
the attribute. Note that a parameter has to have its type defined.
"""

    def __init__(self, json=None, title=None, description=None,
                 authors=None, url=None, executable=None,
                 stdin=True, stdout=True,stderr=True):
        """ Initiate a program from a JSON or empty otherwise.
        Some flow's properties may be further set.
        """

        self.parlist = []

        if json is None:
            self.json = {}

        else:
            if not isinstance(json, dict):
                raise TypeError("Argument should be a dictionary")

            self.json = json
            stdin = None
            stdout = None
            stderr = None

            # Construct the list of paramters from its json representation
            if 'parameters' in self.json:
                for parjs in self.json['parameters']:
                    self.parlist.append(Param(json = parjs))

        # Widgets for program
        self.w = {}

        if not title is None:
            self.title(title)
        if not description is None:
            self.description(description)
        if not authors is None:
            self.authors(authors)
        if not url is None:
            self.url(url)
        if not executable is None:
            self.executable(executable)
        if not stdin is None:
            self.stdin(stdin)
        if not stdout is None:
            self.stdout(stdout)
        if not stderr is None:
            self.stderr(stderr)

    def __str__(self):
        """
        Return a string to run the program from the
        command line, without resolving expressions though.

        To resolve expressions use self.eval().
        """

        cmdline = ""
        if self.has_executable():
            cmdline = self.executable()

        if self.has_parameters():
            for par in self.parameters():
                if not par.type() in ["section","comment"]:

                    if par.required() and not par.has_non_empty_value():
                        raise Exception("required parameter \'" + par.description() + "\' not set")

                    cmdline = " ".join([cmdline, str(par)]).strip()

        return cmdline

    def eval(self, params=None):
        """
        Return a string to run the program from the
        command line, resolving expressions.

        Parameter
        ---------

        param: dict (optional)
           Dictionary of variables to define local scope.
        """

        cmdline = ""
        if self.has_executable():
            cmdline = cmdline + self.executable()

        if self.has_parameters():
            for par in self.parameters():
                if not par.type() in ["section","comment"]:

                    if par.required() and not par.has_non_empty_value():
                        raise Exception("required parameter \'" + par.description() + "\' not set")

                    try:
                        parstr = par.eval(params)
                    except NameError as err:
                        raise NameError(str(err) + ", for program \'" + self.title() + "'")
                    except SyntaxError as err:
                        raise SyntaxError(str(err) + ", for program \'" + self.title() + "'" )
                    except ZeroDivisionError as err:
                        raise ZeroDivisionError(str(err) + ", for program \'" + self.title() + "'" )
                    except Exception as err:
                        raise Exception(str(err) + ", for program \'" + self.title() + "'" )

                    cmdline = " ".join([cmdline, parstr]).strip()

        return cmdline


    def has_title(self):
        """
        Return whether a program has title set
        """
        return 'title' in self.json

    def title(self, value=None):
        """
        Set or return program's title

        Parameter
        ---------

        value: (optinal)
            value to set program's title
        """
        if value is None:
            return self.json['title'] if self.has_title() else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if 'title' in self.json:
                del self.json['title']
        else:
            self.json['title'] = value

    def has_description(self):
        """
        Return whether a program has description set
        """
        return 'description' in self.json

    def description(self, value = None):
        """
        Set or return program's description

        Parameter
        ---------

        value: str (optinal)
            value to set program's description
        """
        if value is None:
            return self.json['description'] if self.has_description() else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if 'description' in self.json:
                del self.json['description']
        else:
            self.json['description'] = value

    def has_url(self):
        """
        Return whether a program has url set
        """
        return 'url' in self.json

    def url(self, value = None):
        """
        Set or return program's url

        Parameter
        ---------

        value: str (optinal)
            value to set program's url command
        """
        if value is None:
            return self.json['url'] if self.has_url() else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if 'url' in self.json:
                del self.json['url']
        else:
            self.json['url'] = value

    def has_executable(self):
        """
        Return whether a program has executable set
        """
        return 'executable' in self.json

    def executable(self, value = None):
        """
        Set or return program's executable

        Parameter
        ---------

        value: str (optinal)
            value to set program's executable command
        """
        if value is None:
            return self.json['executable'] if self.has_executable() else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if 'executable' in self.json:
                del self.json['executable']
        else:
            self.json['executable'] = value

    def has_authors(self):
        """
        Return whether a program has authors set
        """
        return 'authors' in self.json

    def authors(self, value=None):
        """
        Set or return program's authors.

        Parameter
        ---------

        value: List of Person (optinal)
            value to set program's authors
        """
        if value is None:
            if not self.has_authors():
                return []
            authorslist = []
            for item in self.json['authors']:
                authorslist.append(Person(item))
            return authorslist

        if not isinstance(value, list) and not isinstance(value, Person):
            raise TypeError("Argument should be a list of persons")

        if isinstance(value, Person):
            self.json['authors'] = [value.json]
        else:
            if len(value) == 0:
                del self.json['authors']
            else:
                self.json['authors'] = []
                for person in value:
                    if not isinstance(person, Person):
                        raise Exception("Authors should be a list of persons")
                    self.json['authors'].append(person.json)

    def authors_count(self):
        """
        Return number of persons in authors' list
        """
        return len(self.authors())

    def stdin(self, value=None):
        """
        Query or set stdin acceptance for program

        Parameter
        ---------

        value: boolean (optional)
            True if program reads from the standard input
        """
        if value is None:
            if 'io' in self.json:
                return self.json['io']['stdin']

            return False

        if not isinstance(value, bool):
            raise TypeError("Argument should be boolean")

        if 'io' not in self.json:
            self.json['io'] = {}

        self.json['io']['stdin'] = value

    def stdout(self, value=None):
        """
        Query or set stdout write capability for program

        Parameter
        ---------

        value: boolean (optional)
            True if the program writes to standard ouput
        """
        if value is None:
            if 'io' in self.json:
                return self.json['io']['stdout']

            return False

        if not isinstance(value, bool):
            raise TypeError("Argument should be boolean")

        if 'io' not in self.json:
            self.json['io'] = {}

        self.json['io']['stdout'] = value

    def stderr(self, value=None):
        """
        Query or set stderr write capability for program

        Parameter
        ---------

        value: boolean (optional)
            True if the program writes to standard error
        """
        if value is None:
            if 'io' in self.json:
                return self.json['io']['stderr']

            return False

        if not isinstance(value, bool):
            raise TypeError("Argument should be boolean")

        if 'io' not in self.json:
            self.json['io'] = {}

        self.json['io']['stderr'] = value

    def has_parameters(self):
        """
        Return whether a programa has parameter list set
        """
        return 'parameters' in self.json

    def parameters(self):
        """
        Return the parameter list
        """
        return self.parlist if self.has_parameters() else []

    def parameters_count(self):
        """
        Return the number of parameters for the program
        """
        return len(self.parlist)

    def parameter(self, ipar):
        """
        Return the ipar-th program's parameter

        Parameter
        ---------

        ipar: int
            Parameter index ranging from 0 to self.parameters_count()-1
        """
        return self.parlist[ipar]

    def parameter_lookup(self, keyword):
        """
        Return the index for the first parameter
        such that the provided keyword matches keyword.

        It's assumed that the keyword itself may be surrounded]
        by non alphanumeric characters. Therefore, "xs" matches
        with "xs=", "--xs", "-xs ", and so on, but it doesn't
        match with "ixs", "xscale" or "xs1".

        Parameter
        ---------

        keyword: str
            keyword to look for
        """

        pattern = re.compile(r'^\W*'+keyword+r'\W*$')

        for k in range(self.parameters_count()):
            if pattern.match(self.parameter(k).keyword()) is not None:
                return k

        return None

    def parameter_add(self, par):
        """
        Add a parameter to parameter's list for the program

        Parameter
        ---------

        par: Param
            Parameter to add
        """
        if not isinstance(par, Param):
            raise TypeError("Argument should be a Param")

        if len(self.parlist) == 0:
            self.json["parameters"] = []

        self.parlist.append(par)
        self.json["parameters"].append(par.json)

    def parameter_del(self, ipar):
        """
        Delete ipar-th parameter from parameter's list for the program

        Parameter
        ---------

        ipar: int
            Parameter index ranging from 0 to self.parameters_count()-1
        """
        self.json['parameters'].pop(ipar)
        self.parlist.pop(ipar)
        if len(self.parlist) == 0:
            del self.json['parameters']

    def widget(self, status):
        """
        Return a widget to represent the program

        Parameter
        ---------

        status: boolean
            True to set program as active
        """
        if self.w == {}:
            self.widget_construct(status)

        return self.w['main']

    def widget_construct(self,status):
        """
        Construct the widget

        Parameter
        ---------

        status: boolean
            True to set program as active
        """

        stack = []

        # Program's description
        linecontent = []
        if self.has_description():
            desc = W.Label(value=self.description())
            desc.add_class("prog_desc")
            linecontent.append(desc)

        # Link to authors' homepage
        if self.has_url():
            links = W.HTML(value='<a href="' + self.url() +
                           '" target="_blank">' +
                           '<i class="fa fa-external-link" aria-hidden="true"></i></a>')
            linecontent.append(links)

        if linecontent:
            stack.append(W.HBox(linecontent))

        # Active checkbox
        self.w['status'] = W.Checkbox(description="Enable this program in the flow",
                                      indent=False,
                                      layout = W.Layout(width="100%"),
                                      value = status)

        stack.append(W.HBox([self.w['status']]))

        inside = False
        first = True
        accordion = None
        has_required = False
        for par in self.parlist:
            has_required = has_required or par.required()
            if par.type() == 'section':
                accordion = par.w_line()
                stack.append(accordion)
                vbox = accordion.children[0]
                inside = True
                first = True
            else:
                if inside:
                    if first:
                        vbox.children = (par.w_line(),)
                        first = False
                    else:
                        vbox.children = vbox.children + (par.w_line(),)
                else:
                    stack.append(par.w_line())

        if has_required:
            footnote = W.Label(value="* required parameter")
            footnote.add_class("footnote")
            stack.append(footnote)
        self.w['main'] = W.VBox(stack)

    def widget_value_set(self):
        """
        Fill widget values from program/parameter's properties
        """

        for par in self.parameters():
            par.w_set()

    def widget_value_get(self):
        """
        Fill program/parameter's properties from widget's values
        """

        for par in self.parameters():
            par.w_get()
