# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


# %%
df = pd.read_csv('data/Nat_Gas.csv')

# %%
df.head()

# %%
df.dtypes

# %%
df['Dates'] = pd.to_datetime(df['Dates'])
df = df.sort_values('Dates')

# %%
df.dtypes

# %%
plt.plot(df['Dates'], df['Prices'])
plt.title('Natural Gas Price')
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

# %%
df['Days'] = (df['Dates'] - df['Dates'].min()).dt.days
cs =    CubicSpline(df['Days'], df['Prices'])

# %%
last_days = df['Days'].max()
future_days = np.linspace(last_days, last_days + 365, 12)
future_prices = cs(future_days)

# %%
def get_price(date_str):
    input_date = pd.to_datetime(date_str)
    origin = df['Dates'].min()
    day_num = (input_date - origin).days
    price = float(cs(day_num))
    return round(price, 2)

# Example usage
print(get_price("2023-06-15"))   # past date (interpolation)
print(get_price("2025-03-01"))   # future date (extrapolation)


