import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def get_citywise(df):

    city_wise_customer = df.groupby('order_city')['customer_id'].count().reset_index().sort_values(by='customer_id', ascending=False)
    city_wise_customer.rename(columns={'order_city': 'City', 'customer_id': 'No. of Customers'}, inplace=True)

    city_wise_customer.reset_index(drop=True, inplace=True)

   

    st.title('City wise Cutomers')
    show_plot = st.checkbox('Show Plot')


    if show_plot:
        page_size = 10
        total_pages = (len(city_wise_customer) // page_size) + 1

        page = st.selectbox('Select page    ', range(1, total_pages + 1))

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        fig = px.bar(city_wise_customer.iloc[start_idx:end_idx], x='City', y='No. of Customers', title='Number of Customers by City')
        # fig.update_layout(yaxis_type='log')
        st.plotly_chart(fig)

    else:
        city_list = list(df['customer_city'].unique())
        city_list.insert(0, 'Overall')
        selected_city = st.selectbox('Select City', options=city_list, index=0)

        if selected_city != 'Overall':
            city_wise_customer = city_wise_customer[city_wise_customer['City'] == selected_city]

        page_size = 10
        total_pages = (len(city_wise_customer) // page_size) + 1

        page = st.selectbox('Select page   ', range(1, total_pages + 1))

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        st.table(city_wise_customer.iloc[start_idx:end_idx])


def get_countrywise(df):

    country_wise_customer = df.groupby('order_country')['customer_id'].count().reset_index().sort_values(by='customer_id', ascending=False)
    country_wise_customer.rename(columns={'order_country': 'Country', 'customer_id': 'No. of Customers'}, inplace=True)

    country_wise_customer.reset_index(drop=True, inplace=True)

    country_list = list(df['customer_country'].unique())
    country_list.insert(0, 'Overall')

    st.title('Country wise Cutomers')
    show_plot_1 = st.checkbox('Show Plot ')


    if show_plot_1:
        # page_size = 10
        # total_pages = (len(country_wise_customer) // page_size) + 1

        # page = st.selectbox('Select page', range(1, total_pages + 1))

        # start_idx = (page - 1) * page_size
        # end_idx = start_idx + page_size


        top_countries = country_wise_customer.nlargest(18, 'No. of Customers')
        other_customers = country_wise_customer[~country_wise_customer['Country'].isin(top_countries['Country'])]['No. of Customers'].sum()
        other_df = pd.DataFrame({'Country': ['Other'], 'No. of Customers': [other_customers]})
        final_df = pd.concat([top_countries, other_df], ignore_index=True)
        final_df_sorted = final_df.sort_values(by='No. of Customers', ascending=True)

        # fig = px.pie(final_df, names='Country', values='No. of Customers', title='Number of Customers by Country')
        fig_horizontal_bar = px.bar(final_df_sorted, 
                           x='No. of Customers', 
                           y='Country', 
                           title='Number of Customers by Country (Top 18 + Other)',
                           orientation='h')

# Show the plot
        st.plotly_chart(fig_horizontal_bar)

    else:
        country_list = list(df['order_country'].unique())
        country_list.insert(0, 'Overall')
        selected_country = st.selectbox('Select Country', options=country_list, index=0)

        if selected_country != 'Overall':
            country_wise_customer = country_wise_customer[country_wise_customer['Country'] == selected_country]

        page_size = 10
        total_pages = (len(country_wise_customer) // page_size) + 1

        page = st.selectbox('Select page ', range(1, total_pages + 1))

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        st.table(country_wise_customer.iloc[start_idx:end_idx])



def get_Statewise(df):

    state_wise_customer = df.groupby('order_state')['customer_id'].count().reset_index().sort_values(by='customer_id', ascending=False)
    state_wise_customer.rename(columns={'order_state': 'State', 'customer_id': 'No. of Customers'}, inplace=True)

    state_wise_customer.reset_index(drop=True, inplace=True)

    State_list = list(df['customer_state'].unique())
    State_list.insert(0, 'Overall')

    st.title('State wise Cutomers')
    show_plot_1 = st.checkbox('Show Plot  ')


    if show_plot_1:
        page_size = 10
        total_pages = (len(state_wise_customer) // page_size) + 1

        page = st.selectbox('Select page', range(1, total_pages + 1))

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        fig = px.bar(state_wise_customer.iloc[start_idx:end_idx], x='State', y='No. of Customers', title='Number of Customers by State')
        st.plotly_chart(fig)

    else:
        state_list = list(df['customer_state'].unique())
        state_list.insert(0, 'Overall')
        selected_state = st.selectbox('Select State', options=state_list, index=0)

        if selected_state != 'Overall':
            state_wise_customer = state_wise_customer[state_wise_customer['State'] == selected_state]

        page_size = 10
        total_pages = (len(state_wise_customer) // page_size) + 1

        page = st.selectbox('Select page  ', range(1, total_pages + 1))

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        st.table(state_wise_customer.iloc[start_idx:end_idx])



def get_segmentwise(df):

    segment_wise_customer = df.groupby('customer_segment')['customer_id'].count().reset_index().sort_values(by='customer_id', ascending=False)
    segment_wise_customer.rename(columns={'customer_segment': 'Segment', 'customer_id': 'No. of Customers'}, inplace=True)

    segment_wise_customer.reset_index(drop=True, inplace=True)


    st.title('Segment wise Cutomers')
    show_plot_2 = st.checkbox('Show Plot    ',value=True)


    if show_plot_2:
        fig = px.pie(segment_wise_customer, names='Segment', values='No. of Customers', title='Number of Customers by Segment',hole=0.4)
        st.plotly_chart(fig)

    else:
        st.table(segment_wise_customer)


def format_sales(value):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.2f}M'
    else:
        return f'{value / 1_000:.2f}K'
    
def get_segmentsales(df):
    salessegment = df.groupby('customer_segment')[['sales','order_profit_per_order']].sum().reset_index().sort_values(by='sales',ascending=False)
    salessegment.rename(columns={'customer_segment': 'Segment','sales':"Total Sales",'order_profit_per_order':'Total Profit'},inplace=True)
    salessegment['Total Sales ($)'] = salessegment['Total Sales'].apply(format_sales)
    salessegment['Total Profit ($)'] = salessegment['Total Profit'].apply(format_sales)
    salessegment['Profit Ratio (%)'] = round((salessegment['Total Profit'] / salessegment['Total Sales'])*100,2).astype(str)
    st.title('Segment wise Sales and Profit')
    show_plot_3 = st.checkbox('Show Plot     ')

    if show_plot_3:
        fig = px.bar(salessegment, x='Segment', y=['Total Sales','Total Profit'], title='Total sales by segment')
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)
    else:
        salessegment = salessegment[['Segment','Total Sales ($)','Total Profit ($)','Profit Ratio (%)']]
        st.table(salessegment)

def categoryPreferenceSegmentWise(df):
    categorysegment = df.groupby(['customer_segment','category_name'])['order_id'].count().reset_index()
    categorysegment = categorysegment.rename(columns={'category_name':'Category','customer_segment':'Segment','order_id': 'Count'})
    df_sorted = categorysegment.sort_values('Count', ascending= False)
    top_5 = df_sorted.groupby('Segment').head(5)
    # fig = px.scatter(top_5, 
    #              x='Category', 
    #              y='Segment', 
    #              size='Count', 
    #              color='Segment', 
    #              title='Bubble Chart of Category Counts by Customer Segment', 
    #              size_max=60)
    # st.plotly_chart(fig)
    fig_treemap = px.treemap(top_5, 
                        path=['Segment', 'Category'], 
                        values='Count', 
                        title='Treemap of Top 5 Categories by Customer Segment')
    fig_treemap.update_traces(textinfo='label+text')

    # Show the plot
    st.plotly_chart(fig_treemap)

    # fig_grouped_bar = px.bar(top_5, 
    #                     x='Category', 
    #                     y='Count', 
    #                     color='Segment', 
    #                     barmode='group',
    #                     title='Top 5 Categories by Customer Segment (Grouped Bar Chart)')

    # # Show the plot
    # st.plotly_chart(fig_grouped_bar)

    # fig_stacked_bar = px.bar(top_5, 
    #                     x='Segment', 
    #                     y='Count', 
    #                     color='Category', 
    #                     title='Top 5 Categories by Customer Segment (Stacked Bar Chart)',
    #                     barmode='stack')

    # # Show the plot
    # st.plotly_chart(fig_stacked_bar)


