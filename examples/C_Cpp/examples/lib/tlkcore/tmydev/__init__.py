from pathlib import Path
import sys

__file = Path(__file__).absolute()
__root = __file.parent.parent.parent
if sys.path.count(__root) == 0:
    sys.path.insert(0, __root)
    # print(sys.path)

fromLib = True

if __file.suffix == '.py':
    fromLib = False