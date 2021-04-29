import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import base64

with st.sidebar.header('Welcome！ o(*￣▽￣*)ブ'):
    symbol = st.sidebar.text_input('Enter tickers', "MCD")


def get_date():
    today = datetime.date.today()
    start_date = st.sidebar.date_input("Selecting the Start date",datetime.date(2020,1,1))
    end_date = st.sidebar.date_input("Selecting the End date",today)
    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.sidebar.error('Error: End date must fall after start date.')
    return start_date, end_date

start_date, end_date = get_date()

data = yf.download(symbol, start=start_date, end=end_date)
data["return"] = data["Close"].pct_change()
data["Adj return"] = data["Adj Close"].pct_change()
st.write(data)

download=st.button('下载CSV数据')

###file name
filename =  str(start_date) + "-" + str(end_date) + "-" + str(symbol) + ".csv"
if download:
    'Download Started!'
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    linko= f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download csv file</a>'
    #linko=f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ".csv")'
    st.markdown(linko, unsafe_allow_html=True)