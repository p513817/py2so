import sys, os, glob, shutil
from distutils.core import setup
from Cython.Build import cythonize
# we'd better have Cython installed, or it's a no-go
try:
    from Cython.Distutils import build_ext
except:
    print("You don't seem to have Cython installed. Please get a")
    print("copy from www.cython.org and install it")
    sys.exit(1)

def get_arguments(args:list, key:str):
    if key in args:
        idx = args.index(key)
        try:
            val = args[int(idx)+1]           # get value of argument
            [ sys.argv.remove(i) for i in [key, val] ] # remove argument or setup will get error
            return val
        except Exception as e:
            return None

args = sys.argv
build_path = "build"

# check basic argument
for opt in ['build_ext', '--inplace']:
    if not (opt in args):
        raise Exception('\nExcepted command is $ python3 setup.py build_ext --inplace <--src> <src path> <--dst> <dst path>') 

# get custom option
src, dst = "src", "dst"
src, dst = [ get_arguments(args, opt) for opt in ['--src', '--dst'] ]

# check the source is exists
if not os.path.exists(src):
    raise Exception("\nCouldn't find the source path ({})".format(src))

# copy the structure and rename and clear pycache
[ shutil.rmtree(f) for f in glob.glob(f"{src}/**/__pycache__", recursive=True) ]
shutil.copytree(src, dst)

# cpature all python files but exclude __init__.py
extensions = [ f for f in glob.glob(f"{dst}/**/*.py", recursive=True) if not ("__init__" in f) ]
    
# Distutils
setup(
    name=src,
    ext_modules=cythonize(extensions),
    cmdclass = {'build_ext': build_ext},
    build_dir=build_path
)

# remove build and `.py`
[ os.remove(f) for f in extensions ]
[ os.remove(f) for f in glob.glob(f"{dst}/**/*.c", recursive=True) ]
shutil.rmtree(build_path)
