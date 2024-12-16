import pandas as pd
import numpy as np
import statsmodels.api as sm


nasdaq_100 = pd.read_csv("Nasdaq_100_postprocess.csv")

print(nasdaq_100[['1d_forward_return', '1d_change', '2d_change','3d_change','4d_change', '5d_change','10d_change','15d_change', '1d_bad_state']])

Y = nasdaq_100['1d_forward']
X = nasdaq_100[['Open','1d_lag', '2d_lag', '3d_lag', '4d_lag', '5d_lag', '10d_lag' ]]

X = sm.add_constant(X)

# Regression model
model = sm.OLS(Y, X).fit()
print(model.summary())