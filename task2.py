import pandas as pd
from task1 import get_price

df = pd.read_csv('data/Nat_Gas_fortask2.csv')
print(df.head())
print(df.dtypes)
print(df.describe())
print(df.info())

def price_contract(injection_dates, 
                   withdrawal_dates,
                   injection_rate, 
                   withdrawal_rate,
                   max_storage, 
                   storage_cost_rate, 
                   get_price
                   ):
    inj_date = [pd.to_datetime(d) for d in injection_dates]
    with_date = [pd.to_datetime(d) for d in withdrawal_dates]

    storage = 0
    total_injection_cost = 0
    total_withdrawal_revenue = 0

    for date in inj_date:
        can_inject = min(injection_rate, max_storage - storage)
        price = get_price(str(date.date()))
        total_injection_cost += can_inject * price
        storage += can_inject

    for date in with_date:

        can_withdraw = min(withdrawal_rate, storage)
        price = get_price(str(date.date()))
        total_withdrawal_revenue += can_inject * price
        storage -= can_withdraw

    all_date = sorted(inj_date + with_date)
    days_stored = (all_date[-1] - all_date[0]).days
    total_storage_cost = storage_cost_rate * days_stored

    value = total_withdrawal_revenue - total_injection_cost - total_storage_cost
    return round(value, 2)

val = price_contract(
    injection_dates   = ["2023-06-01", "2023-06-15"],
    withdrawal_dates  = ["2023-12-01", "2023-12-15"],
    injection_rate    = 1000,       # 1000 units per day
    withdrawal_rate   = 1000,
    max_storage       = 5000,       # max 5000 units
    storage_cost_rate = 10,         # $10 per day storage
    get_price         = get_price   # your function from task 1
)

print(f"Contract Value: ${val}")