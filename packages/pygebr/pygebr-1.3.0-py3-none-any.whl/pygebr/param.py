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

import functools
import re
import ipywidgets as W

#-------------------------------------------------------------------------------
class Param:
    """Class used to represent a program parameter.

A program parameter can be of one of these types:
flag:
    a parameter that may or may not be present in command line

integer:
    a parameter that expects an integer value

float:
    a parameter that expects an float value

range:
    a parameter that expects value within an acceptable range

string:
    a parameter that expects an string

integers:
    a parameter that expects an array of integer values

floats:
    a parameter that expects an array of float values

strings:
    a parameter that expects an array of string values

file:
    a parameter that expects an file name

path:
    a parameter that expects a path

enum:
    a parameter that expects a value from an list of acceptable options

section:
    a metaparameter used only to group subsequent parameters inside section widget

comment:
    a metaparameter used only to add a line of comment in
    parameters list widget


Literal or expression
---------------------

A parameter's value can be represented by a literal value or by an
expression that has to be evaluated. An expression can employ variables
defined in global and local scopes.

Attributes
----------

json: dict
    Dictionary representing a parameter

widget: dict
    Dictionary holding an widget to edit parameter's attributes

type: str
    Parameter's type

keyword: str
    Keyword in command line used to set the parameter

description: str
    One-line description for the parameter purpose

value: (depending on parameter's type)
    Parameter's value

default: (depending on parameter's type)
    Paramter's default value used to fillin widget

required: boolean
    Flag to indicate whether the parameter is required by the program

multiple: boolean
    Flat to indicate whether the parameter can be provided multiple
    times in command line.

Below, in setter methods, providing "" as value has the effect to delete
the attribute. Note that a parameter has to have its type defined.
"""

    _boolean_types = ['flag']
    _scalar_types = ['enum','file','float','integer','path','range','string']
    _array_types = ['floats','integers','strings']
    _meta_types = ['section','comment']

    _instanciable_types = _scalar_types + _array_types
    _supported_types = _boolean_types + _scalar_types + _array_types + _meta_types

    def __init__(self, json=None, ptype=None, keyword=None, description=None,
                 required=False, multiple=False, separator=",", title=None,
                 placeholder=None, default=None, value=None):
        """
        Parameters
        ----------

        json: dictionary (optional)
            A dictionary to represent a parameter.

        ptype: str (optional)
            Parameter type.
            Acceptable values are

            'comment', 'enum', 'file', 'flag', 'float', 'floats', 'integer',
            'integers', 'path', 'range', 'section', 'string', or 'strings'.

        keyword: str (optional)
            Keyword to provide set the parameter in command line

        description: str (optional)
            One-line sentence describing the parameter's purpose

        required: boolean
            Flag indicating whether the parameter is required by the program

        multiple: boolean
            Flat to indicate whether the parameter can be provided multiple
            times in command line

        separator: str (optional)
            String used as separator between elements of arrays

        title: str (optional)
            Title for section-type parameter in widget

        placeholder: str (optional)
            Placeholder for parameter's entry in widget

        default: (optinal)
            Default value to fill in UI

        value: (optional)
            Value to set the parameter
        """

        if json is None:
            self.json = {}
        else:
            if not isinstance(json, dict):
                raise TypeError("Argument should be a dictionary")

            self.json = json
            required = None
            multiple = None

        # Widget
        self.widget = {}

        if ptype is not None:
            self.type(ptype)

        if 'type' not in self.json:
            raise Exception("Missing parameter type")

        if ptype == 'section':
            required = None
            multiple = None
            if title is not None:
                self.title(title)
            return

        if ptype == 'comment':
            required = None
            multiple = None
            if description:
                self.description(description)
            return

        if title is not None:
            raise Exception("Only section-type parameters admit title attribute")

        # Flag parameters can be provided only once
        if ptype == "flag":
            multiple = False
            required = None

        if keyword is not None:
            self.keyword(keyword)

        if description is not None:
            self.description(description)

        if multiple is not None:
            self.multiple(multiple)

        if default is not None:
            self.default(default)

        if value is not None:
            self.values(value)

        if required is not None:
            self.required(required)

        if (ptype in ['string','file','path'] + self._array_types):
            if placeholder is not None:
                self.placeholder(placeholder)
            elif ptype in self._array_types:
                self.placeholder("List of %s, separated by \"%s\""%(ptype, separator))

        if ptype in self._array_types:
            self.separator(separator)

    #-------------------------------------------------------------------------------------
    # "HAS" methods

    def has_default(self):
        """
        Return whether a parameter has default set
        """
        return 'default' in self.json

    def has_description(self):
        """
        Return whether a parameter has description set
        """
        return 'description' in self.json

    def has_filePattern(self):
        """
        Return whether a file parameter has pattern set
        """

        return 'filePattern' in self.json

    def has_fileType(self):
        """
        Return whether a file parameter has type set
        """

        return 'fileType' in self.json

    def has_keyword(self):
        """
        Return whether a parameter has keyword set
        """
        return 'keyword' in self.json

    def has_multiple(self):
        """
        Return whether a parameter has multiple attribute set
        """
        return 'multiple' in self.json

    def has_options(self):
        """
        Return whether a enum parameter has options set
        """
        if self.type() != "enum":
            raise Exception("Parameter's type isn't enum")

        return 'options' in self.json

    def has_placeholder(self):
        """
        Return whether a string parameter has placeholder set
        """

        return 'placeholder' in self.json

    def has_range(self):
        """
        Return whether a range parameter has range set
        """
        if self.type() != "range":
            raise Exception("Parameter type isn't range")

        return 'min' in self.json and 'max' in self.json

    def has_regexp(self):
        """
        Return whether a string parameter has regexp set
        """

        return 'regexp' in self.json

    def has_required(self):
        """
        Return whether a parameter has required attribute set
        """
        return 'required' in self.json

    def has_separator(self):
        """
        Return whether a parameter has separator set
        """
        return 'separator' in self.json

    def has_title(self):
        """
        Return whether a section parameter has title set
        """
        return 'title' in self.json

    def has_value(self):
        """
        Return whether a parameter has value set
        """
        return 'value' in self.json

    def has_non_empty_value(self):
        """
        Return whether a parameter has value set
        and value isn't empy
        """
        if not self.has_value():
            return False

        for c in self.value_content():
            if len(str(c)) > 0:
                return True

        return False

    #-------------------------------------------------------------------------------------
    # Query-pure methods

    def __str__(self):
        """
        Return a string with the parameter as it would appear in
        command line, without resolving expressions though. If the
        parameter hasn't value set, nothing is returned.

        To resolve expressions use self.eval().
        """

        text = ""
        # If parameter has no value set returns nothing
        if not self.has_non_empty_value():
            return ""

        if ((len(self.values()) >1) and not self.multiple()):
            raise Exception("Parameter %s defined more than once"%self.keyword())

        for value in self.values():
            if self.type()  == "flag":
                if 'expression' in value:
                    raise Exception("Expression for flags not supported")

                if value['literal']:
                    text = " ".join([text,self.keyword()]).strip()
            else:
                if 'literal' in value:
                    valuestr = self._eval_literal(value['literal'])
                    text = " ".join([text,self.keyword() + "\"" + valuestr + "\""]).strip()
                else:
                    if value['expression']:
                        valuestr = str(value['expression'])
                        text = " ".join([text,self.keyword() + "\"" + valuestr + "\""]).strip()

        return text.strip()

    def eval(self, params=None):
        """
        Return a string with the parameter as it would appear in
        command line, resolving expressions. If the
        parameter hasn't value set, nothing is returned.

        Parameter
        ---------

        params: dict (optional)
           Dictionary of variables to define local scope.
        """

        text = ""
        # If parameter has no value set returns nothing
        if not self.has_non_empty_value():
            return ""

        if ((len(self.values()) >1) and not self.multiple()):
            raise Exception("Parameter '%s' defined more than once"%self.description())

        ptype = self.type()

        if ptype == "string":
            if not self.match_regexp():
                raise ValueError("At least on literal value for parameter '%s' isn't valid against acceptable regexp '%s'"%(self.description(),self.regexp()))

        for value in self.values():

            # Treatment for flags
            if ptype  == "flag":
                if 'expression' in value:
                    raise Exception("Expression for flags isn't supported")

                if value['literal']:
                    text = " ".join([text,self.keyword()]).strip()
                continue

            # Treatment for literal values
            if 'literal' in value:
                if ptype == "integer" or (ptype == 'range' and self.json['digits'] == 0):
                    valuestr = str("%i"%value['literal'])
                elif ptype in ["integers","floats"]:
                    valuestr =  self._eval_literal_array(value['literal'])
                else:
                    valuestr = str(value['literal'])

                text = " ".join([text,self.keyword() + "\"" + valuestr + "\""]).strip()
                continue

            # Treatment for non-arrays expressions
            if ptype in self._scalar_types:

                try:
                    valuestr = self._eval_expression(value['expression'], params)
                except:
                    raise

                text = " ".join([text,self.keyword() + "\"" + valuestr + "\""]).strip()
                continue

            # Treatment for expressions in arrays
            valueliststr = self._eval_array(value['expression'], params)
            text = " ".join([text,self.keyword() + "\"" + valueliststr + "\""]).strip()
            continue

        return text.strip()

    def formated(self, isfull, resolve, pardict):
        """
        Return a list of strings describing the parameter

        Parameter
        ---------

        isfull: boolean
            True for a more verbose output

        resolve: boolean
            True to evaluate expressions in parameter's value

        pardict: dictionary
            Dictionary to define local scope to evaluate expressions
        """

        ptype = self.type()

        if ptype in self._scalar_types:
            return self._dump_par(isfull, resolve, pardict)

        if ptype in self._boolean_types:
            return self._dump_flag_par(isfull, resolve, pardict)

        if ptype in self._array_types:
            return self._dump_array_par(isfull, resolve, pardict)

        if ptype in self._meta_types:
            if ptype == 'section':
                return self.title()

            if ptype == 'comment':
                return self.description()

        return ["Unknown parameter type"]

    def match_regexp(self):
        """
        Check if a literal value matches with the
        regexp, for string-type parameter.

        Parameter
        ---------

        value: str
           String to match with regular expression

        Return
        ------
           True if value matches with regular expression
           or if there is no regular expression.
        """

        if self.type() != "string":
            return False

        if not self.has_regexp():
            return True

        for value in self.values():
            if 'literal' in value:
                if re.match(self.regexp(),value['literal']) is None:
                    return False

        return True

    def value_content(self):
        """
        Query parameter's value content
        """
        content = []
        for value in self.values():
            if 'literal' in value:
                content.append(value['literal'])
            else:
                content.append(value['expression'])

        return content

    #-------------------------------------------------------------------------------------
    # Query/set methods

    def default(self, value=None):
        """
        Query or set parameter's default value

        Parameter
        ---------

        value: (optinal)
            Value to set parameter's widget entry default.
            For instanciable parameters, value can be a list.
            Provide an empty string to delete the default.
        """

        def _base_check(self, value, basetype, typestr):

            if isinstance(value, basetype):
                self.json['default'] = value
                return

            if isinstance(value, list):
                if all(isinstance(val, basetype) for val in value):
                    self.json['default'] = value
                    return

            raise TypeError("Default is neither a value nor a list of values of " + typestr + " type")


        if value is None:
            return self.json['default'] if self.has_default() else None

        # Empty string, deletes the default
        if isinstance(value, str) and (not value):
            if self.has_default():
                del self.json['default']
            return

        # Only instanciable parameters can hold a list as default
        if isinstance(value, list) and (not self.multiple()):
            raise TypeError("Default can't be a list when parameter doesn't accept to be defined multiple times")

        ptype = self.type()

        if ptype == "integer":
            _base_check(self, value, int, "integer")
            return

        if ptype in ["range", "float"]:
            _base_check(self, value, (int,float), "number")
            return

        if ptype in ["string", "enum", "file", "path"]+self._array_types:
            _base_check(self, value, str, "string")
            return

        if ptype == "flag":
            _base_check(self, value, bool, "boolean")
            return

        if ptype in self._meta_types:
            raise Exception("Meta parameter hasn't default attribute")

        raise Exception("Case not treated before")

    def description(self, value = None):
        """
        Query or set parameter's description

        Parameter
        ---------

        value: str (optinal)
            value to set parameter's description
        """
        if value is None:
            return self.json['description'] if self.has_description() else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if self.has_description():
                del self.json['description']
        else:
            self.json['description'] = value

    def filePattern(self, value=None):
        """
        Query or set parameter's file pattern

        Parameter
        ---------

        value: (optinal)
            value to set file pattern in entry widget for file-type parameters
        """
        if self.type() != "file":
            raise Exception("Parameter's type isn't file")

        if value is None:
            return self.json['filePattern'] if self.has_filePattern () else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if self.has_filePattern():
                del self.json['filePattern']
        else:
            self.json['filePattern'] = value

    def fileType(self, value=None):
        """
        Query or set parameter's file type

        Parameter
        ---------

        value: (optinal)
            value to set file type in entry widget for file-type parameters
        """
        if self.type() != "file":
            raise Exception("Parameter's type isn't file")

        if value is None:
            return self.json['fileType'] if self.has_fileType () else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if self.has_fileType():
                del self.json['fileType']
        else:
            self.json['fileType'] = value

    def keyword(self, value = None):
        """
        Query or set parameter's keyword

        Parameter
        ---------

        value: str (optinal)
            value to set parameter's keyword
        """
        if value is None:
            return self.json['keyword'] if self.has_keyword() else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if self.has_keyword():
                del self.json['keyword']
        else:
            self.json['keyword'] = value

    def multiple(self, value = None):
        """
        Query or set parameter's multiple attribute

        Parameter
        ---------

        value: str or boolean (optional)
            value to set parameter's multiple flag

        """
        if value is None:
            return self.json['multiple'] if self.has_multiple() else False

        if isinstance(value, str) and (not value):
            if self.has_multiple():
                del self.json['multiple']
            return

        if not isinstance(value, bool):
            raise TypeError("Argument should be a boolean")

        self.json['multiple'] = value

    def options(self, value=None):
        """
        Query or set enum parameter's options

        Parameter
        ---------

        value: list of dict (optional)
            List of acceptable options for enum-type parameter

            This list has the format:
            [
              {"description": "Sunny season", "value": "summer"},
              {"description": "Colder season", "value": "winter"},
              {"description": "Flower's season", "value": "spring"},
              {"description": "Sadiest season", "value": "autumn"}
            ]
        """
        if self.type() != "enum":
            raise Exception("Parameter's type isn't enum")

        if value is None:
            return self.json['options'] if self.has_options () else []

        if not isinstance(value, list):
            raise TypeError("Argument should be a list")

        if not value:
            if self.has_options():
                del self.json['options']
        else:
            self.json['options'] = value

    def placeholder(self, value=None):
        """
        Query or set string parameter's placeholder

        Parameter
        ---------

        value: (optinal)
            value to set placeholder string in widget entry
        """
        if not self.type() in ["string", "file", "path"] + self._array_types:
            raise Exception("Parameter's type isn't string")

        if value is None:
            return self.json['placeholder'] if self.has_placeholder () else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if self.has_placeholder():
                del self.json['placeholder']
        else:
            self.json['placeholder'] = value

    def range(self, limits=None, vinc=None, vdigits=None):
        """
        Query or set parameter's range

        Parameters
        ----------

        limits: list (optional)
            [lower limit value, upper limit value]

        vinc: float (optional)
            value increment in range entry widget

        vdigits: integer (optional)
            amount of digits to display in range entry widget

        """
        if limits is None:
            return [self.json['min'],self.json['max']] if self.has_range() else None

        if not isinstance(limits, list):
            raise TypeError("Argument should be a list of two integers")

        self.json['min'] = limits[0]
        self.json['max'] = limits[1]
        if vinc is not None:
            self.json['inc'] = vinc
        if vdigits is not None:
            self.json['digits'] = vdigits

    def regexp(self, value=None):
        """
        Query or set string parameter's regexp

        Parameter
        ---------

        value: str (optinal)
            regular expression a string parameter has to be validated against
        """
        if self.type() != "string":
            raise Exception("Parameter's type isn't string")

        if value is None:
            return self.json['regexp'] if self.has_regexp() else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if self.has_regexp():
                del self.json['regexp']
        else:
            self.json['regexp'] = value

    def required(self, value = None):
        """
        Query or set parameter's required attribute

        Parameter
        ---------

        value: str or boolean (optional)
            value to set parameter's required flag

        """
        if value is None:
            return self.json['required'] if self.has_required() else False

        if isinstance(value, str) and (not value):
            if self.has_required():
                del self.json['required']
            return

        if not isinstance(value, bool):
            raise TypeError("Argument should be a boolean")

        self.json['required'] = value

    def separator(self, value=None):
        """
        Query or set parameter's separator value

        Parameter
        ---------

        value: str (optinal)
            separator that goes between array elements
        """
        if not self.type() in ["integers", "floats", "strings"]:
            raise Exception("Parameter type doesn't support separator")

        if value is None:
            return self.json['separator'] if self.has_separator() else None

        if isinstance(value, str) and (not value):
            if self.has_separator():
                del self.json['separator']
        else:
            self.json['separator'] = value


    def title(self, value=None):
        """
        Query or set section parameter's title

        Parameter
        ---------

        value: (optinal)
            value to set section's title
        """
        if self.type() != "section":
            raise Exception("Parameter's type isn't section")

        if value is None:
            return self.json['title'] if self.has_title () else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if self.has_title():
                del self.json['title']
        else:
            self.json['title'] = value

    def type(self, value=None):
        """
        Query or set parameter's type

        Parameter
        ---------

        value: str (optinal)
            value to set parameter's value
        """
        if value is None:
            return self.json['type']

        if value not in self._supported_types:
            raise Exception("Unknown parameter type")

        self.json['type'] = value


    def values(self, value=None):
        """
        Query or set parameter's values

        Parameter
        ---------

        value: (optinal)
            value to set parameter's value.

            value can be:
            - A single literal value, or
            - A list of literal/expression values

            See these examples

            # Set an integer parameter value to 12
            intpar.values(12)

            # Also set an integer parameter value to 12
            intpar.values([{'literal': 12}])

            # Set an integer parameter value to 2 * N,
            # where N is a variable defined in the global or local scopes.
            intpar.values([{'expression': '2 * N'}])

            # Set an integer parameter value for a parameter
            # that accepts a list of values (multiple = True)
            intpar.values([{'expression': '2 * N'}, {'literal': 12}])

            # Set a string parameter
            strpar.values([ {'literal': 'some text'}, {'expression': '\'My name is\' + name'}])

            # All array-type parameters has to be set as strings
            intspar.values("2;4;5")
            intspar.values([ {'expression': '2;4;5+7'} ])
        """
        if value is None:
            return self.json['value'] if self.has_value() else []

        if isinstance(value, str) and (not value):
            if self.has_value():
                del self.json['value']
        elif isinstance(value, dict):
            self.json['value'] = [value]
        elif isinstance(value, list):
            self.json['value'] = value
        else:
            self.json['value'] = [{"literal": value}]

    #-------------------------------------------------------------------------------------
    # Widget-related methods

    def w_line(self):
        """
        Return a widget to set/acquire the parameter

        The widget is meant to be included into a VBox.
        """
        if self.widget == {}:
            self.__widget_construct()

        return self.widget['line']

    def w_set(self):
        """
        Set widget value from parameter's value

        Note: Doesn't support flags, ranges and enums with expressions.
        """

        ptype = self.type()
        if ptype in ["flag", "range", "enum"]:
            if self.has_value():
                self.widget['entry'][0].value = self.values()[0]['literal']
            elif self.has_default():
                self.widget['entry'][0].value = self.default()
            return

        if ptype in self._meta_types:
            return

        # Set for parameters that can hold expressions
        if self.has_value():

            values = self.values()

            for k in range(len(values)):
                value = values[k]
                if k == len(self.widget['entry']):
                    on_add_clicked(button = None,par=self)

                if 'expression' in value:
                    self.widget['exp'][k].value = True
                    self.widget['expression'][k].value = value['expression']
                else:
                    self.widget['exp'][k].value = False
                    self.widget['literal'][k].value = value['literal']

            while len(values) < len(self.widget['entry']):
                on_del_clicked(button = None,par=self)
        else:
            for k in range(len(self.widget['entry'])):
                self._init_value_in_widget(k)

        ninstances = len(self.widget['entry'])
        for k in range(ninstances):
            if self.widget['exp'][k].value:
                self.widget['entry'][k] = self.widget['expression'][k]
                self.widget['expression'][k].layout.display = 'flex'
                self.widget['literal'][k].layout.display = 'none'
            else:
                self.widget['entry'][k] = self.widget['literal'][k]
                self.widget['expression'][k].layout.display = 'none'
                self.widget['literal'][k].layout.display = 'flex'

    def w_get(self):
        """
        Get parameter's value from widget value
        """
        if self.type() in self._meta_types:
            return

        nentries = len(self.widget['entry'])

        k = 0
        values = []
        empty = True
        for k in range(nentries):
            value = self.widget['entry'][k].value
            if 'exp' in self.widget and self.widget['exp'][k].value:
                empty = False
                values.append({"expression": value})
            else:
                if self.type() == 'integer':
                    values.append({"literal": int(value)})
                    empty = False
                elif self.type() in ['float', 'range']:
                    values.append({"literal": float(value)})
                    empty = False
                else:
                    if isinstance(value, bool) or (isinstance(value, str) and len(value) > 0):
                        empty = False
                    values.append({"literal": value})

        if empty:
            self.values("")
        else:
            self.values(values)


    #-------------------------------------------------------------------------------------
    # eval-related methods

    def _eval_literal(self, lit):
        """
        Eval a literal (scalar or array) to assure it is correctly defined

        Parameter
        ---------

        lit:
           Literal to evaluate

        Return
        ------
           An string representing the literal value
        """

        ptype = self.type()

        if ptype == "integer" or (ptype == 'range' and self.json['digits'] == 0):
            try:
                valuestr = str(int(lit))
            except TypeError:
                raise TypeError(str(lit) + " doesn't cast to integer, in parameter '" + self.description() + "'")
            except ValueError:
                raise ValueError(str(lit) + " isn't an integer, in parameter '" + self.description() + "'")
            except Exception as err:
                raise Exception(str(err))

            return valuestr

        if ptype == "integers":
            values = lit.split(self.separator())
            valuestrlist = ""
            for value in values:
                try:
                    valuestr = str(int(value))
                except TypeError:
                    raise TypeError(value + " doesn't cast to integer, in parameter '" + self.description() + "'")
                except ValueError:
                    raise ValueError(value + " isn't an integer, in parameter '" + self.description() + "'")
                except Exception as err:
                    raise Exception(str(err))

                valuestrlist = self.separator().join([valuestrlist,valuestr]).strip(self.separator())

            return valuestrlist


        if ptype == "float":
            try:
                valuestr = str(float(lit))
            except TypeError:
                raise TypeError(str(lit) + " doesn't cast to float, in parameter '" + self.description() + "'")
            except ValueError:
                raise ValueError(str(lit) + " isn't a float, in parameter '" + self.description() + "'")
            except Exception as err:
                raise Exception(str(err))

            return valuestr

        if ptype == "floats":
            values = lit.split(self.separator())
            valuestrlist = ""
            for value in values:
                try:
                    valuestr = str(float(value))
                except TypeError:
                    raise TypeError(value + " doesn't cast to float, in parameter '" + self.description() + "'")
                except ValueError:
                    raise ValueError(value + " isn't a float, in parameter '" + self.description() + "'")
                except Exception as err:
                    raise Exception(str(err))

                valuestrlist = self.separator().join([valuestrlist,valuestr]).strip(self.separator())

            return valuestrlist

        return str(lit)

    def _eval_expression(self, exp, params):
        """
        Eval an expression

        Parameters
        ----------

        exp: str
           String with expressions separeted by self.separator()

        params: dict
           Dictionary of variables to define local scope.
        """

        try:
            valuestr = str(eval(exp,globals(),params))

        except NameError as err:
            errormsg = str(err) + " in expression '" + exp + \
                "', for parameter '" + self.description() + "'"
            if params is  None:
                errormsg = errormsg + "\n (indeed, a dictionary of parameters wasn't even provided)"
            raise NameError(errormsg)

        except SyntaxError as err:
            raise SyntaxError("syntax error in expression '" + exp +
                              "', for parameter '" + self.description() + "'" )

        except ZeroDivisionError:
            raise ZeroDivisionError("division by zero while evaluating expression '" +
                                    exp + "', for parameter '" +
                                    self.description() + "'" )
        except:
            raise Exception("unable to evaluate '" + exp + "' in parameter '" + self.description() + "'")

        if self.type() in ['integer', 'integers']:
            try:
                vint = int(float(valuestr))
            except ValueError as err:
                raise ValueError("expression '" + exp + "' doesn't cast to integer, for parameter '" +
                                 self.description()+"'")
            except:
                raise("unable to eval expression'" + exp + "' doesn't cast to integer, for parameter '" +
                                 self.description()+"'")

            valuestr = f"{vint}"

        return valuestr

    def _eval_array(self, exps, params):
        """
        Eval an array of expressions

        Parameters
        ----------

        exps: str
           String with expressions separeted by self.separator()

        params: dict
           Dictionary of variables to define local scope.
        """

        valuelist = exps.split(self.separator())
        valueliststr = ""

        for vexp in valuelist:

            valuestr = self._eval_expression(vexp, params)
            valueliststr = self.separator().join([valueliststr,valuestr]).strip(self.separator())

        return valueliststr

    def _eval_literal_array(self, lit):
        """
        Eval an array of literals

        Parameters
        ----------

        lit: str
           String with literals separeted by self.separator()

        params: dict
           Dictionary of variables to define local scope.
        """

        valuelist = lit.split(self.separator())
        valueliststr = ""

        for vlit in valuelist:

            valuestr = self._eval_literal(vlit)
            valueliststr = self.separator().join([valueliststr,valuestr]).strip(self.separator())

        return valueliststr

    #-------------------------------------------------------------------------------------
    # dump-related private methods

    def _dump_par(self, isfull, resolve, pardict):
        """
        Private function to dump a number or string parameter
        """

        details = self._dump_details()

        output=[]
        keyvalue = self.keyword()
        if self.has_non_empty_value():
            values = self.values()
            first = True
            for value in values:
                valuestr = ""
                if "literal" in value:
                    valuestr = self._eval_literal(value['literal'])
                else:
                    if resolve:
                        valuestr = self._eval_expression(value['expression'], pardict)
                    else:
                        valuestr = value['expression']

                line = keyvalue+"\""+valuestr+"\""
                if first:
                    output.append("%-40s"%line + " %s"%details)
                    first = False
                else:
                    output.append("%-40s"%line)
        else:
            output.append("%-40s"%keyvalue + " %s"%details)

        if isfull:
            output.append("%-70s"%self.description())
            if self.has_regexp():
                output.append("%-70s"%"Regular expression to match literal values:")
                output.append("%-70s"%self.regexp())
            if self.type() == 'enum':
                output.append("Valid options are:")
                options = self.json['options']
                for opt in options:
                    output.append("%15s: %s"%(opt['value'], opt['description']))

        return output

    def _dump_flag_par(self, isfull, resolve, pardict):
        """
        Private function to dump a flag parameter
        """

        details = self._dump_details()

        output = []
        if self.has_value():
            value = self.values()[0]
            if "literal" in value:
                if value['literal']:
                    valuestr = " (on)"
                else:
                    valuestr = " (off)"
            else:
                if resolve:
                    try:
                        valuestr = str(eval(value['expression'],globals(),pardict))
                    except:
                        raise Exception("Unable to evaluate parameter")
                else:
                    valuestr = value['expression']

        else:
            valuestr = " (off)"

        line = self.keyword() + valuestr
        output.append("%-40s"%line + " %s"%details)

        if isfull:
            output.append("%-70s"%self.description())

        return output

    def _dump_array_par(self, isfull, resolve, pardict):
        """
        Private function to dump an array parameter
        """

        details = self._dump_details()

        output=[]
        keyvalue = self.keyword()
        if self.has_non_empty_value():
            values = self.values()
            first = True
            for value in values:
                valuestr = ""
                if "literal" in value:
                    valuestr = self._eval_literal(value['literal'])
                else:
                    if resolve:
                        valuestr = self._eval_array(value['expression'], pardict)
                    else:
                        valuestr = value['expression']

                line = keyvalue+"\""+valuestr+"\""
                if first:
                    output.append("%-40s"%line + " %s"%details)
                    first = False
                else:
                    output.append("%-40s"%line)
        else:
            output.append("%-40s"%keyvalue + " %s"%details)

        if isfull:
            output.append("%-70s"%self.description())
            if self.type() == 'enum':
                output.append("Valid options are:")
                options = self.json['options']
                for opt in options:
                    output.append("%15s: %s"%(opt['value'], opt['description']))

        return output

    def _dump_details(self):
        """
        Private function to generate the comment concerning
        a parameter (its type, default values and attributes)

        *That's not a function to dump a comment-type parameter*
        """

        output = "[" + self.type()
        if self.type() in ['integers', 'floats', 'strings']:
            output = output + "(" + self.separator() + ")"

        if self.type() == 'range':
            template = "%." + str(self.json['digits']) + "f"
            output = output + ", " + template%self.json['min']+":" + \
                     template%self.json['inc']+":" + template%self.json['max']

        if self.has_default():
            if self.type() == 'flag':
                if self.default():
                    output = output + ", on]"
                else:
                    output = output + ", off]"
            else:
                output = output + ", " + str(self.default()) + "]"
        else:
            output = output + "]"

        if self.required():
            output = output + " R"

        if self.multiple():
            output = output + " M"

        return output

    #--------------------------------------------------------------------------------
    # Private methods for widget construction

    def __widget_construct(self):
        """
        Construct the widget depending of the parameter's type
        """

        is_multiple = self.multiple()
        ptype = self.type()

        if is_multiple and ptype not in self._instanciable_types:
            raise Exception("No support for multiple instances of %s parameter"%self.type())

        if ptype == 'flag':
            self.__construct_w_flag()
            return

        if ptype == 'comment':
            self.__construct_w_comment()
            return

        if ptype == 'section':
            self.__construct_w_section()
            return

        if not is_multiple:
            if ptype == 'integer':
                self.__construct_w_non_instanciable_param(W.IntText)
                return

            if ptype == 'float':
                self.__construct_w_non_instanciable_param(W.FloatText)
                return

            if ptype in ['string','file','path', 'strings', 'integers','floats']:
                self.__construct_w_non_instanciable_param(W.Text)
                return

            if ptype == 'range':
                if 'digits' in self.json and self.json['digits'] > 1:
                    Entry_widget = W.BoundedFloatText
                else:
                    Entry_widget = W.BoundedIntText

                self.__construct_w_non_instanciable_param(Entry_widget)
                return

            if ptype == 'enum':
                self.__construct_w_enum()
                return
        else:
            if ptype == "integer":
                self.__construct_w_instanciable_param(W.IntText)
                return

            if ptype == "float":
                self.__construct_w_instanciable_param(W.FloatText)
                return

            if ptype in ["string","file","path","strings","integers","floats"]:
                self.__construct_w_instanciable_param(W.Text)
                return

            if ptype == "range":
                if 'digits' in self.json and self.json['digits'] > 1:
                    Entry_widget = W.BoundedFloatText
                else:
                    Entry_widget = W.BoundedIntText

                self.__construct_w_instanciable_param(Entry_widget)
                return

            raise Exception("Multiple instances not implement for %s-type parameter"%ptype)

    def _set_w_range_attributes(self, widget):

        widget.layout = W.Layout(width="35%")
        widget.min = self.json['min']
        widget.max = self.json['max']
        widget.step = self.json['inc']

    def _set_w_enum_attributes(self, widget):

        options = []
        if self.has_options():
            if not self.required():
                options.append( ('-- unset --', '') )
            for opt in self.options():
                options.append( (opt['description'],opt['value']) )
        self.widget['literal'][0].options = options

    def __construct_w_non_instanciable_param(self,Entry_widget):
        """
        Widget for (integer(s),float(s),string(s),file,path)-type parameter
        which can't be instanciate.
        """
        label = W.Label(value = self.description(), layout = W.Layout(width="60%"))
        label_set_class(self.required(), label, "required")

        is_range = (self.type() == "range")
        if is_range:
            self.widget['literal'] = [ Entry_widget(layout = W.Layout(width="35%")) ]
            self._set_w_range_attributes(self.widget['literal'][0])
        else:
            self.widget['literal'] = [ Entry_widget(layout = W.Layout(width="35%")) ]

        self.widget['exp'] = []
        self.widget['entry'] = []
        self.widget['expression'] = []

        self._init_widget(0)

        self.widget['line'] = W.HBox([label,
                                      self.widget['literal'][0],
                                      self.widget['expression'][0],
                                      self.widget['exp'][0]])

    def __construct_w_instanciable_param(self,Entry_widget):
        """
        Widget for (integer,float,string,file,path)-type parameter
        that can be provided multiple times
        """
        label = W.Label(value = self.description())
        label_set_class(self.required(), label, "required")

        bt_layout = W.Layout(indent=False,width="30px")
        bt_add = W.Button(icon="plus", tooltip="Add an instance", layout = bt_layout)
        bt_del = W.Button(icon="minus", tooltip="Remove last instance", layout = bt_layout)
        bt_add.style.button_color = 'white'
        bt_del.style.button_color = 'white'

        bt_add.on_click(functools.partial(on_add_clicked, par=self))
        bt_del.on_click(functools.partial(on_del_clicked, par=self))
        label_and_buttons = W.HBox([label, bt_add, bt_del], layout = W.Layout(width="60%"))

        self.widget['entry_widget'] = Entry_widget

        self.widget['ninstances'] = 1
        if self.has_value():
            self.widget['ninstances'] = len(self.values())
        elif self.has_default():
            default = self.default()
            if isinstance(default, list):
                self.widget['ninstances'] = len(default)
            else:
                self.widget['ninstances'] = 1

        self.widget['literal'] = []
        self.widget['exp'] = []
        self.widget['entry'] = []
        self.widget['expression'] = []

        children = ()

        is_range = (self.type() == "range")
        for k in range(self.widget['ninstances']):

            if is_range:
                self.widget['literal'].append(Entry_widget(layout = W.Layout(width="35%")))
                self._set_w_range_attributes(self.widget['literal'][k])
            else:
                self.widget['literal'].append(Entry_widget())

            self._init_widget(k)
            self.widget['expression'][k].layout.width = "100%"

            hbox = W.HBox([self.widget['literal'][k],
                           self.widget['expression'][k],
                           self.widget['exp'][k]], layout=W.Layout(width="100%"))
            children = children + (hbox,)

        self.widget['vbox'] = W.VBox(children, layout=W.Layout(width="39%",height="100%"))
        self.widget['line'] = W.HBox([label_and_buttons, self.widget['vbox']])

    def __construct_w_enum(self):
        """
        Widget for enum-type parameter
        """
        label = W.Label(value = self.description(), layout = W.Layout(width="60%"))
        label_set_class(self.required(), label, "required")

        self.widget['entry'] = [W.Dropdown(layout = W.Layout(width="40%"))]

        options = []
        if self.has_options():
            if not self.required():
                options.append( ('-- unset --', '') )
            for opt in self.options():
                options.append( (opt['description'],opt['value']) )
        self.widget['entry'][0].options = options

        if self.has_value():
            self.widget['entry'][0].value = self.value_content()[0]
        elif self.has_default():
            self.widget['entry'][0].value = self.default()

        self.widget['line'] = W.HBox([label, self.widget['entry'][0]])

    def __construct_w_flag(self):
        """
        Widget for flag-type parameter
        """

        self.widget['entry'] = [ W.Checkbox(description=self.description(),
                                            indent=False,
                                            layout = W.Layout(width="100%")) ]

        if self.has_value():
            self.widget['entry'][0].value = self.value_content()[0]
        elif self.has_default():
            self.widget['entry'][0].value = self.default()
        self.widget['line'] = W.HBox([self.widget['entry'][0]])

    def __construct_w_section(self):
        """ Widget for section-type parameter
        """
        vbox = W.VBox()
        self.widget['line'] = W.Accordion(selected_index=None,
                                          children=(vbox,))
        self.widget['line'].set_title(0,self.title())


    def __construct_w_comment(self):
        """ Widget for comment-type parameter
        """
        self.widget['line'] = W.HTML(value='<div class="commentpar">'+self.description()+'</div>',
                                     layout=W.Layout(width="98%"))

    def _init_value_in_widget(self, index):

        if self.has_value() and index < len(self.values()):
            value = self.values()[index]
            if 'literal' in value:
                self.widget['exp'][index].value = False
                self.widget['literal'][index].value = value['literal']
            else:
                self.widget['exp'][index].value = True
                self.widget['expression'][index].value = value['expression']
        elif self.has_default():
            defaults = self.default()
            self.widget['exp'][index].value = False

            if isinstance(defaults, list):
                if index < len(defaults):
                    self.widget['literal'][index].value = defaults[index]
                else:
                    self.widget['literal'][index].value = defaults[-1]
            else:
                self.widget['literal'][index].value = defaults
        else:
            # No value nor default? Set it as an empty expression
            self.widget['exp'][index].value = True


    def _init_widget(self, index):
        """
        Initialize a parameter's widget that has support
        to expressions
        """

        if self.has_placeholder():
            self.widget['literal'][index].placeholder = self.placeholder()

        self.widget['exp'].append (W.Checkbox(indent=False, layout=W.Layout(width="25px")))
        self.widget['expression'].append (W.Text(layout = W.Layout(width="35%"),
                                                 placeholder="expression to evaluate"))

        self._init_value_in_widget(index)
        # Which widget to show?
        if self.widget['exp'][index].value:
            self.widget['entry'].append(self.widget['expression'][index])
            self.widget['literal'][index].layout.display = 'none'
            self.widget['expression'][index].layout.display = 'flex'
        else:
            self.widget['entry'].append(self.widget['literal'][index])
            self.widget['literal'][index].layout.display = 'flex'
            self.widget['expression'][index].layout.display = 'none'

        # From now on, start observe changes in self.widget['exp'][0].value
        self.widget['exp'][index].observe(functools.partial(on_expression_toogle,
                                                            par=self, index=index),
                                          names='value')

