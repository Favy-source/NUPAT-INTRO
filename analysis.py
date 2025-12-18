import pandas as pd
import matplotlib.pyplot as plt
trades = pd.read_csv("data/trades.csv")
activity = pd.read_csv("data/user_activitycsv.csv")
print(trades.head())
print(activity.head())
trades["timestamp"] = pd.to_datetime(trades["timestamp"])
activity["timestamp"] = pd.to_datetime(activity["timestamp"])
print(trades.dtypes)
print(activity.dtypes)

# Question 1
trades["usd_volume"] = trades["amount"] / 1500
print(trades[["pair", "amount", "usd_volume"]].head())

pair_volume = trades.groupby("pair")["usd_volume"].sum()
print(pair_volume)

top_3_pairs = pair_volume.sort_values(ascending=False).head(3)
print(top_3_pairs)

#Question1b (visualization)
plt.figure()
top_3_pairs.plot(kind="bar")
plt.title("Top 3 Most Traded Pairs by USD Volume")
plt.xlabel("Trading Pair")
plt.ylabel("Total USD Volume")
plt.show()

#volatility
btc_trades = trades.loc[trades["pair"] == "BTCNGN"].copy()
btc_trades["price"] = btc_trades["amount"] / btc_trades["volume"]
print(btc_trades[["timestamp", "price"]].head())

btc_trades["date"] = btc_trades["timestamp"].dt.date
daily_volatility = btc_trades.groupby("date")["price"].std()
print(daily_volatility)

daily_volatility_df = daily_volatility.reset_index()
daily_volatility_df.columns = ["date", "daily_price_volatility"]
print(daily_volatility_df.head())

daily_volatility_df = daily_volatility_df.sort_values("date")
daily_volatility_df["volatility_7d_avg"] = (
    daily_volatility_df["daily_price_volatility"]
    .rolling(window=7)
    .mean()
)
print(daily_volatility_df.tail())

#my volatility graph
plt.figure()
plt.plot(
    daily_volatility_df["date"],
    daily_volatility_df["volatility_7d_avg"]
)
plt.title("7-Day Rolling Average of BTCNGN Price Volatility")
plt.xlabel("Date")
plt.ylabel("Price Volatility")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#question 3
deposits = activity[activity["activity_type"] == "deposit"]
print(deposits.head())

deposits["day_of_week"] = deposits["timestamp"].dt.day_name()
deposits["hour"] = deposits["timestamp"].dt.hour

deposits_by_day = (
    deposits
    .groupby("day_of_week")["amount"]
    .sum()
    .sort_values(ascending=False)
)
print(deposits_by_day)

#visualization for deposits
plt.figure()
deposits_by_day.plot(kind="bar")
plt.title("Total Deposits by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Total Deposit Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#deposits by hour
deposits_by_hour = (
    deposits
    .groupby("hour")["amount"]
    .sum()
)

print(deposits_by_hour)

#visualization for deposits by hour
plt.figure()
deposits_by_hour.plot(kind="line")
plt.title("Total Deposits by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Total Deposit Amount")
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()
