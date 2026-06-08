# Stochastic Credit Migrations Simulation

This repository contains a simulation engine and an interactive dashboard for pricing corporate loans and analyzing portfolio risk. The model leverages stochastic processes to simulate the migration of S&P credit ratings over time, using this information to price loans and manage a portfolio based on a defined risk tolerance.

This project was created for MATH 541 Stochastic Processes honors credit.

## Core Concepts

The simulation is built upon a few key financial and mathematical principles:

### 1. Markov Chain for Credit Ratings
Corporate credit ratings (from AAA down to D for Default) are modeled as states in a discrete-time Markov chain. The simulation uses a one-year transition matrix based on historical corporate credit rating changes. This matrix dictates the probability of a company's rating changing from one state to another over a one-year period.

### 2. Risk-Neutral Loan Pricing
Interest rates for new loans are calculated using a risk-neutral pricing approach. The core idea is that the expected return of a risky asset (the loan) should equal the return of a risk-free asset. The interest rate is set to compensate for the annualized probability of default (`pDef`) and the expected loss given default (1 - `Recovery Rate`). A spread based on the company's credit rating is also added to ensure profitability.

The formula is derived from:
`(1 + Interest) * (1 - pDef) + (RecoveryRate * pDef) = 1 + RiskFreeRate`

### 3. Chapman-Kolmogorov for Lifetime Default Probability
To determine the probability of a company defaulting over the entire remaining life of its loan, the model uses matrix exponentiation on the one-year transition matrix. This is an application of the Chapman-Kolmogorov equation, which allows us to calculate the n-step transition probabilities from the one-step matrix.

## Interactive Dashboard

An interactive dashboard built with Streamlit (`dashboard.py`) allows for easy exploration of the model.

You can configure the following parameters:
- **Investment per Company ($):** The principal amount for each loan issued in the simulation.
- **Recovery Rate (%):** The percentage of the outstanding loan balance recovered if a company defaults.
- **Loan Term (years):** The total life of the loans being simulated.
- **Simulations:** The number of individual loan simulations to run for each data point. Higher numbers yield more accurate results but take longer to compute.

After running the simulations, the dashboard displays two plots:
1.  **Yearly Return By Risk Tolerance:** This graph shows the annualized return of the portfolio at different levels of risk tolerance. Risk tolerance is defined as the maximum probability of default a loan can have before it is sold off. A red dashed line indicates the risk-free rate for comparison.
2.  **Total Losses By Risk Tolerance:** This graph illustrates the total monetary losses incurred across the entire portfolio at different risk tolerance levels.

## Getting Started

To run the simulation and launch the interactive dashboard locally, follow these steps.

### Prerequisites
- Python 3.8+
- Git

### Installation
1.  Clone the repository:
    ```sh
    git clone https://github.com/lloveless005/Stochastic-Credit-Migrations-Simulation.git
    cd Stochastic-Credit-Migrations-Simulation
    ```

2.  Create and activate a virtual environment (recommended):
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Usage
1.  Run the Streamlit application from your terminal:
    ```sh
    streamlit run dashboard.py
    ```

2.  Your web browser will open with the dashboard. Adjust the input parameters and click the "Run Simulations" button to start.