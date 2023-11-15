import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from streamlit_extras.metric_cards import style_metric_cards
from clean_data import process_file

def load_data():
    file = st.sidebar.file_uploader("Upload Excel file", type=['xlsx'])
    if file:
        df = process_file(file)  # Assuming process_file is similar to this
        df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce').round(2)
        df['Check Number'] = df['Check Number'].astype(str)
        return df
    return None 


# Function to convert DataFrame to CSV and return it
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

new_df = load_data()

# Calculate Check month
today = datetime.now()
# Subtract one month from the current date
last_month_date = today - relativedelta(months=1)

last_month = last_month_date.strftime("%B")
months_list = list(calendar.month_name)[1:]  

# Find the index of the last month in months_list
last_month_index = months_list.index(last_month)

# creates the container for page title
dash_1 = st.container()

with dash_1:
    st.markdown("<h2 style='text-align: center;'>Essential Check Counter Dashboard</h2>", unsafe_allow_html=True)
    st.write("")

# Instructions
with st.expander("Instructions"):
    st.write("Upload an Excel file with the columns 'Employee' and 'Check Count'.")

# Sidebar options
st.sidebar.header("Options")
month = st.sidebar.selectbox("Select Month", months_list, index=last_month_index)
check_count_greater = st.sidebar.slider('Employees with check less than', 0, 9, 2)
check_count_less = st.sidebar.slider('Employees with checks less than', 0, 2, 2)



# Streamlit app
def main():
    # Check if data is loaded
    if new_df is not None:
        today = datetime.now()
        # Subtract one month from the current date
        last_month_date = today - relativedelta(months=1)

        last_month = last_month_date.strftime("%B")
        months_list = list(calendar.month_name)[1:]  

        # Find the index of the last month in months_list
        last_month_index = months_list.index(last_month)

        df_greater = new_df[new_df['Check Count'] > check_count_greater]
        df_less_equal = new_df[new_df['Check Count'] < check_count_less]   

        # Check if data is loaded
        if new_df is not None:
            # creates the container for metric card
            dash_2 = st.container()

            with dash_2:
                # get kpi metrics
                total_check_num = new_df['Check Number'].count()
                total_employees = new_df['Employee ID'].nunique()
                total_h_worked = new_df['Hours Worked'].sum()
                total_gross = new_df['Gross'].sum()

                col1, col2, col3, col4 = st.columns(4)
                col1.metric(label="Total Checks", value=total_check_num)
                col2.metric(label="Total Employees", value=total_employees)
                col3.metric(label="Hours Worked", value=total_h_worked)
                col4.metric(label="Total Gross", value=total_gross)  # Adjusted label

            # Style the metric card
            style_metric_cards(border_left_color="#DBF227")

        # Data display
        if st.checkbox('Show Data'):
            st.table(new_df.head())

        # Display tables one above the other
        st.subheader(f"Employees with more than {check_count_greater} Checks")
        st.table(df_greater)  # Use the full width of the page

        # Create CSV download link
        csv_greater = convert_df_to_csv(df_greater)
        st.download_button(
            label="Download data as CSV",
            data=csv_greater,
            file_name=f'employees_more_than_{check_count_greater}_checks.csv',
            mime='text/csv',
        )
        st.subheader(f"Employees with Less than {check_count_less} Checks")
        st.table(df_less_equal)  # Use the full width of the page

        # Create CSV download link
        csv_less_equal = convert_df_to_csv(df_less_equal)
        st.download_button(
            label="Download data as CSV",
            data=csv_less_equal,
            file_name=f'employees_less_than_{check_count_less}_checks.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()