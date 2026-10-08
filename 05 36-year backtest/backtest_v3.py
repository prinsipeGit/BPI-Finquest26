"""36-year proxy aligned to the v3 capacity types (run after backtest.py, which writes results.pkl).
Owners: Util, Telcm, Trans; Suppliers: ElcEq, Chips. Same ERC, role limits, 25% sleeve cap, 10% reserve, 1.50% fee.
Market fund = 90% US market + 10% T-bill reserve, 1.50% fee. Writes results_v3.pkl (cap3, w3, mkt)."""
import pandas as pd, backtest as BT
df = BT.load()
CAP3 = {'Util': 'O', 'Telcm': 'O', 'Trans': 'O', 'ElcEq': 'S', 'Chips': 'S'}
cap3, w3 = BT.run(df, CAP3, BT.CAP_LIMITS)
us = BT.to_php(df.Mkt, df.fxret).loc[cap3.index]
cash = BT.to_php(df.RF, df.fxret).loc[cap3.index]
mkt = (1 + 0.9*us + 0.1*cash)*(1 - BT.FEE)**(1/12) - 1
pd.to_pickle(dict(cap3=cap3, w3=w3, mkt=mkt), 'results_v3.pkl')
print(BT.stats(cap3)); print(BT.stats(mkt))
