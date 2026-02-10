import numpy as np

#
#
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

def newRating(curRating, mat):
    # get new rating based on current rating (Markov chain)
    return np.random.choice(range(8), p = mat[curRating])

# assume recovery rate is 0.4 for all companies
# risk free rate on 2-9-26 is 0.03442
# use geom. average Pdefault over time remaining on loan
def getInterest(pDef, yearsRem, rating):
    ann = 1 - (1 - pDef)**(1 / yearsRem)    # annualized probability of default

    # derived from (1 + Interest) * (1 - PD) + (Recovery * PD) = 1 + risk free rate
    spread = (1 + 0.03442 - ann * 0.4) / (1 - ann) - 1    

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
    rate = margin + spread

    return rate



#
#
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
# AAA given a chance to demote and AA to promote
yearmat_clean = [[0.98, 0.02, 0, 0, 0, 0, 0, 0], 
                [0.02, 0.9456, 0.0344, 0, 0, 0, 0, 0], 
                [0, 0.0087, 0.9663, 0.0250, 0, 0, 0, 0], 
                [0, 0, 0.0258, 0.9573, 0.0134, 0.0017, 0.0009, 0.0009], 
                [0, 0, 0.0008, 0.0383, 0.9266, 0.026, 0.0027, 0.0056], 
                [0, 0, 0, 0.0007, 0.0509, 0.8798, 0.0375, 0.0311], 
                [0, 0, 0, 0, 0, 0.1234, 0.5335, 0.3431], 
                [0, 0, 0, 0, 0, 0, 0, 1]]

yearmat_a = np.array(yearmat_clean)

#
#
# Simulation for one company

rating = genRating()
yearsRem = 10
loops = yearsRem

myBal = 0    # give 10000 to company as loan
compBal = 10000

for i in range(loops):
    label = ratings[rating]
    print(f"\nYear {loops+1-yearsRem}")
    print(f"Company is rated {label} with {yearsRem} years remaining.")

    # our money is reinvested at the risk free rate
    myBal *= 1.03442

    print(f"My balance is ${myBal:.2f}.")

    if compBal > 0:
        PDtotal = matpow(yearmat_a, yearsRem)[rating][7]
        interest = getInterest(PDtotal, yearsRem, rating)

        print(f"Probability of default is {PDtotal:.4f}")
        print(f"Interest rate is {interest:.4f}")

        # apply interest
        compBal *= (1 + interest)

        rating = newRating(rating, yearmat_a)

        if rating == 7:
            # recovery of balance
            myBal += 0.4 * compBal
            compBal = 0
        else:
            # loan payment
            payment = compBal / yearsRem
            print(f"Company paid ${payment:.2f}.")

            myBal += payment
            compBal -= payment

    else:
        print("Company went default.")

    yearsRem -= 1

print(f"\nWe now have ${myBal:.2f} and the company has ${compBal:.2f}")

rfr = 10000 * (1.03442 ** loops)
profit = myBal - rfr

print(f"We profited ${profit:.2f} over the risk-free rate.")
