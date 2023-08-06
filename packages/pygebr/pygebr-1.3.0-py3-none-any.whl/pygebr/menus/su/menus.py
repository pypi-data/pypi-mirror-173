#!/bin/python3

# This file is part of PyGeBR.
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
# You should have received a copy of the GNqU General Public License
# along with PyGeBR.  If not, see <https://www.gnu.org/licenses/>
#
# Copyright 2021-2022 Ricardo Biloti <biloti@unicamp.br>
#                     Eduardo Filpo <efilpo@gmail.com>
#

from pygebr import Person, Prog, Param, Flow
import os

#---------------------------------------------------------------------
# Global variables
orderstr = ['st','nd','rd','th']

# authors
biloti = Person(name="Ricardo Biloti",
                email="biloti@unicamp.br",
                institution="University of Campinas",
                homepage="https://www.ime.unicamp.br/~biloti")

baoniu_han = Person(name="Baoniu Han", email="bhan@mines.edu")
bjoern_rommel = Person(name="Bjoern Rommel", institution="CWP")
brian_summer = Person(name="Brian Summer", institution="SEP")
carlos_theodoro = Person(name="Carlos E. Theodoro", institution="CWP")
chris_liner = Person(name="Chris Liner", institution="CWP")
chuck_sword = Person(name="Chuck Sword", institution="SEP")
dave_hale = Person(name="Dave Hale", institution="CWP")
david_forel = Person(name="David Forel", institution="MTU")
dominique_rousset = Person(name = "Dominique Rousset",
                           institution="Université de Pau et des Pays de l'Adour")
einar_kjartansson = Person(name="Einar Kjartansson", institution="SEP")
fernando_roxo = Person(name="Fernando M. Roxo da Motta", email="petro@roxo.org")
hans_ecke = Person(name="Hans Ecke")
jack_cohen = Person(name="Jack K. Cohen", institution="CWP")
john_stockwell = Person(name="John Stockwell", institution="CWP")
jon_claerbout = Person(name="Jon Claerbout", institution="SEP")
mohamed_hamza = Person(name = "Mohamed Hamza",
                       institution = "Université de Pau et des Pays de l'Adour")
nils_maercklin = Person(name="Nils Maercklin",
                        institution="RISSC, University of Napoli")
sang_yong_suh = Person(name="Sang-Yong Suh")
shuki_ronen = Person(name="Shuki Ronen", institution="CWP")
stew_levin = Person(name="Stew Levin", institution="SEP")
tanya_slota = Person(name="Tanya Slota", institution="CSM")
toralf_foerster = Person(name="Toralf Foerster", institution="Warnemuende")
werner_heigl = Person(name="Werner M. Heigl", institution="CENPET")

suurl = "https://github.com/JohnWStockwellJr/SeisUnix"
su = Person(institution="Sesmic Un*x", homepage=suurl)

su_hdr_fields = [
    {"description": "Alias filter frequency if used", "value": "afilf"},
    {"description": "Alias filter slope", "value": "afils"},
    {"description": "Alignment padding", "value": "shortpad"},
    {"description": "CDP ensemble number", "value": "cdp"},
    {"description": "Coordinate units code", "value": "counit"},
    {"description": "Correlated flag", "value": "corr"},
    {"description": "Data use", "value": "duse"},
    {"description": "Datum elevation at receiver group", "value": "gdel"},
    {"description": "Datum elevation at source", "value": "sdel"},
    {"description": "Day of year", "value": "day"},
    {"description": "Delay recording time in ms", "value": "delrt"},
    {"description": "Energy source point number", "value": "ep"},
    {"description": "Field record number", "value": "fldr"},
    {"description": "Final mute time", "value": "mute"},
    {"description": "First sample location for non-seismic data", "value": "f1"},
    {"description": "First trace location", "value": "f2"},
    {"description": "Gain type of field instruments code", "value": "gain"},
    {"description": "Gap size", "value": "gaps"},
    {"description": "Geophone group number of last trace within original field record", "value": "grnlof"},
    {"description": "Geophone group number of roll switch position one", "value": "grnors"},
    {"description": "Geophone group number of trace one within original field record", "value": "grnofr"},
    {"description": "Group static correction", "value": "gstat"},
    {"description": "High cut frequncy if used", "value": "hcf"},
    {"description": "High cut slope", "value": "hcs"},
    {"description": "Hour of day (24 hour clock)", "value": "hour"},
    {"description": "Initial mute time", "value": "muts"},
    {"description": "Instrument early or initial gain", "value": "igi"},
    {"description": "Instrument gain constant", "value": "igc"},
    {"description": "Lag time A", "value": "laga"},
    {"description": "Lag time B", "value": "lagb"},
    {"description": "Low cut frequency if used", "value": "lcf"},
    {"description": "Low cut slope", "value": "lcs"},
    {"description": "Mark selected traces", "value": "mark"},
    {"description": "Minute of hour", "value": "minute"},
    {"description": "Negative of power used for dynamic range compression", "value": "ungpow"},
    {"description": "Notch filter frequency if used", "value": "nofilf"},
    {"description": "Notch filter slope", "value": "nofils"},
    {"description": "Number of horizontally summed traces", "value": "nhs"},
    {"description": "Number of samples", "value": "ns"},
    {"description": "Number of traces", "value": "ntr"},
    {"description": "Number of vertically summed traces", "value": "nvs"},
    {"description": "Offset (signed distance from source to receiver group)", "value": "offset"},
    {"description": "Overtravel taper code", "value": "otrav"},
    {"description": "Receiver group elevation from sea level", "value": "gelev"},
    {"description": "Reciprocal of scaling factor to normalize range", "value": "unscale"},
    {"description": "Sampling interval in microseconds", "value": "dt"},
    {"description": "Sample spacing between traces", "value": "d2"},
    {"description": "Sample spacing for non-seismic data", "value": "d1"},
    {"description": "Scale factor for source/receiver coordinates", "value": "scalco"},
    {"description": "Scale factor for source/receiver elevations, datum and water depth", "value": "scalel"},
    {"description": "Second of minute", "value": "sec"},
    {"description": "Source depth (positive)", "value": "sdepth"},
    {"description": "Source elevation from sea level", "value": "selev"},
    {"description": "Source static correction", "value": "sstat"},
    {"description": "Subweathering velocity", "value": "swevel"},
    {"description": "Sweep frequency at end", "value": "sfe"},
    {"description": "Sweep frequency at start", "value": "sfs"},
    {"description": "Sweep length in ms", "value": "slen"},
    {"description": "Sweep trace length at end in ms", "value": "stae"},
    {"description": "Sweep trace length at start in ms", "value": "stas"},
    {"description": "Sweep type code", "value": "styp"},
    {"description": "Taper type", "value": "tatyp"},
    {"description": "Time basis code", "value": "timbas"},
    {"description": "Total static applied", "value": "tstat"},
    {"description": "Trace identification code", "value": "trid"},
    {"description": "Trace number sequence within field record", "value": "tracf"},
    {"description": "Trace number sequence within line", "value": "tracl"},
    {"description": "Trace number sequence within reel", "value": "tracr"},
    {"description": "Trace number within CDP ensemble", "value": "cdpt"},
    {"description": "Trace weighting factor", "value": "trwf"},
    {"description": "Uphole time at receiver group", "value": "gut"},
    {"description": "Uphole time at source", "value": "sut"},
    {"description": "Water depth at receiver group", "value": "gwdep"},
    {"description": "Water depth at source", "value": "swdep"},
    {"description": "Weathering velocity", "value": "wevel"},
    {"description": "X group coordinate", "value": "gx"},
    {"description": "X source coordinate", "value": "sx"},
    {"description": "Y group coordinate", "value": "gy"},
    {"description": "Y source coordinate", "value": "sy"},
    {"description": "Year data recorded", "value": "year"}
]

