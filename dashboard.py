import streamlit as st
from main import *

st.title("Loan Risk Dashboard")

left_column, right_column = st.columns(2)

investment = st.number_input("Investment per Company ($)", min_value = 1)

with left_column:
    riskTolerance = st.number_input("Risk Tolerance (%)", min_value = 0.0, max_value = 100.0)

    RR = st.number_input("Recovery Rate (%)", min_value = 0.0, max_value = 100.0)

with right_column:
    loanLife = st.number_input("Loan Term (years)", min_value = 1, max_value = 100)

    sims = st.number_input("Simulations", min_value = 1, max_value = 1_000_000)

if st.button(label = 'Run Simulations'):
    startTime = time.perf_counter()

    myBal, totalLosses = riskSim(yearmat_a, riskTolerance/100, RR/100, loanLife, sims, investment)

    endTime = time.perf_counter()
    elapsed = endTime - startTime   

    st.write(f"\nTotal initial investment of \\${sims*investment:,.0f}.")
    st.write(f"Our risk tolerance is {riskTolerance}%.")
    st.write(f"We now have \\${myBal:,.2f} and lost \\${totalLosses:,.2f} on defaults.")

    rfr = sims * investment * (1.03442 ** loanLife)
    profit = myBal - rfr

    totalPct = (myBal / (sims * investment)) * 100
    annualPct = ((totalPct/100)**(1 / loanLife) - 1) * 100

    st.write(f"We profited \\${profit:,.2f} over the risk-free rate of \\${rfr:,.2f}.")
    st.write(f"We got a total profit of {totalPct:.2f}%.")
    st.write(f"Yearly profit of {annualPct:.2f}%.")
    st.write(f"Program took {elapsed:.4f} seconds to run.\n")