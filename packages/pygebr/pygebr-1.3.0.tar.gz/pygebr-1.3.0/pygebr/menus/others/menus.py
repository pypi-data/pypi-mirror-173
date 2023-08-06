#!/bin/python3

# Create menus for using with PyGêBR

from pygebr import Person, Prog, Param, Flow
import os

basepath = os.path.dirname(__file__)

# authors
biloti = Person(name="Ricardo Biloti",
                email="biloti@unicamp.br",
                institution="University of Campinas",
                homepage="https://www.ime.unicamp.br/~biloti")

filpo = Person(name="Eduardo Filpo",
               email="efilpo@gmail.com",
               institution="Petrobras",
               homepage="https://www.researchgate.net/profile/Eduardo-Filpo-2")

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
# CSModeling -- https://gitlab.com/Biloti/csmodeling

def csmodeling():
    title = "CS Modeling"
    description = "CShot modeling wrapper"
    authors = biloti
    executable = "csmodeling"
    tags = ['su','simulation and model building','inct-gp','ggc - unicamp']

    prog = Prog(title=title, description=description,
                url="https://gitlab.com/Biloti/csmodeling",
                authors=biloti,
                executable=executable,
                stdin=False, stdout=False)

    prog.parameter_add(
        Param(ptype="path",
              keyword="--basedir=",
              description="Working directory",
              required=True,
              default="/tmp"))

    prog.parameter_add(
        Param(ptype="string",
              keyword="--subdir=",
              description="Folder name to store outputs",
              required=True,
              default="csmodel"))

    prog.parameter_add(
        Param(ptype="section", title="Model"))

    par = Param(ptype="enum",
                keyword="--xfactor=",
                description="Spatial unit",
                default="0")
    par.options([{"description": "autodetect", "value": "0"},
                 {"description": "kilometers", "value": "1000"},
                 {"description": "meters", "value": "1"}])
    prog.parameter_add(par)

    par = Param(ptype="string",
                keyword="--knots=",
                description="Interface's knots",
                required=True, multiple=True,
                placeholder="x1,z1;x2,z2;...;xn,zn",
                default=['0.0,0.0; 5.0,0.0','0.0,0.5; 1.5,0.55; 3.6,0.8; 5,0.8','0.0,1.0; 5.0,1.0'])
    par.regexp('^(((\s*)[+-]?(\d*[.])?\d+(\s*),(\s*)[+-]?(\d*[.])?\d+(\s*));)*(\s*)[+-]?(\d*[.])?\d+(\s*),(\s*)[+-]?(\d*[.])?\d+(\s*)$')
    prog.parameter_add(par)

    prog.parameter_add(
        Param(ptype="comment",
              description="Provide as many velocities below as interfaces specified above."))

    prog.parameter_add(
        Param(ptype="floats",
              keyword="--velocity=",
              description="Layers' velocities",
              required=True, separator=",",
              placeholder="v1,v2,...,vn",
              default='1.5, 2.1, 2.3'))

    prog.parameter_add(
        Param(ptype="section",
              title="Acquisition geometry"))

    prog.parameter_add(
        Param(ptype="flag",
              keyword="--direct",
              description="Enable direct wave computation",
              default=False))

    prog.parameter_add(
        Param(ptype="flag",
              keyword="--primary",
              description="Enable primary reflections computation",
              default=True))

    prog.parameter_add(
        Param(ptype="flag",
              keyword="--bottom",
              description="Enable reflection at bottom interface",
              default=False))

    par = Param(ptype="string",
                keyword="--raycode=",
                description="Ray code (list of interfaces where ray reflects)",
                required=False, multiple=True,
                placeholder="i1 i2 ... ik")
    par.regexp('^(\s*\d+\s*)+$')
    prog.parameter_add(par)

    par = Param(ptype="range",
                keyword="--takeoff=",
                description="Maximum takeoff angle (degrees)",
                default=80)
    par.range([0,90], vinc=1, vdigits=2)
    prog.parameter_add(par)

    prog.parameter_add(
        Param(ptype="float",
              keyword="--inc=",
              description="Takeoff angle step (degrees)",
              default=1))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--xstation=",
              description="First station x-coordinate",
              default=0))

    prog.parameter_add(
        Param(ptype="integer",
              keyword="--istation=",
              description="Reference index for the first station",
              default=0))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--dstation=",
              description="Station spacing",
              default=0.05))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--rdepth=",
              description="Receiver depth",
              default=0))

    par = Param(ptype="string",
                keyword="--well=",
                description="Knots for well",
                placeholder="x1,z1;x2,z2;...;xn,zn")

    par.regexp('^(((\s*)[+-]?(\d*[.])?\d+(\s*),(\s*)[+-]?(\d*[.])?\d+(\s*));)*(\s*)[+-]?(\d*[.])?\d+(\s*),(\s*)[+-]?(\d*[.])?\d+(\s*)$')

    prog.parameter_add(par)

    comment =  """Every shot, described below, is prescribed by receiver's locations,
    determined by the initial station reference number (or station
    index), last station index before a gap, first station index after
    a gap, and last station index. Also the shot location is provided
    in terms of the station it occupies and its depth.  However, shots
    can be allocated between stations, by providing a float station
    index.<br><br>For example, a shot specified as
    <strong>50, 150, 170, 270, 160.0, 0.015</strong> means that the shot is located at
    station 160, buried (15m), and the receivers are located from
    station 50 up to 150, and from station 170 up to 270. Therefore,
    there is a gap in the acquisition."""

    prog.parameter_add(Param(ptype="comment", description=comment))

    par = Param(ptype="string",
              keyword="--shot=",
              description="Active range of stations for a shot at (sx,sz)",
              required=True, multiple=True,
              placeholder="st1,st2,st3,st4,sx,sz",
              default='30,50,51,70,50,0')
    par.regexp("^(\s*[+-]?\d+\s*,){4}\s*[+-]?(\d*[.])?\d+\s*,\s*[+-]?(\d*[.])?\d+\s*$")
    prog.parameter_add(par)

    prog.parameter_add(
        Param(ptype="integer",
              keyword="--dxshot=",
              description="Shot increment (stations) for surface acquisition",
              default=1))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--sdepth=",
              description="Depth of the first source for downhole acquisition"))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--dwshot=",
              description="Distance between shots for downhole acquisition"))

    prog.parameter_add(
        Param(ptype="integer",
              keyword="--nshots=",
              description="Number of regular shots",
              default=1))

    prog.parameter_add(
        Param(ptype="section",
              title="Seismogram"))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--f0=",
              description="First wavelet frequency (trapezoidal band-pass filter)",
              default=10))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--f1=",
              description="Second wavelet frequency (trapezoidal band-pass filter)",
              default=25))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--f2=",
              description="Third wavelet frequency (trapezoidal band-pass filter)",
              default=35))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--f3=",
              description="Fourth wavelet frequency (trapezoidal band-pass filter)",
              default=50))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--wlen=",
              description="Wavelet length (seconds)",
              default=0.15))

    prog.parameter_add(
        Param(ptype="integer",
              keyword="--dt=",
              description="Sampliong rate (micro-seconds)",
              default=4000))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--tmax=",
              description="Maximum recorded time (seconds)",
              default=4))

    prog.parameter_add(
        Param(ptype="section",
              title="Export"))

    prog.parameter_add(
        Param(ptype="flag",
              keyword="--nogplt",
              description="Suppress model/rays export through gnuplot",
              default=False))

    par = Param(ptype="enum",
                keyword="--palette=",
                description="Palette for graphics",
                default='2')
    par.options([{'description': 'Black & white', 'value': '0'},
                 {'description': 'Transparent', 'value': '1'},
                 {'description': 'Samalamalam', 'value': '2'},
                 {'description': 'Terrain', 'value': '3'},
                 {'description': 'Citrus', 'value': '4'},
                 {'description': 'Light terrain', 'value': '5'},
                 {'description': 'Sweet autum', 'value': '6'},
                 {'description': 'Sunset', 'value': '7'}])
    prog.parameter_add(par)

    prog.parameter_add(
        Param(ptype="string",
              keyword="--title=",
              description="Figure's title",
              default="CS Modeling"))

    prog.parameter_add(
        Param(ptype="flag",
              keyword="--rays",
              description="Plot rays",
              default=True))

    prog.parameter_add(
        Param(ptype="integer",
              keyword="--decimate=",
              description="Plot one ray at every n",
              default=1))

    prog.parameter_add(
        Param(ptype="integer",
              keyword="--limit=",
              description="Maximum number of ploted rays"))

    prog.parameter_add(
        Param(ptype="flag",
              keyword="--nointerfaces",
              description="Suppress interfaces in figure",
              default=False))

    prog.parameter_add(
        Param(ptype="flag",
              keyword="--well",
              description="Suppress well in figure",
              default=False))

    prog.parameter_add(
        Param(ptype="flag",
              keyword="--nogrid",
              description="Suppress grid lines in figure",
              default=True))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--xmin=",
              description="Minimum x coordinate in figure"))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--xmax=",
              description="Maximum x coordinate in figure"))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--zmin=",
              description="Minimum z coordinate in figure"))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--zmax=",
              description="Maximum z coordinate in figure"))

    prog.parameter_add(
        Param(ptype="float",
              keyword="--xvel=",
              description="Horizontal coordinate to display layer velocities"))

    menu = Flow(title=title, description=description,
                authors=biloti, tags=tags)

    commit_menu(title, description, authors, executable, tags, prog)

