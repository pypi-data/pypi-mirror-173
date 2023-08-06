# PyGêBR on Ubuntu 22.04

This tutorial will guide you through the install process of PyGêBR, as well as other packages and tools for seismic processing, on Ubuntu Linux 22.04.

## Ubuntu

Follow Ubuntu instructions to install it as usual. After that, be sure to have your system updated. On a terminal, run:

    sudo apt update  
    sudo apt -y upgrade
 
Now, install some packages to fullfil dependencies for other softwares we'll install below.
 
    sudo apt install -y freeglut3-dev g++ gcc gfortran git gnuplot libavcodec-dev \
    libblas-dev libc6-dev libcairo2-dev libfftw3-dev libgd-dev libglib2.0-dev libjpeg-dev \
    liblapack-dev libmotif-dev libopenmpi-dev libplplot-dev libsuitesparse-dev \
    libtiff5-dev libxaw7-dev libxi-dev python3-dev python3-numpy python3-pip \
    python3-venv scons stow swig

## Madagascar

_[Madagascar](https://github.com/ahay) is an open-source package for seismic processing, developed with contributions of many researchers._
 
Madagascar uses Python and looks for its binary in `/usr/bin/python`. In Ubuntu 22.04, Python 3 is installed by default, but its binary is `/usr/bin/python3`. To fix that, run

    apt install -y python-is-python3

Download the latest development version of Madagascar and compile it. Be patient, this will take a while.

    mkdir Madagascar && cd Madagascar
    git clone https://github.com/ahay/src.git
    cd src
    export RSFROOT=/usr/local/stow/madagascar
    ./configure --prefix=$RSFROOT API=c++,fortran-90
    make -j
    sudo make -j install

To make Madagascar available to use, run the script below.

    . $RSFROOT/share/madagascar/etc/env.sh

To make that automatic, add that line to your .bashrc with:

    echo '. $RSFROOT/share/madagascar/etc/env.sh' >> ~/.bashrc

## Seismic Un*x
_[Seismic Un*x](https://github.com/JohnWStockwellJr/SeisUnix) (SU) is a open-source seismic processing package born at Colorado School of Mines, with contributions of many researchers._

Install SU with:

    sudo bash
    
    export CWPROOT=/usr/local/stow/su
    mkdir $CWPROOT
    cd $CWPROOT
    git clone https://github.com/JohnWStockwellJr/SeisUnix.git
    mv SeisUnix/* .
    rm -rf SeisUnix
    cd src
    
    # Adjusts to Makefile.config
    cp Makefile.config{,-original}
    cat << EOF > Makefile.config.patch
    16a17
    > CWPROOT=$CWPROOT
    49c50
    < XDRFLAG = -DSUXDR
    ---
    > #XDRFLAG = -DSUXDR
    95c96
    < OPTC = -g -std=c99  -m64 -Wall -ansi  -Wno-long-long 
    ---
    > OPTC = -g -O3 -m64 -Wall -Wno-long-long -fcommon
    101c102
    < FFLAGS = \$(FOPTS) -ffixed-line-length-none  -fallow-argument-mismatch
    ---
    > FFLAGS = \$(FOPTS) -ffixed-line-length-none  -Wno-argument-mismatch
    EOF
    patch -p2 Makefile.config Makefile.config.patch
    
    # Patch for CShot
    cd Fortran/Cshot
    cat > cshot2.f.patch <<EOF
    100c100
    <      :            MAXTPT =1001,
    ---
    >      :            MAXTPT =4001,
    EOF
    
    cat > graphics.f.patch <<EOF
    63c63
    <       PARAMETER ( NXPTS = 10)
    ---
    >       PARAMETER ( NXPTS = 20)
    EOF
    cp cshot2.f cshot2.f-original
    patch -p2 cshot2.f cshot2.f.patch
    cp graphics.f graphics.f-original
    patch -p2 graphics.f graphics.f.patch
    
    cd $CWPROOT/src
    	
    CWPROOT=$CWPROOT make install
    CWPROOT=$CWPROOT make xtinstall
    
    # Now to compile Fortran codes in SU run the command below. 
    # Note that sometimes this command may fail. That's because
    # some libraries or binarys are already compile and may not
    # match with your system. If that's the case, inspect the error
    # message, go to directory where the problem occurs and
    # delete the file so that it will be built again from scratch.
    # That's not nice, I known. Complain with SU developers or, 
    # even better, submit a patch.
    
    CWPROOT=$CWPROOT make finstall
        
    CWPROOT=$CWPROOT make mglinstall
    CWPROOT=$CWPROOT make utils
    CWPROOT=$CWPROOT make xminstall
    
    cd $CWPROOT/..
    stow -v su
    
    sed '/CWPROOT=/d' /etc/profile > /tmp/profile
    echo "export CWPROOT=$CWPROOT" >> /tmp/profile
    cp /tmp/profile /etc/profile
    
    echo "export CWPROOT=$CWPROOT" > /tmp/bash.bashrc
    sed '/CWPROOT=/d' /etc/bash.bashrc >> /tmp/bash.bashrc
    cp /tmp/bash.bashrc /etc/bash.bashrc
    
    exit


## Gplot
_[Gplot](https://gitlab.com/Biloti/gplot) is a tool to display data as image or wiggle and export images to PDF, SVG and PNG. It was written by Ricardo Biloti and employs Gnuplot as backend. It comes with a Python wrapper to be able to display nice images with jupyter notebooks._

Install gplot with:

    git clone https://gitlab.com/Biloti/gplot.git
    cd gplot
    make


## CSModeling

_[CSModeling](https://gitlab.com/Biloti/csmodeling) is a seismic modeling tool, written by Ricardo Biloti as a wrapper to CShot, from Seismic Un*x._

    git clone https://gitlab.com/Biloti/csmodeling.git
    cd csmodeling
    sudo make install
    cd /usr/local/stow
    sudo stow -v csmodeling

## DZT2RSF
_[Dzt2rsf](https://gitlab.com/Biloti/dzt2rsf) is a tool to convert GPR raw data from DZT format to RSF, used mainly by Madagascar codes. It was written by Ricardo Biloti and Eduardo Filpo._

To install dz2rsf, run:

    git clone https://gitlab.com/Biloti/dzt2rsf.git
    cd dzt2rsf
    make install


## PyGêBR

Finally, install (or update) PyGêBR with:

    pip3 install -U pygebr

We suggest you install jupyter to run PyGêBR interactively too.

    sudo apt install -y jupyter

That's it. PyGêBR and the most important seismic tools are installed (to use them it may be necessary to logout and login again). Enjoy!
