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
# You should have received a copy of the GNU General Public License
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

filpo = Person(name="Eduardo Filpo",
               email="efilpo@gmail.com",
               institution="Petrobras",
               homepage="https://www.researchgate.net/profile/Eduardo-Filpo-2")

matheus = Person(name="Matheus Farias Barbosa",
		 email="m230888@dac.unicamp.br",
		 institution="University of Campinas")

renato = Person(name="Renato Nakai Biloti",
                email="renato.biloti@protonmail.com")

rsfurl="https://www.reproducibility.org/"

rsf = Person(name="Madagascar",
             institution="University of Texas at Austin",
             homepage=rsfurl)

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
def add_common_plot_params(p):

    p.parameter_add(Param(ptype="section", title="Common plot parameters"))

    p.parameter_add(Param(ptype="string", keyword="title=",
                          description="Plot title"))

    p.parameter_add(Param(ptype="flag", keyword="transp=y",
                          description="Transpose graph",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="xreverse=y",
                          description="Reverse the horizontal axes",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="yreverse=y",
                          description="Reverse y axis",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="scalebar=y",
                          description="Draw scale bar",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="screenratio=",
                          description="Screen ratio"))

    p.parameter_add(Param(ptype="float", keyword="obarnum=",
                          description="Scale bar origin"))

    p.parameter_add(Param(ptype="float", keyword="tickscale=",
                          description="Default ticks scaling",
                          default=0.5))

    for k in range(1,5):
        p.parameter_add(Param(ptype="section", title="Axis %i"%k))

        p.parameter_add(Param(ptype="string",keyword="label%i="%k,
                              description="Axis label"))

        p.parameter_add(Param(ptype="string",keyword="unit%i="%k,
                              description="Axis unit"))

        p.parameter_add(Param(ptype="float", keyword="o%inum="%k,
                              description="Tic origin"))

        p.parameter_add(Param(ptype="integer", keyword="n%itic="%k,
                              description="Number of ticmarks"))

        p.parameter_add(Param(ptype="float", keyword="d%inum="%k,
                              description="Tic incremet"))

        p.parameter_add(Param(ptype="string",keyword="format%i="%k,
                              description="Ticmark format"))

        p.parameter_add(Param(ptype="float", keyword="tickscale%i="%k,
                              description="Ticks scalings"))