#------------------------------------------------------------------------------
# dzt2rsf -- https://gitlab.com/Biloti/dzt2rsf

def dzt2rsf():
    title = "DZT to RSF"
    description = "Convert GPR raw data file (DZT) to RSF"
    authors = biloti
    executable = 'dzt2rsf'
    tags = ['dzt', 'rsf', 'gpr', 'import/export', 'data format conversion',
            'inct-gp','ggc - unicamp']

    prog = Prog(title=title, description=description,
                url="https://gitlab.com/Biloti/dzt2rsf",
                authors=[biloti, filpo],
                executable=executable)

    prog.parameter_add(Param(ptype="file", keyword="--prefix=",
                             description="Prefix for RSF ouput file",
                             required=True))

    prog.parameter_add(Param(ptype="float", keyword="--d2=",
                             description="Distance between consecutive traces (in meters)",
                             default=1))

    prog.parameter_add(Param(ptype="flag", keyword="--mean",
                             description="Print mean value to stdout",
                             default=False))

    prog.parameter_add(Param(ptype="flag", keyword="--verbose",
                             description="Verbose output",
                             default=False))

    menu = Flow(title=title, description=description,
                authors=biloti, tags=tags)

    commit_menu(title, description, authors, executable, tags, prog)
#------------------------------------------------------------------------------

csmodeling()
dzt2rsf()
