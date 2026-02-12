import numpy as np
import time

#
#
# FUNCTIONS
# Shorter function name for matrix exponentiation
def matpow(matrix, times):
    return np.linalg.matrix_power(matrix, times)

# Number of companies per rating: {7, 285, 1399, 1848, 1190, 1744, 342} corresponding to AAA, AA, ...
# ratings = {0: "AAA", 1: "AA", 2: "A", 3: "BBB", 4: "BB", 5: "B", 6: "C", 7: "D"}
def genRating():
    counts = np.array([7, 285, 1399, 1848, 1190, 1744, 342])
    probs = counts / counts.sum()

    # Returns int corresponding to ratings dictionary
    return np.random.choice(len(counts), p = probs)

def newRating(curRating, mat):
    # get new rating based on current rating (Markov chain)
    return np.random.choice(range(8), p = mat[curRating])

# assume recovery rate is 0.4 for all companies
# risk free rate on 2-9-26 is 0.03442
# use geom. average Pdefault over time remaining on loan
def getInterest(pDef, yearsRem, rating):
    ann = 1 - (1 - pDef)**(1 / yearsRem)    # annualized probability of default

    # derived from (1 + Interest) * (1 - PD) + (Recovery * PD) = 1 + risk free rate
    loanRate = (1 + 0.03442 - ann * 0.4) / (1 - ann) - 1    

    # # derived from PD = (Interest - rfr) / (1 - recovery)
    # loanRate = ann * 0.6 + 0.03442

    # different profit margins for each interest rate
    if rating < 2:
        margin = 0.004
    elif rating < 4:
        margin = 0.015
    elif rating < 6:
        margin = 0.04
    else:
        margin = 0.1

    # multiply the rate so that we are earning money vs charging the rfr equivalent
    rate = margin + loanRate

    return rate



#
#
# MAIN

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
# AAA given a chance to demote and AA to promote
yearmat_clean = [[0.98, 0.02,   0,      0,      0,      0,      0,      0],      # AAA
                [0.02,  0.9456, 0.0344, 0,      0,      0,      0,      0],      # AA
                [0,     0.0087, 0.9663, 0.0250, 0,      0,      0,      0],      # A
                [0,     0,      0.0258, 0.9573, 0.0134, 0.0017, 0.0009, 0.0009], # BBB
                [0,     0,      0.0008, 0.0383, 0.9266, 0.026,  0.0027, 0.0056], # BB
                [0,     0,      0,      0.0007, 0.0509, 0.8798, 0.0375, 0.0311], # B
                [0,     0,      0,      0,      0,      0.1234, 0.5335, 0.3431], # C
                [0,     0,      0,      0,      0,      0,      0,      1]]      # D

yearmat_a = np.array(yearmat_clean)

#
#
# Simulation

myBal = 0
totalLosses = 0
loanLife = 10

# generate matrices for years until loan matures
# reduced simulation time by 30%
rows, cols = yearmat_a.shape

matrices = np.zeros((loanLife, rows, cols))
for k in range(loanLife):
    matrices[k] = matpow(yearmat_a, loanLife - k)

sims = 10000

startTime = time.perf_counter()

for m in range(sims):

    rating = genRating()
    yearsRem = loanLife

    gain = 0    # give 10000 to company as loan
    loss = 10000

    for i in range(loanLife):
        # our money is reinvested at the risk free rate
        gain *= 1.03442

        if loss > 0:
            PDtotal = matrices[loanLife - yearsRem][rating][7]
            interest = getInterest(PDtotal, yearsRem, rating)

            # apply interest
            loss *= (1 + interest)

            rating = newRating(rating, yearmat_a)

            if rating == 7:
                # recovery of balance
                gain += 0.4 * loss
                totalLosses += loss
                loss = 0
            else:
                # loan payment
                payment = loss / yearsRem

                gain += payment
                loss -= payment


        yearsRem -= 1

    myBal += gain

endTime = time.perf_counter()
elapsed = endTime - startTime

print(f"\nInitial investment of ${sims*10000:,.2f}.")
print(f"We now have ${myBal:,.2f} and lost ${totalLosses:,.2f} on defaults.")

rfr = sims * 10000 * (1.03442 ** loanLife)
profit = myBal - rfr

totalPct = (myBal / (sims * 10000)) * 100
annualPct = ((totalPct/100)**(1 / loanLife) - 1) * 100

print(f"We profited ${profit:,.2f} over the risk-free rate of ${rfr:,.2f}.")
print(f"We got a total profit of {totalPct:.2f}%.")
print(f"Yearly profit of {annualPct:.2f}%.")
print(f"Program took {elapsed:.4f} seconds to run.\n")