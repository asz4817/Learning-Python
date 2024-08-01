import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
import datetime, time


gc = gspread.service_account()
sh = gc.open("Money")
worksheets = sh.worksheets()


df = pd.read_csv("/Users/amandazhang/Downloads/Discover-2024-YearToDateSummary.csv")

#Clean Dataframe
df.rename(columns={'Trans. Date': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df.drop(columns='Post Date', inplace=True)


#Separate into months
monthly_dfs = {}
for month in range(1, 13):
    monthly_dfs[month] = df[df['Date'].dt.month == month]

# Print the DataFrames for each month
for month, df_month in monthly_dfs.items():
    if not df.empty:
        month=datetime.date(1900, month, 1).strftime('%B')
        print(f"Data for {month} added")

        #Separate payments from data
        payments = df_month[df_month['Description'].str.contains("INTERNET PAYMENT", regex=True)].index
        df_payments = df.iloc[payments]
        df_month.drop(payments, inplace=True)

        #Reset the Indices
        df_month.reset_index(inplace=True, drop=True)
        df_payments.reset_index(inplace=True, drop=True)

        try:
            ws = sh.worksheet(f"{month}")
        except:
            sh.add_worksheet(f"{month}", rows="100", cols="10")
            ws = sh.worksheet(f"{month}")
        ws.clear()

        set_with_dataframe(ws, df_month)
        set_with_dataframe(ws, df_payments, col = 6)
        ws.format('A1:J1', {'textFormat': {'bold': True}})

        time.sleep(5)








