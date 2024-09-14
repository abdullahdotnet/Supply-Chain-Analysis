import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def getSummary(df):
    # st.title('Summary Analysis (Order wise)')
    # payment_count = df['payment_type'].value_counts()
    # fig = go.Figure([go.Bar(x=payment_count.index, y=payment_count.values)])
    # fig.update_layout(title='Payment Type Count', xaxis_title='Payment Type', yaxis_title='Count')
    # st.plotly_chart(fig)

    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Marketwise Orders Distribution
        </h2>""",unsafe_allow_html=True)
    market_count = df['market'].value_counts()
    fig = go.Figure([go.Pie(labels=market_count.index, values=market_count.values)])
    fig.update_layout()
    st.plotly_chart(fig)

    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Top Product Categories by Orders
        </h2>""",unsafe_allow_html=True)
    category_count = df['category_name'].value_counts().head(10)
    fig = go.Figure([go.Bar(x=category_count.index, y=category_count.values)])
    fig.update_layout(xaxis_title='Category', yaxis_title='Count')
    st.plotly_chart(fig)



def overallcards(df):
    st.write("")
    st.title("Business Overview Dashboard")

    st.markdown(""" <h2 style="font-size: 34px; font-weight: bold; color: #31333f;">
            Key Metrics Summary
        </h2>""",unsafe_allow_html=True)
    totalcustomers = len(df['customer_id'].unique())
    totalorders = len(df)
    totalsales = df['sales'].sum() / 1_000_000  # Convert to millions
    totalprofit = df['order_profit_per_order'].sum() / 1_000
    totalmarkets = len(df['market'].unique())
    totalproducts = len(df['product_name'].unique())

    variables = [
        ("Customers", totalcustomers),
        ("Orders", totalorders),
        ("Sales", f"${totalsales:.2f}M"),  # Format sales in millions
        ("Profit", f"${totalprofit:.2f}K"),  # Format profit in millions
        ("Markets", totalmarkets),
        ("Products", totalproducts)
    ]

    # Create rows of cards with 3 cards per row
    for i in range(0, len(variables), 3):
        cols = st.columns(3)  # Create a row with 3 columns
        for j in range(3):
            if i + j < len(variables):
                title, value = variables[i + j]
                
                # Add card to the current column
                cols[j].markdown(
                    f"""
                    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px; text-align:center; box-shadow: 1px 1px 8px rgba(0, 0, 0, 0.3);">
                        <h3 style="color:#333;">{title}</h3>
                        <p style="font-size:24px; font-weight:bold; color:#2196f3;">{value}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )




    # st.subheader("Sales by Customer City")
    # fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='sales', hover_name='order_city',
    #                     size='sales', projection='natural earth', title='Sales by Customer City')
    # st.plotly_chart(fig)

    



def orderStatusCount(df):
    st.write("")
    st.write("")
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Order Status Count
        </h2>""",unsafe_allow_html=True)
    order_status_count = df['order_status'].value_counts().reset_index()
    fig = px.bar(order_status_count, x='count', y='order_status')
    st.plotly_chart(fig)

def salesTrend(df):
    st.write("")
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Sales Trend Over Time
        </h2>""",unsafe_allow_html=True)
    df['order_date'] = pd.to_datetime(df['order_date'])
    sales_trend = df.groupby('order_date')['sales'].sum().reset_index()
    fig = px.line(sales_trend, x='order_date', y='sales')
    st.plotly_chart(fig)

def productPriceByShippingMode(df):
    st.write("")
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Product Price by Shipping Mode
        </h2>""",unsafe_allow_html=True)
    fig = px.box(df, x='shipping_mode', y='order_item_product_price')
    st.plotly_chart(fig)

def paymentTypeDistribution(df):
    st.write("")
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Payment Type Distribution
        </h2>""",unsafe_allow_html=True)
    payment_type_count = df['payment_type'].value_counts().reset_index()
    fig = px.pie(payment_type_count, values='count', names='payment_type')
    st.plotly_chart(fig)