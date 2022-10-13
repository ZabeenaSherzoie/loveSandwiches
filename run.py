import gspread
from google.oauth2.service_account import Credentials
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
    """
    print('Please enter the data for the last market.')
    print('Data should be six numbers, separated by commas')
    print('Example: 50,60,70,80,90,100 \n')
    data_str = input('Enter your data here: ')
    sales_data = data_str.split(',')
    validate_data(sales_data)

def validate_data(values):
    """
    Inside the try, converts all string values to integer.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exact 6 values
    """
    num=[]
    try:
        if len(values) !=6 :
            raise ValueError(
                f"Exactly needed 6 values, you entered {len(values)} items"
            )
    except ValueError as e:
        print(f'Invalid data: {e} please try again.\n')

get_sales_data()