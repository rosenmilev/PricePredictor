import requests
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.express as px


key = '30DQX6JQOX72GQ4E'
ts = TimeSeries(key=key)


# Create function to fetch historical data from API.
def get_historical_data(symbol, start_date, end_date):
	data, meta_data = ts.get_daily(symbol, outputsize='full')
	df = pd.DataFrame(data).T
	df.columns = ['open', 'high', 'low', 'close', 'volume']
	df.index = pd.to_datetime(df.index)
	df.sort_index(inplace=True)

	name = f'{symbol}_{start_date}_{end_date}'

	result = df[start_date:end_date]
	result.to_csv(name)

	return result




start_date = '2023-01-01'
end_date = '2023-12-31'

gold_data = get_historical_data('GOLD', start_date, end_date)
oil_data = get_historical_data('CL=F', start_date, end_date)

gold_data_file_path = 'GLD_2023-01-01_2023-12-31'
gold_df = pd.read_csv(gold_data_file_path, index_col=0, parse_dates=True)
print(gold_df)

oil_data_file_path = 'OIL_2023-01-01_2023-12-31'
oil_df = pd.read_csv(oil_data_file_path, index_col=0, parse_dates=True)
print(oil_df)

# Dataframes for oil and gold prices. The selected indicator is closing price
# Filter both dataframes based on common dates

common_dates = gold_df.index.intersection(oil_df.index)
print(len(common_dates))

oil_data = oil_df.loc[common_dates, ['close']]
oil_data = oil_data.rename(columns={'close': 'oil_price'})
gold_data = gold_df.loc[common_dates, ['close']]
gold_data = gold_data.rename(columns={'close': 'gold_price'})
merged_data = pd.concat([oil_data, gold_data], axis=1)

print(merged_data)
# Calculate correlation between two
correlation = merged_data.oil_price.corr(merged_data.gold_price)
print(correlation)
# It appears there is weak negative correlation of -0.183
# Visualize the correlation

fig = px.line(merged_data, x=merged_data.index, y=['oil_price', 'gold_price'], labels={'value': 'Price', 'variable': 'Asset'},
              title='Oil and Gold Prices Over Time')

fig.update_layout(xaxis_title='Date', yaxis_title='Price')
# fig.show()

input, target = merged_data[['oil_price']], merged_data['gold_price']

model = LinearRegression()
model.fit(input, target)

predictions = model.predict(input)

mse = mean_squared_error(target, predictions)
print(mse)

