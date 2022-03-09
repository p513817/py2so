from ast import arg
import sys, os, glob, shutil
from distutils.core import setup
from Cython.Build import cythonize
from datetime import datetime
# we'd better have Cython installed, or it's a no-go
try:
    from Cython.Distutils import build_ext
except:
    print("You don't seem to have Cython installed. Please get a")
    print("copy from www.cython.org and install it")
    sys.exit(1)

# get custom argument: if no key return None , if no value return default
def get_args(args:list, key:str, default:str=None):
    if key in args:
        idx = args.index(key)
        try:
            val = args[int(idx)+1]           # get value of argument
            [ sys.argv.remove(i) for i in [key, val] ] # remove argument or setup will get error
            return os.path.abspath(val)
        except Exception as e:
            if default:
                return default        
            else:
                raise Exception('Could not find the value of argument ({})'.format(key))
    else:
        return default

# print help
def helper():
    info = [
        "$ python setup.py build_ext --inplace --src <the_source_path> [Options]",
        "",
        "[Options]",
        "--dst       if not provide the destination path, will backup and replace the original one.",
        "--backup    the backup path.",
        "--build     the path of build folder, the default is './build'",
        "" ]
    [print(i) for i in info]
    sys.exit(1)

# setup basic variable
args = sys.argv

# show helper 
if not (('build_ext' in args) and ('--inplace' in args) and ('--src' in args)) or (('--help' in args) and ('-h' in args)): helper()

# ------------------------------------------------------------------------------------------------------------------------------
# parse custom variable
src_path = get_args(args, '--src') 
dst_path = get_args(args, '--dst', src_path)                   
backup_path = get_args(args, '--backup', './backup') 
build_path = get_args(args, '--build', './build') 

print(src_path, dst_path, backup_path, build_path)

# if the source is exists, clear pycahe folder
if not os.path.exists(src_path):
    raise Exception('\nCould not find the source path ({})'.format(src_path))                
else:
    [ shutil.rmtree(f) for f in glob.glob(f"{src_path}/**/__pycache__", recursive=True) ] 

# backup the old one with time if the source path is same with the destination path or the backup option is enable
if (src_path==dst_path) or backup_path :
    if not os.path.exists(backup_path): os.makedirs(backup_path)
    shutil.copytree(src_path, os.path.join(backup_path, "{}_{}".format(os.path.basename(src_path), datetime.now().strftime("%Y%m%D_%H%M%S"))))

# create a temp_dst for setup.py if the source path is not same with the destination path
temp_dst = os.path.join( os.getcwd(), os.path.basename(dst_path) )
if src_path!=dst_path:
    shutil.copytree(src_path, temp_dst)

# distutils
# cpature all python files but exclude __init__.py
extensions = [ f for f in glob.glob(f"{temp_dst}/**/*.py", recursive=True) if not ("__init__" in f) ]
setup(
    name=temp_dst,
    ext_modules=cythonize(extensions),
    cmdclass = {'build_ext': build_ext},
    build_dir=build_path
)

# remove build and `.py`
[ os.remove(f) for f in extensions ]
[ os.remove(f) for f in glob.glob(f"{temp_dst}/**/*.c", recursive=True) ]
shutil.rmtree(build_path)

# overwrite
if src_path!=dst_path:
    shutil.move(temp_dst, dst_path)