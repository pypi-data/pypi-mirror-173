#!/bin/python3

# Create menus for using with PyGêBR, that make
# common shell tools available.

from pygebr import Person, Prog, Param, Flow
import os

basepath = os.path.dirname(__file__)

# author for menus
biloti = Person(name="Ricardo Biloti",
                email="biloti@unicamp.br",
                institution="University of Campinas",
                homepage="https://www.ime.unicamp.br/~biloti")

# authors for programs
eggert = Person(name="Paul Eggert")
granlund = Person(name="Torbjorn Granlund")
haertel = Person(name="Mike Haertels")
mackenzie = Person(name="David MacKenzie")
meyering = Person(name="Jim Meyering")
rubin = Person(name="Paul Rubin")
stallman = Person(name="Richard M. Stallman")
taylor = Person(name="Ian Lance Taylor")

fsf = Person(name="Free Software Foundation, Inc.",
             homepage="https://www.fsf.org/")
#------------------------------------------------------------------------------
def commit_menu(title, description, authors, executable, tags, prog,
                fname=None):
    menu = Flow(title=title, description=description,
                authors=authors, tags=tags)

    menu.program_add(prog)

    if fname == None:
        fname = executable

    fn = os.path.join(os.path.dirname(__file__), fname + ".json")
    menu.save(fn)

#------------------------------------------------------------------------------
def cat():
    title = "Shell Cat"
    description = "Concatenate files and print on the standard output"
    executable = "cat"
    authors = biloti
    tags=['sh', 'files']

    prog = Prog(title=title, description=description,
                authors=[granlund, stallman, fsf],
                url = "https://www.gnu.org/software/coreutils",
                executable=executable,
                stdin=False, stdout=True, stderr=True)

    prog.parameter_add(Param(ptype="file", keyword=" ",
                             description="File",
                             required=True,multiple=True))

    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
def df():
    title = "Shell DF"
    description = "Report file system disk space usage"
    executable = "df"
    authors = biloti
    tags=['sh', 'file system']

    prog = Prog(title=title, description=description,
                authors=[granlund, mackenzie, eggert, fsf],
                url = "https://www.gnu.org/software/coreutils",
                executable=executable,
                stdin=False, stdout=True, stderr=True)

    prog.parameter_add(Param(ptype="flag", keyword="-a",
                             description="Include pseudo, duplicate, inaccessible file systems",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-h",
                             description="Print sizes in powers of 1024 (e.g., 1023M)",
                             default=True))

    prog.parameter_add(Param(ptype="flag", keyword="-H",
                             description="Print sizes in powers of 1000 (e.g., 1.1G)",
                             default=False))

    par = Param(ptype="enum", keyword="--block-size=",
                description="Scale factor for sizes")
    par.options([
        {"description": "KiB (1024 bytes)",   "value": "KiB"},
        {"description": "MiB (1024^2 bytes)", "value": "MiB"},
        {"description": "GiB (1024^3 bytes)", "value": "GiB"},
        {"description": "TiB (1024^4 bytes)", "value": "TiB"},
        {"description": "PiB (1024^5 bytes)", "value": "PiB"},
        {"description": "EiB (1024^6 bytes)", "value": "EiB"},
        {"description": "ZiB (1024^7 bytes)", "value": "ZiB"},
        {"description": "YiB (1024^8 bytes)", "value": "YiB"},
        {"description": "KB (1000 bytes)",   "value": "KB"},
        {"description": "MB (1000^2 bytes)", "value": "MB"},
        {"description": "GB (1000^3 bytes)", "value": "GB"},
        {"description": "TB (1000^4 bytes)", "value": "TB"},
        {"description": "PB (1000^5 bytes)", "value": "PB"},
        {"description": "EB (1000^6 bytes)", "value": "EB"},
        {"description": "ZB (1000^7 bytes)", "value": "ZB"},
        {"description": "YB (1000^8 bytes)", "value": "YB"}
    ])
    prog.parameter_add(par)

    prog.parameter_add(Param(ptype="flag", keyword="-l",
                             description="Limit listing to local file systems",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--total",
                             description="Produce a grand total",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-T",
                             description="Print type file system",
                             default=False))

    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
