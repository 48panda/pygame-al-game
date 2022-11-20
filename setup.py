from cx_Freeze import setup, Executable
import sys
import shutil
from glob import glob

png = glob("assets/*.png") + glob("assets/*/*.png")
tc = glob("assets/*.tc") + glob("assets/*/*.tc")
csv = glob("assets/*.csv")

# exclude unneeded packages. More could be added. Has to be changed for
# other programs.
build_exe_options = {"includes": ["pygame", "PIL", "numpy"],
                    "excludes":["_distutils_hack", "_pytest", "asyncio", "atomicwrites", "attr", "backcall", "backports", "black", "blib2to3", "bs4", "cairo", "certifi", "cffi", "chardet", "charset_normalizer",
                    "click", "cloudpickle", "colorama", "concurrent", "cryptography", "ctypes", "curses", "dateutil", "defusedxml", "distutils", "docutils", "email",
                    "fonttools", "html", "http", "idna", "inportlib", "importlib_metadata", "ipykernel", "Ipython", "ipython_genutils", "jedi", "jinja2", "jsonschema", "jupyter_client", "jupyter_core",
                    "lib2to3","lib", "lxml", "markupsafe", "matplotlib", "more_itertools", "mpl_toolkits", "mpmath", "multiprocessing", "nbconvert", "nbformat", "notebook", "OpenGL", "OpenGL_accelerate",
                    "packaging", "pandas", "parso", "pathlib2", "pathspec", "pkg_resources", "platrformdirs", "pluggy", "prompt_toolkit", "py", "pycparser", "pydoc_data", "pyglet", "pygments", "PyQt5",
                    "pyreadline", "pyrsistent", "pytest", "pytz", "pyximport", "qtpy", "requests", "scipy", "setuptools", "soupsieve", "sqlalchemy", "sqlite", "sqlite3", "sympy", "tcltk", "test", "testpath", "tkinter",
                    "tomli", "tornado", "traitlets", "unittest", "urllib3", "wcwidth", "wheel", "win32com", "wx", "xlsxwriter", "xml", "xmlrpc", "zipp", "zmq", "zope", "Cython"],
                    "bin_excludes": ["libcrypto-1_1.dll", "unicodedata.pyd"],
                     "optimize": 0,
                     "include_files": list(zip(png, png)) + list(zip(tc, tc)) + list(zip(csv, csv))}

# Information about the program and build command. Has to be adjusted for
# other programs
setup(
    name="MyProgram",                           # Name of the program
    version="0.1",                              # Version number
    description="MyDescription",                # Description
    options = {"build_exe": build_exe_options}, # <-- the missing line
    executables=[Executable("main.py",     # Executable python file
                            base = ("Win32GUI" if sys.platform == "win32" 
                            else None))],
)
shutil.rmtree(r"build\exe.win-amd64-3.8\lib\pygame\docs")
shutil.make_archive("game", 'zip', "build\exe.win-amd64-3.8")