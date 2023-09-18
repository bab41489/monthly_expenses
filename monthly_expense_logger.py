import pandas as pd
import os
import datetime

#detect files
month=str(input('Enter month: ') or 'unentered month')
folder = str(input('Enter folder directory: '))
os.chdir(folder)
calendar_dict = {
    '01': 'january',
    '02': 'february',
    '03': 'march',
    '04': 'april',
    '05': 'may',
    '06': 'june',
    '07': 'july',
    '08': 'august',
    '09': 'september',
    '10': 'october',
    '11': 'november',
    '12': 'december'
}
year = str(datetime.datetime.now())[:4]
df_for_review=pd.DataFrame(columns=['Date', 'Vendor', 'Detail', 'Category', 'Amount', 'Account'])
frames=[]

def convert_checking_acct(df):
    df=df.rename(columns = {
         'Details' : 'Date',
         'Posting Date': 'Vendor',
         'Description' : 'Amount',
         'Amount': 'Type',
         'Type': 'Balance'
        })

    df=df[['Date', 'Vendor', 'Amount', 'Type']]

    df.insert(
                loc=2,
                column='Detail',
                value = None)
    df.insert(
                loc=3,
                column='Category',
                value = None)
    df.insert(
                loc=6,
                column='Account',
                value = None)

    df=df[(df.Type=='ACH_DEBIT')]
    df=df[~(df.Vendor.str.contains('ORIG CO NAME:SCHWAB BROKERAGE'))]
    df=df.drop(['Type'], axis=1)
    df.Account=file[5:9]
    return df
    

def log_statement(file):

#create df from csv for cc only, not checking account
##this line will probably change so user can select multiple files or accounts
    df = pd.read_csv(f'{folder}/{file}')
#for checking accounts
    if len(df.columns)==7:
        df = convert_checking_acct(df)
    

#for credit cards
    if len(df.columns)==8:
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
 

        #create new column and insert it at index 2
        df.insert(
            loc=2,
            column='Detail',
            value = None)

        #remove card payments
        df = df[df.Vendor != 'Payment Thank You-Mobile']
    #convert amounts to positive numbers
    df.Amount = abs(df.Amount)
   #delete rows out of date range
    for k,v in calendar_dict.items():
        if month.lower() in v:
            df=df[(df.Date.str.contains(year)) & ((df.Date >= f'{k}/01/{year}') & (df.Date <= f'{k}/31/{year}'))]
            # df = df[(df.Date >= f'{k}/01/{year}') & (df.Date <= f'{k}/31/{year}') & (df.Date[-4:]==year)]
            # df=df[df.Date==k]
    #sort by date order PER ACCOUNT
    # df = df.sort_values('Date').reset_index(drop=True)
    return df

# result_path = os.mkdir(f'/Users/benjaminberger/Downloads/sept result')

for file in os.listdir(folder):
    print(file)
    if file[-4:]=='.CSV':
        current_df = log_statement(file)
        frames.append(current_df)
        print(current_df)
        df_for_review = pd.concat(frames)
#sort by date
df_for_review = df_for_review.sort_values('Date').reset_index(drop=True)
print(df_for_review)
df_for_review.to_csv(f'/Users/benjaminberger/Downloads/{month} result.CSV',\
    index=False)
