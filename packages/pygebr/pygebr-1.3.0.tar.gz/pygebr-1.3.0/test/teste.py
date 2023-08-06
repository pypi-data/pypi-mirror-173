#!/usr/bin/python3
import os,sys
from pygebr  import Setup, Flow

def SearchFlow(names):
    
    setup = Setup()
    paths = setup.menudirs()
    menus = []
    
    for name in names:

        # Append .json to name, if needed
        if name[-5:] == ".json":
            menufn = name
        else:
            menufn = name + '.json'

        for path in paths:
            fname = os.path.join(path,menufn)

            if os.path.isfile(fname):
                menus.append(fname)
                break

    return menus

def CmdToFlow(cmdtuple):
    """
    Return a flow from a tuple representing a command line.

    The tuple should have the structure:
    
    ( "<infile", ">outfile",
      ("menu1", "keyword", value1, "keyword2", value2, ...),
      ("menu2", "keyword", value1, "keyword2", value2, ...),
      ...
      ("menuM", "keyword", value1, "keyword2", value2, ...)
    )

    For each menu, a list os pairs with keyword and value follows.
    
    For example, the command-line 

    <in.rsf sfput o2=10 d2=0.02 unit2="meters" >out.rsf

    should be represented as
    
    ("<in.rsf", ">out.rsf",
     ("sfput", "o2", 10, "d2", 0.02, "unit2", "meters")
    )
    """

    def _add_flow(base, newfn):
        ff = Flow(filename = newfn)
        
        if not (base):
            base = ff
            base.title("New Flow")
            base.description("")
        else:
            base.merge(ff)

        return base

    stdin = ""
    stdout = ""
    stdoutmode = ""
    flow = None
    
    for line in cmdtuple:

        # Check for stdin and stdout or programs with no parameters
        if isinstance(line, str):
            if "<" in line:
                # stdin
                stdin = line.strip(" <")
                stdin = stdin.strip()
            elif ">>" in line:
                # stdout (append mode)
                stdout = line.strip(" >")
                stdout = stdout.strip()
                stdoutmode = "a"
            elif ">" in line:
                # stdout (overwrite mode)
                stdout = line.strip(" >")
                stdout = stdout.strip()
                stdoutmode = "w"
            else:
                # program with no parameters
                menufn = SearchFlow([line])
                if not (menufn):
                    raise Exception("No menu found for %s"%line)
                else:
                    flow = _add_flow(flow, menufn[0])

            continue

        # Check for program with parameters (tuple)
        if isinstance(line, tuple):
            menu = line[0]
            menufn = SearchFlow([menu])

            if not (menufn):
                raise Exception("No menu found for %s"%line[0])
            else:
                flow = _add_flow(flow, menufn[0])

                # Tacitly assumes the menu has only one program
                prog = flow.program(flow.programs_count()-1)

            npar = len(line) - 1
            if npar % 2 == 1:
                raise Exception("List of parameters/values for menu %s has odd number of terms"%line[0])
            
            # Loop over parameters
            k = 1
            while k < npar:

                if not isinstance(line[k],str):
                    raise Exception("Parameter %s in menu %s should be an string"%(str(line[k]),line[0]))
                else:
                    idx = prog.parameter_lookup(line[k])
                    if idx is not None:
                        par = prog.parameter(idx)
                        if not par.multiple():
                            par.values(line[k+1])
                        else:
                            value = par.values()
                            value.append({"literal": line[k+1]})
                            par.values(value)
                        k = k +2
                    else:
                        raise Exception("Parameter %s not found for menu %s"%(line[k],line[0]))
                        


    if stdin:
        flow.stdin(stdin)
    if stdout:
        flow.stdout([stdout, stdoutmode])

    flow.title("New flow")
    flow.description("")
    flow.authors(Setup().authors())
    flow.tags([])
    return flow
        

cmd = (("csmodeling","basedir","/tmp", "subdir","2dline","xfactor","0",
        "knots","0.0,0.0; 5.0,0.0",
        "knots","0.0,0.5; 1.5,0.55; 3.6,0.8; 5,0.8",
        "knots","0,1.2; 0.3, 1.28; 0.93, 0.75; 1.6, 1.3; 2.7,1.4;5, 1.3",
        "knots","0, 1.6; 2, 1.75; 3.3, 1.7; 4, 1.8;5,1.6",
        "knots","0.0,2.0; 5.0,2.0",
        "velocity","1.5, 2.1, 2.3, 3, 3.2",
        "primary",True,
        "takeoff",80.0,
        "inc",1.0,
        "xstation",0.0,
        "istation",0,"dstation",0.05,"rdepth",-1.0,
        "shot","4,5,6,42,2.0,0",
        "dxshot",4,"nshots",15,
        "f0",10.0,"f1",25.0,
        "f2",35.0,"f3",50.0,
        "wlen",0.15,
        "dt",4000,"tmax",2.5,
        "palette","5",
        "title","CS Modeling",
        "rays",True,
        "decimate",10,
        "nogrid", True),
       ("cat"," ","/tmp/2dline/out-0001.bin"),
       ("supaste","ns",626,"head","/tmp/2dline/out.hdr","ftn","1"),
       ">/tmp/2dline/out.su")

try:
    flow = ImportFlow(cmd)
except Exception as err:
    print(str(err))

print("\n-----")
flow.dump(setonly=True)

(isvalid, error) = flow.validate(True)
if not isvalid:
    print("Flow isn't valid")
    for er in error:
        print(er)
else:
    print("Flow is ok")
