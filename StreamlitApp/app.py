import streamlit as st
import pandas as pd
import summary as sm
import customer as cs
import preprocessor as pr
import market as mr
import product as pd
import order as od

# Applying Plotly theme
import plotly.io as pio
pio.templates.default = 'plotly_white'
# pio.templates.default =  'none'


df = pr.preprocess()

st.sidebar.title('Supply Chain Analysis')

usermenu = st.sidebar.radio('Sections',('Summary','Customer','Market','Order','Product'))

if usermenu == 'Summary':
    sm.overallcards(df)
    sm.orderStatusCount(df)
    sm.salesTrend(df)
    sm.productPriceByShippingMode(df)
    sm.getSummary(df)
    
    
if usermenu == 'Customer':
    st.title("Customers Analysis")
    cs.get_segmentwise(df)
    cs.get_citywise(df)
    cs.get_countrywise(df)
    cs.get_Statewise(df)
    cs.categoryPreferenceSegmentWise(df)
    cs.get_segmentsales(df)
    

if usermenu == 'Market':
    st.title("Market Analysis")
    mr.marketwisetrend(df)
    mr.get_marketsales(df)
    # mr.daywiseorder(df)
    # mr.mapforprofit(df)
    mr.marketduration(df)
    

if usermenu == 'Product':
    st.title("Product Analysis")
    pd.bestSellingProducts(df)
    pd.bestSellingCategories(df)
    pd.bestProductMargins(df)
    pd.discountVsSales(df)
    # pd.producPriceProfit(df)
    pd.priceprofit(df)

if usermenu == 'Order':
    st.title("Order Analysis")
    od.daywiseorder(df)
    od.shippingmode(df)
    od.averageshippingdelay(df)
    od.shipdurationdistribution(df)
    od.shipdurationbymode(df)