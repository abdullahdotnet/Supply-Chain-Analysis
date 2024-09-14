import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import summary as sm
import customer as cs
import preprocessor as pr
import market as mr
import product as pd
import order as od

df = pr.preprocess()

st.sidebar.title('Supply Chain Analysis')

usermenu = st.sidebar.radio('Filters',('Summary','Customer','Market','Order','Product'))

if usermenu == 'Summary':
    sm.getSummary(df)
    
if usermenu == 'Customer':
    cs.get_segmentwise(df)
    cs.get_citywise(df)
    cs.get_countrywise(df)
    cs.get_Statewise(df)
    cs.categoryPreferenceSegmentWise(df)
    cs.get_segmentsales(df)
    

if usermenu == 'Market':
    mr.marketwisetrend(df)
    mr.get_marketsales(df)
    # mr.daywiseorder(df)
    #mr.mapforprofit(df)
    # pd.bestSellingProducts(df)
    # pd.bestSellingCategories(df)
    mr.marketduration(df)
    

if usermenu == 'Product':
    pd.bestSellingProducts(df)
    pd.bestSellingCategories(df)
    pd.bestProductMargins(df)
    pd.discountVsSales(df)
    # pd.producPriceProfit(df)
    pd.priceprofit(df)

if usermenu == 'Order':
    od.daywiseorder(df)
    od.shippingmode(df)
    od.averageshippingdelay(df)
    od.shipdurationdistribution(df)
    od.shipdurationbymode(df)