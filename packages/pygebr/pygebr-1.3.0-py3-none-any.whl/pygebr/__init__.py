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
# along with PyGeBR. If not, see <https://www.gnu.org/licenses/>
#
# Copyright 2021-2022 Ricardo Biloti <biloti@unicamp.br>
#                     Eduardo Filpo <efilpo@gmail.com>
#

__version__ = "1.3.0"
__author__ = ["Ricardo Biloti, biloti@unicamp.br",
              "Eduardo Filpo, efilpo@gmail.com"]
__license__ = "GPL 3.0"

from .setup   import Setup
from .person  import Person
from .param   import Param
from .program import Prog
from .flow    import Flow
from .utils   import *
