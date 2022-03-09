# py2so
Package python API to dynamic shared objects

# Feature
1. Package the project to a new one but will not confuse the original one.
2. The user could use the generated project in the same way as the python module, but could not see any details.
3. Delete `pycache` and exclude `__init__.py` in order to generate a more concise structure.
4. Backup the source file automatically ( the default is `./backup` ).
# Prerequirement
```shell
pip3 install Cython
```

# Help
```shell
$ python setup.py build_ext --inplace --src <the_source_path> [Options]

[Options]
--dst       if not provide the destination path, will backup and replace the original one.
--backup    change the backup path, the default is './backup'
--build     change the path of build folder, the default is './build'
```

# DEMO
* Build shared object from the python API (demo).
    > The python API with shared objects ( out ) will be generated after this command.
    ```shell
    $ python3 setup.py build_ext --inplace --src demo --dst out
    ```
    
* Test the python api and shared object.
    ```shell
    # test the python file (.py)
    $ python3 test_py.py
    /home/max/Workspace/Other/python_packaging/demo/foo/print_me.py
    /home/max/Workspace/Other/python_packaging/demo/bar/print_me.py
    /home/max/Workspace/Other/python_packaging/demo/bar/barbar/print_me.py

    # test the shared object file (.so) 
    $ python3 test_so.py
    /home/max/Workspace/Other/python_packaging/out/foo/print_me.cpython-36m-x86_64-linux-gnu.so
    /home/max/Workspace/Other/python_packaging/out/bar/print_me.cpython-36m-x86_64-linux-gnu.so
    /home/max/Workspace/Other/python_packaging/out/bar/barbar/print_me.cpython-36m-x86_64-linux-gnu.so
    ```

# Feature
[　] Distribute a Python package with a compiled dynamic shared library.