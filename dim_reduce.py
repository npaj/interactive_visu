import os 
import argparse
import glob

import pandas as pd
import numpy as np
import umap


parser = argparse.ArgumentParser()
parser.add_argument('--datapath', type=str, required=True)
args = parser.parse_args()

LIST_PATH = glob.glob(os.path.join(args.datapath, '*.txt'))


# SVM

# SVD

# PCA

# ICA

