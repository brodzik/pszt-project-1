# Authors:
#   Adrian Brodzik
#   Jakub Górka


import os
import random

import numpy as np


def seed_everything(seed):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
