import os, sys

cmd = f'export PYTHONPATH=\'{os.path.dirname(os.path.realpath("__file__"))}\''

print(cmd)
os.system(cmd)
os.system("echo $PYTHONPATH")
