import streamlit as st
import pandas as pd

import plotly.express as px


def daywiseorder(df):
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Day wise order counts
        </h2>""",unsafe_allow_html=True)
    
    
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

        fig = px.bar(orderdaywise, x='Day', y='No. of Orders')
        st.plotly_chart(fig)

    else:
        st.table(orderdaywise)
    st.write("Number of Orders increase as the weekend approaches.")


def shippingmode(df):
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Order Status by Shipping Modes
        </h2>""",unsafe_allow_html=True)
    shippingmode = df.groupby(['order_status','shipping_mode'])['order_id'].count().reset_index()
    shippingmode.rename(columns = {'order_status':'Status','shipping_mode':'Shipping Mode','order_id':'Count'},inplace=True)

    
    show_plot = st.checkbox('Show Table')

    if not show_plot:
        fig = px.bar(shippingmode, x='Status', y='Count',color = 'Shipping Mode'
                    #  , title='Status by Shipping Mode'
                     )
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

    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Average Shipping Duration by Shipping Mode
        </h2>""",unsafe_allow_html=True)

    # Custom CSS for consistent card styling
    st.markdown("""
        <style>
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

    # Display the cards in rows of 2
    with st.container():
        cols = st.columns(2)  # Create 2 columns per row
        
        # Loop through each shipping mode and display it as a card
        for index, row in average_duration.iterrows():
            shipping_mode = row['shipping_mode']
            avg_duration = row['shipping_duration']
            
            # Determine which column to place the card in
            col_index = index % 2
            
            # Place the card in the appropriate column
            with cols[col_index]:
                st.markdown(
                    f"""
                    <div class="small-card">
                        <h3>{shipping_mode}</h3>
                        <p style="font-size:24px; font-weight:bold; color: #636efa;">{avg_duration:.2f} days</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

            # Create new columns for every new row after two cards
            if (index + 1) % 2 == 0:
                cols = st.columns(2)
def shipdurationdistribution(df):

    # st.title('Ship Duration Distribution')
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Shipping Duration Distribution
        </h2>""",unsafe_allow_html=True)
    st.write("Most of the orders are taking 8 to 10 days to deliver.")

    fig = px.histogram(df, x='shipping_duration', nbins=6, 
                #    title='Shipping Duration Distribution',
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
    st.markdown(""" <h2 style="font-size: 32px; font-weight: bold; color: #31333f;">
            Shipping Duration by Shipping Mode
        </h2>""",unsafe_allow_html=True)
    st.write("First and Second class are delivering orders in time. While Same Day is facing some issues and showing exceptions in delivery time.")
    fig = px.box(df, x='shipping_mode', y='shipping_duration',
            #  title='Shipping Duration by Shipping Mode',
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


