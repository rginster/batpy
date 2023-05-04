# -*- coding: UTF-8 -*-
"""batpy's build in datasets
"""

import os

__versions__ = [f.name for f in os.scandir(f"{__path__[0]}") if f.is_dir()]
