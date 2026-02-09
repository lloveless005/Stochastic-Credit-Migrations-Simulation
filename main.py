import numpy as np

# FUNCTIONS
# Shorter function name for matrix exponentiation
def matpow(matrix, times):
    return np.linalg.matrix_power(matrix, times)

# MAIN
# Correspond rating to matrix row
ratings = {"AAA": 0, "AA": 1, "A": 2, "BBB": 3, "BB": 4, "B": 5, "C": 6, "D": 7, "NR": 8}

# Transition matrix for corporate credit ratings in one year
yearmat = [[1, 0, 0, 0, 0, 0, 0, 0, 0], 
           [0, 0.9368, 0.0316, 0, 0, 0, 0, 0, 0.0316], 
           [0, 0.0086, 0.9507, 0.0243, 0, 0, 0, 0, 0.0164], 
           [0, 0, 0.0249, 0.9253, 0.013, 0.0011, 0.0005, 0.0005, 0.0346], 
           [0, 0, 0.0008, 0.0361, 0.8731, 0.0245, 0.0025, 0.0017, 0.0613], 
           [0, 0, 0, 0.0006, 0.0459, 0.793, 0.0338, 0.0172, 0.1095], 
           [0, 0, 0, 0, 0, 0.1082, 0.4678, 0.2836, 0.1404], 
           [0, 0, 0, 0, 0, 0, 0, 1, 0], 
           [0, 0, 0, 0, 0, 0, 0, 0, 1]]

yearmat_a = np.array(yearmat)