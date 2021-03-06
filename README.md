[![DOI](https://zenodo.org/badge/19384518.svg)](https://zenodo.org/badge/latestdoi/19384518)  

Inferno
=======
A command line tool for controlling MultiClampCommander and Clampex and saving data.

Installation
------------
If your computer can run MultiClampCommander then it can run Inferno.
You can get the most recent version of the Windows installer from the
[releases page](https://github.com/tgbugs/inferno/releases).
Please check the installation folder and read the README.txt provided there
(it is the same as [docs/README.md](docs/README.md) so you can read that
instead). Otherwise you can download the zip file or use git clone and
run Inferno from inferno.py.

Usage
-----
If you do not use the standalone installer, Inferno can be run from the command
line via inferno.py if you have installed python and the dependencies listed
below. The [README.md in docs](docs/README.md) also has information relevant
for using Inferno from source.

Supported Programs
------------------
* pClamp9, pClamp10 (Clampex)
* MultiClampCommander (so far only tested with MultiClamp 700B)

Dependencies
------------
The python version of Inferno has the following dependencies:
* x86 python 3.3.x (64bit WILL NOT WORK with the multiclamp dll!)
* docopt
* pywin32
* cx_Freeze (if you are building)

Building
--------
Inferno must be built against 32bit Python to communicate with AxMuliClampMsg.dll.
Thus to package Inferno into an msi installer using setup.py you will need an x86
python install and cx_Freeze. Once you have these, change `PATHON_PATH_X86` in build.py
to match your install location.

Extending Inferno
-----------------
Inferno currently only supports Clampex and MultiClampCommander. However there
are only three functions that need to be implemented to control a data acquisition
program: `LoadProtocol`, `Record`, and `GetFilename` (and possibly `IsOn`?).
