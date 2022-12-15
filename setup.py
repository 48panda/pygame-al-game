from cx_Freeze import setup, Executable
import sys
import shutil
from glob import glob
import gzip
import json
import os

png = glob("assets/*.png") + glob("assets/*/*.png")
tc = glob("assets/*.tc") + glob("assets/*/*.tc")
csv = glob("assets/*.csv")
mp3 = glob("assets/sound/music/*.mp3")
txt = glob("assets/*.txt") + glob("assets/*/*.txt")
ttf = glob("assets/fonts/*.ttf")
json_files = glob("assets/*.json", recursive=True)
# To build do `python .\setup.py build`

# exclude unneeded packages. If building yourself, add libraries here to reduce file size
build_exe_options = {"includes": ["pygame"],
                    "excludes":["_distutils_hack", "_pytest", "asyncio", "atomicwrites", "attr", "backcall", "backports", "black", "blib2to3", "bs4", "cairo", "certifi", "cffi", "chardet", "charset_normalizer",
                    "click", "cloudpickle", "colorama", "concurrent", "cryptography", "ctypes", "curses", "dateutil", "defusedxml", "distutils", "docutils", "email",
                    "fonttools", "html", "http", "idna", "inportlib", "importlib_metadata", "ipykernel", "Ipython", "ipython_genutils", "jedi", "jinja2", "jsonschema", "jupyter_client", "jupyter_core",
                    "lib2to3","lib", "lxml", "markupsafe", "matplotlib", "more_itertools", "mpl_toolkits", "mpmath", "multiprocessing", "nbconvert", "nbformat", "notebook", "OpenGL", "OpenGL_accelerate",
                    "packaging", "pandas", "parso", "pathlib2", "pathspec", "pkg_resources", "platrformdirs", "pluggy", "prompt_toolkit", "py", "pycparser", "pydoc_data", "pyglet", "pygments", "PyQt5",
                    "pyreadline", "pyrsistent", "pytest", "pytz", "pyximport", "qtpy", "requests", "scipy", "setuptools", "soupsieve", "sqlalchemy", "sqlite", "sqlite3", "sympy", "tcltk", "test", "testpath", "tkinter",
                    "tomli", "tornado", "traitlets", "unittest", "urllib3", "wcwidth", "wheel", "win32com", "wx", "xlsxwriter", "xml", "xmlrpc", "zipp", "zmq", "zope", "Cython", "numpy", "PIL", "logging"],
                    "bin_excludes": ["libcrypto-1_1.dll", "unicodedata.pyd"],
                     "optimize": 0,
                     "include_files": list(zip(png, png)) + list(zip(tc, tc)) + list(zip(csv, csv)) + list(zip(mp3, mp3)) + list(zip(txt, txt)) + list(zip(ttf, ttf)) + list(zip(json_files, json_files))}

setup(
    name="MyProgram",
    version="0.1",
    description="MyDescription",
    options = {"build_exe": build_exe_options},
    executables=[Executable("main.py",
                            base = ("Win32GUI" if sys.platform == "win32" 
                            else None))],
)
shutil.rmtree(r"build\exe.win-amd64-3.8\lib\pygame\docs")

for filename in glob("build/exe.win-amd64-3.8/assets/*.json", recursive=True):
    with open(filename, 'r') as f:
        data = f.read()
    with gzip.open(os.path.splitext(filename)[0] + '.gzon', 'wb') as f:
        f.write(json.dumps(json.loads(data), separators=(',', ':')).encode())
    os.remove(filename)

shutil.make_archive("game", 'zip', "build\exe.win-amd64-3.8")
