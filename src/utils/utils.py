import os
import random
import hashlib

import numpy as np

def init_seed(seed:int = 0):
    np.random.seed(seed)
    random.seed(seed)

def project_path():
    return os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ), "..", ".."
    )