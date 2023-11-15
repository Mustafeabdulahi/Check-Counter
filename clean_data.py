  # Adjusting the function to better suit the data in the Excel file
import pandas as pd
import streamlit as st


def process_file(file):
    # Assuming the Excel has 'Employee' and 'Check Count' columns
    df = pd.read_excel(file)
    # """
    # Adjusted function to clean and filter the df and include 'Employee ID' and 'Employee Name':
    # - 'Check #' is filtered for values that are numeric and at least five digits
    # - 'Regular' is filtered to contain only numeric values
    # - New columns 'Employee ID' and 'Employee Name' are created based on the pattern in the data
    # - Removes rows with NaN values in 'Check #', 'Regular', 'Employee ID', and 'Employee Name'
    # """

    # Function to check if a value is a string
    def is_string(value):
        return isinstance(value, str)

    # Adjusting 'Check #' to handle string representations of numbers
    df['Check #'] = pd.to_numeric(df['Check #'], errors='coerce')
    # Wrap the operation in a try-except block

    # Creating 'Employee ID' and 'Employee Name' columns based on observed pattern in the data
    current_employee_id = None
    current_employee_name = None

    for index, row in df.iterrows():
        if is_string(row['Regular']):
            current_employee_id = row['Check #']
            current_employee_name = row['Regular']

        df.at[index, 'Employee ID'] = current_employee_id
        df.at[index, 'Employee Name'] = current_employee_name

    # Filtering 'Check #' to only contain values that are at least five-digit numbers
    df_filtered = df[df['Check #'] >= 10000]

    # Ensuring 'Regular' only contains numeric values
    df_filtered['Regular'] = df_filtered['Regular'].apply(lambda x: x if isinstance(x, int) else None)


    # Removing rows with NaN values in the relevant columns
    df_cleaned = df_filtered.dropna(subset=['Check #', 'Regular', 'Employee ID', 'Employee Name'])
    columns_to_drop = ['Premium', 'Regular.1', 'Premium.1', 'Amount','Local \nW/H']

    df_cleaned = df_cleaned.dropna(axis=1, how='all').drop(columns=columns_to_drop)
    df_cleaned.rename(columns={'Unnamed: 20': 'Withholding Taxes'}, inplace=True)

    df_cleaned['Employee ID'] = df_cleaned['Employee ID'].astype(int, errors='ignore')
    df_cleaned['Check #'] = df_cleaned['Check #'].astype(int, errors='ignore')


    rename_dict = {
    'Unnamed: 20': 'Taxes WH',
    'Check #': 'Check Number',
    'Regular': 'Hours Worked',
    'FICA-\nMED': 'FICA-MED',
    'State \nW/H': 'State WH',
    }
    df_cleaned.rename(columns=rename_dict, inplace=True)
    df_cleaned.reset_index(drop=True, inplace=True)

    column_order = [
        'Date','Beg Date',	'End Date','Check Number',
        'Employee ID',	'Employee Name','Hours Worked',
        'Gross',	'FICA-SS',	'FICA-MED','Withholding Taxes',
        'State WH',	'Net Pay'
    ]

    df_cleaned = df_cleaned[column_order]


        # Convert 'Date' to datetime and count checks in October
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], format='%m/%d/%y')
    filtered_month = df_cleaned[df_cleaned['Date'].dt.month == 10]
    check_count = filtered_month.groupby('Employee ID').size().reset_index(name='Check Count')

    # Merge the count back into the original DataFrame and fill NaN with 0
    df_final = df_cleaned.merge(check_count, on='Employee ID', how='left')
    df_final['Check Count'] = df_final['Check Count'].fillna(0).astype(int)

    df_final = df_final.set_index('Date')

    # df_greater = df[df['Check Count'] > check_count_greater]
    # df_less_equal = df[df['Check Count'] < check_count_less_equal]


    return df_final 