def on_expression_toogle(c, par, index = 0):
    """
    Callback to expression checkbox
    """

    if c.new:
        par.widget['entry'][index] = par.widget['expression'][index]
        par.widget['expression'][index].layout.display = 'flex'
        par.widget['literal'][index].layout.display = 'none'
    else:
        par.widget['entry'][index] = par.widget['literal'][index]
        par.widget['expression'][index].layout.display = 'none'
        par.widget['literal'][index].layout.display = 'flex'

def on_add_clicked(button, par):
    """
    Callback to add button for multiple-value capable parameters
    """
    ptype = par.type()

    k = len(par.widget['entry'])
    par.widget['literal'].append(par.widget['entry_widget']())
    if ptype == 'range':
        par._set_w_range_attributes(par.widget['literal'][k])

    if par.has_placeholder():
        par.widget['literal'][k].placeholder = par.placeholder()

    par.widget['expression'].append(W.Text(placeholder="expression to evaluate"))
    par.widget['entry'].append(par.widget['literal'][k])

    par.widget['expression'][k].layout.display = 'none'

    par.widget['exp'].append(W.Checkbox(value=False, indent=False,
                                        layout = W.Layout(width="25px")))
    par.widget['exp'][k].observe(functools.partial(on_expression_toogle,
                                                   par=par, index = k),
                                 names='value')

    par._init_value_in_widget(k)
    hbox = W.HBox([par.widget['literal'][k],
                   par.widget['expression'][k],
                   par.widget['exp'][k]], layout=W.Layout(width="100%"))
    children = par.widget['vbox'].children
    children = children + (hbox,)
    par.widget['vbox'].children = children

def on_del_clicked(button, par):
    """
    Callback to del button for multiple-value capable parameters
    """

    n = len(par.widget['entry'])
    if n == 1:
        return

    children = par.widget['vbox'].children
    par.widget['vbox'].children = children[:n-1]

    par.widget['literal'].pop(n-1)
    par.widget['expression'].pop(n-1)
    par.widget['exp'].pop(n-1)
    par.widget['entry'].pop(n-1)

def label_set_class(flag, label, css_class):

    if flag:
        label.add_class(css_class)
