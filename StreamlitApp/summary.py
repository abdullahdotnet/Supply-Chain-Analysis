import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def getSummary(df):
    st.title('Summary Analysis (Order wise)')
    payment_count = df['payment_type'].value_counts()
    fig = go.Figure([go.Bar(x=payment_count.index, y=payment_count.values)])
    fig.update_layout(title='Payment Type Count', xaxis_title='Payment Type', yaxis_title='Count')
    st.plotly_chart(fig)


    market_count = df['market'].value_counts()
    fig = go.Figure([go.Pie(labels=market_count.index, values=market_count.values)])
    fig.update_layout(
    title='Markets')
    st.plotly_chart(fig)


    category_count = df['category_name'].value_counts().head(10)
    fig = go.Figure([go.Bar(x=category_count.index, y=category_count.values)])
    fig.update_layout(title='Top Product Categories', xaxis_title='Category', yaxis_title='Count')
    st.plotly_chart(fig)
