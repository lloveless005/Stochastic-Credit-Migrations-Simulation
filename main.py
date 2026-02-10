import numpy as np

# FUNCTIONS
# Shorter function name for matrix exponentiation
def matpow(matrix, times):
    return np.linalg.matrix_power(matrix, times)

# Number of companies per rating: {7, 285, 1399, 1848, 1190, 1744, 342} corresponding to AAA, AA, ...
def genRating():
    counts = np.array([7, 285, 1399, 1848, 1190, 1744, 342])
    probs = counts / counts.sum()

    # Returns int corresponding to ratings dictionary
    return np.random.choice(len(counts), p = probs)

# rate = Pdefault * (1 - Recovery rate) + risk free rate
# assume recovery rate is 0.4 for all companies
# risk free rate on 2-9-26 is 0.03442
# use geom. average Pdefault over time remaining on loan
def getInterest(pDef, yearsRem):
    ann = 1 - (1 - pDef)**(1 / yearsRem)    # annualized interest rate

    return (1 + 0.03442 - ann * 0.4) / (1 - ann) - 1





# MAIN
# Correspond rating to matrix row
ratings = {0: "AAA", 1: "AA", 2: "A", 3: "BBB", 4: "BB", 5: "B", 6: "C", 7: "D"}

# Transition matrix for corporate credit ratings in one year
# yearmat = [[1, 0, 0, 0, 0, 0, 0, 0, 0], 
#            [0, 0.9368, 0.0316, 0, 0, 0, 0, 0, 0.0316], 
#            [0, 0.0086, 0.9507, 0.0243, 0, 0, 0, 0, 0.0164], 
#            [0, 0, 0.0249, 0.9253, 0.013, 0.0011, 0.0005, 0.0005, 0.0346], 
#            [0, 0, 0.0008, 0.0361, 0.8731, 0.0245, 0.0025, 0.0017, 0.0613], 
#            [0, 0, 0, 0.0006, 0.0459, 0.793, 0.0338, 0.0172, 0.1095], 
#            [0, 0, 0, 0, 0, 0.1082, 0.4678, 0.2836, 0.1404], 
#            [0, 0, 0, 0, 0, 0, 0, 1, 0], 
#            [0, 0, 0, 0, 0, 0, 0, 0, 1]]

# Redistribute NR
yearmat_clean = [[1, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0.9656, 0.0344, 0, 0, 0, 0, 0], 
                [0, 0.0087, 0.9663, 0.0250, 0, 0, 0, 0], 
                [0, 0, 0.0258, 0.9573, 0.0134, 0.0029, 0.0008, 0.0008], 
                [0, 0, 0.0008, 0.0383, 0.9266, 0.026, 0.0027, 0.0056], 
                [0, 0, 0, 0.0007, 0.0509, 0.8798, 0.0375, 0.0311], 
                [0, 0, 0, 0, 0, 0.1234, 0.5335, 0.3431], 
                [0, 0, 0, 0, 0, 0, 0, 1]]

yearmat_a = np.array(yearmat_clean)
