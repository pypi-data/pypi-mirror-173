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

import json as JSON
import subprocess
import functools
from time import sleep
import os

from colorama import Fore, Style
from jsonschema import Draft202012Validator
import ipywidgets as W
from IPython.core.display import display, HTML

from .person  import Person
from .program import Prog

#--------------------------------------------------------------------------------
def _dump_parameter(par, isfull, setonly, resolve, pardict, parcount):
    """ Private function to dump a parameter
    """

    ptype = par.type()
    if ptype == 'section':
        print("      " + Fore.GREEN + par.formated(isfull, resolve, pardict)+":" + Style.RESET_ALL)
        return

    if ptype == 'comment' and not setonly:
        print("      " + Fore.YELLOW + par.formated(isfull, resolve, pardict) + Style.RESET_ALL)
        if isfull:
            print("")
        return

    if setonly and not par.has_non_empty_value():
        return

    output = par.formated(isfull, resolve, pardict)
    first = True

    for line in output:
        if first:
            print("      [%2d] "%parcount + line)
            first = False
        else:
            print("           " + line)

    if isfull:
        print("")

#-------------------------------------------------------------------------------
class Flow:
    """Class to represent a processing flow.

A flow is a representation of a processing,
in which data flows through a pipe of programs.

Internally, a flow is a python dictionary, save/exported
as a JSON.

A flow can be initialized from another flow, eventually read from
a file.

Optionaly, a dictionary can be provided to evaluate
parameters defined by expressions.

Attributes
----------

json: dict
    Dictionary representing the flow

widget: dict
    Dictionary holding an widget to setup, inspect and run the flow

filename: str
    Filename from which the flow is loaded or saved

par: dict
    Dictionary of variables to define local scope to evaluate parameters' expressions

authors: List of Person
    List of program's authors

title: str
    Program's title

description: str
    One-line description for the parameter purpose

tags: List of str
    List of tags for catalog purpose

stdin: str
    Filename feed to standard input

stdout: str
    Filename to write the standard output

stderr: str
    Filename to write the standard error

"""

    schemafn = os.path.join(os.path.dirname(__file__),
                            "schema",
                            "full-flow.schema")
    validator = None

    def __init__(self, flow=None, filename=None, par=None,
                 title=None, description=None,
                 authors=None, tags=None,
                 stdin=None, stdout=None, stderr=None):
        """
        Attributes
        ----------

        flow: dict (optional)
            dictionary representing the flow

        filename: str (optional)
            Filename from which the flow is loaded

        par: dict (optional)
            Dictionary of variables to define local scope to evaluate parameters' expressions

        authors: List of Person (optional)
            List of program's authors

        title: str (optional)
            Program's title

        description: str (optional)
            One-line description for the parameter purpose

        tags: List of str (optional)
            List of tags for catalog purpose

        stdin: str (optional)
            Filename feed to standard input

        stdout: str (optional)
            Filename to write the standard output

        stderr: str (optional)
            Filename to write the standard error
        """

        if not par is None:
            self.pardict = par
        else:
            self.pardict = {}

        self.json = {}
        self.proglist = []
        self.authorlist = []
        self.w = {}

        if flow is not None:
            if not isinstance(flow, Flow):
                raise TypeError("Argument should be Flow")
            self.json = JSON.loads(JSON.dumps(flow.json))
        elif not filename is None:
            with open(filename) as fp:
                text = fp.read()

            self.json = JSON.loads(text)
            self.filename(filename)

        # Recreate Programs and Parameters
        if self.json != {} and 'programs' in self.json:
            for item in self.json['programs']:
                self.proglist.append(Prog(json = item['program']))

        # Recreate Authors
        if self.json != {} and 'authors' in self.json:
            for item in self.json['authors']:
                self.authorlist.append(Person(json = item))

        if not title is None:
            self.title(title)
        if not description is None:
            self.description(description)
        if not authors is None:
            self.authors(authors)
        if not tags is None:
            self.tags(tags)
        if not stdin is None:
            self.stdin(stdin)
        if not stdout is None:
            self.stdout(stdout)
        if not stderr is None:
            self.stderr(stderr)

    def save(self, filename=None):
        """
        Save the flow as a JSON to disk

        Parameter
        ---------

        filename: str (optional)
           Filename to save the flow in. If not provided
           the flow will be saved in self.filename().
        """

        if filename is None:
            if self.has_filename():
                fn = self.filename()
            else:
                raise Exception("Filename nor set neither provided")
        else:
            fn = filename

        with open(fn, "w") as fp:
            fp.write(JSON.dumps(self.json))

        self.filename(fn)

    def copy(self):
        """
        Copy the flow preserving reference to dictionary of parameters
        """
        flow = Flow(flow=self, par=self.pardict)
        flow.filename("")
        return flow

    def has_par(self):
        """
        Return whether the flow has dictionary of parameters
        """
        return bool(self.pardict)

    def par(self, value=None):
        """
        Set or return flow's dictionary of parameters

        Parameter
        ---------

        value: dict (optional)
            Dictionary containing variables to define local scope
            when evaluating parameter's expressions (leave it blank for querying)
        """
        if value is None:
            return self.pardict

        if not isinstance(value, dict):
            raise TypeError("Argument should be a dictionary")

        self.pardict = value

    def has_title(self):
        """
        Return whether the flow has title set
        """
        return 'title' in self.json

    def title(self, value = None):
        """
        Set or return flow's title

        Parameter
        ---------

        value: str (optional)
            Short title for the flow (leave it blank for querying)
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
        Return whether the flow has description set
        """
        return 'description' in self.json

    def description(self, value = None):
        """
        Set or return flow's description

        Parameter
        ---------

        value: str (optional)
            One-sentence description for the flow (leave it blank for querying)
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

    def has_tags(self):
        """
        Return whether the flow has tags set
        """
        return 'tags' in self.json

    def tags(self, value = None):
        """
        Set or return flow's tags

        Parameter
        ---------

        value: list of str (optional)
            List of tags (leave it blank for querying)
        """
        if value is None:
            return self.json['tags'] if self.has_tags() else []

        if not isinstance(value, list):
            raise TypeError("Argument should be a list of strings")

        if not value:
            if 'tags' in self.json:
                del self.json['tags']
        else:
            self.json['tags'] = value

    def accept_stdin(self):
        """
        Return whether flow reads from stdin
        """
        nprogs = self.programs_count()

        k = 0
        while k < nprogs:
            if self.program_status(k):
                return self.program(k).stdin()
            k = k + 1
        return False

    def accept_stdout(self):
        """
        Return whether flow writes to stdout
        """

        nprogs = self.programs_count()

        k = nprogs -1
        while k >=0:
            if self.program_status(k):
                return self.program(k).stdout()
            k = k - 1
        return False

    def accept_stderr(self):
        """
        Return whether flow writes to stderr
        """

        nprogs = self.programs_count()

        k = nprogs -1
        while k >=0:
            if self.program_status(k):
                return self.program(k).stderr()
            k = k - 1
        return False

    def has_authors(self):
        """
        Return whether the flow has authors set
        """
        return 'authors' in self.json

    def authors(self, value=None):
        """
        Set or return flow's authors.

        Parameter
        ---------

        value: (optional)
            A list of Person (leave it blank for querying)
        """
        if value is None:
            return self.authorlist if self.has_authors() else []

        if not isinstance(value, list) and not isinstance(value, Person):
            raise TypeError("Argument should be a list of persons")

        if isinstance(value, Person):
            self.json['authors'] = [value.json]
            self.authorlist = [value]
        else:
            if not value:
                if 'authors' in self.json:
                    del self.json['authors']
            else:
                self.json['authors'] = []
                for person in value:
                    if not isinstance(person, Person):
                        raise Exception("Authors should be a list of persons")
                    self.json['authors'].append(person.json)
                self.authorlist = value

    def authors_count(self):
        """ Return the number of persons in credit's list
        """
        return len(self.authors())

    def has_filename(self):
        """
        Return whether the flow has filename set
        """
        return 'filename' in self.json

    def filename(self, value = None):
        """
        Set or return flow's filename

        Parameter
        ---------

        value: str (optional)
            Filename to save/load the flow (leave it blank for querying)
        """
        if value is None:
            return self.json['filename'] if self.has_filename() else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if 'filename' in self.json:
                del self.json['filename']
        else:
            self.json['filename'] = value

        return 'filename' in self.json

    def has_stdin(self):
        """ Return whether the flow has stdin set
        """
        if 'io' in self.json:
            return 'stdin' in self.json['io']

        return False

    def stdin(self, value=None):
        """Set or return flow's stdin
        """
        if value is None:
            return self.json['io']['stdin'] if self.has_stdin() else ""

        if not isinstance(value, str):
            raise TypeError("Argument should be a string")

        if not value:
            if 'io' in self.json:
                if 'stdin' in self.json['io']:
                    del self.json['io']['stdin']
                if not self.json['io']:
                    del self.json['io']
        else:
            if 'io' not in self.json:
                self.json['io']={}

            self.json['io']['stdin'] = value

    def has_stdout(self):
        """ Return whether the flow has stdout set
        """
        if 'io' in self.json:
            return 'stdout' in self.json['io']

        return False

    def stdout(self, value=None):
        """
        Set or return flow's stdout.

        When set, provide a tuple with filename and mode ('a' or 'w').
        For example,
        flow.stdout(['/tmp/data.rsf','w'])
        """
        if value is None:
            return self.json['io']['stdout'] if self.has_stdout() else []

        if (not isinstance(value, list)) and (not value == ""):
            raise TypeError("Argument should be a list, like ['filename','w']")

        if not value:
            if 'io' in self.json:
                if 'stdout' in self.json['io']:
                    del self.json['io']['stdout']
                if not self.json['io']:
                    del self.json['io']
        else:
            if 'io' not in self.json:
                self.json['io']={}

            self.json['io']['stdout'] = value

    def has_stderr(self):
        """
        Return whether the flow has stderr set
        """
        if 'io' in self.json:
            return 'stderr' in self.json['io']

        return False

    def stderr(self, value=None):
        """
        Set or return flow's stderr.

        When set, provide a list with filename and mode ('a' or 'w').
        For example,
        flow.stderr(['/tmp/log.txt','a'])
        """
        if value is None:
            return self.json['io']['stderr'] if self.has_stderr() else []

        if (not isinstance(value, list)) and (not value == ""):
            raise TypeError("Argument should be a list, like ['filename','w']")

        if not value:
            if 'io' in self.json:
                if 'stderr' in self.json['io']:
                    del self.json['io']['stderr']
                if not self.json['io']:
                    del self.json['io']
        else:
            if 'io' not in self.json:
                self.json['io']={}

            self.json['io']['stderr'] = value

    def has_programs(self):
        """
        Return whether the flow has programs
        """
        return 'programs' in self.json

    def programs(self):
        """
        Return the list of programs for the flow
        """
        return self.proglist

    def programs_count(self):
        """
        Return the number of programs in the flow
        """
        return len(self.proglist)

    def program_status(self, iprog, status=None):
        """
        Set or return the iprog-th program's status

        Parameter
        ----------

        iprog: int
            Index of the program

        status: boolean
            Indicates with the program should be
            added as active (True) or inactive (False)
        """
        if (iprog < 0 or iprog >= self.programs_count()):
            raise ValueError("Program index out of range")

        if status is None:
            return self.json['programs'][iprog]['enabled']

        if not isinstance(status, bool):
            raise TypeError("Argument should be a boolean")

        self.json['programs'][iprog]['enabled']  = status

    def program(self, iprog):
        """
        Return the iprog-th program in flow

        Parameter
        ---------

        iprog: int
            Index of the program
        """
        if (iprog < 0 or iprog >= self.programs_count()):
            raise ValueError("Program index out of range")

        return self.proglist[iprog]

    def program_add(self, prog, status=True):
        """
        Add a program to the flow

        Parameters
        ----------

        prog: Prog
            Program to be added

        status: boolean
            Indicates with the program should be
            added as active (True) or inactive (False)
        """

        if not isinstance(prog, Prog):
            raise TypeError("Argument should be a Prog")

        if len(self.proglist) == 0:
            self.json['programs'] = []

        self.proglist.append(prog)
        self.json['programs'].append({"enabled": status, "program": prog.json})

    def program_del(self, iprog):
        """ Delete i-th program in flow

        Parameter
        ---------

        iprog: int
            Index of the program to be deleted
        """

        if (iprog < 0 or iprog >= self.programs_count()):
            raise ValueError("Program index out of range")

        self.json['programs'].pop(iprog)
        self.proglist.pop(iprog)
        if len(self.proglist) == 0:
            del self.json['programs']

    def program_parameter_values(self, iprog, ipar, value = None):
        """ Set or return the value of ipar-th parameter
        of iprog-th program of flow

        Parameter
        ---------

        iprog: int
            Index of the program to be deleted

        ipar: int
            Index of the parameter to set or query

        value: (optional)
            Value to set (leave empty to query)
        """
        if (iprog < 0 or iprog >= self.programs_count()):
            raise ValueError("Program index out of range")

        if (ipar < 0 or ipar >= self.program(iprog).parameters_count()):
            raise ValueError("Parameter index out of range")

        param = self.proglist[iprog].parameter(ipar)

        if value is None:
            return param.values()

        param.values(value)

    def program_parameter_values_by_keyword(self, iprog, keyword, value = None):
        """ Set or return the value of parameter
        of iprog-th program of flow, looking by
        parameter's keyword.

        Parameter
        ---------

        iprog: int
            Index of the program to be deleted

        keyword: str
            Keyword of the parameter to set or query

        value: (optional)
            Value to set (leave empty to query)
        """
        if (iprog < 0 or iprog >= self.programs_count()):
            raise ValueError("Program index out of range")

        if not isinstance(keyword, str):
            raise TypeError("Keyword isn't an string")

        prog = self.proglist[iprog]
        ipar = prog.parameter_lookup(keyword)

        if ipar is None:
            raise ValueError("%s doesn't match any keyword for program %s"%(keyword,prog.title()))

        par = prog.parameter(ipar)
        if value is None:
            return par.values()

        par.values(value)

    def validate(self,verbose=False):
        """
        Validate the flow against schema

        Parameter
        ---------

        verbose: bool (optional)
            If True, besides returning whether the flow is
            valid, returns the list of errors.
        """
        if self.validator is None:
            with open(Flow.schemafn,'r') as fp:
                Flow.validator = Draft202012Validator(JSON.loads(fp.read()))

        valid = Flow.validator.is_valid(self.json)
        if not verbose:
            return valid

        errorlist = []
        for error in sorted(Flow.validator.iter_errors(self.json),key=str):
            errorlist.append(error.message)

        return valid,errorlist

    def dump(self,verbose=False,setonly=False,resolve=False):
        """
        Dump the flow's content

        Parameter
        ---------

        verbose: boolean (optional)
            Be more verbose than usual

        setonly: boolean (optional)
            Show only parameters with value set

        resolve: boolean (optional)
            Resolve parameters' values defined by expression
        """

        # Title -- Description
        headtext = self.title()
        if self.has_description():
            headtext = headtext + " — " + self.description()

        print(headtext)

        # Authors
        if self.has_authors():
            for person in self.authors():
                print(str(person)+"\n")

        # Tags
        if self.has_tags():
            tags = self.tags()
            ntags = len(tags)
            for k in range(ntags-1):
                print(Fore.CYAN + tags[k] + Style.RESET_ALL, end=" ∙ ")

            print(Fore.CYAN + tags[ntags-1] + Style.RESET_ALL+"\n")

        # IO: stdin, stdout and stderr
        iotext = ""
        if self.has_stdin():
            iotext = iotext + "<" + self.stdin() + "  "

        if self.has_stdout():
            filename, mode = self.stdout()
            if mode == "w":
                iotext = iotext + ">" + filename + "  "
            else:
                iotext = iotext + ">>" + filename + "  "

        if self.has_stderr():
            filename, mode = self.stderr()
            if mode == "w":
                iotext = iotext + "2>" + filename
            else:
                iotext = iotext + "2>>" + filename

        if iotext:
            print(iotext)

        # Programs
        print("Flow with " + str(self.programs_count()) + " program(s):")

        for k in range(0, self.programs_count()):
            prog = self.program(k)

            headtext = "\n[%2i]: "%k + Fore.GREEN + prog.title() + Style.RESET_ALL
            if prog.has_description():
                headtext = headtext + " — " + prog.description()
            headtext = headtext + " (" + prog.executable() + ")"

            print(headtext)

            if self.program_status(k):
                if prog.has_parameters():
                    print(Fore.GREEN + "      Parameters:" + Style.RESET_ALL)
                    parcount = 0
                    for parcount in range(prog.parameters_count()):
                        _dump_parameter(prog.parameter(parcount),verbose,setonly,resolve,self.pardict, parcount)
                else:
                    print("      No parameters")
            else:
                print("      Disabled")

    def __str__(self):
        """
        Return the command line to run the flow,
        without resolving expressions though.

        To resolve parameters use self.eval().
        """
        return self.__cmdline(False)

    def eval(self):
        """
        Return the command line to run the flow,
        resolving expressions.
        """
        return self.__cmdline(True)


    def __cmdline(self, resolve):
        """
        Return the command line to run the flow.

        Parameter
        ---------

        resolve: boolean
            Resolve or not parameter's valued defined by expressions
        """
        nprogs = self.programs_count()
        if nprogs == 0:
            return ""

        cmdline = ""
        k = 0
        first = True
        for k in range(nprogs):
            if self.program_status(k):
                prog = self.program(k)
                if first:
                    if prog.stdin() and not self.has_stdin():
                        raise Exception("First program reads from stdin")

                    if prog.stdin():
                        cmdline = "<" + self.stdin() + " "

                    if resolve:
                        cmdline = cmdline + prog.eval(self.par())
                    else:
                        cmdline = cmdline + str(prog)

                    first = False
                else:
                    if ((self.program(k).stdin() and not self.program(k-1).stdout()) or
                        (not self.program(k).stdin() and self.program(k-1).stdout())):
                        raise Exception("Broken flow between %s and %s"%
                                        (self.program(k-1).executable(),
                                         self.program(k).executable()))

                    if (self.program(k).stdin() and self.program(k-1).stdout()):
                        if resolve:
                            cmdline = cmdline + " | " + prog.eval(self.par())
                        else:
                            cmdline = cmdline + " | " + str(prog)

                    if (not self.program(k).stdin() and not self.program(k-1).stdout()):
                        if resolve:
                            try:
                                progstr = prog.eval(self.par())
                            except:
                                raise

                            cmdline = cmdline + " && " + progstr
                        else:
                            cmdline = cmdline + " && " + str(prog)

            k = k + 1

        if first:
            return ""

        if self.has_stdout():
            nprog = nprogs - 1
            while nprog >= 0:
                if self.program_status(nprog):
                    break

                nprog = nprog - 1

            if nprog >= 0:
                prog = self.program(nprog)
                if prog.stdout():
                    stdout = self.stdout()
                    if stdout[1] == "w":
                        cmdline = cmdline + " >"
                    elif stdout[1] == "a":
                        cmdline = cmdline + " >>"
                    else:
                        raise Exception("Unknown stdout mode")

                    cmdline = cmdline + stdout[0]

        if self.has_stderr():
            nprog = nprogs - 1
            while nprog >=0 :
                if self.program_status(nprog):
                    break

                nprog = nprog - 1

            if nprog >= 0:
                prog = self.program(nprog)
                if prog.stderr():
                    stderr = self.stderr()
                    if stderr[1] == "w":
                        cmdline = cmdline + " 2>"
                    elif stderr[1] == "a":
                        cmdline = cmdline + " 2>>"
                    else:
                        raise Exception("Unknown stderr mode")

                    cmdline = cmdline + stderr[0]

        return cmdline

    def merge(self, flow):
        """
        Merge flow

        Parameter
        ---------

        flow: Flow
            A flow to merge into self
        """
        self.json['programs'] = self.json['programs'] + flow.json['programs']
        for prog in flow.proglist:
            self.proglist.append(prog)

        # Destroy the widget to rebuild it when necessary
        self.w = {}

    def run(self):
        """
        Run the flow

        """
        accept_stdout = self.accept_stdout()
        accept_stderr = self.accept_stderr()

        has_stdout = self.has_stdout()
        has_stderr = self.has_stderr()

        if accept_stdout:
            if has_stdout:
                path = os.path.dirname(self.stdout()[0])
                if (path) and not os.path.exists(path):
                    os.mkdir(path)
                stdout = open(self.stdout()[0], self.stdout()[1])
            else:
                stdout = subprocess.PIPE
        else:
            stdout = None

        if accept_stderr:
            if has_stderr:
                path = os.path.dirname(self.stderr()[0])
                if (path) and not os.path.exists(path):
                    os.mkdir(path)
                stderr = open(self.stderr()[0], self.stderr()[1])
            elif not has_stdout and accept_stdout:
                stderr = subprocess.STDOUT
            else:
                stderr = subprocess.PIPE
        else:
            stderr = None

        output = ""
        cmdstr = None
        try:
            cmdstr = self.eval()
        except:
            raise

        if cmdstr:
            run = subprocess.run([cmdstr], shell=True, text=True,
                                 stdout=stdout, stderr=stderr)

            if accept_stdout:
                if has_stdout:
                    stdout.close()
                else:
                    output = output + run.stdout

            if accept_stderr:
                if has_stderr:
                    stderr.close()
                else:
                    if run.stderr:
                        output = output + run.stderr

        return output

    def _widget_io_update(self):
        """
        Enable or disable standard in/out/err
        and filled it in widget
        """

        if self.accept_stdin():
            self.w['stdin'].disabled = False
            if self.has_stdin():
                self.w['stdin'].value = self.stdin()
            else:
                self.w['stdin'].value = ''
        else:
            self.w['stdin'].disabled = True

        if self.accept_stdout():
            self.w['stdout'].disabled = False
            if self.has_stdout():
                self.w['stdout'].value = self.stdout()[0]
            else:
                self.w['stdout'].value = ''
        else:
            self.w['stdout'].disabled = True

        if self.accept_stderr():
            self.w['stderr'].disabled = False
            if self.has_stderr():
                self.w['stderr'].value = self.stderr()[0]
            else:
                self.w['stderr'].value = ''
        else:
            self.w['stderr'].disabled = True


    def widget_populate(self):
        """
        Populate flow's widget
        """

        self.w['title'].value = self.title()
        self.w['description'].value = self.description()

        self._widget_io_update()

        self.w['filename'].value = self.filename()
        k = 0
        for prog in self.programs():
            prog.w['status'].value = self.program_status(k)
            prog.widget_value_set()
            k = k + 1

    def widget_construct(self):
        """
        Construct the widget to inspect, edit and run the flow
        """

        display(HTML("""
        <style>
            .flow_title {font-weight: bold;}
            .flow_desc  {font-style: italic;}
            .prog_desc  {font-style: italic; padding-right: 10px;}
            .section {font-weight: bold;}
            .required {font-weight: bold;}
            .required::after {content: "*"}
            .footnote {font-style: italic;}
            .flowoutput {font-family: monospace;}
            .commentpar {line-height: 14pt;
                         padding-bottom: 5px;
                         padding-top: 5px;
                         color: #006680;}
        </style>"""))

        if self.w != {}:
            self.widget_populate()
            return

        #----------------------------------------------------------------------------------------
        # Side bar
        label_title = W.Label(value = self.title())
        label_title.add_class("flow_title")
        self.w['title'] = W.Text(placeholder="Flow's title")
        link_title = W.link((label_title,'value'),(self.w['title'],'value'))

        label_description = W.Label(value = self.description())
        label_description.add_class("flow_desc")
        self.w['description'] = W.Text(placeholder="Flow's description")
        link_description = W.link((label_description,'value'),(self.w['description'],'value'))

        label_files = W.HTML(value='Files <i class="fa fa-files-o" aria-hidden="true"></i>',
                             layout=W.Layout(margin="10px 0px 0px 0px"))
        label_files.add_class("section")

        self.w['stdin'] = W.Text(placeholder="Input file")
        self.w['stdout'] = W.Text(placeholder="Output file")
        self.w['stderr'] = W.Text(placeholder="Error log")

        bt_info = W.Button(description="Info", button_style = "info", icon="info")
        bt_info.on_click(functools.partial(on_info_clicked, flow=self))

        bt_commit = W.Button(description="Commit", button_style="info", icon="download")
        bt_commit.on_click(functools.partial(on_commit_clicked, flow=self))

        self.w['filename'] = W.Text(placeholder="File to save this flow")
        bt_save = W.Button(description="Save",button_style="info", icon="floppy-o")
        bt_save.on_click(functools.partial(on_save_clicked, flow=self))

        bt_run = W.Button(description="Run",button_style="danger", icon="check")
        bt_run.on_click(functools.partial(on_run_clicked, flow=self))

        #----------------------------------------------------------------------------------------
        # Programs
        self.w['programs'] = W.Tab(layout=W.Layout(width="67%",padding="0px 2px 0px 5px"))

        #----------------------------------------------------------------------------------------
        # Info bar
        label_titdesc = W.Label(value = "Title and description")
        label_titdesc.add_class("section")

        label_authors = W.HTML(value='Authors <i class="fa fa-id-card-o" aria-hidden="true"></i>',
                               layout=W.Layout(margin="10px 0px 0px 0px"))
        label_authors.add_class("section")
        children = (label_titdesc, W.HBox([self.w['title'], self.w['description']]), label_authors,)

        for person in self.authors():
            children = children + (person.w_line(),)

        self.w['info'] = W.VBox(children, layout=W.Layout(width="67%", padding="0px 2px 0px 5px"))
        self.w['info'].layout.display = 'none'

        #----------------------------------------------------------------------------------------
        # Main window
        self.w['main'] = W.HBox([W.VBox([label_title,label_description, label_files,
                                         self.w['stdin'],
                                         self.w['stdout'],
                                         self.w['stderr'],
                                         self.w['filename'],
                                         W.HBox([bt_info,bt_commit],layout=W.Layout(margin="10px 0px 0px 0px")),
                                         W.HBox([bt_save,bt_run])],
                                         layout=W.Layout(widht="27%",padding="0px 2px 0px 5px")),
                         self.w['info'],
                         self.w['programs']],
                         layout=W.Layout(widht="100%",border="1px solid"))
        self.w['output'] = W.Textarea(layout=W.Layout(width="100%", height="98%"))
        self.w['output'].add_class("flowoutput")

        if len(self.proglist) > 0:
            children = (self.program(0).widget(self.program_status(0)),)
            for k in range(1,self.programs_count()):
                children = children + (self.program(k).widget(self.program_status(k)),)
            children = children + (self.w['output'],)
            self.w['programs'].children = children

        k = 0
        for prog in self.programs():
            self.w['programs'].set_title(k, prog.title())
            prog.w['status'].observe(functools.partial(on_program_status_changed, flow=self, k=k), names='value')
            k = k + 1
        self.w['programs'].set_title(k, "Flow's output")

        # After constructing the widget, populate it
        self.widget_populate()

    def w_get(self):
        """
        Set flow's properties from widget value
        """

        self.title(self.w['title'].value)
        self.description(self.w['description'].value)
        self.filename(self.w['filename'].value)

        if not self.w['stdin'].disabled:
            self.stdin(self.w['stdin'].value)

        if not self.w['stdout'].disabled:
            if self.w['stdout'].value:
                self.stdout([self.w['stdout'].value,"w"])
            else:
                self.stdout("")

        if not self.w['stderr'].disabled:
            if self.w['stderr'].value:
                self.stderr([self.w['stderr'].value,"w"])
            else:
                self.stderr("")

        for person in self.authors():
            person.w_get()

        for prog in self.programs():
            prog.widget_value_get()

    def w_set(self):
        """
        Set widget value from flow's properties
        """

        self.w['title'].value = self.title()
        self.w['description'].value = self.description()
        self.w['filename'].value = self.filename()

        self._widget_io_update()

        for person in self.authors():
            person.w_set()

        for prog in self.programs():
            prog.widget_value_set()

    def ui(self):
        """
        Construct and display flow's widget
        """
        self.widget_construct()
        display(self.w['main'])

def on_commit_clicked(button, flow):
    """
    Callback to commit button
    """

    flow.w_get()

def on_info_clicked(button, flow):
    """
    Callback to info button
    """

    if flow.w['info'].layout.display == 'none':
        flow.w['info'].layout.display = 'flex'
        flow.w['programs'].layout.display = 'none'

        button.description = "Programs"
        button.button_style = "warning"
        button.icon = "cubes"

    else:
        flow.w['info'].layout.display = 'none'
        flow.w['programs'].layout.display = 'flex'

        button.description = "Info"
        button.button_style = "info"
        button.icon = "info"

def on_run_clicked(button, flow):
    """
    Callback to run button
    """

    button.button_style = "warning"
    button.icon = "gear"
    flow.w_get()
    try:
        output = flow.run()
    except Exception as err:
        flow.w['output'].value = "ERROR: "+str(err)
        flow.w['programs'].selected_index = flow.programs_count()
        button.button_style = "danger"
        button.icon = "check"
        return

    flow.w['output'].value = output
    flow.w['programs'].selected_index = flow.programs_count()
    button.button_style = "danger"
    button.icon = "check"

def on_save_clicked(button, flow):
    """
    Callback to save button
    """

    if flow.w['filename'].value:
        flow.w_get()
        try:
            flow.save(flow.w['filename'].value)
        except Exception as err:
            flow.w['output'].value = "Error: " + str(err)
            flow.w['programs'].selected_index = flow.programs_count()
            return

        button.button_style = "success"
        sleep(0.4)
        button.button_style = "info"

    else:
        button.button_style = "danger"
        sleep(0.4)
        button.button_style = "info"

def on_program_status_changed(c, flow, k):
    """
    Callback to program status checkbox
    """

    flow.program_status(k, c.new)
    flow._widget_io_update()
