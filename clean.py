import sys, os

this_module = os.path.abspath(os.path.dirname(sys.modules[__name__].__file__))

calc_path = os.path.join(this_module, 'calculation')

for (path, dirs, files) in os.walk(calc_path):
    for f in files:
        if f.endswith('.obj'):
            os.remove(os.path.join(path, f))
        if f.startswith('calc.'):
            os.remove(os.path.join(path, f))