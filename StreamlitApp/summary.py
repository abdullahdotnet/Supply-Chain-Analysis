import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def getSummary(df):
    st.title('Summary Analysis (Order wise)')
    # payment_count = df['payment_type'].value_counts()
    # fig = go.Figure([go.Bar(x=payment_count.index, y=payment_count.values)])
    # fig.update_layout(title='Payment Type Count', xaxis_title='Payment Type', yaxis_title='Count')
    # st.plotly_chart(fig)


    market_count = df['market'].value_counts()
    fig = go.Figure([go.Pie(labels=market_count.index, values=market_count.values)])
    fig.update_layout(
    title='Markets')
    st.plotly_chart(fig)


    category_count = df['category_name'].value_counts().head(10)
    fig = go.Figure([go.Bar(x=category_count.index, y=category_count.values)])
    fig.update_layout(title='Top Product Categories', xaxis_title='Category', yaxis_title='Count')
    st.plotly_chart(fig)



def overallcards(df):
    st.title("Business Overview Dashboard")
    st.header("Key Metrics Summary")
    totalcustomers = len(df['customer_id'].unique())
    totalorders = len(df)
    totalsales = df['sales'].sum() / 1_000_000  # Convert to millions
    totalprofit = df['order_profit_per_order'].sum() / 1_000  # Convert to millions
    totalmarkets = len(df['market'].unique())
    totalproducts = len(df['product_name'].unique())

# Display cards in Streamlit, 3 cards per row
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
                    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px; text-align:center; box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);">
                        <h3 style="color:#333;">{title}</h3>
                        <p style="font-size:24px; font-weight:bold; color:#2196f3;">{value}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

    st.subheader("Order Status Count")
    order_status_count = df['order_status'].value_counts().reset_index()
    fig = px.bar(order_status_count, x='count', y='order_status', title='Order Status Count')
    st.plotly_chart(fig)

    st.subheader("Sales Trend Over Time")
    df['order_date'] = pd.to_datetime(df['order_date'])
    sales_trend = df.groupby('order_date')['sales'].sum().reset_index()
    fig = px.line(sales_trend, x='order_date', y='sales', title='Sales Trend Over Time')
    st.plotly_chart(fig)

    # st.subheader("Sales by Customer City")
    # fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='sales', hover_name='order_city',
    #                     size='sales', projection='natural earth', title='Sales by Customer City')
    # st.plotly_chart(fig)

    st.subheader("Product Price by Shipping Mode")
    fig = px.box(df, x='shipping_mode', y='order_item_product_price', title='Product Price by Shipping Mode')
    st.plotly_chart(fig)

    st.subheader("Payment Type Distribution")

    payment_type_count = df['payment_type'].value_counts().reset_index()
    fig = px.pie(payment_type_count, values='count', names='payment_type', title='Payment Type Distribution')
    st.plotly_chart(fig)

