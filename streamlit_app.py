import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd
from transformers import pipeline

# Load the dataset
csv_file_path = 'https://raw.githubusercontent.com/Tizzy1279/Capstone_Project/refs/heads/main/sales_data.csv'
df = pd.read_csv(csv_file_path)
df['Date'] = pd.to_datetime(df['Date'])

# Define default periods
default_periods = {
    'Q1': ['01', '02', '03'],
    'Q2': ['04', '05', '06'],
    'Q3': ['07', '08', '09'],
    'Q4': ['10', '11', '12']
}

# Initialize session state for custom periods
if 'custom_periods' not in st.session_state:
    st.session_state.custom_periods = {}

# Combine default and custom periods
def get_all_periods():
    return {**default_periods, **st.session_state.custom_periods}

# Sales Performance Analysis Functions
def show_monthly_sales():
    monthly_sales = df.resample('M', on='Date')['Sales'].sum().reset_index()
    monthly_sales['YearMonth'] = monthly_sales['Date'].dt.strftime('%Y-%m')
    st.line_chart(monthly_sales.set_index('YearMonth')['Sales'])

def compare_periods(periods, years):
    all_periods = get_all_periods()
    if periods and years:
        results = []

        for year in years:
            year_data = df[df['Date'].dt.year == year]

            for period in periods:
                period_months = all_periods[period]
                period_data = year_data[year_data['Date'].dt.strftime('%m').isin(period_months)]

                if not period_data.empty:
                    results.append({
                        'Period': period,
                        'Year': year,
                        'Sales': period_data['Sales'].sum(),
                        'AvgSales': period_data['Sales'].mean()
                    })

        if results:
            results_df = pd.DataFrame(results)
            results_df['PeriodYear'] = results_df['Period'] + ' ' + results_df['Year'].astype(str)
            pivot_table = results_df.pivot(index='PeriodYear', columns='Year', values='Sales')
            st.bar_chart(pivot_table, use_container_width=True)
            st.write('Summary Statistics:', results_df.groupby('Period').agg({
                'Sales': ['sum', 'mean', 'count'],
                'AvgSales': 'mean'
            }).round(2))
    else:
        st.error('Please select at least one period and one year.')

# Product Analysis Functions
def show_product_sales():
    product_sales = df.groupby('Product')['Sales'].sum()
    st.bar_chart(product_sales)

def show_product_customer_age():
    product_age = df.groupby('Product')['Customer_Age'].mean()
    st.bar_chart(product_age)

def show_product_satisfaction():
    product_satisfaction = df.groupby('Product')['Customer_Satisfaction'].mean()
    st.bar_chart(product_satisfaction)

def show_product_gender_ratio():
    product_gender = df.groupby('Product')['Customer_Gender'].value_counts(normalize=True).unstack()
    st.bar_chart(product_gender)

# Regional Analysis Functions
def show_regional_sales():
    regional_sales = df.groupby('Region')['Sales'].sum()
    st.bar_chart(regional_sales)

def show_regional_customer_age():
    regional_age = df.groupby('Region')['Customer_Age'].mean()
    st.bar_chart(regional_age)

def show_regional_satisfaction():
    regional_satisfaction = df.groupby('Region')['Customer_Satisfaction'].mean()
    st.bar_chart(regional_satisfaction)

def show_regional_gender_ratio():
    regional_gender = df.groupby('Region')['Customer_Gender'].value_counts(normalize=True).unstack()
    st.bar_chart(regional_gender)

# Demographic Analysis Functions
def show_gender_analysis():
    gender_sales = df.groupby('Customer_Gender')['Sales'].sum()
    st.bar_chart(gender_sales)

def show_age_analysis():
    age_sales = df.groupby('Customer_Age')['Sales'].sum()
    st.bar_chart(age_sales)

def show_regional_demographics():
    regional_demographics = df.groupby('Region')['Customer_Gender'].value_counts(normalize=True).unstack()
    st.bar_chart(regional_demographics)

def show_regional_age_analysis():
    regional_age = df.groupby('Region')['Customer_Age'].mean()
    st.bar_chart(regional_age)

def show_satisfaction_correlation():
    satisfaction_correlation = df.corr()['Customer_Satisfaction'].sort_values(ascending=False)
    st.write(satisfaction_correlation)

def show_age_distribution():
    st.hist(df['Customer_Age'])

# Custom Period Creation
st.subheader('Create Custom Period')
new_period_name = st.text_input('New Period Name:')
month_options = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
selected_months = st.multiselect('Select Months for Custom Period', month_options)

if st.button('Add Custom Period'):
    if new_period_name and selected_months:
        st.session_state.custom_periods[new_period_name] = selected_months
        st.success(f'Added new period: {new_period_name}')
        # Update the periods selection widget
        all_periods = get_all_periods()
    else:
        st.error('Please enter a name and select months for the custom period.')

# Main Menu
menu = st.selectbox('Choose Analysis Category', ['Sales Performance', 'Product Analysis', 'Regional Analysis', 'Demographics', 'Ask a Question'])

if menu == 'Sales Performance':
    analysis = st.radio('Choose Analysis', ['Show me monthly sales', 'Compare periods'])
    if analysis == 'Show me monthly sales':
        show_monthly_sales()
    elif analysis == 'Compare periods':
        selected_periods = st.multiselect('Select Periods', list(get_all_periods().keys()))
        selected_years = st.multiselect('Select Years', df['Date'].dt.year.unique())
        compare_periods(selected_periods, selected_years)

elif menu == 'Product Analysis':
    analysis = st.radio('Choose Analysis', ['Show me product sales', 'Show me product customer age', 'Show me product satisfaction', 'Show me product gender ratio'])
    if analysis == 'Show me product sales':
        show_product_sales()
    elif analysis == 'Show me product customer age':
        show_product_customer_age()
    elif analysis == 'Show me product satisfaction':
        show_product_satisfaction()
    elif analysis == 'Show me product gender ratio':
        show_product_gender_ratio()

elif menu == 'Regional Analysis':
    analysis = st.radio('Choose Analysis', ['Show me regional sales', 'Show me regional customer age', 'Show me regional satisfaction', 'Show me regional gender ratio'])
    if analysis == 'Show me regional sales':
        show_regional_sales()
    elif analysis == 'Show me regional customer age':
        show_regional_customer_age()
    elif analysis == 'Show me regional satisfaction':
        show_regional_satisfaction()
    elif analysis == 'Show me regional gender ratio':
        show_regional_gender_ratio()

elif menu == 'Demographics':
    analysis = st.radio('Choose Analysis', ['Show me gender analysis', 'Show me age analysis', 'Show me regional demographics', 'Show me regional age analysis', 'Show me satisfaction correlation', 'Show me age distribution'])
    if analysis == 'Show me gender analysis':
        show_gender_analysis()
    elif analysis == 'Show me age analysis':
        show_age_analysis()
    elif analysis == 'Show me regional demographics':
        show_regional_demographics()
    elif analysis == 'Show me regional age analysis':
        show_regional_age_analysis()
    elif analysis == 'Show me satisfaction correlation':
        show_satisfaction_correlation()
    elif analysis == 'Show me age distribution':
        show_age_distribution()

elif menu == 'Ask a Question':
    st.subheader("What questions do you have about the data?")
    user_question = st.text_input("Ask your question here:")
    
    if user_question:
        # Initialize the question-answering pipeline
        qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

        # Convert the dataframe to a string context for the NLP model
        context = df.to_string()

        # Get the answer from the NLP model
        result = qa_pipeline(question=user_question, context=context)
        answer = result['answer']

        st.write(f"Answer: {answer}")