#---------------------------------------------------------------------
def sfacurv():
    title = "SF ACurv"
    description = "Azimuth curvature"
    executable = "sfacurv"
    authors = renato
    tags=['rsf','madagascar']

    p = Prog(title=title, description=description,
             url=rsfurl, authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="string", keyword="interp=",
                          description="Interpolation method: maxflat lagrange bspline"))

    p.parameter_add(Param(ptype="integer", keyword="nazmuth=",
                          description="Azimuth number",
                          default=10))

    p.parameter_add(Param(ptype="integer", keyword="order=",
	                  description="Approximating order of finite difference",
                          default=2))

    p.parameter_add(Param(ptype="integer", keyword="rect1=",
                          description="Smoothness on 1st axis",
                          default=1))

    p.parameter_add(Param(ptype="integer", keyword="rect2=",
                          description="Smoothness on 2nd axis",
                          default=1))

    p.parameter_add(Param(ptype="integer", keyword="rect3=",
                          description="Smoothness on 3rd axis",
                          default=1))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfafac():
    title="SF Afac"
    description = "Wilson-Burg factorization"
    executable = "sfafac"
    authors = matheus
    tags = ['rsf','madagascar']

    p = Prog(title=title, description=description,
	     authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="file",
			  keyword="lag=",
			  description="Auxiliary output file name"))

    p.parameter_add(Param(ptype="integer",
			  keyword="nf=",
			  description="Factor coefficients",
			  default=32))

    p.parameter_add(Param(ptype="integer",
			  keyword="niter=",
			  description="Wilson iterations",
			  default=20))

    p.parameter_add(Param(ptype="integer",
			  keyword="nn=",
			  description="Helix diameter",
			  default=1000))

    p.parameter_add(Param(ptype="integer",
			  keyword="ompchunk=",
			  description="OMP chunk size",
			  default=1))

    p.parameter_add(Param(ptype="flag",
			  keyword="stable=y",
			  description="Stability flag",
			  default=False))

    p.parameter_add(Param(ptype="flag",
			  keyword="verb=y",
			  description="Verbosity flag",
			  default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfagc():
    title = "SF AGC"
    description = "Automatic gain control"
    executable = "sfagc"
    authors = biloti
    tags=['rsf','madagascar','gain, nmo, stack and standard processes']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2011/10/01/program-of-the-month-sfagc/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="rect1=",
                          description="Smoothing radius on 1st axis",
                          default=125))
    for k in range(2,5):
        p.parameter_add(Param(ptype="integer", keyword="rect%i="%k,
                              description="Smoothing radius on %i%s axis"%(k,orderstr[k-1]),
                              default=1))

    p.parameter_add(Param(ptype="integer", keyword="repeat=",
                          description="How many times to repeat filtering",
                          default=1))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfagmig():
    title="SF AG Mig"
    description = "Angle-gather constant-velocity time migration"
    executable = "sfagmig"
    authors = matheus
    tags = ['rsf','madagascar','migration and dip moveout']
    p = Prog(title=title, description=description,
	     authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float",
			  keyword="vel=",
			  description="Velocity",
			  required=True))

    p.parameter_add(Param(ptype="float",
			  keyword="a=",
			  description="Maximum dip angle",
			  default=80.0))

    p.parameter_add(Param(ptype="float",
			  keyword="dg=",
			  description="Reflection angle sampling"))

    p.parameter_add(Param(ptype="float",
			  keyword="g0=",
			  description="Reflection angle origin"))

    p.parameter_add(Param(ptype="integer",
			  keyword="na=",
			  description="Number of dip angles"))

    p.parameter_add(Param(ptype="integer",
			  keyword="ng=",
			  description="Number of reflection angles"))


    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfai2refl():
    title = "SF AI to Refl"
    description = "Convert acoustic impedance to reflectivity"
    executable = "sfai2refl"
    authors = biloti
    tags=['rsf','madagascar','utilities']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2013/08/02/program-of-the-month-sfai2refl/",
             authors=rsf, executable=executable)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfattr():
    title = "SF Attributes"
    description = "Display dataset attributes"
    executable = "sfattr"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/wiki/Guide_to_madagascar_programs#sfattr",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="lval=",
                          description="Non-negative norm index for vector norm",
                          default=2))

    par = Param(ptype="enum", keyword="want=",
                description="Which attribute to show",
                default='all')

    par.json['options'] = [{'description': 'all attributes', 'value': 'all'},
                           {'description': 'maximum', 'value': 'max'},
                           {'description': 'minimum', 'value': 'min'},
                           {'description': 'mean', 'value': 'mean'},
                           {'description': 'root mean square', 'value': 'rms'},
                           {'description': 'l-norm', 'value': 'norm'},
                           {'description': 'variance', 'value': 'var'},
                           {'description': 'standard deviation', 'value': 'std'},
                           {'description': 'number of nonzero samples', 'value': 'nonzero'},
                           {'description': 'total number of samples', 'value': 'samples'},
                           {'description': 'short one-line', 'value': 'short'}]

    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfbandpass():
    title = "SF Bandpass"
    description = "Bandpass filtering"
    executable = "sfbandpass"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url="https://reproducibility.org/blog/2012/11/03/program-of-the-month-sfbandpass/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float", keyword="flo=",
                          description="Low frequency in band",
                          default=0))
    p.parameter_add(Param(ptype="float", keyword="fhi=",
                          description="High frequency in band (leave blank for Nyquist)"))
    p.parameter_add(Param(ptype="integer", keyword="nplo=",
                          description="Number of poles for low cutoff",
                          default=6))
    p.parameter_add(Param(ptype="integer", keyword="nphi=",
                          description="Number of poles for high cutoff",
                          default=6))
    p.parameter_add(Param(ptype="flag", keyword="phase=y",
                          description="Minimum phase",
                          default=False))
    p.parameter_add(Param(ptype="flag", keyword="verb=y",
                          description="Verbose output",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfbin():
    title = "SF Data Binning"
    description = "Data binning in 2-D slices"
    executable = "sfbin"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2014/12/01/program-of-the-month-sfbin/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float", keyword="clip=",
                          description="Clip value for fold normalization"))

    p.parameter_add(Param(ptype="file", keyword="fold=",
                          description="Ouput file for fold"))

    p.parameter_add(Param(ptype="file", keyword="head=",
                          description="Header file"))

    par = Param(ptype="enum", keyword="interp=",
                description="Interpolation method",
                default="1", required=True)

    par.options([
        {"description": "Median", "value": "0"},
        {"description": "Nearest neighbor", "value": "1"},
        {"description": "Bi-linear", "value": "2"}
        ])

    p.parameter_add(par)


    p.parameter_add(Param(ptype="flag", keyword="norm=n",
                          description="Do not normalize",
                          default=False))

    p.parameter_add(Param(ptype="section", title="X direction"))

    p.parameter_add(Param(ptype="integer", keyword="nx=",
                          description="Number of bins in x"))

    p.parameter_add(Param(ptype="float", keyword="dx=",
                          description="Bin size in x"))

    p.parameter_add(Param(ptype="float", keyword="x0=",
                          description="X origin"))

    p.parameter_add(Param(ptype="integer", keyword="xkey=",
                          description="X key number",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="xmax=",
                          description="X maximum"))

    p.parameter_add(Param(ptype="float", keyword="xmin=",
                          description="X minimum"))

    p.parameter_add(Param(ptype="section", title="Y direction"))

    p.parameter_add(Param(ptype="integer", keyword="ny=",
                          description="Number of bins in y"))

    p.parameter_add(Param(ptype="float", keyword="dy=",
                          description="Bin size in y"))

    p.parameter_add(Param(ptype="float", keyword="y0=",
                          description="Y origin"))

    p.parameter_add(Param(ptype="integer", keyword="ykey=",
                          description="Y key number",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="ymax=",
                          description="Y maximum"))

    p.parameter_add(Param(ptype="float", keyword="ymin=",
                          description="Y minimum"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfbox():
    title = "SF Box"
    description = "Draw a balloon-style label"
    executable = "sfbox"
    authors = matheus
    tags=['rsf','madagascar','graphics']

    p = Prog(title=title, description=description,
    		url="https://reproducibility.org/blog/2015/05/01/program-of-the-month-sfbox/",
    		authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="string", keyword="label=",
                          description="Text for label"))

    p.parameter_add(Param(ptype="flag", keyword="boxit=n",
                          description="No box around text",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="xt=",
                          description="xt: relative position of text in x",
                          default=2.0))

    p.parameter_add(Param(ptype="float", keyword="yt=",
                      description="yt: relative position of text in y",
                      default=0.0))

    p.parameter_add(Param(ptype="float", keyword="length=",
                      description="Normalization for xt and yt"))

    p.parameter_add(Param(ptype="float", keyword="scalet=",
                      description="Scalet scale factor for xt and yt (if length is not set)"))

    p.parameter_add(Param(ptype="float", keyword="lat=",
                          description="Latitude of viewpoint in 3-D",
                          default=0.0))

    p.parameter_add(Param(ptype="float", keyword="long=",
                      description="Longitude of viewpoint in 3-D",
                      default=90.0))

    p.parameter_add(Param(ptype="float", keyword="angle=",
                      description="Longitude of floating label in 3-D",
                      default=0.0))

    p.parameter_add(Param(ptype="float", keyword="x0=",
                      description="x0: x position of the pointer tip",
                      default=0.0))

    p.parameter_add(Param(ptype="float", keyword="y0=",
                      description="y0: y position of the pointer tip",
                      default=0.0))

    p.parameter_add(Param(ptype="float", keyword="scale0=",
                      description="Scale factor for x0 and y0",
                      default=1.0))

    p.parameter_add(Param(ptype="float", keyword="x_oval=",
                      description="X size of the oval around pointer",
                      default=0.0))

    p.parameter_add(Param(ptype="float", keyword="y_oval=",
                      description="Y size of oval around pointer",
                      default=0.0))

    p.parameter_add(Param(ptype="float", keyword="pscale=",
                      description="Scale factor for width of pointer",
                      default=1.0))

    p.parameter_add(Param(ptype="float", keyword="size=",
                      description="Text height in inches",
                      default=0.25))

    p.parameter_add(Param(ptype="flag", keyword="pointer=n",
                      description="Suppress arrow pointer",
                      default=False))

    p.parameter_add(Param(ptype="flag", keyword="reverse=y",
                      description="Reverse",
                      default=True))

    p.parameter_add(Param(ptype="integer", keyword="font=",
                      description="Text font"))

    p.parameter_add(Param(ptype="integer", keyword="lab_color=",
                      description="Label color"))

    p.parameter_add(Param(ptype="integer", keyword="lab_fat=",
                      description="Label fatness",
                      default=0))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfcausint():
    title = "SF Causal Integration"
    description = "Causal integration on the first axis"
    executable = "sfcausint"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2013/12/01/program-of-the-month-sfcausint/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="adj=y",
                          description="Adjoint integration",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfclip():
    title = "SF Clip"
    description = "Clip the data"
    executable = "sfclip"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2011/09/03/program-of-the-month-sfclip/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float", keyword="clip=",
                          description="Clip value"))

    p.parameter_add(Param(ptype="float", keyword="value=",
                          description="Replacement value"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfclip2():
    title = "SF Clip 2"
    description = "One- or two-sided data clipping"
    executable = "sfclip2"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=rsfurl, authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float", keyword="lower=",
                          description="Lower clip value"))

    p.parameter_add(Param(ptype="float", keyword="upper=",
                          description="Upper clip value"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfcontour():
    title = "SF Contour"
    description = "Contour plot"
    executable = "sfcontour"
    authors = biloti
    tags=['rsf','madagascar','graphics']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2011/12/03/programs-of-the-month-sfcontour/",
             authors=rsf, executable=executable)


    p.parameter_add(Param(ptype="flag", keyword="allpos=n",
                          description="Contour negative values also",
                          default=False))

    p.parameter_add(Param(ptype="string", keyword="barlabel=",
                          description="Scale bar label"))

    p.parameter_add(Param(ptype="integer", keyword="nc=",
                          description="Number of contours",
                          default=50))

    p.parameter_add(Param(ptype="float", keyword="c0=",
                          description="First contour"))

    p.parameter_add(Param(ptype="float", keyword="dc=",
                          description="Contour increment"))

    p.parameter_add(Param(ptype="floats", keyword="c=",
                          description="Contour values",
                          separator=","))

    p.parameter_add(Param(ptype="file", keyword="cfile=",
                          description="File with contours"))

    p.parameter_add(Param(ptype="section", title="Axes"))

    p.parameter_add(Param(ptype="float", keyword="min1=",
                          description="Minimum on 1st axis"))

    p.parameter_add(Param(ptype="float", keyword="max1=",
                          description="Maximum on 1st axis"))

    p.parameter_add(Param(ptype="float", keyword="min2=",
                          description="Minimum on 2st axis"))

    p.parameter_add(Param(ptype="float", keyword="max2=",
                          description="Maximum on 2nd axis"))

    p.parameter_add(Param(ptype="flag", keyword="transp=y",
                          description="Transpose the axes",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfconv():
    title = "SF Conv"
    description = "1-D convolution"
    executable = "sfconv"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url=rsfurl, authors=rsf, executable=executable)

    par = Param(ptype="file", keyword="filt=",
                description="Filter file",
                placeholder="RSF file")
    par.filePattern("*.rsf")
    par.fileType("RSF")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="integer", keyword="lag=",
                          description="Lag for internal convolution",
                          default=1))

    p.parameter_add(Param(ptype="flag", keyword="trans=y",
                          description="Transient convolution (instead of internal)",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="each=y",
                          description="New filter for each trace",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="adj=y",
                          description="Adjoint",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfcorral():
    title = "SF  Corr All"
    description = "Cross-correlate every trace with every other in frequency domain"
    executable = "sfcorral"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url=rsfurl, authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="nlag=",
                          description="Number of lags",
                          default=100))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfcosft():
    title = "SF Cossine transform"
    description = "Multi-dimensional cossine transform"
    executable = "sfcosft"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url=rsfurl, authors=rsf, executable=executable)

    for k in range(1,4):
        par = Param(ptype="enum", keyword="sign%i="%k,
                    description="Transform along %i"%k + orderstr[k-1] + " dimension", default="0")
        p.parameter_add(par)
        par.json['options'] = [{'description': "Forward", 'value': "1"},
                               {'description': "Do nothing", 'value': '0'},
                               {'description': "Backward", 'value': "-1"}]

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfcostaper():
    title = "SF Cossine taper"
    description = "Cosine taper around the borders (N-D)"
    executable = "sfcostaper"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2014/04/02/program-of-the-month-sfcostaper/",
             authors=rsf, executable=executable)

    for k in range(1,5):
        p.parameter_add(Param(ptype="integer", keyword="nw%i="%k,
                              description="Tapering on %i"%k + orderstr[k-1] + " axis",
                              default=0))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfcpef():
    title = "SF PEF Complex"
    description = "1-D prediction-error filter estimation from complex data"
    executable = "sfcpef"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=rsfurl, authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="nf=",
                          description="Filter length"))

    p.parameter_add(Param(ptype="flag", keyword="single=n",
                          description="Multichannel",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfcut():
    title = "SF Cut"
    description = "Zero a portion of the dataset"
    executable = "sfcut"
    authors = biloti
    tags=['rsf','madagascar', 'editing, sorting and manipulation']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sfcut",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="verb=y",
                          description="Verbose output",
                          default=False))

    for k in range(1,5):
        p.parameter_add(Param(ptype="section", title="Axis %i"%k))
        p.parameter_add(Param(ptype="float", keyword="d%i="%k,
                              description="Sampling in %i"%k + orderstr[k-1] + " dimension"))
        p.parameter_add(Param(ptype="integer", keyword="f%i="%k,
                              description="Window start in %i"%k + orderstr[k-1] + " dimension",
                              default=0))
        p.parameter_add(Param(ptype="integer", keyword="j%i="%k,
                              description="Jump in %i"%k + orderstr[k-1] + " dimension",
                              default=1))
        p.parameter_add(Param(ptype="float", keyword="min%i="%k,
                              description="Minimum in %i"%k + orderstr[k-1] + " dimension"))
        p.parameter_add(Param(ptype="float", keyword="max%i="%k,
                              description="Maximum in %i"%k + orderstr[k-1] + " dimension"))
        p.parameter_add(Param(ptype="integer", keyword="n%i="%k,
                              description="Window size in %i"%k + orderstr[k-1] + " dimension"))


    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfderiv():
    title = "SF Deriv"
    description = "First derivative with a maximally linear FIR differentiator"
    executable = "sfderiv"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="http://reproducibility.org/blog/2012/05/01/program-of-the-month-sfderiv/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="order=",
                          description="Filter order",
                          default=6))

    p.parameter_add(Param(ptype="flag", keyword="scale=y",
                          description="Scale by 1/dx",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfdip():
    title = "SF Dip"
    description = "3-D dip estimation by plane wave destruction"
    executable = "sfdip"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="http://reproducibility.org/blog/2012/06/02/program-of-the-month-sfdip/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="both=y",
                          description="Compute both left and right predictions",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="drift=y",
                          description="Shift filter",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="eps=",
                          description="Regularization",
                          default=0))

    par = Param(ptype="file", keyword="mask=",
                description="Mask file",
                placeholder="RSF file")

    par.filePattern("*.rsf")
    par.fileType("RSF")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="integer", keyword="liter=",
                          description="Number of linear iterations",
                          default=20))

    par = Param(ptype="enum", keyword="n4=",
                description="Compute mode",
                default="2")
    par.options([{"description": "in-line", "value": "0"},
                 {"description": "cross-line", "value": "1"},
                 {"description": "both", "value": "2"}])

    p.parameter_add(par)

    p.parameter_add(Param(ptype="integer", keyword="niter=",
                          description="Number of iterations",
                          default=5))

    p.parameter_add(Param(ptype="integer", keyword="order=",
                          description="Accuracy order",
                          default=1))

    for k in range(1,4):
        p.parameter_add(Param(ptype="integer", keyword="rect%i="%k,
                              description="Dip smoothness on %i%s axis"%(k,orderstr[k-1]),
                              default=1))

    p.parameter_add(Param(ptype="flag", keyword="verb=y",
                          description="Be more verbose",
                          default=False))

    p.parameter_add(Param(ptype="section", title="In-line"))

    p.parameter_add(Param(ptype="integer", keyword="nj1=",
                          description="In-line antialiasing",
                          default=1))

    p.parameter_add(Param(ptype="float", keyword="p0=",
                          description="Initial in-line dip",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="pmin=",
                          description="Minimum in-line dip"))

    p.parameter_add(Param(ptype="float", keyword="pmax=",
                          description="Maximum in-line dip"))

    par = Param(ptype="file", keyword="idip=",
                description="In-line dip file",
                placeholder="RSF file")

    par.filePattern("*.rsf")
    par.fileType("RSF")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="section", title="Cross-line"))

    p.parameter_add(Param(ptype="integer", keyword="nj2=",
                          description="Cross-line antialiasing",
                          default=1))

    p.parameter_add(Param(ptype="float", keyword="10=",
                          description="Initial cross-line dip",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="qmin=",
                          description="Minimum cross-line dip"))

    p.parameter_add(Param(ptype="float", keyword="qmax=",
                          description="Maximum cross-line dip"))

    par = Param(ptype="file", keyword="xdip=",
                description="Initial cross-line dip file",
                placeholder="RSF file")

    par.filePattern("*.rsf")
    par.fileType("RSF")
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfdipfilter_a():
    title = "SF Dip Filter (angle)"
    description = "Filter data by angle based on dip in 2-D or 3-D"
    executable = "sfdipfilter angle=y"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2014/02/06/program-of-the-month-sfdipfilter/",
             authors=rsf, executable=executable)

    par = Param(ptype="enum", keyword="dim=",
                description="Dimension",
                default="2", required=True)
    par.options([{"description": "2D", "value": "2"},
                 {"description": "3D", "value": "3"}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="ang1=",
                          description="First angle in gate (degree)",
                          default=-50))

    p.parameter_add(Param(ptype="float", keyword="ang2=",
                          description="Second angle in gate (degree)",
                          default=-45))

    p.parameter_add(Param(ptype="float", keyword="ang3=",
                          description="Third angle in gate (degree)",
                          default=45))

    p.parameter_add(Param(ptype="float", keyword="ang4=",
                          description="Fourth angle in gate (degree)",
                          default=50))

    par = Param(ptype="enum", keyword="pass=",
                description="Filter operation",
                default="y", required=True)
    par.options([{"description": "Accept angles inside gate", "value": "y"},
                 {"description": "Reject angles inside gate", "value": "n"}])
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p,
                fname="sfdipfiltera")

