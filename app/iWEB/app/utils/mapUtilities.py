# Dimitar: read_map() code
# Kai: linting
"""
Small module to define the read_map() function.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'utils/maps/streatham-campus.txt')

# This function reads the map from the file and returns it as a list of lists
def read_map():
    
    with open(file_path, 'r', encoding="utf-8") as f:
        map = [[char for char in line.strip()] for line in f]
    return map