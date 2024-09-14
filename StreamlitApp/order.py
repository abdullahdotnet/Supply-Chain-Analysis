import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def daywiseorder(df):
    
    st.title('Weekday wise order')
    df['order_weekday'] = df['order_date'].dt.day_name()
    orderdaywise = df.groupby('order_weekday')['order_id'].count().reset_index()
    orderdaywise.rename( columns = {'order_id':'No. of Orders','order_weekday':'Day'},inplace = True)
    show_plot_12 = st.checkbox('Show Plot          ')



    if show_plot_12:
    #     fig_line_plot = px.line(
    #     orderdaywise, 
    #     x='Day',               # Use the string format of 'order_period'
    #     y='No. of Orders',                   # Different lines for each market
    #     title='Day wise order counts',
    #     markers=True                        # Display markers for each data point
    # )
    #     fig_line_plot.update_layout(
    #         xaxis_title="Day",
    #         yaxis_title="Order Count",
    #         hovermode='x unified',              # Unified hover mode for clearer comparison
    #     )
    #     st.plotly_chart(fig_line_plot)

        fig = px.bar(orderdaywise, x='Day', y='No. of Orders', title='Number of Orders by Day')
        st.plotly_chart(fig)

    else:
        
        st.table(orderdaywise)


def shippingmode(df):
    st.title('Order status')
    shippingmode = df.groupby(['order_status','shipping_mode'])['order_id'].count().reset_index()
    shippingmode.rename(columns = {'order_status':'Status','shipping_mode':'Shipping Mode','order_id':'Count'},inplace=True)

    
    show_plot = st.checkbox('Show Plot',value=True)

    if show_plot:
        fig = px.bar(shippingmode, x='Status', y='Count',color = 'Shipping Mode', title='Status by Shipping Mode')
        st.plotly_chart(fig)
    else:
        shippingmodelist = list(df['shipping_mode'].unique())
        shippingmodelist.insert(0, 'Overall')
        selected_mode = st.selectbox('Select Shipping Mode', options=shippingmodelist, index=0)

        statuslist = list(df['order_status'].unique())
        statuslist.insert(0, 'Overall')
        selected_status = st.selectbox('Select Order Status', options=statuslist, index=0)

        if selected_status!='Overall' and  selected_mode != 'Overall':
            shippingmode = shippingmode[(shippingmode['Shipping Mode'] == selected_mode) & (shippingmode['Status'] == selected_status)]
        elif selected_status != 'Overall' and selected_mode == 'Overall':
            shippingmode = shippingmode[shippingmode['Status'] == selected_status]
        elif selected_status == 'Overall' and selected_mode != 'Overall':
            shippingmode = shippingmode[shippingmode['Shipping Mode'] == selected_mode]
        elif selected_status == 'Overall' and selected_mode == 'Overall':
            shippingmode = shippingmode




        st.table(shippingmode)