def du():
    title = "Shell DU"
    description = "Summarize disk usage of the set of FILEs, recursively for directories"
    executable = "du"
    authors = biloti
    tags=['sh', 'file system']

    prog = Prog(title=title, description=description,
                authors=[granlund, mackenzie, mackenzie, fsf],
                url = "https://www.gnu.org/software/coreutils",
                executable=executable,
                stdin=False, stdout=True, stderr=True)

    prog.parameter_add(Param(ptype="flag", keyword="-a",
                             description="Write counts for all files, not just directories",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--apparent-size",
                             description="Print apparent sizes, rather than disk usage",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--bytes",
                             description="Print size in bytes",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-D",
                             description="Dereference only symlinks that are listed on the command line",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-h",
                             description="Print sizes in human readable format (e.g., 1K 234M 2G)",
                             default=True))

    par = Param(ptype="enum", keyword="--block-size=",
                description="Scale factor for sizes")
    par.options([
        {"description": "KiB (1024 bytes)",   "value": "KiB"},
        {"description": "MiB (1024^2 bytes)", "value": "MiB"},
        {"description": "GiB (1024^3 bytes)", "value": "GiB"},
        {"description": "TiB (1024^4 bytes)", "value": "TiB"},
        {"description": "PiB (1024^5 bytes)", "value": "PiB"},
        {"description": "EiB (1024^6 bytes)", "value": "EiB"},
        {"description": "ZiB (1024^7 bytes)", "value": "ZiB"},
        {"description": "YiB (1024^8 bytes)", "value": "YiB"},
        {"description": "KB (1000 bytes)",   "value": "KB"},
        {"description": "MB (1000^2 bytes)", "value": "MB"},
        {"description": "GB (1000^3 bytes)", "value": "GB"},
        {"description": "TB (1000^4 bytes)", "value": "TB"},
        {"description": "PB (1000^5 bytes)", "value": "PB"},
        {"description": "EB (1000^6 bytes)", "value": "EB"},
        {"description": "ZB (1000^7 bytes)", "value": "ZB"},
        {"description": "YB (1000^8 bytes)", "value": "YB"}
    ])
    prog.parameter_add(par)

    prog.parameter_add(Param(ptype="flag", keyword="-L",
                             description="Dereference all symbolic links",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-l",
                             description="Limit listing to local file systems",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--total",
                             description="Produce a grand total",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--separate-dirs",
                             description="For directories do not include size of subdirectories",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-x",
                             description="Skip directories on different file systems",
                             default=False))

    prog.parameter_add(Param(ptype="file", keyword=" ",
                             description="Path or files to scan",
                             required=True, multiple=True))

    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
def head():
    title = "Shell Head"
    description = "Output the first part of files"
    executable="head"
    authors = biloti
    tags = ['sh', 'files']

    prog = Prog(title=title, description=description,
                authors=[mackenzie, meyering, fsf],
                url="https://www.gnu.org/software/coreutils/",
                executable=executable, stdin=True)

    prog.parameter_add(Param(ptype="integer", keyword="-n ",
              description="How many lines to output",
              default=10))

    prog.parameter_add(Param(ptype="flag", keyword="-q",
              description="Never print headers giving file names",
              default=False))

    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
def ls():
    title = "Shell LS"
    description = "List directory contents"
    executable="ls"
    authors = biloti
    tags = ['sh', 'file system']

    prog = Prog(title=title, description=description,
                authors=[stallman, mackenzie, fsf],
                url="https://www.gnu.org/software/coreutils",
                executable=executable, stdin=False)

    prog.parameter_add(Param(ptype="flag", keyword="--all",
              description="Do not ignore entries starting with .",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--author",
              description="Print the author of each file (when long format is in use)",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-d",
              description="List directories themselves, not their contents",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-F",
              description="Append indicator (one of */=>@|) to entries",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--group-directories-first",
              description="Group directories before file",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-h",
              description="Print human readable size units",
              default=True))

    prog.parameter_add(Param(ptype="flag", keyword="-l",
              description="Long list format",
              default=True))

    prog.parameter_add(Param(ptype="flag", keyword="-S",
              description="Sort list by size",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--reverse",
              description="Reverse order",
              default=False))

    prog.parameter_add(Param(ptype="path", keyword=" ",
              description="Paths to list",
              multiple=True))

    prog.parameter_add(Param(ptype="file", keyword=" ",
              description="Files to list",
              multiple=True))

    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
