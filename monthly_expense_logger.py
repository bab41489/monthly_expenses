import pandas as pd
#create df from csv for cc only, not checking account
##this line will probably change so user can select multiple files or accounts
df = pd.read_csv('/Users/benjaminberger/Downloads/Chase5834_Activity20230807_20230906_20230918.CSV')
#rename columns
df=df.rename(columns = {
    'Transaction Date' : 'Date',
    'Description' : 'Vendor',
    'Memo': 'Account'
    })
#update account column from card column bc we're going to delete card column
df['Account'] = df['Card']
#remove unnecessary columns
df = df[['Date', 'Vendor', 'Category', 'Amount', 'Account']]

#delete rows out of date range
###change this to reflect the user input month!!
df = df[(df.Date >= '09/01/2023') & (df.Date <= '09/31/2023')]
#sort by date order
df = df.sort_values('Date').reset_index(drop=True)

#create new column and insert where I want it
df.insert(
    loc=2,
    column='Detail',
    value = None)

# print(df.Detail.isnull)
# print(df.head())

#remove card payments
df = df[df.Vendor != 'Payment Thank You-Mobile']
#convert amounts to positive numbers
df.Amount = abs(df.Amount)

print(df)
df_for_review = df.to_csv('/Users/benjaminberger/Downloads/bencsvtest.CSV', index=False)
