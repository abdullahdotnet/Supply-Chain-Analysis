import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np



def bestSellingProducts(df):
    # st.title('Best Selling Products')
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Best Selling Products
        </h2>""",unsafe_allow_html=True)

    bestsellingproducts = df.groupby('product_name')['sales'].sum().reset_index().sort_values(by='sales',ascending=False).head(10)
    bestsellingproducts.rename(columns = {'product_name':'Product','sales':"Total Sales"},inplace=True)
    show_plot_9 = st.checkbox('Show Table  ')

    if show_plot_9 == False:
        fig_horizontal_bar = px.bar(bestsellingproducts, 
                           x='Total Sales', 
                           y='Product', 
                        #    title='Best selling products',
                           orientation='h')
        st.plotly_chart(fig_horizontal_bar)
    else:
        st.table(bestsellingproducts)

def bestSellingCategories(df):
    # st.title('Best Selling Categories')
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Best Selling Product Categories
        </h2>""",unsafe_allow_html=True)
    bestsellingcategories = df.groupby(['category_name', 'product_name'])['sales'].sum().reset_index().sort_values(by='sales',ascending=False)
    top_categories = bestsellingcategories.groupby('category_name')['sales'].sum().reset_index().sort_values(by='sales', ascending=False).head(10)['category_name']
    bestsellingcategories = bestsellingcategories[bestsellingcategories['category_name'].isin(top_categories)]
    bestsellingcategories.rename(columns={'category_name': 'Category', 'sales': 'Total Sales','product_name':"Product"}, inplace=True)
    show_plot_9 = st.checkbox('Show Table   ')
    if show_plot_9 == False:
        fig_horizontal_bar = px.bar(bestsellingcategories, 
                            x='Total Sales', 
                            y='Category',
                            color= 'Product',
                            # title='Best selling categories',
                            orientation='h')
        #fig_horizontal_bar.update_layout(xaxis_type='log')
        st.plotly_chart(fig_horizontal_bar)
    else:
        st.table(bestsellingcategories.head(10))

def bestProductMargins(df):
    # st.title('Best Product Margins')
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Best Products by Profit Margin
        </h2>""",unsafe_allow_html=True)
    # Calculate order item profit
    df['order_item_profit'] = df['order_item_profit_ratio'] * df['sales']
    bestproductmargins = df.groupby('product_name')['order_item_profit'].mean().reset_index().sort_values(by='order_item_profit', ascending=False).head(7)
    bestproductmargins.rename(columns={'product_name': 'Product', 'order_item_profit': "Profit Margin"}, inplace=True)
    show_plot_10 = st.checkbox('Show Table')
    if show_plot_10 == False:
        # Create a bubble chart instead of a bar chart
        fig_bubble = px.scatter(bestproductmargins, 
                                x='Product', 
                                y='Profit Margin', 
                                size='Profit Margin',  # Use Profit Margin to determine the bubble size
                                color='Product',       # Different colors for each product
                                # title='Top 5 Product Margins',
                                hover_name='Product', 
                                size_max=60)           # Maximum size of the bubbles
        # Hide x-axis labels
        fig_bubble.update_layout(xaxis=dict(showticklabels=False))
        st.plotly_chart(fig_bubble)
    else:
        st.table(bestproductmargins)


def categorize_discount_rate(df):
    # Define the bins and corresponding labels (based on 2.5% intervals)
    bins = [-float('inf'), 0, 0.025, 0.05, 0.075, 0.10, 0.125, 0.15, 0.175, 0.20, 0.225, 0.25, float('inf')]
    labels = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, '25+']

    # Create a new column with the categorized discount rate based on 2.5% intervals
    df['discount_category'] = pd.cut(df['order_item_discount_rate'], 
                                     bins=bins, 
                                     labels=labels, 
                                     right=False)  # right=False means the intervals are [)

    return df

def discountVsSales(df):
    # st.title("Discount Sales Trend")
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Discount Sales Trend
        </h2>""",unsafe_allow_html=True)
    st.write("There seems to be no clear relationship between discount rate and sales volume.")
    df = categorize_discount_rate(df)
    df = df.groupby('discount_category')['order_item_discount_rate'].count().reset_index()
    df.rename(columns={'discount_category': 'Discount Rate (%)','order_item_discount_rate': "No. of Orders"}, inplace=True)
    fig_line = px.line(df, 
                       x='Discount Rate (%)', 
                       y="No. of Orders", 
                    #    title='Count of Orders by Discount Category',
                       markers=True)  # markers=True to show points on the line
    
    st.plotly_chart(fig_line)

# def producPriceProfit(df):
#     st.title('Product Price vs Profit')
#     df = df[['order_profit_per_order','product_price']]
#     df = df[df['order_profit_per_order'] > 0]

#     # Create a scatter plot with Plotly
#     fig_scatter = px.scatter(df, 
#                              x='product_price', 
#                              y='order_profit_per_order', 
#                              title='Order Profit per Order vs Product Price',
#                              labels={'product_price': 'Product Price', 'order_profit_per_order': 'Order Profit per Order'},
#                             #  size='order_profit_per_order',  # Optional: Bubble size based on order profit
#                             #  color='product_price',          # Optional: Color based on product price
#                              hover_name='product_price')      # Tooltip will show product price

#     # Display the plot in the Streamlit app
#     st.plotly_chart(fig_scatter)



def priceprofit(df):
    correlation = df['product_price'].corr(df['product_profit'])

    # st.title("Correlation Analysis")
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Product Price VS Profit
        </h2>""",unsafe_allow_html=True)


    st.markdown(
        f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px; text-align:center;">
            <h3 style="color:#333;">Correlation Coefficient</h3>
            <p style="font-size:36px; font-weight:bold; color: #636efa;">{correlation:.2f}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.subheader("Scatter Plot of Product Price vs Order Profit")
    st.write("Ther is significant positive correlation between Product Price and Order Profit.")


    fig = px.scatter(df, x='product_price', y='product_profit', 
                    title='Price vs Profit',
                     labels={'product_price': 'Product Price', 'product_profit': 'Order Profit'},
                     template="plotly_white",
                     )
    
    # Customize the layout for better readability
    fig.update_layout(
        title={'x': 0.5},  # Center the title
        xaxis_title='Product Price',
        yaxis_title='Order Profit per Order',
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )

    st.plotly_chart(fig)