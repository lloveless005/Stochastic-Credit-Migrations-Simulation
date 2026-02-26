import streamlit as st
import matplotlib.pyplot as plt
from main import *

st.title("Loan Risk Dashboard")

left_column, right_column = st.columns(2)

with left_column:
    investment = st.number_input("Investment per Company ($)", min_value = 1)

    RR = st.number_input("Recovery Rate (%)", min_value = 0.0, max_value = 100.0)

with right_column:
    loanLife = st.number_input("Loan Term (years)", min_value = 1, max_value = 100)

    sims = st.number_input("Simulations", min_value = 1, max_value = 10_000_000)

if st.button(label = 'Run Simulations'):
    startTime = time.perf_counter()

    losses = []
    risks = []
    pcts = []
    index = 0
    riskTolerance = 5

    while riskTolerance <= 100:
        risks.append(riskTolerance)

        myBal, totalLosses = riskSim(yearmat_a, riskTolerance/100, RR/100, loanLife, sims, investment)

        losses.append(totalLosses)

        index += 1
        riskTolerance += 5

        totalPct = (myBal / (sims * investment)) * 100
        annualPct = ((totalPct/100)**(1 / loanLife) - 1) * 100

        pcts.append(annualPct)

    endTime = time.perf_counter()
    elapsed = endTime - startTime   

    losses = np.array(losses)
    risks = np.array(risks)
    pcts = np.array(pcts)

    lossesGraph, ax1 = plt.subplots()

    ax1.plot(risks, losses)
    ax1.set_xlabel("Risk Tolerance (%)")
    ax1.set_ylabel("Total Losses ($)")
    ax1.set_title("Total Losses By Risk Tolerance")

    pctsGraph, ax2 = plt.subplots()

    ax2.plot(risks, pcts)
    ax2.axhline(y = RISKFREE*100, color = "red", linestyle = "dashed")
    ax2.set_xlabel("Risk Tolerance (%)")
    ax2.set_ylabel("Yearly Return (%)")
    ax2.set_title("Yearly Return By Risk Tolerance")

    leftGraph, rightGraph = st.columns(2)

    with leftGraph:
        st.pyplot(pctsGraph)

    with rightGraph:
        st.pyplot(lossesGraph)

    st.write(f"Program took {elapsed:.4f} seconds to run.\n")