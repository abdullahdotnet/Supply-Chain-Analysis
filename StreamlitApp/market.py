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
    st.title('Market wise Sales and Profit')
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

    st.title('Market-Wise Monthly Sales')

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
        title='Market-Wise Monthly Sales',
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