#---------------------------------------------------------------------
# COMMON PARAMETERS

par_f_dt_004 = Param(ptype="float", keyword="dt=",
                     description="Time sampling interval (sec)",
                     default=0.004)
par_f_dt_04 = Param(ptype="float", keyword="dt=",
                    description="Time sampling interval (sec)",
                    default=0.04)

par_p_tmpdir = Param(ptype="path", keyword="tmpdir=",
                     description="Prefix for storing temporary files")

#---------------------------------------------------------------------
def commit_menu(title, description, authors, executable, tags, prog,
                fname=None):
    menu = Flow(title=title, description=description,
                authors=authors, tags=tags)

    menu.program_add(prog)

    if fname == None:
        fname = executable

    fn = os.path.join(os.path.dirname(__file__), fname + ".json")
    menu.save(fn)

#---------------------------------------------------------------------
def a2b():

    title = "ASCII to Binary"
    description = "Convert ascii floats to binary"
    executable = "a2b"
    authors = biloti
    tags=['seismic unix', 'import/export']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[jack_cohen, dave_hale, hans_ecke, su],
             executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="n1=",
                          description="Floats per line in input file",
                          default=2, required=False))

    p.parameter_add(Param(ptype="file", keyword="outpar=",
                          description="Output parameter file (contains the number of lines)",
                          default="/dev/null",
                          value=[{"literal":"/dev/null"}]))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def b2a():

    title = "Binary to ASCII"
    description = "Convert binary floats to ascii"
    executable = "b2a"
    authors = biloti
    tags=['seismic unix', 'import/export']

    p = Prog(title=title, description=description,
             url=suurl, authors=[jack_cohen, su], executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="n1=",
                          description="Floats per line in output file",
                          default=2, required=False))

    par = Param(ptype="enum", keyword="format=",
                description="Format",
                default="0")
    par.options([{"description": "Scientific notation", "value": "0"},
                 {"description": "Long decimal float form", "value": "1"}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="file", keyword="outpar=",
                          description="Output parameter file (contains the number of lines)",
                          default="/dev/null",
                          value=[{"literal":"/dev/null"}]))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def segyclean():
    title = "SEG-Y Clean"
    description = "Zero out unassigned portion of header"
    executable = "segyclean"
    authors = biloti
    tags=['su','seismic unix', 'header', 'import/export']

    p = Prog(title=title, description=description,
             url=suurl, authors=[jack_cohen, su], executable=executable)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def segyread():
    title = "SEG-Y Read"
    description = "Read an SEG-Y file"
    executable = "segyread"
    authors = biloti
    tags=['su','seismic unix', 'header', 'import/export']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[einar_kjartansson,
                      jack_cohen,
                      john_stockwell,
                      Person(name="Tony Kocurko", institution="Memorial University of Newfoundland"),
                      Person(name="Remco Romijn", institution="Applied Geophysics, TU Delft"),
                      Person(name="J.W. de Bruijn", institution="Applied Geophysics, TU Delft"),
                      Person(name="Matthias Imhof", institution="Virginia Tech"),
                      su],
             executable=executable,
             stdin=False)

    par = Param(ptype="file", keyword="tape=",
                description="SEG-Y filename",
                required=True)
    par.fileType("SEG-Y data file")
    par.filePattern("*.segy")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Echo every block of traces",
                          default=False))

    p.parameter_add(Param(ptype="integer", keyword="vblock=",
                          description="Block of traces to echo",
                          default=50))

    p.parameter_add(Param(ptype="file", keyword="hfile=",
                          description="File to store ebcdic block (as ascii)"))

    p.parameter_add(Param(ptype="file", keyword="bfile=",
                          description="File to store binary block"))

    p.parameter_add(Param(ptype="file", keyword="xfile=",
                          description="File to store extended text block"))

    p.parameter_add(Param(ptype="flag", keyword="over=1",
                          description="Override and attempt conversion",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="conv=0",
                          description="Dismiss convertion to native format",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="ebcdic=0",
                          description="Don't convert ebcdic to ascii",
                          default=False))

    p.parameter_add(Param(ptype="integer", keyword="ns=",
                          description="Number of samples per trace"))

    par = Param(ptype="enum", keyword="trcwt=",
                description="Trace weighting factor")
    par.options([
        {"description": "Apply", "value": "1"},
        {"description": "Do not apply", "value": "0"}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="integer", keyword="trmin=",
                          description="First trace to read",
                          default=1))

    p.parameter_add(Param(ptype="integer", keyword="trmax=",
                          description="Last trace to read"))

    par = Param(ptype="enum", keyword="endian=",
                description="Byte order (leave unset for autodetection)")
    par.options([
        {"description": "Little-endian", "value": "0"},
        {"description": "Big-endian", "value": "1"}])
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suaddevent():
    title = "SU Add Event"
    description = "Add a linear or hyperbolic moveout event to seismic data"
    executable = "suaddevent"
    authors = biloti
    tags=['su','seismic unix', 'simulation and model building']

    p = Prog(title=title, description=description,
             url=suurl, authors=su, executable=executable)

    par = Param(ptype="enum", keyword="type=",
                description="Event type",
                default='nmo', required=True)
    par.options([
        {'description': 'Hyperbolic moveout', 'value': 'nmo'},
        {'description': 'Linear moveout', 'value': 'lmo'}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="t0=",
                          description="Zero-offset intercept (sec)",
                          default=1))

    p.parameter_add(Param(ptype="float", keyword="vel=",
                          description="Moveout velocity (m/s)",
                          default=3000))

    p.parameter_add(Param(ptype="float", keyword="amp=",
                          description="Amplitude",
                          default=1))

    p.parameter_add(Param(ptype="float", keyword="dt=",
                          description="Time sampling interval (sec)"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suaddhead():
    title = "SU Add Head"
    description = "Put headers on bare traces and set the tracl and ns fields"
    executable = "suaddhead"
    authors = biloti
    tags=['su','seismic unix', 'header', 'import/export']

    p = Prog(title=title, description=description,
             url=suurl, authors=su, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="ns=",
                          description="Number of samples per trace",
                          required=True))

    par = Param(ptype="enum", keyword="ftn=",
                description="Binary format", default='0')
    par.options([
        {'description': 'Unformatted data written from C', 'value': '0'},
        {'description': 'Unformatted data written from Fortran', 'value': '1'}])
    p.parameter_add(par)

    par = Param(ptype="enum", keyword="tsort=",
                description="Trace sorting", default='3')
    par.options([
        {'description': 'as recorded (no sorting)', 'value': '1'},
        {'description': 'CDP ensable', 'value': '2'},
        {'description': 'single fold continuous profile', 'value': '3'},
        {'description': 'horizontally stacked', 'value': '4'}])
    p.parameter_add(par)

    par = Param(ptype="integer", keyword="ntrpr=",
                description="Number of data traces per record", default=1)
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suaddnoise():
    title = "SU Add Noise"
    description = "Add noise to traces"
    executable = "suaddnoise"
    authors = biloti
    tags=['su','seismic unix', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[jack_cohen,
                      john_stockwell,
                      su],
             executable=executable)

    p.parameter_add(Param(ptype="float", keyword="sn=",
                          description="Signal to noise ratio",
                          default=20))

    par = Param(ptype="enum", keyword="noise=",
                description="Noise type", default='gauss',
                required=True)
    par.values('gauss')
    par.options([
        {'description': 'Gaussian distribuition', 'value': 'gauss'},
        {'description': 'Uniform distribution', 'value': 'flat'}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="integer", keyword="seed=",
                          description="Random number seed"))

    p.parameter_add(Param(ptype="floats", keyword="f=",
                          description="Array of filter frequencies",
                          separator=","))

    p.parameter_add(Param(ptype="floats", keyword="amps=",
                          description="Array of filter amplitudes",
                          separator=","))

    p.parameter_add(Param(ptype="float", keyword="dt=",
                          description="Time sampling interval"))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Print some useful information",
                          default=False))

    p.parameter_add(par_p_tmpdir)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sucdpbin():
    title = "SU CDP Binning"
    description = "Compute CDP bin number"
    executable = "sucdpbin"
    authors = biloti
    tags=['su','seismic unix']

    p = Prog(title=title, description=description,
             url=suurl, authors=[dominique_rousset, mohamed_hamza, su],
             executable=executable)

    par = Param(ptype="comment",
                description="Next 2 parameters are arrays with equal number of elements")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="floats", keyword="xline=",
                          description="Array of x coordinates defining the CDP line",
                          separator=",",
                          required=True))

    p.parameter_add(Param(ptype="floats", keyword="yline=",
                          description="Array of y coordinates defining the CDP line",
                          separator=",",
                          required=True))

    p.parameter_add(Param(ptype="float", keyword="dcdp=",
                          description="Distance between bin centers",
                          required=True))

    p.parameter_add(Param(ptype="integer", keyword="cdpmin=",
                          description="Minimu CDP bin number",
                          default=1001))

    p.parameter_add(Param(ptype="float", keyword="distmax=",
                          description="Search radius"))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Verbose output",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suchw():
    title = "SU Change Header"
    description = "Change Header Word using one or two header word fields"
    executable = "suchw"
    authors = biloti
    tags=['su','seismic unix', 'header', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[
                 einar_kjartansson,
                 jack_cohen,
                 john_stockwell,
                 su],
             executable=executable)

    par = Param(ptype="enum", keyword="key1=",
                description="Output header field")
    par.options(su_hdr_fields)
    p.parameter_add(par)

    par = Param(ptype="enum", keyword="key2=",
                description="First input header field")
    par.options(su_hdr_fields)
    p.parameter_add(par)

    par = Param(ptype="enum", keyword="key3=",
                description="Second input header field")
    par.options(su_hdr_fields)
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="a=",
                          description="Overall shift", default=0))

    p.parameter_add(Param(ptype="float", keyword="b=",
                          description="Scale on first input key", default=1))

    p.parameter_add(Param(ptype="float", keyword="c=",
                          description="Scale on second input key", default=0))

    p.parameter_add(Param(ptype="float", keyword="d=",
                          description="Overall scale", default=1))

    p.parameter_add(Param(ptype="float", keyword="e=",
                          description="Exponent on first input key", default=1))

    p.parameter_add(Param(ptype="float", keyword="f=",
                          description="Exponent on second input key", default=1))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sucountkey():
    title = "SU Count Key"
    description = "Count the number of unique values for a given keyword"
    executable = "sucountkey"
    authors = biloti
    tags=['su','seismic unix', 'header', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl, authors=[baoniu_han, su],
             executable=executable)

    p.parameter_add(Param(ptype="strings", keyword="key=",
                          description="List of header words",
                          separator=",",
                          default="cdp,offset"))

    p.parameter_add(Param(ptype="flag", keyword="verbose=0",
                          description="Be less verbose",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sudiff():
    title = "SU Diff"
    description = "Compute the difference of two data sets"
    executable = "sudiff"
    authors = biloti
    tags=['su','seismic unix', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl, authors=[shuki_ronen, jack_cohen,
                                 john_stockwell, fernando_roxo, su],
             executable=executable, stdin=False)

    par = Param(ptype="file", keyword=" ",
                description="First data set",
                placeholder="SU file",
                required=True)
    par.fileType("SU")
    par.filePattern("*.su")
    p.parameter_add(par)

    par = Param(ptype="file", keyword=" ",
                description="Second data set",
                placeholder="SU file",
                required=True)
    par.fileType("SU")
    par.filePattern("*.su")
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sudipfilt():
    title = "SU Dip Filter"
    description = "Dip, or better, slope filter in f-k domain"
    executable = "sudipfilt"
    authors = biloti
    tags=['su','seismic unix', 'filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=suurl, authors=[dave_hale, jack_cohen, su],
             executable=executable)

    p.parameter_add(Param(ptype="float", keyword="dt=",
                          description="Time sampling (sec)"))

    p.parameter_add(Param(ptype="float", keyword="dx=",
                          description="Spatial sampling"))

    p.parameter_add(Param(ptype="floats", keyword="slopes=",
                          description="Array of monotonically increasing slopes",
                          separator=",",
                          placeholder="s1,s2,...,sn"))

    p.parameter_add(Param(ptype="floats", keyword="amps=",
                          description="Array of amplitudes corresponding to slopes",
                          separator=",",
                          placeholder="a1,a2,...,an"))

    p.parameter_add(Param(ptype="float", keyword="bias=",
                          description="Slope made horizontal before filtering",
                          default=0))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Be more verbose",
                          default=False))

    p.parameter_add(par_p_tmpdir)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sufilter():
    title = "SU Filter"
    description = "Applies a zero-phase, sine-squared tapered filter"
    executable = "sufilter"
    authors = biloti
    tags=['su','seismic unix', 'filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=suurl, authors=[john_stockwell, werner_heigl, su],
             executable=executable)

    p.parameter_add(Param(ptype="comment",
                          description="Next 2 parameters are arrays with equal number of elements"))

    p.parameter_add(Param(ptype="floats", keyword="f=",
                          description="Array of filter frequencies (Hz)",
                          separator=",",
                          placeholder="f1,f2,f3,...,fn"))

    p.parameter_add(Param(ptype="floats", keyword="amps=",
                          description="Array of filter amplitudes",
                          separator=",",
                          placeholder="a1,a2,a3,...,an"))

    p.parameter_add(Param(ptype="float", keyword="dt=",
                          description="Time sampling interval (sec)"))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Be more verbose",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suflip():
    title = "SU Flip"
    description = "Flip a data set in various ways"
    executable = "suflip"
    authors = biloti
    tags=['su','seismic unix', 'filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=suurl, authors=[chris_liner, jack_cohen, john_stockwell, su],
             executable=executable)

    comment = """Time sampling information is lost when rotating
    data (counter-)clockwise."""

    p.parameter_add(Param(ptype="comment", description=comment))

    par = Param(ptype="enum", keyword="flip=",
                description="Flip mode",
                default="1", required=True)

    p.parameter_add(par)

    par.options([
        {"description": "Rotate 90 degrees clockwise", "value": "1"},
        {"description": "Rotate 90 degrees counter-clockwise", "value": "-1"},
        {"description": "Transpose data", "value": "0"},
        {"description": "Flip right-to-left", "value": "2"},
        {"description": "Flip top-to-bottom", "value": "3"}])

    p.parameter_add(par_p_tmpdir)

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Echos flip information",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sufxdecon():
    title = "SU FX Decon"
    description = "Random noise attenuation by FX deconvolution"
    executable = "sufxdecon"
    authors = biloti
    tags=['su','seismic unix', 'filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=suurl, authors=[carlos_theodoro, su],
             executable=executable)

    p.parameter_add(Param(ptype="float", keyword="taper=",
                          description="Length of taper",
                          default=0.1))

    p.parameter_add(Param(ptype="float", keyword="fmin=",
                          description="Minimum frequency to process in Hz",
                          default=6))

    p.parameter_add(Param(ptype="float", keyword="fmax=",
                          description="Maximum frequency to process in Hz"))

    p.parameter_add(Param(ptype="integer", keyword="twlen=",
                          description="Time window length"))

    p.parameter_add(Param(ptype="integer", keyword="ntrw=",
                          description="Number of traces in window",
                          default=10))

    p.parameter_add(Param(ptype="integer", keyword="ntrf=",
                          description="Number of traces for filter",
                          default=4))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Verbose output",
                          default=False))

    p.parameter_add(par_p_tmpdir)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sugain():
    title = "SU Gain"
    description = "Apply various types of gain"
    executable = "sugain"
    authors = biloti
    tags=['su','seismic unix',
          'gain, nmo, stack and standard processes']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[jon_claerbout, jack_cohen,
                      brian_summer, dave_hale, su],
             executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="panel=1",
                          description="Gain whole data set instead of trace by trace",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="tpow=",
                          description="A: multiply data by t^A",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="epow=",
                          description="B: Multiply data by exp(B * t)",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="etpow=",
                          description="C: Multiply data by exp(B * t^C)",
                          default=1))

    p.parameter_add(Param(ptype="float", keyword="gpow=",
                          description="D: Take signed D-th power of scale data",
                          default=1))

    p.parameter_add(Param(ptype="flag", keyword="agc=1",
                          description="Do automatic gain control (AGC)",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="wagc=1",
                          description="Do automatic gain control with gaussian taper",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="wagc=",
                          description="AGC window (sec)",
                          default=0.5))

    p.parameter_add(Param(ptype="float", keyword="trap=",
                          description="Zero any value whose magnitude exceeds this value"))

    p.parameter_add(Param(ptype="float", keyword="clip=",
                          description="Clip any value whose magnitude exceeds this value"))

    p.parameter_add(Param(ptype="float", keyword="pclip=",
                          description="Clip any value greater than this value"))

    p.parameter_add(Param(ptype="float", keyword="nclip=",
                          description="Clip any value less than this value"))

    p.parameter_add(Param(ptype="float", keyword="qclip=",
                          description="E: Clip by quantile on absolute values on trace",
                          default=1))

    p.parameter_add(Param(ptype="flag", keyword="qbal=1",
                          description="Balance traces by E and scale",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="pbal=1",
                          description="Balance traces by dividing by RMS value",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="mbal=1",
                          description="Balance traces by subtracting the mean",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="maxbal=1",
                          description="Balance traces by subtracting the max",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="scale=",
                          description="Multiply data by overall this scale factor",
                          default=1))

    p.parameter_add(Param(ptype="float", keyword="norm=",
                          description="Divide data by overall scale factor"))

    p.parameter_add(Param(ptype="float", keyword="bias=",
                          description="Bias data by adding this overall value",
                          default=0))

    p.parameter_add(Param(ptype="flag", keyword="jon=1",
                          description="Jon Claerbout's particular setup (A=2, D=0.5, E=0.95)",
                          default=False))

    par = Param(ptype="enum", keyword="mark=",
                          description="Traces to gain")
    par.options([{"description": "apply to trace with mark = 0", "value": "0"},
                 {"description": "apply to trace with mark != 0", "value": "1"}])

    p.parameter_add(par_p_tmpdir)

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Echos information",
                          default=False))


    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sugethw():
    title = "SU Get HW"
    description = "Write the values of the selected key words"
    executable = "sugethw"
    authors = biloti
    tags=['su','seismic unix', 'header', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[shuki_ronen, jack_cohen, john_stockwell, su],
             executable=executable)

    p.parameter_add(Param(ptype="strings", keyword="key=",
                          description="List of keys words",
                          separator=",",
                          default="sx,gy,offset"))

    par = Param(ptype="enum", keyword="output=",
                description="Output mode",
                default="ascii")
    par.options([{"description": "as ascii for display", "value": "ascii"},
                 {"description": "as binary floats", "value": "binary"},
                 {"description": "as ascii for geometry setting", "value": "geom"}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Be more verbose",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sukeycount():
    title = "SU Key Count"
    description = "Write a count of a selected key"
    executable = "sukeycount"
    authors = biloti
    tags=['su','seismic unix', 'header', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl, authors=[david_forel, su],
             executable=executable)


    par = Param(ptype="enum", keyword="key=",
                description="Key word to count",
                required=True,
                default="cdp")
    par.options(su_hdr_fields)
    p.parameter_add(par)

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Be more verbose",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sunmo():
    title = "SU NMO"
    description = "NMO for an arbitrary velocity function of time and CDP"
    executable = "sunmo"
    authors = biloti
    tags=['su','seismic unix', 'gain, nmo, stack and standard processes']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[shuki_ronen, chuck_sword, jack_cohen, dave_hale, bjoern_rommel,
                      carlos_theodoro, sang_yong_suh, john_stockwell, su],
             executable=executable)

    p.parameter_add(Param(ptype="floats", keyword="tnmo=",
                          description="NMO times corresponding to velocities below",
                          default="0", multiple=True))

    p.parameter_add(Param(ptype="floats", keyword="vnmo=",
                          description="NMO velocities corresponding to times above",
                          default="1500", multiple=True))

    p.parameter_add(Param(ptype="integers", keyword="cdp=",
                          description="CDPs for which times and velocities are specified"))

    p.parameter_add(Param(ptype="float", keyword="smute=",
                          description="Samples with NMO stretch exceeding this value are zeroed",
                          default=1.5))

    p.parameter_add(Param(ptype="integer", keyword="lmute=",
                          description="Length (in samples) of linear ramp for stretch mute",
                          default=25))

    p.parameter_add(Param(ptype="flag", keyword="sscale=0",
                          description="Don't divide output samples by NMO stretch factor",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="invert=1",
                          description="Perform approximate invers NMO",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="upward=1",
                          description="Scan upward to find first sample to kill",
                          default=False))

    p.parameter_add(Param(ptype="file", keyword="voutfile=",
                          description="File to save interpolated velocity function"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sunull():
    title = "SU Null"
    description = "Create null (all zeroes) traces"
    executable = "sunull"
    authors = biloti
    tags=['su','seismic unix', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[jack_cohen, su],
             executable=executable, stdin=False)

    p.parameter_add(Param(ptype="integer", keyword="nt=",
                          description="Number of samples per trace",
                          default=251, required=True))

    p.parameter_add(Param(ptype="integer", keyword="ntr=",
                          description="Number of traces to create",
                          default=5))

    p.parameter_add(par_f_dt_004)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def supaste():
    title = "SU Paste"
    description = "Paste existing SU headers on existing binary data"
    executable = "supaste"
    authors = biloti
    tags=['su','seismic unix', 'header', 'import/export']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[jack_cohen, su],
             executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="ns=",
                          description="Number of samples per trace",
                          required=True))

    p.parameter_add(Param(ptype="file", keyword="head=",
                          description="File to load SEG-Y headers from"))

    par = Param(ptype="enum", keyword="ftn=",
                description="Binary format", default='0')
    par.options([
        {'description': 'Unformatted data written from C', 'value': '0'},
        {'description': 'Unformatted data written from Fortran', 'value': '1'}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Verbose output",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def supef():
    title = "SU PEF"
    description = "Wiener (least squares) predictive error filtering"
    executable = "supef"
    authors = biloti
    tags=['su','seismic unix', 'header', 'import/export']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[shuki_ronen, john_stockwell, tanya_slota, su],
             executable=executable)

    p.parameter_add(Param(ptype="float", keyword="dt=",
                          description="Time sampling interval"))

    p.parameter_add(Param(ptype="integers", keyword="cdp=",
                          description="Array of CDP's",
                          separator=",",
                          placeholder="cdp1,cdp2,...,cdpN"))

    p.parameter_add(Param(ptype="floats", keyword="minlag=",
                          description="Array of minimum lag of prediction",
                          separator=",",
                          placeholder="min1,min2,...,minN"))

    p.parameter_add(Param(ptype="floats", keyword="maxlag=",
                          description="Array of maximum lag of prediction",
                          separator=",",
                          placeholder="max1,max2,...,maxN"))

    p.parameter_add(Param(ptype="float", keyword="pnoise=",
                          description="Relative additive noise",
                          default=0.001))

    p.parameter_add(Param(ptype="float", keyword="mincorr=",
                          description="Start of autocorrelation window (sec)"))

    p.parameter_add(Param(ptype="float", keyword="maxcorr=",
                          description="End of autocorrelation window (sec)"))

    p.parameter_add(Param(ptype="flag", keyword="wienerout=1",
                          description="Show Wiener filter on each trace",
                          default=False))

    p.parameter_add(Param(ptype="file", keyword="outpar=",
                          description="Output parameter file when flag above is checked"))

    p.parameter_add(Param(ptype="floats", keyword="mix=",
                          description="Array of weights for moving average of the autocorrelations",
                          separator=","))

    par = Param(ptype="enum", keyword="method=",
                description="Interpolation method of CDPs", default='linear')
    par.options([
        {'description': 'Linear', 'value': 'linear'},
        {'description': 'Monotonic cubic', 'value': 'mono'},
        {'description': "Akima's cubic", 'value': 'akima'},
        {'description': 'Cubic spline', 'value': 'spline'}])
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suplane():
    title = "SU Plane"
    description = "Create common offset data file with up to 3 planes"
    executable = "suplane"
    authors = biloti
    tags=['su','seismic unix', 'simulation and model building']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[chris_liner, su],
             executable=executable,
             stdin=False, stdout=True, stderr=True)

    p.parameter_add(Param(ptype="integer", keyword="npl=",
                          description="Number of planes",
                          default=3))

    p.parameter_add(Param(ptype="integer", keyword="nt=",
                          description="Number of time samples",
                          default=64))

    p.parameter_add(Param(ptype="integer", keyword="ntr=",
                          description="Number of traces",
                          default=32))

    p.parameter_add(Param(ptype="flag", keyword="taper=1",
                          description="Taper planes to zero at the end",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="offset=",
                          description="Offset",
                          default=400))

    p.parameter_add(par_f_dt_004)

    for k in range(1,4):
        p.parameter_add(Param(ptype="section", title="%i"%k + orderstr[k-1] + " plane"))
        p.parameter_add(Param(ptype="integer", keyword="dip%i="%k,
                              description="Dip of plane (ms/trace)"))
        p.parameter_add(Param(ptype="integer", keyword="len%i="%k,
                              description="Horizontal extent of plane in traces"))
        p.parameter_add(Param(ptype="integer", keyword="ct%i="%k,
                              description="Time sample for center pivot"))
        p.parameter_add(Param(ptype="integer", keyword="cx%i="%k,
                              description="Trace for center pivot"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def surange():
    title = "SU Range"
    description = "Get min and max values for non-zero header entries"
    executable = "surange"
    authors = biloti
    tags=['su','seismic unix', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[chris_liner, su],
             executable=executable)

    par = Param(ptype="enum", keyword="key=",
                description="Header field to range (leave unset to see all)")
    par.options(su_hdr_fields)
    p.parameter_add(par)

    par = Param(ptype="enum", keyword="dim=",
                description="Dimension",
                default="0")
    par.options([
        {"description": "Do nothing", "value": "0"},
        {"description": "Coordinates in feet", "value": "1"},
        {"description": "Coordinates in meters", "value": "2"}
    ])
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sushw():
    title = "SU Set HW"
    description = "Set one or more header words"
    executable = "sushw"
    authors = biloti
    tags=['su','seismic unix', 'header', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description, url=suurl,
             authors=[einar_kjartansson, jack_cohen, john_stockwell, su],
             executable=executable)

    p.parameter_add(Param(ptype="strings", keyword="key=",
                          description="List of keys words",
                          separator=",",
                          default="tracl",
                          required=True))

    p.parameter_add(Param(ptype="file", keyword="infile=",
                          description="Binary file with values for fields specified above"))

    p.parameter_add(Param(ptype="integers", keyword="a=",
                          description="Values for first trace",
                          separator=",",
                          default="1"))

    p.parameter_add(Param(ptype="integers", keyword="b=",
                          description="Increments with group",
                          separator=",",
                          default="1"))

    p.parameter_add(Param(ptype="integers", keyword="c=",
                          description="Group increments",
                          separator=",",
                          default="0"))

    p.parameter_add(Param(ptype="integers", keyword="d=",
                          description="Trace number shits",
                          separator=",",
                          default="0"))

    p.parameter_add(Param(ptype="integers", keyword="j=",
                          description="Number of elements in groups",
                          separator=","))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def susort():
    title = "SU Sort"
    description = "Sort on any segy header keywords"
    executable = "susort"
    authors = biloti
    tags=['su','seismic unix', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[einar_kjartansson, stew_levin,
                      shuki_ronen, jack_cohen, su],
             executable=executable)

    for k in range(4):
        par = Param(ptype="enum", keyword="+",
                    description="Sort in ascending order by this key")
        par.options(su_hdr_fields)
        p.parameter_add(par)

        par = Param(ptype="enum", keyword="-",
                    description="Sort in descending order by this key")
        par.options(su_hdr_fields)
        p.parameter_add(par)

    p.parameter(0).default("cdp")
    p.parameter(2).default("offset")

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suspecfk():
    title = "SU Spec FK"
    description = "F-K Fourier Spectrum of data set"
    executable = "suspecfk"
    authors = biloti
    tags=['su','seismic unix', 'filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[dave_hale, jack_cohen, su],
             executable=executable)


    p.parameter_add(Param(ptype="float", keyword="dt=",
                          description="Time sampling interval (sec)"))

    p.parameter_add(Param(ptype="float", keyword="dx=",
                          description="Spatial sampling interval"))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Echos information",
                          default=False))

    p.parameter_add(par_p_tmpdir)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suspecfx():
    title = "SU Spec FX"
    description = "Spectrum (T->F) of traces"
    executable = "suspecfx"
    authors = biloti
    tags=['su','seismic unix', 'filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[dave_hale, jack_cohen, su],
             executable=executable)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suspike():
    title = "SU Spike"
    description = "Make a small spike data set"
    executable = "suspike"
    authors = biloti
    tags=['su','seismic unix', 'simulation and model building']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[dave_hale, jack_cohen, su],
             executable=executable, stdin=False)

    p.parameter_add(Param(ptype="integer", keyword="nt=",
                          description="Number of time samples",
                          default=64))

    p.parameter_add(Param(ptype="integer", keyword="ntr=",
                          description="Number of traces",
                          default=32))

    p.parameter_add(par_f_dt_004)

    p.parameter_add(Param(ptype="integer", keyword="offset=",
                          description="Offset",
                          default=400))

    par = Param(ptype="range", keyword="nspk=",
                          description="Number of spikes",
                          default=4)
    par.range([1,4], vinc=1,vdigits=0)
    p.parameter_add(par)

    for k in range(1,5):
        p.parameter_add(Param(ptype="integer", keyword="ix%i="%k,
                              description="Trace number for spike #%i"%k))

        p.parameter_add(Param(ptype="integer", keyword="it%i="%k,
                              description="Time sample for spike #%i"%k))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sustack():
    title = "SU Stack"
    description = "Stack adjacent traces having the same key header word"
    executable = "sustack"
    authors = biloti
    tags=['su','seismic unix', 'gain, nmo, stack and standard processes']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[einar_kjartansson, jack_cohen,
                      dave_hale, werner_heigl, su],
             executable=executable)

    par = Param(ptype="enum", keyword="key=",
                description="Key word to count",
                default="cdp")
    par.options(su_hdr_fields)
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="normpow=",
                          description="Each sample is divide by number of non-zero raised to this power",
                          default=1))

    p.parameter_add(Param(ptype="flag", keyword="repeat=1",
                          description="Repeat the stack traces",
                          default=False))

    p.parameter_add(Param(ptype="integer", keyword="nrepeat=",
                          description="How many repeations of the stack traces are produced",
                          default=10))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Echos information",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sustolt():
    title = "SU Stolt Mig"
    description = "Stolt migration for stacked data or common-offset gathers"
    executable = "sustolt"
    authors = biloti
    tags=['su','seismic unix', 'migration and dip moveout']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[dave_hale, su],
             executable=executable)

    comment= """If unstacked traces are input, they should be NMO-corrected and sorted
    into common-offset gathers. One common-offset gather ends and another
    begins when the offset field of the trace headers changes. If both
    NMO and DMO are applied, then this is equivalent to prestack time
    migration (though the velocity profile is assumed v(t), only). """

    p.parameter_add(Param(ptype="comment", description=comment))

    p.parameter_add(Param(ptype="integer", keyword="cdpmin=",
                          description="Minimum CDP in dataset",
                          required=True))

    p.parameter_add(Param(ptype="integer", keyword="cdpmax=",
                          description="Maximum CDP in dataset",
                          required=True))

    p.parameter_add(Param(ptype="float", keyword="dxcdp=",
                          description="Distance between adjacent cdp bins (m)",
                          required=True))

    p.parameter_add(Param(ptype="integer", keyword="noffmix=",
                          description="Number of offsets to mix (for unstacked data only)",
                          default=1))

    p.parameter_add(Param(ptype="floats", keyword="tmig=",
                          description="Array of times corresponding to rms velocities below",
                          separator=",",
                          default="0"))

    p.parameter_add(Param(ptype="floats", keyword="vmig=",
                          description="Array of rms velocities corresponding to times above (m/s)",
                          separator=",",
                          default="1500"))

    p.parameter_add(Param(ptype="float", keyword="smig=",
                          description="Stretch factor (0.6 typical if vrms increasing)",
                          default=1.0))

    p.parameter_add(Param(ptype="float", keyword="vscale=1",
                          description="Scale factor to apply to velocities",
                          default=1.0))

    p.parameter_add(Param(ptype="float", keyword="fmax=",
                          description="Maximum frequency in input data (Hz)"))

    p.parameter_add(Param(ptype="integer", keyword="lstaper=",
                          description="Length of side tapers (# of traces)",
                          default=0))

    p.parameter_add(Param(ptype="integer", keyword="lbtaper=",
                          description="Length of bottom tapers (# of traces)",
                          default=0))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Diagnostic print",
                          default=False))

    p.parameter_add(par_p_tmpdir)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sustrip():
    title = "SU Strip"
    description = "Remove the SEGY headers from the traces"
    executable = "sustrip"
    authors = biloti
    tags=['su','seismic unix', 'header', 'import/export']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[einar_kjartansson, jack_cohen, su],
             executable=executable)

    p.parameter_add(Param(ptype="file", keyword="head=",
                          description="File to save headers in"))

    p.parameter_add(Param(ptype="file", keyword="outpar=",
                          description="Output parameter file",
                          default="/dev/null",
                          value=[{"literal":"/dev/null"}]))

    par = Param(ptype="enum", keyword="ftn=",
                description="Binary format", default='0')
    par.options([
        {'description': 'Unformatted data written from C', 'value': '0'},
        {'description': 'Unformatted data written from Fortran', 'value': '1'}])
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def susynlv():
    title = "SU Syn LV"
    description = "Synthetic seismograms for Linear Velocity function"
    executable = "susynlv"
    authors = biloti
    tags=['su','seismic unix', 'simulation and model building']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[dave_hale, chris_liner, su],
             executable=executable,
             stdin=False, stdout=True, stderr=True)

    p.parameter_add(Param(ptype="integer", keyword="nt=",
                          description="Number time samples",
                          default=101))

    p.parameter_add(par_f_dt_04)

    p.parameter_add(Param(ptype="float", keyword="ft=",
                          description="First time (sec)",
                          default=0))

    par = Param(ptype="enum", keyword="kilounits=",
                description="Input length unit",
                default="1", required=True)
    par.values('1')
    par.options([
        {"description": "km or kilo-feet", "value": "1"},
        {"description": "m or ft", "value": "0"}
        ])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="fpeak=",
                          description="Peak frequency of symmetric Ricker wavelet (Hz)"))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Print some useful information",
                          default=False))

    p.parameter_add(Param(ptype="section", title="Offsets"))
    p.parameter_add(Param(ptype="integer", keyword="nxo=",
                          description="Number of source-receiver offsets",
                          default=1))

    p.parameter_add(Param(ptype="float", keyword="dxo=",
                          description="Offset sampling interval (kilounits)",
                          default=0.05))

    p.parameter_add(Param(ptype="float", keyword="fxo=",
                          description="First offset (kilounits)",
                          default=0))

    p.parameter_add(Param(ptype="floats", keyword="xo=",
                          description="Array of offsets (only for non-uniform offsets)",
                          separator=","))

    p.parameter_add(Param(ptype="section", title="Midpoints"))
    p.parameter_add(Param(ptype="integer", keyword="nxm=",
                          description="Number of midpoints",
                          default=101))

    p.parameter_add(Param(ptype="float", keyword="dxm=",
                          description="Midpoint sampling interval (kilounits)",
                          default=0.05))

    p.parameter_add(Param(ptype="float", keyword="fxm=",
                          description="First midpoint (kilounits)",
                          default=0))

    p.parameter_add(Param(ptype="section", title="Shotpoints"))
    par = Param(ptype="integer", keyword="nxs=",
                description="Number of shotpoints",
                default=101)
    par.values([{'expression': ''}])
    p.parameter_add(par)

    par=Param(ptype="float", keyword="dxs=",
              description="Shotpoint sampling interval (kilounits)",
              default=0.05)
    par.values([{'expression': ''}])
    p.parameter_add(par)

    par=Param(ptype="float", keyword="fxs=",
              description="First shotpoint (kilounits)",
              default=0)
    par.values([{'expression': ''}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="section", title="Velocity model"))

    p.parameter_add(Param(ptype="float", keyword="x0=",
                          description="Horizontal distance at which background velocity is specified",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="z0=",
                          description="Depth at which background velocity is specified",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="v00=",
                          description="Background velocity (kilounits/sec)",
                          default=2.0))

    p.parameter_add(Param(ptype="float", keyword="dvdx=",
                          description="Derivative of velocity with horizontal distance (dv/dx)",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="dvdz=",
                          description="Derivative of velocity with depth (dv/dz)",
                          default=0))

    p.parameter_add(Param(ptype="section", title="Reflectors"))

    p.parameter_add(Param(ptype="string", keyword="ref=",
                          description="Amplitude and refletor knots",
                          placeholder="amp:x1,z1;x2,z2;x3,z3;...",
                          multiple=True, required=True,
                          default="1:0,0.5;5,0.5"))

    p.parameter_add(Param(ptype="flag", keyword="smooth=1",
                          description="Smooth reflectors (picewise cubic splines)",
                          default=False))

    p.parameter_add(Param(ptype="section", title="Experiment"))

    p.parameter_add(Param(ptype="flag", keyword="er=1",
                          description="Exploding reflector amplitudes",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="ls=1",
                          description="Line source (2D), instead of point source (3D)",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="ob=0",
                          description="Do not consider obliquity factors",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="tmin=",
                          description="Minimum time of interest (sec)"))

    p.parameter_add(Param(ptype="integer", keyword="ndpfz=",
                          description="Number of diffractors per Fesnel zone",
                          default=5))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def susynlvcw():
    title = "SU Syn LV CW"
    description = "Synthetic seismograms for Linear Velocity function for mode converted waves"
    executable = "susynlvcw"
    authors = biloti
    tags=['su','seismic unix', 'simulation and model building']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[Person(name="Mohammed Alfaraj"),su],
             executable=executable,
             stdin=False, stdout=True, stderr=True)

    p.parameter_add(Param(ptype="integer", keyword="nt=",
                          description="Number time samples",
                          default=101))

    p.parameter_add(par_f_dt_04)

    p.parameter_add(Param(ptype="float", keyword="ft=",
                          description="First time (sec)",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="fpeak=",
                          description="Peak frequency of symmetric Ricker wavelet (Hz)"))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Print some useful information",
                          default=False))

    p.parameter_add(Param(ptype="section", title="Offsets"))
    p.parameter_add(Param(ptype="integer", keyword="nxo=",
                          description="Number of source-receiver offsets",
                          default=1))

    p.parameter_add(Param(ptype="float", keyword="dxo=",
                          description="Offset sampling interval (km)",
                          default=0.05))

    p.parameter_add(Param(ptype="float", keyword="fxo=",
                          description="First offset (km)",
                          default=0))

    p.parameter_add(Param(ptype="floats", keyword="xo=",
                          description="Array of offsets (only for non-uniform offsets)",
                          separator=","))

    p.parameter_add(Param(ptype="section", title="Midpoints"))
    p.parameter_add(Param(ptype="integer", keyword="nxm=",
                          description="Number of midpoints",
                          default=101))

    p.parameter_add(Param(ptype="float", keyword="dxm=",
                          description="Midpoint sampling interval (km)",
                          default=0.05))

    p.parameter_add(Param(ptype="float", keyword="fxm=",
                          description="First midpoint (km)",
                          default=0))

    p.parameter_add(Param(ptype="section", title="Shotpoints"))
    par = Param(ptype="integer", keyword="nxs=",
                description="Number of shotpoints",
                default=101)
    par.values([{'expression': ''}])
    p.parameter_add(par)

    par=Param(ptype="float", keyword="dxs=",
              description="Shotpoint sampling interval (km)",
              default=0.05)
    par.values([{'expression': ''}])
    p.parameter_add(par)

    par=Param(ptype="float", keyword="fxs=",
              description="First shotpoint (km)",
              default=0)
    par.values([{'expression': ''}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="section", title="Velocity model"))

    p.parameter_add(Param(ptype="float", keyword="x0=",
                          description="Horizontal distance at which background velocity is specified",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="z0=",
                          description="Depth at which background velocity is specified",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="v00=",
                          description="Background velocity (kilounits/sec)",
                          default=2.0))

    p.parameter_add(Param(ptype="float", keyword="gamma=",
                          description="Velocity ratio (upgoing/downgoing)",
                          default=1.0))

    p.parameter_add(Param(ptype="float", keyword="dvdx=",
                          description="Derivative of velocity with horizontal distance (dv/dx)",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="dvdz=",
                          description="Derivative of velocity with depth (dv/dz)",
                          default=0))

    p.parameter_add(Param(ptype="section", title="Reflectors"))

    p.parameter_add(Param(ptype="string", keyword="ref=",
                          description="Amplitude and refletor knots",
                          placeholder="amp:x1,z1;x2,z2;x3,z3;...",
                          multiple=True, required=True,
                          default="1:0,0.5;5,0.5"))

    p.parameter_add(Param(ptype="flag", keyword="smooth=1",
                          description="Smooth reflectors (picewise cubic splines)",
                          default=False))

    p.parameter_add(Param(ptype="section", title="Experiment"))

    p.parameter_add(Param(ptype="flag", keyword="er=1",
                          description="Exploding reflector amplitudes",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="ls=1",
                          description="Line source (2D), instead of point source (3D)",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="ob=0",
                          description="Do not consider obliquity factors",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="sp=0",
                          description="Constant amplitude throught out",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="tmin=",
                          description="Minimum time of interest (sec)"))

    p.parameter_add(Param(ptype="integer", keyword="ndpfz=",
                          description="Number of diffractors per Fesnel zone",
                          default=5))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suwaveform():
    title = "SU Waveform"
    description = "Generate a seismic wavelet"
    executable = "suwaveform"
    authors = biloti
    tags=['su','seismic unix', 'simulation and model building']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[nils_maercklin, su],
             executable=executable, stdin=False)

    par = Param(ptype="enum", keyword="type=",
                description="Wavelet type", default='akb')
    par.options([
        {'description': 'AKB wavelet defined by max frequency fpeak',
         'value': 'akb'},
        {'description': 'Berlage wavelet', 'value': 'berlage'},
        {'description': 'Gaussian wavelet defined by frequency fpeak',
         'value': 'gauss'},
        {'description': 'Gaussian first derivative wavelet', 'value': 'gaussd'},
        {'description': '1st Ricker wavelet defined by frequency fpeak',
         'value': 'ricker1'},
        {'description': '2nd Ricker wavelet defined by half and period',
         'value': 'ricker2'},
        {'description': 'Spike wavelet, shifted in time', 'value': 'spike'},
        {'description': 'Unit wavelet', 'value': 'unit'}])
    p.parameter_add(par)

    p.parameter_add(par_f_dt_004)

    p.parameter_add(Param(ptype="integer", keyword="ns=",
                          description="Number of samples per trace"))

    p.parameter_add(Param(ptype="float", keyword="fpeak=",
                          description="Peak (Berlage/Ricker/Gaussian) or maximum frequency (AKB)",
                          default=20.0))

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Output wavelet length",
                          default=False))

    p.parameter_add(Param(ptype="section", title="2nd Ricker wavelet parameters"))

    p.parameter_add(Param(ptype="float", keyword="half=",
                          description="Half-length"))

    p.parameter_add(Param(ptype="float", keyword="period=",
                          description="Period"))

    p.parameter_add(Param(ptype="float", keyword="distort=",
                          description="Distortion factor"))

    p.parameter_add(Param(ptype="section", title="Berlage wavelet parameters"))

    p.parameter_add(Param(ptype="float", keyword="decay=",
                          description="Exponential decay factor in 1/second"))

    p.parameter_add(Param(ptype="float", keyword="tn=",
                          description="Time exponent",
                          default=2))

    p.parameter_add(Param(ptype="float", keyword="ipa=",
                          description="Initial phase angle in degrees",
                          default=-90))

    p.parameter_add(Param(ptype="section", title="Spike wavelet parameter"))

    p.parameter_add(Param(ptype="float", keyword="tspike=",
                          description="Time at spike in seconds",
                          default=0))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def suwind():
    title = "SU Window"
    description = "Window traces by key word"
    executable = "suwind"
    authors = biloti
    tags=['su','seismic unix', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url=suurl,
             authors=[einar_kjartansson, shuki_ronen, jack_cohen,
                 chris_liner, toralf_foerster, werner_heigl, su],
             executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="verbose=1",
                          description="Be more verbose",
                          default=False))

    par = Param(ptype="enum", keyword="key=",
                description="Key header word to window",
                default="tracl")
    par.options(su_hdr_fields)
    p.parameter_add(par)

    p.parameter_add(Param(ptype="integer", keyword="min=",
                          description="Minimum value of key word to pass"))

    p.parameter_add(Param(ptype="integer", keyword="max=",
                          description="Maximum value of key word to pass"))

    p.parameter_add(Param(ptype="flag", keyword="abs=1",
                          description="Take absolute value of key header word",
                          default=False))

    p.parameter_add(Param(ptype="integer", keyword="j=",
                          description="Pass every j-th trace if (key-s)%j == 0. (j value)",
                          default=1))

    p.parameter_add(Param(ptype="integer", keyword="s=",
                          description="Pass every j-th trace if (key-s)%j == 0. (s value)",
                          default=0))

    p.parameter_add(Param(ptype="integer", keyword="skip=",
                          description="Amount of initial traces to skip",
                          default=0))

    p.parameter_add(Param(ptype="integer", keyword="count=",
                          description="How many traces to pass"))

    p.parameter_add(Param(ptype="integers", keyword="reject=",
                          description="Skip traces with this key value",
                          separator=","))

    p.parameter_add(Param(ptype="integers", keyword="accept=",
                          description="Pass traces with this key value",
                          separator=","))

    par = Param(ptype="enum", keyword="order=",
                description="Trace order by key value",
                default="0")
    par.options([{'description': 'increasing', 'value': '1'},
                 {'description': 'leave unsorted', 'value': '0'},
                 {'description': 'decreasing', 'value': '-1'}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="section", title="Time windowing"))

    p.parameter_add(Param(ptype="float", keyword="dt=",
                          description="Sampling time interval (sec)"))

    p.parameter_add(Param(ptype="float", keyword="f1=",
                          description="First sample value"))

    p.parameter_add(Param(ptype="float", keyword="tmin=",
                          description="Minimum time to pass"))

    p.parameter_add(Param(ptype="float", keyword="tmax=",
                          description="Maximum time to pass"))

    p.parameter_add(Param(ptype="integer", keyword="itmin=",
                          description="Minimum time sample to pass"))

    p.parameter_add(Param(ptype="integer", keyword="itmax=",
                          description="Maximum time sample to pass"))

    p.parameter_add(Param(ptype="integer", keyword="nt=",
                          description="Number of time samples to pass"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
# Main
a2b()
b2a()
segyclean()
segyread()
suaddevent()
suaddhead()
suaddnoise()
sucdpbin()
suchw()
sucountkey()
sudiff()
sudipfilt()
sufilter()
suflip()
sufxdecon()
sugain()
sugethw()
sukeycount()
sunmo()
sunull()
supaste()
supef()
suplane()
surange()
sushw()
susort()
suspecfk()
suspecfx()
suspike()
sustack()
sustolt()
sustrip()
susynlv()
susynlvcw()
suwaveform()
suwind()
