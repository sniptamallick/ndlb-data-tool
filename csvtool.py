#import relevant packages 

import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

#set titles
st.title('No Dem Left Behind Dashboard')

st.header('ActBlue Data Processing Tool', divider='rainbow')

#csv upload 
st.header('1. File Upload')
uploaded_file = st.file_uploader("Upload ActBlue Report (.csv only)")

#csv upload 
st.header('2. File Content Preview')
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

#subtask titles 
st.header('3. Download Processed Report Data')

st.subheader("[Optional]: Filter Donors by State")

states = st.multiselect(
    'Select State(s)',
    ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])

st.subheader("Aggregate Lifetime Donation Total and Counts")

#check for columns for one type of ActBlue Report 
if set(['DONATION_TOTAL','NUMBER_OF_DONATIONS']).issubset(dataframe.columns):
    
    #remove duplicates by first name, last name, and email and aggregate by DONATION_TOTAL and NUMBER_OF_DONATIONS 
    donation_counts = dataframe.groupby(['First Name', 'Last Name', 'Donor Email'])['DONATION_TOTAL'].agg('sum').reset_index()
    donation_totals = dataframe.groupby(['First Name', 'Last Name', 'Donor Email'])['NUMBER_OF_DONATIONS'].agg('sum').reset_index()

    #merge dataframes 
    merge_df = pd.merge(donation_counts, donation_totals,  how='left', left_on=['First Name', 'Last Name', 'Donor Email'], right_on = ['First Name', 'Last Name', 'Donor Email'])
    sort_df = merge_df.sort_values(['DONATION_TOTAL', 'NUMBER_OF_DONATIONS'], ascending = [False, False]).reset_index(drop=True)
    final_df = pd.merge(sort_df, dataframe,  how='left', left_on=['First Name', 'Last Name', 'Donor Email'], right_on = ['First Name', 'Last Name', 'Donor Email'])
    final_df = final_df.drop(['DONATION_TOTAL_y', 'NUMBER_OF_DONATIONS_y'], axis=1)

    #rename columns 
    final_df = final_df.rename(columns={"DONATION_TOTAL_x": "DONATION_TOTAL", "NUMBER_OF_DONATIONS_x": "NUMBER_OF_DONATIONS"})
    final_df = final_df.drop_duplicates(subset=['First Name', 'Last Name', 'Donor Email'])


elif set(['Amount', 'Donor First Name', 'Donor Last Name']).issubset(dataframe.columns):

    #remove duplicates by first name, last name, and email and aggregate by DONATION_TOTAL and NUMBER_OF_DONATIONS 
    donation_totals = dataframe.groupby(['Donor First Name', 'Donor Last Name', 'Donor Email'])['Amount'].agg('sum').reset_index()

    #merge dataframes 
    final_df = pd.merge(dataframe, donation_totals,  how='left', left_on=['Donor First Name', 'Donor Last Name', 'Donor Email'], right_on = ['Donor First Name', 'Donor Last Name', 'Donor Email'])

    #drop and rename columns 
    final_df = final_df.drop(['Amount_y'], axis=1)
    final_df = final_df.rename(columns={"Amount_x": "Amount"})
    final_df = final_df.sort_values(['Amount'], ascending = [False]).reset_index(drop=True)

elif set(['Donation Total', 'Donor First Name', 'Donor Last Name']).issubset(dataframe.columns):

    #remove duplicates by first name, last name, and email and aggregate by DONATION_TOTAL and NUMBER_OF_DONATIONS 
    donation_totals = dataframe.groupby(['Donor First Name', 'Donor Last Name', 'Donor Email'])['Donation Total'].agg('sum').reset_index()

    #merge dataframes 
    final_df = pd.merge(dataframe, donation_totals,  how='left', left_on=['Donor First Name', 'Donor Last Name', 'Donor Email'], right_on = ['Donor First Name', 'Donor Last Name', 'Donor Email']).reset_index(drop=True)

    #drop and rename columns 
    final_df = final_df.drop(['Donation Total_y'], axis=1)
    final_df = final_df.rename(columns={"Donation Total_x": "Donation_Total"})
    final_df = final_df.sort_values(['Donation_Total'], ascending = [False]).reset_index(drop=True)


#check for state filter
if states:  

    if set(['Donor State']).issubset(final_df.columns):
        new_dataframe = final_df[final_df['Donor State'].isin(states)]
        st.write(new_dataframe)
    
    elif set(['State']).issubset(final_df.columns): 
        new_dataframe = final_df[final_df['State'].isin(states)]
        st.write(new_dataframe)

    
else: 
    st.dataframe(final_df)


