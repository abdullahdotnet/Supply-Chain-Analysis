import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def daywiseorder(df):
    
    st.title('Weekday wise order')
    
    orderdaywise = df.groupby('order_weekday')['order_id'].count().reset_index()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Create a categorical type with the custom order
    orderdaywise['order_weekday'] = pd.Categorical(orderdaywise['order_weekday'], categories=weekday_order, ordered=True)

# Sort based on the custom order
    orderdaywise = orderdaywise.sort_values('order_weekday').reset_index(drop=True)

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

def averageshippingdelay(df):
    average_duration = df.groupby('shipping_mode')['shipping_duration'].mean().reset_index()
    st.title("Average Shipping Duration by Shipping Mode")

    with st.container():
        cols = st.columns(2)  # Create 2 columns

        # Loop through each shipping mode and display it as a card
        for index, row in average_duration.iterrows():
            shipping_mode = row['shipping_mode']
            avg_duration = row['shipping_duration']
            
            # Determine which column to place the card in
            col_index = index % 2
            with cols[col_index]:
                st.markdown(
                    f"""
                    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px;">
                        <h3 style="color:#333;">{shipping_mode}</h3>
                        <p style="font-size:24px; font-weight:bold; color:#4CAF50;">{avg_duration:.2f} days</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

def shipdurationdistribution(df):

    st.title('Ship Duration Distribution')
    fig = px.histogram(df, x='shipping_duration', nbins=6, 
                   title='Shipping Duration Distribution',
                   labels={'shipping_duration': 'Shipping Duration (days)'},
                   color_discrete_sequence=['skyblue'])

    fig.update_layout(
        xaxis_title='Shipping Duration (days)',
        yaxis_title='Frequency',
        bargap=0.2, 
        paper_bgcolor='white', 
        plot_bgcolor='white' 
    )

    st.plotly_chart(fig)


def shipdurationbymode(df):
    fig = px.box(df, x='shipping_mode', y='shipping_duration',
             title='Shipping Duration by Shipping Mode',
             labels={'shipping_duration': 'Shipping Duration (days)', 'shipping_mode': 'Shipping Mode'},
             color='shipping_mode')

# Customize the layout for better appearance
    fig.update_layout(
        xaxis_title='Shipping Mode',
        yaxis_title='Shipping Duration (days)',
        paper_bgcolor='white',  # Background color of the plot area
        plot_bgcolor='white'    # Background color of the plotting area
    )


    st.plotly_chart(fig)


