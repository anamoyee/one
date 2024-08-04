import os
import pathlib as p

if 'one.py' not in os.listdir():
  raise RuntimeError('Wrong directory!')

for file in p.Path(__file__).parent.iterdir():
  if file.suffix == '.py' and file.name not in ['reset.py', 'main.py', 'one.py']:
    file.unlink()

if __name__ != '__main__':
  import sys
  del sys.modules[__name__]