#---------------------------------------------------------------------
def sfdipfilter_v():
    title = "SF Dip Filter (vel)"
    description = "Filter data by velocity based on dip in 2-D or 3-D"
    executable = "sfdipfilter angle=n"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2014/02/06/program-of-the-month-sfdipfilter/",
             authors=rsf, executable=executable)

    par = Param(ptype="enum", keyword="dim=",
                description="Dimension",
                default="2", required=True)
    par.options([{"description": "2D", "value": "2"},
                 {"description": "3D", "value": "3"}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="v1=",
                          description="First velocity in gate (degree)",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="v2=",
                          description="Second velocity in gate (degree)",
                          default=0.1))

    p.parameter_add(Param(ptype="float", keyword="v3=",
                          description="Third velocity in gate (degree)",
                          default=99999))

    p.parameter_add(Param(ptype="float", keyword="v4=",
                          description="Fourth velocity in gate (degree)",
                          default=999999))

    par = Param(ptype="enum", keyword="pass=",
                description="Filter operation",
                default="y", required=True)
    par.options([{"description": "Accept velocities inside gate", "value": "y"},
                 {"description": "Reject velocities inside gate", "value": "n"}])
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p,
                fname="sfdipfilterv")

#---------------------------------------------------------------------
def sfeikonal():
    title = "SF Eikonal"
    description = "Fast marching eikonal solver (3-D)"
    executable = "sfeikonal"
    authors = biloti
    tags=['rsf','madagascar','simulation and model building']

    p = Prog(title=title, description=description,
             url="http://reproducibility.org/blog/2014/06/11/program-of-the-month-sfeikonal/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="b1=",
                          description="Constant-velocity box 1 around the source (in samples)"))

    p.parameter_add(Param(ptype="integer", keyword="b2=",
                          description="Constant-velocity box 2 around the source (in samples)"))

    p.parameter_add(Param(ptype="integer", keyword="b3=",
                          description="Constant-velocity box 3 around the source (in samples)"))

    p.parameter_add(Param(ptype="float", keyword="br1=",
                          description="Constant-velocity box 1 around the source (in physical dimensions)"))

    p.parameter_add(Param(ptype="float", keyword="br2=",
                          description="Constant-velocity box 2 around the source (in physical dimensions)"))

    p.parameter_add(Param(ptype="float", keyword="br3=",
                          description="Constant-velocity box 3 around the source (in physical dimensions)"))

    p.parameter_add(Param(ptype="integer", keyword="order=",
                          description="Accuracy order",
                          default=2))

    p.parameter_add(Param(ptype="flag", keyword="plane1=y",
                          description="Plane-wave source 1",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="plane2=y",
                          description="Plane-wave source 2",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="plane3=y",
                          description="Plane-wave source 3",
                          default=False))

    p.parameter_add(Param(ptype="file", keyword="shotfile=",
                          description="File with shot locations (n2=number of shots, n1=3)"))

    p.parameter_add(Param(ptype="flag", keyword="sweep=y",
                          description="Use fast sweeping instead of fast marching",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="vel=n",
                          description="Input field is slowness squared instead of velocity",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="xshot=",
                          description="X shot location"))

    p.parameter_add(Param(ptype="float", keyword="yshot=",
                          description="Y shot location"))

    p.parameter_add(Param(ptype="float", keyword="zshot=",
                          description="Z shot location",
                          default=0))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfenvelope():
    title = "SF Envelope"
    description = "Compute data envelope or phase rotation"
    executable = "sfenvelope"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2011/11/05/program-of-the-month-sfenvelope/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="hilb=y",
                          description="Compute Hilbert transform",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="phase=",
                          description="Phase shift (in degrees) to use with Hilbert transform",
                          default=90))

    p.parameter_add(Param(ptype="integer", keyword="order=",
                          description="Hilbert transform order",
                          default=100))

    par = Param(ptype="range", keyword="ref=",
                description="Hilbert transformer reference",
                default=1)
    par.range([0.5,1],vinc=0.05,vdigits=2)
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sffft1():
    title = "SF FFT1"
    description = "Fast Fourier Transform along the first axis"
    executable = "sffft1"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=rsfurl, authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="inv=y",
                          description="Inverse transform",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="sym=y",
                          description="Symmetric scaling for Hermitian FFT",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="opt=n",
                          description="Don't try to determine optimal size for efficiency",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="memsize=",
                          description="Memory size",
                          default=1000))

    p.parameter_add(Param(ptype="flag", keyword="verb=y",
                          description="Be more verbose",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sffft3():
    title = "SF FFT3"
    description = "FFT transform on extra axis"
    executable = "sffft3"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=rsfurl, authors=rsf, executable=executable)

    par = Param(ptype="range", keyword="axis=",
                description="Axis to transform",
                default=2)

    par.range([1,5],vinc=1,vdigits=0)
    p.parameter_add(par)

    p.parameter_add(Param(ptype="integer", keyword="pad=",
                          description="Padding factor",
                          default=2))

    p.parameter_add(Param(ptype="flag", keyword="inv=y",
                          description="Inverse transform",
                          default=False))

    par = Param(ptype="enum", keyword="sign=",
                description="Transform direction")

    par.options([{"description": "forward", "value": "0"},
                 {"description": "backward", "value": "1"}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="flag", keyword="sym=y",
                          description="Symmetric scaling for Hermitian FFT",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="opt=n",
                          description="Don't try to determine optimal size for efficiency",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sffxdecon():
    title = "SF F-X Decon"
    description = "Random noise attenuation using f-x deconvolution"
    executable = "sffxdecon"
    authors = filpo
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url=rsfurl, authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float",
                          keyword="fmin=",
                          description="Minimun frequency to process in Hz",
                          default=1))

    p.parameter_add(Param(ptype="float",
                          keyword="fmax=",
                          description="Maximum frequency to process in Hz"))

    p.parameter_add(Param(ptype="float",
                          keyword="taper=",
                          description="Lenght of taper",
                          default=.1))

    p.parameter_add(Param(ptype="float",
                          keyword="twlen=",
                          description="Time window length"))

    p.parameter_add(Param(ptype="integer",
                          keyword="lenf=",
                          description="Number of traces for filter",
                          default=4))

    p.parameter_add(Param(ptype="integer",
                          keyword="n2w=",
                          description="Number of traces in window",
                          default=10))

    p.parameter_add(Param(ptype="flag",
                          keyword="verb=y",
                          description="Verbose output",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfgraph():
    title = "SF Graph"
    description = "Graph plot"
    executable = "sfgraph"
    authors = biloti
    tags=['rsf','madagascar','graphics']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2011/08/09/program-of-the-month-sfgraph/",
             authors=rsf, executable=executable)


    p.parameter_add(Param(ptype="file", keyword="bar=",
                          description="File for scalebar data"))

    p.parameter_add(Param(ptype="flag", keyword="barreverse=y",
                          description="Reverse bar scale",
                          default=False))

    p.parameter_add(Param(ptype="string", keyword="color=",
                          description="Color scheme",
                          default="j"))

    p.parameter_add(Param(ptype="file", keyword="depth=",
                          description="Auxiliary input filename"))

    p.parameter_add(Param(ptype="float", keyword="maxval=",
                          description="Maximum value for scalebar (default is the data maximum)"))

    p.parameter_add(Param(ptype="float", keyword="minval=",
                          description="Minimum value for scalebar (default is the data minimum)"))

    p.parameter_add(Param(ptype="integer", keyword="nreserve=",
                          description="Reserved colors",
                          default=8))

    par = Param(ptype="range", keyword="pclip=",
                description="Clip percitile",
                default=100)
    par.range([0,100],vinc=1,vdigits=2)
    p.parameter_add(par)

    p.parameter_add(Param(ptype="flag", keyword="scalebar=y",
                          description="Draw scale",
                          default=False))

    p.parameter_add(Param(ptype="string", keyword="symbol=",
                          description="Plot with this symbols instead of lines"))

    p.parameter_add(Param(ptype="float", keyword="symbolsz=",
                          description="Symbol size",
                          default=2))

    add_common_plot_params(p)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfgrey():
    title = "SF Grey"
    description = "Generate raster plot"
    executable = "sfgrey"
    authors = biloti
    tags=['rsf','madagascar','graphics']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2015/03/04/program-of-the-month-sfgrey/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="allpos=y",
                          description="Assume positive data",
                          default=False))

    par = Param(ptype="range", keyword="pclip=",
                description="Data clip percentile",
                default=99)
    par.range(limits=[0,100], vinc=0.5, vdigits=2)
    p.parameter_add(par)

    add_common_plot_params(p)
    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfhalfint():
    title = "SF Half Int"
    description = "Half-order integration or differentiation"
    executable = "sfhalfint"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2012/12/23/program-of-the-month-sfhalfint/",
             authors=rsf, executable=executable)

    par = Param(ptype="enum", keyword="inv=",
                description="Mode",
                default="n",
                required=True)

    par.options([{"description": "differentiation", "value": "y"},
                 {"description": "integration", "value": "n"}])

    p.parameter_add(par)

    p.parameter_add(Param(ptype="flag", keyword="adj=y",
                          description="Apply adjoint",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="rho=",
                          description="Leak integration constant"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfhelicon():
    title = "SF Helicon"
    description = "Multidimensional convolution and deconvolution by helix transform"
    executable = "sfhelicon"
    authors = renato
    tags=['rsf','madagascar']

    p = Prog(title=title,description=description,
             url="https://reproducibility.org/blog/2014/05/13/program-of-the-month-sfhelicon/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="adj=y",
                          description="Do adjoint operation",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="div=y",
                          description="Do inverse operation (deconvolution)",
                          default=False))

    p.parameter_add(Param(ptype="file", keyword="filt=",
                          description="Filter file"))

    p.parameter_add(Param(ptype="file", keyword="lag=",
                          description="File with filter lags",))

    p.parameter_add(Param(ptype="integers", keyword="n=",
                          description="Dimensions",
                          separator=","))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfin():
    title = "SF In"
    description = "Display basic information about RSF files"
    executable = "sfin"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sfin",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float", keyword="check=",
                          description="Portion of the data (in Mb) to check for zero values",
                          default=2))

    p.parameter_add(Param(ptype="flag", keyword="info=n",
                          description="Show data file name only",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="trail=n",
                          description="Skip trailing dimensions of one",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfintbin():

    title = "SF IntBin"
    description = "Data binning by trace sorting"
    executable = "sfintbin"
    authors = matheus
    tags=['rsf','madagascar']

    p = Prog(title=title, description=description,
    		url="http://reproducibility.org/blog/2015/06/10/program-of-the-month-sfintbin/",
    		authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="inv=y",
                      description="Inversion flag",
                      default=True))

    p.parameter_add(Param(ptype="file", keyword="head=",
                      description="Header file"))

    p.parameter_add(Param(ptype="file", keyword="map=",
    			  description="Output map file"))

    p.parameter_add(Param(ptype="file", keyword="mask=",
                      description="Output mask file"))

    p.parameter_add(Param(ptype="string", keyword="xk=",
                      description="X key name",
                      default="fldr"))

    p.parameter_add(Param(ptype="string", keyword="yk=",
                      description="Y key name",
                      default="tracf"))

    p.parameter_add(Param(ptype="integer", keyword="xkey=",
                      description="X key number"))

    p.parameter_add(Param(ptype="integer", keyword="ykey=",
                      description="Y key number"))

    p.parameter_add(Param(ptype="integer", keyword="xmin=",
                      description="X minimum"))

    p.parameter_add(Param(ptype="integer", keyword="ymin=",
                      description="Y minimum"))

    p.parameter_add(Param(ptype="integer", keyword="xmax=",
                      description="X maximum"))

    p.parameter_add(Param(ptype="integer", keyword="ymax=",
                      description="Y maximum"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfkirmod():
    title = "SF Kirchhoff Mod"
    description = "Kirchhoff 2-D/2.5-D modeling with analytical Green's functions"
    executable = "sfkirmod"
    authors = biloti
    tags=['rsf','madagascar','simulation and model building']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2012/10/03/program-of-the-month-sfkirmod/",
             authors=rsf, executable=executable)

    par = Param(ptype="enum", keyword="twod=",
                description="Dimension",
                default="n")
    par.options([{"description": "2-D", "value": "y"},
                 {"description": "2.5-D", "value": "n"}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="freq=",
                          description="Peak frequency for Ricker wavelet"))

    p.parameter_add(Param(ptype="float", keyword="t0=",
                          description="Time origin",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="dt=",
                          description="Time sampling (sec)",
                          default=0.004))

    p.parameter_add(Param(ptype="integer", keyword="nt=0",
                          description="Number of time samples"))

    par = Param(ptype="file", keyword="curv=",
                description="Curvature auxiliary file",
                placeholder="RSF file")
    par.filePattern("*.rsf")
    par.fileType("RSF")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="file", keyword="dip=",
                          description="Reflector dip file"))

    par = Param(ptype="file", keyword="picks=",
                description="Auxiliary output file",
                placeholder="RSF file")
    par.filePattern("*.rsf")
    par.fileType("RSF")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="r0=",
                          description="Normal reflectivity (if constant)",
                          default=1))

    par = Param(ptype="file", keyword="refl=",
                description="Auxiliary input file (reflectivity)",
                placeholder="RSF file")
    par.filePattern("*.rsf")
    par.fileType("RSF")
    p.parameter_add(par)

    par = Param(ptype="file", keyword="rgrad=",
                description="AVO gradient file",
                placeholder="RSF file")
    par.filePattern("*.rsf")
    par.fileType("RSF")
    p.parameter_add(par)

    par = Param(ptype="file", keyword="slopes=",
                description="Auxiliary output file (slopes)",
                placeholder="RSF file")
    par.filePattern("*.rsf")
    par.fileType("RSF")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="flag", keyword="adj=y",
                          description="Adjoint",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="lin=y",
                          description="Linear operator",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="verb=y",
                          description="Verbose mode",
                          default=False))

    p.parameter_add(Param(ptype="section", title="Acquisition geometry"))

    p.parameter_add(Param(ptype="flag", keyword="absoff=y",
                          description="First-offset value is not in shot coordinate system",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="h0=",
                          description="First offset",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="dh=",
                          description="Offset increment"))

    p.parameter_add(Param(ptype="integer", keyword="nh=",
                          description="Number of offsets"))

    p.parameter_add(Param(ptype="flag", keyword="cmp=y",
                          description="Compute CMP instead of shot gathers",
                          default=False))

    p.parameter_add(Param(ptype="float", keyword="s0=",
                          description="First shot (when computing CMP's)"))

    p.parameter_add(Param(ptype="float", keyword="ds=",
                          description="Shot or midpoint increment"))

    p.parameter_add(Param(ptype="integer", keyword="ns=",
                          description="Number of shots (when computing CMP's)"))

    p.parameter_add(Param(ptype="section", title="Velocity"))

    p.parameter_add(Param(ptype="float", keyword="refx=",
                          description="Reference x-coordinate for velocity"))

    p.parameter_add(Param(ptype="float", keyword="refz=",
                          description="Reference z-coordinate for velocity"))

    par = Param(ptype="enum", keyword="type=",
                description="Type of velocity",
                default="c")
    par.options([{"description": "constant", "value": "c"},
                 {"description": "linear sloth", "value": "s"},
                 {"description": "linear velocity", "value": "v"},
                 {"description": "VTI anisotropy", "value": "a"}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="vel=",
                          description="Velocity"))

    p.parameter_add(Param(ptype="float", keyword="gradx=",
                          description="Horizontal velocity gradient"))

    p.parameter_add(Param(ptype="float", keyword="gradz=",
                          description="Vertical velocity gradient"))

    par = Param(ptype="enum", keyword="type2=",
                description="Type of velocity for the converted (receiver side) branch",
                default="c")
    par.options([{"description": "constant", "value": "c"},
                 {"description": "linear sloth", "value": "s"},
                 {"description": "linear velocity", "value": "v"},
                 {"description": "VTI anisotropy", "value": "a"}])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="vel2=",
                          description="Converted velocity"))

    p.parameter_add(Param(ptype="float", keyword="gradx2=",
                          description="Converted velocity, horizontal gradient"))

    p.parameter_add(Param(ptype="float", keyword="gradz2=",
                          description="Converted velocity, vertical gradient"))

    p.parameter_add(Param(ptype="float", keyword="velz=",
                          description="Vertical velocity for VTI anisotropy"))

    p.parameter_add(Param(ptype="float", keyword="eta=",
                          description="Eta parameter for VTI anisotropy"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sflinear():
    title = "SF Linear"
    description = "1-D linear interpolation of irregularly spaced data"
    executable = "sflinear"
    authors = matheus
    tags = ['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2016/03/23/program-of-the-month-sflinear/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float", keyword="o1=",
                          description="Output origin"))

    p.parameter_add(Param(ptype="float", keyword="d1=",
                          description="Output sampling"))

    p.parameter_add(Param(ptype="integer", keyword="n1=",
                          description="Output grid size"))

    p.parameter_add(Param(ptype="comment",
                          description="For non-regular output grid, leave parameters "+
                          "above in blank and provide the file below."))

    p.parameter_add(Param(ptype="file", keyword="pattern=",
                          description="File with ouput grid pattern"))

    p.parameter_add(Param(ptype="integer", keyword="niter=",
                          description="Number of iterations",
                          default=0))

    p.parameter_add(Param(ptype="integer", keyword="nw=",
                          description="Interpolator size",
                          default=2))

    p.parameter_add(Param(ptype="flag", keyword="sort=y",
                          description="Coordinates need sorting",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sflpf():
    title = "SF LPF"
    description = "Local prediction filter (n-dimensional)"
    executable = "sflpf"
    authors = matheus
    tags=['rsf','madagascar', 'filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2019/07/09/program-of-the-month-sflpf/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="niter=",
			  description="Number of iterations",
			  default=100))

    p.parameter_add(Param(ptype="file", keyword="match=",
			  description="Target data file",
			  required=True))

    p.parameter_add(Param(ptype="file", keyword="pred=",
			  description="Prediction filter",
			  required=True))

    p.parameter_add(Param(ptype="flag", keyword="verb=n",
			  description="Be less verbose",
			  default=False))

    p.parameter_add(Param(ptype="section", title="Prediction-error filter"))

    p.parameter_add(Param(ptype="file", keyword="pef=",
			  description="Signal PEF file"))

    p.parameter_add(Param(ptype="file", keyword="lag=",
			  description="File with PEF lags"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfmath():
    title = "SF Math"
    description = "Mathematical operations on data files"
    executable = "sfmath"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sfmath",
             authors=rsf, executable=executable)

    par = Param(ptype="comment",
                description="In the next parameter, usual functions can be employed, "
                "like sin, cos, exp, sqrt, and so on.<br>To represent the input " +
                "amplitude use 'input'. For example: 'sin(2*input)'")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="string", keyword="output=",
                          description="Mathematical description of the output"))

    p.parameter_add(Param(ptype="string", keyword="label=",
                          description="Data label"))

    p.parameter_add(Param(ptype="string", keyword="unit=",
                          description="Data unit"))

    p.parameter_add(Param(ptype="flag", keyword="nostdin=y",
                          description="Ignore standard input",
                          default=False))

    par = Param(ptype="enum", keyword="type=",
                description="Output data type",
                default="float")

    par.json['options'] = [{'description': 'real values', 'value': 'float'},
                           {'description': 'complex values', 'value': 'complex'}]

    p.parameter_add(par)

    for k in range(1,5):
        p.parameter_add(Param(ptype="section", title="Axis %i"%k))

        p.parameter_add(Param(ptype="float", keyword="d%i="%k,
                              description="Sampling rate"))
        p.parameter_add(Param(ptype="integer", keyword="n%i="%k,
                              description="Number of samples"))
        p.parameter_add(Param(ptype="float", keyword="o%i="%k,
                              description="Origin"))
        p.parameter_add(Param(ptype="string", keyword="label%i="%k,
                              description="Axis label"))
        p.parameter_add(Param(ptype="string", keyword="unit%i="%k,
                              description="Axis unit"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfmath2():
    title = "SF Math (w/o stdin)"
    description = "Mathematical operations"
    executable = "sfmath"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sfmath",
             authors=rsf, executable=executable,
             stdin=False, stdout=True, stderr=True)

    par = Param(ptype="comment",
                description="In the next parameter, usual functions can be employed, "
                "like sin, cos, exp, sqrt, and so on.<br>For example: 'sin(2*x1)+x2'")
    p.parameter_add(par)
    p.parameter_add(Param(ptype="string", keyword="output=",
                          description="Mathematical description of the output"))

    p.parameter_add(Param(ptype="string", keyword="label=",
                          description="Data label"))

    p.parameter_add(Param(ptype="string", keyword="unit=",
                          description="Data unit"))

    p.parameter_add(Param(ptype="flag", keyword="nostdin=y",
                          description="Ignore standard input",
                          default=False))

    par = Param(ptype="enum", keyword="type=",
                description="Output data type",
                default="float")

    par.json['options'] = [{'description': 'real values', 'value': 'float'},
                           {'description': 'complex values', 'value': 'complex'}]

    p.parameter_add(par)

    for k in range(1,5):
        p.parameter_add(Param(ptype="section", title="Axis %i"%k))

        p.parameter_add(Param(ptype="float", keyword="d%i="%k,
                              description="Sampling rate"))
        p.parameter_add(Param(ptype="integer", keyword="n%i="%k,
                              description="Number of samples"))
        p.parameter_add(Param(ptype="float", keyword="o%i="%k,
                              description="Origin"))
        p.parameter_add(Param(ptype="string", keyword="label%i="%k,
                              description="Axis label"))
        p.parameter_add(Param(ptype="string", keyword="unit%i="%k,
                              description="Axis unit"))

    commit_menu(title, description, authors, executable, tags, p, "sfmath2")

#---------------------------------------------------------------------
def sfmf():
    title = "SF Median Filter"
    description = "1D median filtering"
    executable = "sfmf"
    authors = biloti
    tags=['rsf','madagascar', 'filtering, transforms and attributes']

    p = Prog(title=title, description=description,
    		url="https://reproducibility.org/blog/2015/01/30/program-of-the-month-sfmf/",
    		authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="boundary=y",
                      description="Consider boundary as data",
                      default=False))

    p.parameter_add(Param(ptype="integer", keyword="nfw=",
                      description="Filter-window length (positive and odd integer)"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfmutter():

    title = "SF Mutter"
    description = "Muting"
    executable = "sfmutter"
    authors = matheus
    tags=['rsf','madagascar', 'editing, sorting and manipulation']

    p = Prog(title=title, description=description,
    		url="http://reproducibility.org/blog/2015/07/10/program-of-the-month-sfmutter/",
    		authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="abs=n",
                      description="Consider the signal of (x-x0)",
                      default=False))

    p.parameter_add(Param(ptype="flag", keyword="half=n",
                      description="Second axis is offset instead of half-offset",
                      default=False))

    p.parameter_add(Param(ptype="flag", keyword="hyper=y",
                      description="Do hyperbolic mute",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="inner=y",
                      description="Do inner muter",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="nan=y",
                      description="Put NAN's instead of zeros",
                          default=False))

    p.parameter_add(Param(ptype="file", keyword="offset=",
                      description="File with offset (when irregular)"))

    p.parameter_add(Param(ptype="float", keyword="slope0=",
                      description="Slope"))

    p.parameter_add(Param(ptype="float", keyword="slopep=",
                      description="End slope"))

    p.parameter_add(Param(ptype="float", keyword="t0=",
                      description="Starting time",
                      default=0.0))

    p.parameter_add(Param(ptype="float", keyword="tp=",
                      description="End time",
                      default=0.150))

    p.parameter_add(Param(ptype="float", keyword="v0=",
                      description="Velocity",
                      default=1.45))

    p.parameter_add(Param(ptype="float", keyword="x0=",
                      description="Starting space",
                      default=0.0))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfnoise():
    title = "SF Noise"
    description = "Add random noise to the data"
    executable = "sfnoise"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2011/07/03/program-of-the-month-sfnoise/",
             authors=rsf,
             executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="seed=",
                          description="Random seed"))

    p.parameter_add(Param(ptype="flag", keyword="rep=y",
                          description="Replace data with noise",
                          default=False))

    par = Param(ptype="enum", keyword="type=",
                description="Noise distribution",
                default="y")
    par.options([
        {"description": "normal", "value": "y"},
        {"description": "uniform", "value": "n"}
    ])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="mean=",
                          description="Noise mean",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="var=",
                          description="Noise variance"))


    p.parameter_add(Param(ptype="float", keyword="range=",
                          description="Noise range",
                          default=1))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfricker1():
    title = "SF Ricker (with deriv)"
    description = "Convolution with a Ricker wavelet"
    executable = "sfricker1"
    authors = matheus
    tags=['rsf','madagascar','simulation and model building']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2013/01/08/program-of-the-month-sfricker1/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="deriv=y",
	                  description="Apply a half-order derivative filter",
                          default=False))

    p.parameter_add(Param(ptype="comment",
                          description='Provide, at most, one of the next two parameters.'))

    p.parameter_add(Param(ptype="float", keyword="freq=",
                          description="Peak frequency for Ricker wavelet (as fraction of Nyquist)"))

    p.parameter_add(Param(ptype="float", keyword="frequency=",
                          description="Peak frequency for Ricker wavelet (in Hz)"))


    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfsnr2():
    title = "SF SNR2"
    description = "Compute signal-noise-ratio"
    executable = "sfsnr2"
    authors = matheus
    tags=['rsf','madagascar','utilities']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2019/08/10/program-of-the-month-sfsnr2/",
             authors=rsf, executable=executable)

    par = Param(ptype="file", keyword="noise=",
	        description="Noise vector file",
                required=True)
    par.fileType("RSF")
    par.filePattern("*.rsf")
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfpad():
    title = "SF Pad"
    description = "Pad a dataset with zeros"
    executable = "sfpad"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sfpad",
             authors=rsf, executable=executable)

    for k in range(1,4):
        p.parameter_add(Param(ptype="section", title="Axis %i"%k))
        p.parameter_add(Param(ptype="integer",keyword="beg%i="%k,
                              description="The number of zeros to add before the beginning of axis",
                              default=0))
        p.parameter_add(Param(ptype="integer",keyword="end%i="%k,
                              description="The number of zeros to add after the end of axis",
                              default=0))
        p.parameter_add(Param(ptype="integer",keyword="n%i="%k,
                              description="The output length of axis (padding at the end)"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfpen():
    title = "SF Xt pen"
    description = "Vplot filter for X windows using the X Toolkit (Xt)"
    executable = "sfpen"
    authors = biloti
    tags=['rsf','madagascar','graphics']

    p = Prog(title=title,description=description,
             url=rsfurl, authors=rsf, executable=executable,
             stdin=True, stdout=False, stderr=True)

    p.parameter_add(Param(ptype="float",keyword="aspect=",
                          description="Aspect ratio"))

    p.parameter_add(Param(ptype="flag",keyword="buttons=n",
                          description="Hide buttons on panel's top",
                          default=False))

    p.parameter_add(Param(ptype="flag",keyword="stretchy=y",
                          description="Stretch horizontal axis to the window's length",
                          default=False))

    par = Param(ptype="range", keyword="pclip=",
                description="Clip percitile",
                default=100)
    par.range([0,100],vinc=0.5,vdigits=2)
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfpostrtm2d():
    title = "SF Post RTM 2D"
    description = "2-D exploding-reflector RTM and its adjoint"
    executable = "sfpostrtm2d"
    authors = biloti
    tags=['rsf','madagascar',
          'simulation and model building',
          'migration and dip moveout']

    p = Prog(title=title,description=description,
             url=rsfurl, authors=rsf, executable=executable,
             stdin=True, stdout=False, stderr=True)

    par = Param(ptype="enum",keyword="adj=",
                description="Operation",
                default="y", required=True)
    par.options([{"description": "modeling", "value": "n"},
                 {"description": "migration", "value": "y"}])
    p.parameter_add(par)

    par = Param(ptype="file",keyword="vel=",
                description="Velocity file",
                required=True)
    par.fileType("RSF")
    par.filePattern("*.rsf")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="dt=",
                          description="Time sampling interval (sec)"))

    p.parameter_add(Param(ptype="integer", keyword="nt=",
                          description="Samples per trace"))

    p.parameter_add(Param(ptype="integer", keyword="padx=",
                          description="Padding in x"))

    p.parameter_add(Param(ptype="integer", keyword="padz=",
                          description="Padding in z"))

    p.parameter_add(Param(ptype="flag",keyword="snap=y",
                          description="Save wave field snapshots",
                          default=False))

    par = Param(ptype="file",keyword="wave=",
                description="Filename to save wave field snapshots")
    par.fileType("RSF")
    par.filePattern("*.rsf")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="integer", keyword="jt=",
                          description="Time steps between snapshots",
                          default=50))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfput():
    title = "SF Put"
    description = "Input parameters into a header"
    executable = "sfput"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sfput",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="file", keyword="in=",
                          description="Data file"))

    p.parameter_add(Param(ptype="string", keyword=" ",
                          description="General parameters as \"keyword=value\"",
                          multiple=True))

    for k in range(1,4):
        p.parameter_add(Param(ptype="section", title="Axis %i"%k))
        p.parameter_add(Param(ptype="float", keyword="o%i="%k,
                              description="First sample"))
        p.parameter_add(Param(ptype="float", keyword="d%i="%k,
                              description="Sampling rate"))
        p.parameter_add(Param(ptype="integer", keyword="n%i="%k,
                              description="Number of samples"))
        p.parameter_add(Param(ptype="string", keyword="label%i="%k,
                              description="Axis label"))
        p.parameter_add(Param(ptype="string", keyword="unit%i="%k,
                              description="Axis unit"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfscale():
    title="SF Scale"
    description="Scale data"
    executable = "sfscale"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sfscale",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="axis=",
                          description="Scale by maximum in the dimensions up to this axis",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="dscale=",
                          description="Scale factor", default=1))

    par = Param(ptype="range",
                keyword="pclip=",
                description="Data clip percitile",
                default=100)
    par.range([0,100],vinc=0.5,vdigits=2)
    p.parameter_add(par)

    p.parameter_add(Param(ptype="float", keyword="rscale=",
                          description="Scale factor", default=0))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfseislet():
    title = "SF Seislet"
    description = "2-D seislet transform"
    executable = "sfseislet"
    authors = matheus
    tags = ['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2017/04/19/program-of-the-month-sfseislet/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="file", keyword="dip=",
			  description="Estimated dip field file",
                          required=True))

    p.parameter_add(Param(ptype="float", keyword="eps=",
			  description="Regularization",
			  default=0.01))

    p.parameter_add(Param(ptype="integer", keyword="order=",
			  description="Accuracy order",
			  default=1))
    par = Param(ptype="enum", keyword="type=",
		description="Wavelet type",
		default='linear')

    par.json['options'] = [{'description': 'linear', 'value': 'linear'},
                           {'description': 'Haar', 'value': 'haar'},
                           {'description': 'biorthogonal', 'value': 'biorthogonal'}]

    p.parameter_add(par)

    p.parameter_add(Param(ptype="flag", keyword="adj=y",
			  description="Do adjoint transform",
			  default=False))

    p.parameter_add(Param(ptype="flag", keyword="inv=y",
			  description="Do inverse transform",
			  default=False))

    p.parameter_add(Param(ptype="flag", keyword="unit=y",
			  description="Use unitary scaling",
			  default=False))

    p.parameter_add(Param(ptype="flag", keyword="verb=y",
			  description="Be more verbose",
			  default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfsigmoid():
    title = "SF Sigmoid"
    description = "2-D synthetic model from J.F.Claerbout"
    executable = "sfsigmoid"
    authors = biloti
    tags = ['rsf','madagascar','simulation and model building']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2014/10/08/program-of-the-month-sfsigmoid/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="comment",
                          description="Leaving next parameter blank means that it will be set as 5 times the number of samples in time direction."))

    p.parameter_add(Param(ptype="integer", keyword="large=",
			  description="Length of the syntethic reflectivity series"))

    p.parameter_add(Param(ptype="flag", keyword="reflectivity=n",
			  description="Output impedance instead of reflectivity",
			  default=False))

    p.parameter_add(Param(ptype="flag", keyword="taper=n",
			  description="Do not taper the edges",
			  default=False))

    p.parameter_add(Param(ptype="section", title="Time axis"))

    p.parameter_add(Param(ptype="integer", keyword="n1=",
			  description="Number of samples in time",
			  default=400))

    p.parameter_add(Param(ptype="float", keyword="d1=",
			  description="Sampling rate (sec)",
                          default=0.004))

    p.parameter_add(Param(ptype="integer", keyword="o1=",
			  description="Origin",
			  default=0))

    p.parameter_add(Param(ptype="section", title="Horizontal axis"))

    p.parameter_add(Param(ptype="integer", keyword="n2=",
			  description="Number of traces",
			  default=100))

    p.parameter_add(Param(ptype="float", keyword="d2=",
			  description="Sampling rate (km)",
                          default=0.032))

    p.parameter_add(Param(ptype="integer", keyword="o2=",
			  description="Origin",
			  default=0))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfslice():
    title = "SF Slice"
    description = "Extract a slice using picked surface (usually from a stack or a semblance)"
    executable = "sfslice"
    authors = matheus
    tags=['rsf','madagascar','utilities']

    p = Prog(title=title, description=description,
             url="http://reproducibility.org/blog/2019/06/12/program-of-the-month-sfslice/",
             authors=rsf, executable=executable)

    par = Param(ptype="file", keyword="pick=",
		description="Picked surface file (as produced by SF Pick)",
                required=True)
    par.fileType("RSF")
    par.filePattern("*.rsf")
    p.parameter_add(par)

    commit_menu(title, description, authors, executable, tags, p)