def sort():
    title = "Shell Sort"
    description = "Sort lines of text"
    executable="sort"
    authors = biloti
    tags = ['sh']

    prog = Prog(title=title, description=description,
                authors=[haertel, eggert, fsf],
                url="https://www.gnu.org/software/coreutils",
                executable=executable, stdin=True)

    prog.parameter_add(Param(ptype="flag", keyword="--ignore-leading-blanks",
              description="Ignore leading blanks",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--dictionary-order",
              description="Consider only blanks and alphanumeric characters",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--ignore-case",
              description="Fold lower case to upper case characters (ignore case)",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--general-numeric-sort",
              description="Compare according to general numerical value",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--ignore-nonprinting",
              description="Consider only printable characters",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--month-sort",
              description="Compare (unknown) < 'JAN' < ... < 'DEC'",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--human-numeric-sort",
              description="Compare human readable numbers (e.g., 2K 1G)",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--numeric-sort",
              description="Compare according to string numerical value",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-R",
              description="Shuffle, but group identical keys",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--reverse",
              description="Reverse the result of comparisons",
              default=False))

    prog.parameter_add(Param(ptype="string", keyword="--key=",
              description="Sort via a key (see documentation)"))

    prog.parameter_add(Param(ptype="string", keyword="--field-separator=",
              description="Field separator"))

    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
def tail():
    title = "Shell Tail"
    description = "Output the last part of files"
    executable="tail"
    authors = biloti
    tags = ['sh','files']

    prog = Prog(title=title, description=description,
                authors=[rubin, mackenzie, taylor, meyering, fsf],
                url="https://www.gnu.org/software/coreutils/",
                executable=executable, stdin=True)

    prog.parameter_add(Param(ptype="flag", keyword="-f",
              description="Output appended data as the file grows",
              default=False))

    prog.parameter_add(Param(ptype="integer", keyword="-n ",
              description="How many lines to output",
              default=10))

    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
def uniq():
    title = "Shell Uniq"
    description = "Report or omit repeated lines"
    executable="uniq"
    authors = biloti
    tags = ['sh','files']

    prog = Prog(title=title, description=description,
                authors=[stallman, mackenzie, fsf],
                url="https://www.gnu.org/software/coreutils/",
                executable=executable, stdin=True)

    prog.parameter_add(Param(ptype="flag", keyword="--count",
              description="Prefix lines by the number of occurrences",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--repeated",
              description="Only print duplicate lines, one for each group",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-D",
              description="Print all duplicate lines",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--ignore-case",
              description="Ignore differences in case when comparing",
              default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--uniq",
              description="Only print unique lines",
              default=False))

    prog.parameter_add(Param(ptype="integer", keyword="--skip-fields=",
              description="Number of first fields to skip when comparing"))

    prog.parameter_add(Param(ptype="integer", keyword="--skip-chars=",
              description="Number of characters to skip when comparing"))

    prog.parameter_add(Param(ptype="integer", keyword="--check-chars=",
              description="Maximum number of characters in lines to compare"))


    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
def wc():
    title = "Shell WC"
    description = "Print newline, word, and byte counts for a file"
    executable="wc"
    authors = biloti
    tags = ['sh','files']

    prog = Prog(title=title, description=description,
                authors=[rubin, mackenzie, fsf],
                url="https://www.gnu.org/software/coreutils/",
                executable=executable, stdin=True)

    prog.parameter_add(Param(ptype="flag", keyword="-c",
                             description="Count bytes",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-m",
                             description="Count characters",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-l",
                             description="Count newlines",
                             default=True))

    prog.parameter_add(Param(ptype="flag", keyword="-w",
                             description="Count words",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="-L",
                             description="Print the maximum display width",
                             default=False))

    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
cat()
df()
du()
head()
ls()
sort()
tail()
uniq()
wc()
