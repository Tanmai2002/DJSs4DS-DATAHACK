import streamlit as st
st.write("# Personal Finance")
import pandas as pd
import os.path
import numpy as np

path = 'budget.csv'

check_file = os.path.isfile(path)
# Load budget data
budget_data=pd.DataFrame(columns=["Name","Amount", "Category"])
if check_file:
 budget_data = pd.read_csv("budget.csv")



# Add new transaction
st.header("Add New Transaction")
transaction_name = st.text_input("Enter transaction name:")
transaction_amount = st.number_input("Enter transaction amount:")
transaction_category = st.selectbox("Select transaction category:", 
                                   ["Housing", "Transportation", "Food", "Utilities", "Entertainment", "Other"])
if st.button("Add"):
    new_row = {"Name": transaction_name, "Amount": transaction_amount, "Category": transaction_category}
    budget_data = budget_data.append(new_row, ignore_index=True)
    budget_data.to_csv("budget.csv", index=False)
    st.success("Transaction added successfully!")
    
# View transactions by category
st.header("View Transactions")
category = st.selectbox("Select category:", ["All"] + list(budget_data["Category"].unique()))
op_data=budget_data
if category == "All":
    pass
else:
    op_data= budget_data[budget_data["Category"] == category]
    
if len(op_data)>0:
 max_amount = float(np.max(op_data["Amount"]))
 min_amount = float(np.min(op_data["Amount"]))
 amount_range = st.slider("Select amount range:", min_amount, max_amount,(min_amount-1,max_amount))

 op_data = op_data[(op_data["Amount"] >= amount_range[0]) & (op_data["Amount"] <= amount_range[1])]
 st.write(op_data)












def calculate_tax_reductions(income, deductions, is_new_regime):
    # Set the tax rates for the old and new regimes
    old_rates = {0: 0, 250000: 0.05, 500000: 0.1, 750000: 0.15, 1000000: 0.2, 1250000: 0.25, 1500000: 0.3}
    new_rates = {0: 0, 250000: 0.05, 500000: 0.1, 750000: 0.15, 1000000: 0.2, 1250000: 0.25, 1500000: 0.3, 2500000: 0.35, 5000000: 0.3}

    # Calculate the tax reductions for the old and new regimes
    old_tax = 0
    new_tax = 0
    for rate, cutoff in old_rates.items():
        if income <= cutoff:
            old_tax += rate * income
            break
        else:
            old_tax += rate * (cutoff - (0 if cutoff == 0 else old_rates[list(old_rates.keys())[list(old_rates.keys()).index(rate)-1]]))
            income -= cutoff
    for rate, cutoff in new_rates.items():
        if income <= cutoff:
            new_tax += rate * income
            break
        else:
            new_tax += rate * (cutoff - (0 if cutoff == 0 else new_rates[list(new_rates.keys())[list(new_rates.keys()).index(rate)-1]]))
            income -= cutoff

    # Calculate the tax reductions based on the deductions
    old_tax_reduction = deductions if is_new_regime else max(0, old_tax - deductions)
    new_tax_reduction = deductions if not is_new_regime else max(0, new_tax - deductions)

    # Print the tax reductions
    print("Tax reductions under old regime: INR %.2f" % old_tax_reduction)
    print("Tax reductions under new regime: INR %.2f" % new_tax_reduction)

st.number_input("Enter gross salary",value=0)




