import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np




def format_sales(value):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.2f}M'
    else:
        return f'{value / 1_000:.2f}K'
    
def get_marketsales(df):
    salesmarket = df.groupby('market')[['sales','order_profit_per_order']].sum().reset_index().sort_values(by='sales',ascending=False)
    salesmarket.rename(columns={'market': 'Market','sales':"Total Sales",'order_profit_per_order':'Total Profit'},inplace=True)
    salesmarket['Total Sales ($)'] = salesmarket['Total Sales'].apply(format_sales)
    salesmarket['Total Profit ($)'] = salesmarket['Total Profit'].apply(format_sales)
    salesmarket['Profit Ratio (%)'] = round((salesmarket['Total Profit'] / salesmarket['Total Sales'])*100,2).astype(str)

    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: black;">
            Market wise Sales and Profit
        </h2>""",unsafe_allow_html=True)
    show_plot_4 = st.checkbox('Show Plot      ')

    if show_plot_4:
        fig = px.bar(salesmarket, x='Market', y=['Total Sales','Total Profit'], title='Total sales by Market')
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)
    else:
        salesmarket = salesmarket[['Market','Total Sales ($)','Total Profit ($)','Profit Ratio (%)']]
        st.table(salesmarket)

def mapforprofit(df):
    indextodrop = df[df['order_profit_per_order'] < 0 ].index
    df.drop(indextodrop,inplace=True)
    fig = px.choropleth(
    df,
    locations='order_country',           # Column for the country names
    locationmode='country names',        # The type of location, which is the country name
    color='order_profit_per_order',      # Column for coloring based on profit
    # color_continuous_scale='RdYlGn',     # Cyclic color scale from red to green
    labels={'order_profit_per_order': 'Profit Amount'},
    title='Profit Amount per Country'
)

# Update layout for a dark mode style
    fig.update_layout(
        geo=dict(
            bgcolor='white',                 # Background color of the map
            lakecolor='white',               # Color for lakes
            landcolor='white',               # Land color
            subunitcolor='white',            # Subunit boundaries color
            countrycolor='white'             # Country boundaries color
        ),
        paper_bgcolor='white',               # Background color of the entire plot
        plot_bgcolor='white'                 # Background color of the plotting area
    )
    st.plotly_chart(fig)



def marketwisetrend(df):
    df['order_period'] = df['order_date'].dt.to_period('M')
    df['order_period_str'] = df['order_period'].astype(str)

    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: black;">
            Market-Wise Monthly Sales
        </h2>""",unsafe_allow_html=True)

    market_list = list(df['market'].unique())
    market_list.insert(0, 'Overall')
    selected_market = st.selectbox('Select Market', options=market_list, index=0)

    update = df
    if selected_market == 'Europe':
        update = df[df['market'] == 'Europe']
    if selected_market == 'LATAM':
        update = df[df['market'] == 'LATAM']
    if selected_market == 'USCA':
        update = df[df['market'] == 'USCA']
    if selected_market == 'Africa':
        update = df[df['market'] == 'Africa']
    if selected_market == 'Pacific Asia':
        update = df[df['market'] == 'Pacific Asia']


    monthly_sales = update.groupby(['market', 'order_period_str'])['sales'].sum().reset_index()

    fig_line_plot = px.line(
        monthly_sales, 
        x='order_period_str',               # Use the string format of 'order_period'
        y='sales', 
        color='market',                     # Different lines for each market
        # title='Market-Wise Monthly Sales',
        labels={'sales': 'Total Sales', 'order_period_str': 'Month-Year'},
        markers=True                        # Display markers for each data point
    )

    # Update the layout to show month names properly
    fig_line_plot.update_layout(
        xaxis_title="Month-Year",
        yaxis_title="Sales",
        xaxis=dict(tickformat="%b %Y"),     # Format X-axis to show Month and Year
        hovermode='x unified',              # Unified hover mode for clearer comparison
    )

    # Display the plot using Streamlit
    st.plotly_chart(fig_line_plot)

def marketduration(df):
    marketwiseduration = df.groupby('market')['shipping_duration'].mean().reset_index()
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: black;">
            Average Shipping Duration by Market
        </h2>""",unsafe_allow_html=True)

# # Loop through each market and display a card for each
#     if not marketwiseduration.empty:
#         first_row = marketwiseduration.iloc[0]
#         st.markdown(
#             f"""
#             <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px; text-align:center; box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);">
#                 <h3 style="color:#333;">{first_row['market']}</h3>
#                 <p style="font-size:24px; font-weight:bold; color:#2196f3;">{first_row['shipping_duration']:.2f} days</p>
#                 <p style="color:#555;">Average Shipping Duration</p>
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )

# # Display the remaining cards in rows of 2
#     remaining_rows = marketwiseduration.iloc[1:]

#     for i in range(0, len(remaining_rows), 2):
#         cols = st.columns(2)  # Create a row with 2 columns
#         for j in range(2):
#             if i + j < len(remaining_rows):
#                 row = remaining_rows.iloc[i + j]
#                 market = row['market']
#                 avg_duration = row['shipping_duration']
                
#                 # Add card to the current column
#                 cols[j].markdown(
#                     f"""
#                     <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px; text-align:center; box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);">
#                         <h3 style="color:#333;">{market}</h3>
#                         <p style="font-size:24px; font-weight:bold; color:#2196f3;">{avg_duration:.2f} days</p>
#                         <p style="color:#555;">Average Shipping Duration</p>
#                     </div>
#                     """, 
#                     unsafe_allow_html=True
#                 )
    # Custom CSS for larger centered card
    st.markdown("""
        <style>
        .big-card {
            background-color:#f0f2f6; 
            padding: 30px; 
            border-radius: 15px; 
            margin-bottom: 20px; 
            text-align:center; 
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        }
        .small-card {
            background-color:#f0f2f6; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 20px; 
            text-align:center; 
            box-shadow: 1px 1px 8px rgba(0, 0, 0, 0.3);
        }
        </style>
        """, unsafe_allow_html=True)


    # First row with a single centered card (larger)
    col1, col2, col3 = st.columns([1, 2, 1])  # Middle column is bigger to center the card
    with col2:
        st.markdown(
            f"""
            <div class="big-card">
                <h3>{marketwiseduration.iloc[0]['market']}</h3>
                <p style="font-size:24px; font-weight:bold; color:#2196f3;">{marketwiseduration.iloc[0]['shipping_duration']:.2f} days</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Second and subsequent rows with two cards per row
    for i in range(1, len(marketwiseduration), 2):
        cols = st.columns(2)
        
        for j in range(2):
            if i + j < len(marketwiseduration):
                market = marketwiseduration.iloc[i + j]['market']
                duration = marketwiseduration.iloc[i + j]['shipping_duration']
                
                # Add the cards in smaller size
                with cols[j]:
                    st.markdown(
                        f"""
                        <div class="small-card">
                            <h3>{market}</h3>
                            <p style="font-size:20px; font-weight:bold; color:#2196f3;">{duration:.2f} days</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )