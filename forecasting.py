import streamlit as st
import pandas as pd
import random  # Import the random module

def main():
    st.title("P&L Report - Forecasting")

    st.info("**Parameters to adjust:**")
    
    st.markdown("**Basic:**")
    with st.container(border=False):
        with st.container():
            col1, col2 = st.columns(2)  # Create two columns        
            with col1:
                with st.container(border=True):
                    st.slider("**Exchange Rate (USD/CNY)**", min_value=5.0, max_value=10.0, value=7.09, format='%f')            
            with col2:
                with st.container(border=True):
                    st.slider("**Expense**", min_value=0.0, max_value=10000.0, value=6666.88, format='%f')


    st.markdown("**HC number:**")
    with st.container(border=True):
        with st.container():
            col1, col2 = st.columns(2)  # Create two columns        
            with col1:
                with st.container(border=True):
                    st.slider("**HC number (BJ)**", value=18, format='%d')            
            with col2:
                with st.container(border=True):
                    st.slider("**HC number (GZ)**", value=56, format='%d')
        with st.container():
            col1, col2 = st.columns(2)  # Create two columns        
            with col1:
                with st.container(border=True):
                    st.slider("**HC number (CD)**", value=32, format='%d')            
            with col2:
                with st.container(border=True):
                    st.slider("**HC number (MY)**", value=6, format='%d')


    st.button("**Click to calculate**")

    st.info("**Forecast Result:**")
    # Create a sample DataFrame with 12 columns (Jan to Dec) plus MTD and YTD
    data_df = pd.DataFrame({
        'Jan': [random.randint(10, 2000) for _ in range(10)],
        'Feb': [random.randint(10, 2000) for _ in range(10)],
        'Mar': [random.randint(10, 2000) for _ in range(10)],
        'Apr': [random.randint(10, 2000) for _ in range(10)],
        'May': [random.randint(10, 2000) for _ in range(10)],
        'Jun': [random.randint(10, 2000) for _ in range(10)],
        'Jul': [random.randint(10, 2000) for _ in range(10)],
        'Aug': [random.randint(10, 2000) for _ in range(10)],
        'Sep': [random.randint(10, 2000) for _ in range(10)],
        'Oct': [random.randint(10, 2000) for _ in range(10)],
        'Nov': [random.randint(10, 2000) for _ in range(10)],
        'Dec': [random.randint(10, 2000) for _ in range(10)],
        'MTD': [random.randint(10, 2000) for _ in range(10)],
        'YTD': [random.randint(10, 2000) for _ in range(10)]
    }, index=['Income1', 'Income2', 'Income Total', 'Expense 1', 'Expense 2', 
               'Expense 3', 'Expense 4', 'Expense 5', 'Expense 6', 'Expense 7'])  # Set row names

    # Apply conditional formatting to the DataFrame for columns from 4 to end
    styled_df = data_df.style.applymap(lambda x: 'color: red' if x > 1000 else '', 
                                        subset=data_df.columns[3:])  # Apply to columns from 4 to end
    st.dataframe(styled_df)

if __name__ == "__main__":
    main()