#---------------------------------------------------------------------
def sfsmooth():
    title = "SF Smooth"
    description = "Multi-dimensional triangle smoothing"
    executable = "sfsmooth"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2012/01/01/program-of-the-month-sfsmooth/",
             authors=rsf, executable=executable)


    p.parameter_add(Param(ptype="flag", keyword="adj=y",
                          description="Run in the adjoint mode",
                          default=False))

    p.parameter_add(Param(ptype="integer", keyword="repeat=",
                          description="How many times apply the filter",
                          default=1))

    for k in range(1,5):
        p.parameter_add(Param(ptype="section", title="Axis %i"%k))

        p.parameter_add(Param(ptype="flag",keyword="diff%i=y"%k,
                              description="Differentiation on %i%s axis"%(k,orderstr[k-1]),
                              default=False))

        p.parameter_add(Param(ptype="integer",keyword="rect%i="%k,
                              description="Smoooth radius",
                              default=1))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfsmoothder():
    title = "SF Smooth Der"
    description = "Smooth first derivative on the first axis"
    executable = "sfsmoothder"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url=rsfurl, authors=rsf, executable=executable)


    p.parameter_add(Param(ptype="float", keyword="eps=",
                          description="Smoothness parameter",
                          default=0.2))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfsort():
    title = "SF Sort"
    description = "Sort a float/complex vector by absolute values"
    executable = "sfsort"
    authors = matheus
    tags = ['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2016/01/16/program-of-the-month-sfsort/",
             authors=[
                 Person(name="Gilles Hennenfent", institution="UBC"),
                 Person(name="Henryk Modzelewski", institution="UBC"),
                 rsf], executable=executable)

    par = Param(ptype="enum", keyword="ascmode=",
                description="Sort order",
                default="n")

    par.options([
        {"description": "ascending", "value": "y"},
        {"description": "descending", "value": "n"}
    ])
    p.parameter_add(par)

    p.parameter_add(Param(ptype="integer", keyword="dim=",
                          description="Maximum dimension"))

    p.parameter_add(Param(ptype="integer", keyword="memsize=",
                          description="Max amount of RAM (in Mb) to be used"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfsphase():
    title = "SF SPhase"
    description = "Smooth estimate of instantaneous phase"
    executable = "sfsphase"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url=rsfurl, authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="ninter=",
                          description="Number of iterations",
                          default=100))

    p.parameter_add(Param(ptype="integer", keyword="order=",
                          description="Hilbert transformer order",
                          default=10))

    par = Param(ptype="range", keyword="ref=",
                description="Hilbert transformer reference",
                default=1)
    par.range([0.5,1],vinc=.05,vdigits=2)
    p.parameter_add(par)

    for k in range(1,5):
        p.parameter_add(Param(ptype="integer", keyword="rect%i="%k,
                              description="Smoothing radius on %i"%k + orderstr[k-1] + " axis",
                              default=1))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfspectra():
    title = "SF Spectra"
    description = "Frequency spectra"
    executable = "sfspectra"
    authors = biloti
    tags=['rsf','madagascar','filtering, transforms and attributes']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2012/03/18/program-of-the-month-sfspectra/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="all=y",
                          description="Compute average spectrum for all traces",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="opt=n",
                          description="Don't bother to compute optimal size for efficiency",
                          default=False))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfspike():
    title = "SF Spike"
    description = "Generate simple data: spikes, boxes, planes, constants"
    executable = "sfspike"
    authors = biloti
    tags=['rsf','madagascar', 'simulation and model building']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sfspike",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="nsp=",
                          description="Number of spikes",
                          default=1, required=True))

    p.parameter_add(Param(ptype="floats", keyword="mag=",
                          description="Spike magnitudes",
                          default="1"))

    p.parameter_add(Param(ptype="string", keyword="title=",
                          description="Title for plots"))

    # Axis 1
    p.parameter_add(Param(ptype="section", title="Axis 1"))

    p.parameter_add(Param(ptype="float", keyword="d1=",
                          description="Sampling interval",
                          default=0.004))

    p.parameter_add(Param(ptype="float", keyword="o1=",
                          description="Axis origin",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="n1=",
                          description="Number of samples"))

    p.parameter_add(Param(ptype="integers", keyword="k1=",
                          description="Spikes' staring position",
                          separator=",",
                          default="0"))

    p.parameter_add(Param(ptype="integers", keyword="l1=",
                          description="Spikes' ending position",
                          separator=",",
                          default="0"))

    p.parameter_add(Param(ptype="float", keyword="p1=",
                          description="Spike inclination (in samples)",
                          default=0))

    p.parameter_add(Param(ptype="string", keyword="label1=",
                          description="Axis label",
                          default="Time"))

    p.parameter_add(Param(ptype="string", keyword="unit1=",
                          description="Axis unit",
                          default="s"))

    # Axis 2,3 and 4
    for k in range(2,5):
        p.parameter_add(Param(ptype="section", title="Axis %i"%k))

        p.parameter_add(Param(ptype="float", keyword="d%i="%k,
                              description="Sampling interval",
                              default=0.1))

        p.parameter_add(Param(ptype="float", keyword="o%i="%k,
                              description="Axis origin",
                              default=0))

        p.parameter_add(Param(ptype="float", keyword="n%i="%k,
                              description="Number of samples"))

        p.parameter_add(Param(ptype="integers", keyword="k%i="%k,
                              description="Spikes' staring position",
                              separator=",",
                              default="0"))

        p.parameter_add(Param(ptype="integers", keyword="l%i="%k,
                              description="Spikes' ending position",
                              separator=",",
                              default="0"))

        p.parameter_add(Param(ptype="float", keyword="p%i="%k,
                              description="Spike inclination (in samples)",
                              default=0))

        p.parameter_add(Param(ptype="string", keyword="label%i="%k,
                              description="Axis label",
                              default="Distance"))

        p.parameter_add(Param(ptype="string", keyword="unit%i="%k,
                              description="Axis unit",
                              default="km"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfstolt():
    title = "SF Stolt"
    description = "Post-stack Stolt modeling/migration"
    executable = "sfstolt"
    authors = biloti
    tags=['rsf','madagascar','migration and dip moveout']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2014/08/03/program-of-the-month-sfstolt/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="extend=",
                          description="Trace extension",
                          default=4))
    p.parameter_add(Param(ptype="float", keyword="minstr=",
                          description="Minimum stretch allowed",
                          default=0))
    p.parameter_add(Param(ptype="integer", keyword="mute=",
                          description="Mute zone",
                          default=12))
    p.parameter_add(Param(ptype="integer", keyword="pad=",
                          description="Padding on the time axis"))
    p.parameter_add(Param(ptype="float", keyword="stretch=",
                          description="Stolt stretch parameter",
                          default=1))
    p.parameter_add(Param(ptype="float", keyword="vel=",
                          description="Constant velocity (use negative for modeling)",
                          required=True))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfstolt2():
    title = "SF Stolt 2"
    description = "Post-stack Stolt modeling/migration"
    executable = "sfstolt2"
    authors = biloti
    tags=['rsf','madagascar','migration and dip moveout']

    p = Prog(title=title,description=description,
             url=rsfurl, authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float", keyword="vel=",
                          description="Constant velocity (use negative for modeling)",
                          required=True))

    p.parameter_add(Param(ptype="integer", keyword="nf=",
                          description="Interpolation accuracy",
                          default=2))
    p.parameter_add(Param(ptype="integer", keyword="pad=",
                          description="Padding on the time axis"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfpick():

    title = "SF Pick"
    description = "Automatic picking from semblance-like panels"
    executable = "sfpick"
    authors = biloti
    tags=['rsf','madagascar','utilities']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/blog/2012/08/01/program-of-the-month-sfpick/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float", keyword="vel0=",
                          description="Surface velocity"))

    p.parameter_add(Param(ptype="integer", keyword="gate=",
                          description="Picking gate",
                          default=3))

    p.parameter_add(Param(ptype="integer", keyword="niter=",
                          description="Number of iterations",
                          default=100))

    p.parameter_add(Param(ptype="float", keyword="an=",
                          description="Axes anisotropy",
                          default=1))

    p.parameter_add(Param(ptype="flag", keyword="back=y",
                          description="Run backward",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="norm=y",
                          description="Apply normalization",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="smooth=n",
                          description="Don't smooth",
                          default=False))
    for k in range(1,5):
        p.parameter_add(Param(ptype="integer", keyword="rect%i="%k,
                              description="Smoothing radius on %i"%k + orderstr[k-1] + " axis",
                              default=1))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sftransp():

    title = "SF Transpose"
    description = "Transpose two axes in a dataset"
    executable = "sftransp"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title,description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sftransp",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="integer", keyword="memsize=",
                          description="Maximum amount of RAM (in Mb) to be used"))

    p.parameter_add(Param(ptype="integer", keyword="plane=",
                          description="Two-digit number with axes to transpose",
                          default=12))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfunif2():
    title = "SF Unif 2D"
    description = "Generate 2-D layered velocity model from specified interfaces"
    executable = "sfunif2"
    authors = biloti
    tags=['rsf','madagascar','simulation and model building']

    p = Prog(title=title, description=description,
             url="https://reproducibility.org/blog/2013/10/03/program-of-the-month-sfunif2/",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="float", keyword="o1=",
                          description="Origin of the depth axis",
                          default=0))

    p.parameter_add(Param(ptype="float", keyword="d1=",
                          description="Sampling of the depth data"))

    p.parameter_add(Param(ptype="integer", keyword="n1=",
                          description="Number of samples on depth axis"))

    par = Param(ptype="comment",
                description="Next 5 parameters are arrays with equal number of elements")
    p.parameter_add(par)

    p.parameter_add(Param(ptype="floats", keyword="v00=",
                          description="Array of background velocities",
                          separator=","))

    p.parameter_add(Param(ptype="floats", keyword="dvdx=",
                          description="Array of horizontal velocity gradients",
                          separator=","))

    p.parameter_add(Param(ptype="floats", keyword="dvdz=",
                          description="Array of vertical velocity gradients",
                          separator=","))

    p.parameter_add(Param(ptype="floats", keyword="x0=",
                          description="Array of x-coords of reference points",
                          separator=","))

    p.parameter_add(Param(ptype="floats", keyword="z0=",
                          description="Array of z-coords of reference points",
                          separator=","))

    p.parameter_add(Param(ptype="string", keyword="label1=",
                          description="Depth axis label"))

    p.parameter_add(Param(ptype="string", keyword="unit1=",
                          description="Depth axis unit label"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
def sfwindow():
    title = "SF Window"
    description = "Window a portion of a dataset"
    executable = "sfwindow"
    authors = biloti
    tags=['rsf','madagascar','editing, sorting and manipulation']

    p = Prog(title=title, description=description,
             url="http://reproducibility.org/wiki/Guide_to_madagascar_programs#sfwindow",
             authors=rsf, executable=executable)

    p.parameter_add(Param(ptype="flag", keyword="squeeze=n",
                          description="Don't squeeze dimensions equal to 1 to the end",
                          default=False))

    p.parameter_add(Param(ptype="flag", keyword="verb=y",
                          description="Be more verbose",
                          default=False))
    for k in range(1,4):
        p.parameter_add(Param(ptype="section", title="Axis %i"%k))
        p.parameter_add(Param(ptype="float",keyword="d%i="%k,description="Sampling rate"))
        p.parameter_add(Param(ptype="integer",keyword="f%i="%k,description="Window start"))
        p.parameter_add(Param(ptype="integer",keyword="n%i="%k,description="Window size"))
        p.parameter_add(Param(ptype="integer",keyword="j%i="%k,description="Jump"))
        p.parameter_add(Param(ptype="float",keyword="min%i="%k,description="Minimum value"))
        p.parameter_add(Param(ptype="float",keyword="max%i="%k,description="Maximum value"))

    commit_menu(title, description, authors, executable, tags, p)

#---------------------------------------------------------------------
# Main
sfacurv()
sfafac()
sfagc()
sfagmig()
sfai2refl()
sfattr()
sfbandpass()
sfbin()
sfbox()
sfcausint()
sfclip()
sfclip2()
sfcontour()
sfconv()
sfcorral()
sfcosft()
sfcostaper()
sfcpef()
sfcut()
sfderiv()
sfdip()
sfdipfilter_a()
sfdipfilter_v()
sfeikonal()
sfenvelope()
sffft1()
sffft3()
sffxdecon()
sfgraph()
sfgrey()
sfhalfint()
sfhelicon()
sfin()
sfintbin()
sfkirmod()
sflinear()
sflpf()
sfmath()
sfmath2()
sfmf()
sfmutter()
sfnoise()
sfsnr2()
sfpad()
sfpen()
sfpostrtm2d()
sfput()
sfricker1()
sfscale()
sfseislet()
sfsigmoid()
sfslice()
sfsmooth()
sfsmoothder()
sfsort()
sfsphase()
sfspectra()
sfspike()
sfstolt()
sfstolt2()
sfpick()
sftransp()
sfunif2()
sfwindow()
