import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS= CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid
    """
    while True:

        print('Please enter the data for the last market.')
        print('Data should be six numbers, separated by commas')
        print('Example: 50,60,70,80,90,100 \n')
        data_str = input('Enter your data here: ')
        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values to integer.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exact 6 values
    """
    
    try:
        [int(value) for value in values]
        if len(values) !=6 :
            raise ValueError(
                f"Exactly needed 6 values, you entered {len(values)} items"
            )
    except ValueError as e:
        print(f'Invalid data: {e} please try again.\n')
        return False
    return True


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each itme type.
    The surplus is defined as the sales figure subracted from the stock:
    -Positive surplus indicates waste
    -Negative surplus indicates extra made when stock has sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock,sales in zip(stock_row,sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def update_worksheet(data, worksheet):
    """
    update surplus worksheet, add new row with the list data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated succesfully.\n')
def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting the last 5
    entries for each sandwich and returns the data as a list of lists
    """
    sales = SHEET.worksheet('sales')
    
    columns =[]
    for int in range(1,7):
        column=sales.col_values(int)
        columns.append(column[-5:])
    return columns
def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding int
    """
    print('Calculating stock data...\n')
    new_stock_data = []
    for column in data:
        in_column = [int(num)for num in column]
        average = sum(in_column)/len(in_column)
        stock_num = average*1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data

def main():
    '''Run all program function'''
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,'sales')
    calculate_surplus_data(sales_data)
    new_surplus_data= calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data,'stock')
print('Welcome to Love Sandwiches Data Automation')    
main()

