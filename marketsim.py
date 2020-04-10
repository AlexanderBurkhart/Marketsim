import pandas as pd

import numpy as np
import datetime as dt
import os
from util import get_data, plot_data, calc_stats

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    df_orders = pd.read_csv(orders_file)
    
    syms = []
    for sym in df_orders['Symbol']:
        if sym not in syms:
            syms.append(sym)
    prices_all = get_data(syms, pd.date_range(df_orders['Date'].iloc[0], df_orders['Date'].iloc[-1]))
    
    df_port = pd.DataFrame(columns=['Date', 'Value'])
    val = start_val
    for idx, act in df_orders.iterrows():
        p = prices_all.loc['Adj Close'][act['Symbol']][act['Date']]*act['Shares']
        if(act['Order'] == 'BUY'):
            val -= p        
        if(act['Order'] == 'SELL'):
            val += p
        val -= 2*commission + 2*p*impact
        df_port = df_port.append({'Date': act['Date'], 'Value': val}, ignore_index=True)
    
    df_port = df_port.set_index('Date')
    return df_port


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters
    of = "orders/orders-01.csv"
    sv = 1000000

    # Process orders 	 		 			  		  			
    portvals = compute_portvals(orders_file = of, start_val = sv)
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = portvals.index[0]
    end_date = portvals.index[1]
    dates = pd.date_range(start_date, end_date)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = calc_stats(portvals)
    cum_ret_GOOG, avg_daily_ret_GOOG, std_daily_ret_GOOG, sharpe_ratio_GOOG = calc_stats(get_data(['GOOG'], dates))
    # Compare portfolio against $SPX
    print(f"Date Range: {start_date} to {end_date}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print(f"Sharpe Ratio of GOOG : {sharpe_ratio_GOOG}")
    print()
    print(f"Cumulative Return of Fund: {cum_ret}")
    print(f"Cumulative Return of GOOG : {cum_ret_GOOG}")
    print()
    print(f"Standard Deviation of Fund: {std_daily_ret}")
    print(f"Standard Deviation of GOOG : {std_daily_ret_GOOG}")
    print()
    print(f"Average Daily Return of Fund: {avg_daily_ret}")
    print(f"Average Daily Return of GOOG : {avg_daily_ret_GOOG}")
    print(f"Final Portfolio Value: {portvals['Value'].iloc[-1]}")

if __name__ == "__main__":
	test_code()  		  	   		     			  		 			     			  	  		 	  	 		 			  		  			
