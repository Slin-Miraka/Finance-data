import json
from urllib.request import urlopen
import pandas as pd
import easyquotation
import streamlit as st
import base64

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)




def get_real_time_data(code):
    quotation = easyquotation.use('qq') # 新浪 ['sina'] 腾讯 ['tencent', 'qq'] 
    code = str(code)
    dic = quotation.real(code)
    name = dic[code]["name"]
    #close = dic[code]["close"]
    #volume = dic[code]["volume"]
    #time = dic[code]["time"]
    now = dic[code]["now"]
    return name, now

def hist_min_data(market = "sh", symbol = "600519", datalen = 1000, scale = 1):
    #设置参数
    symbol = market + symbol
    datalen = str(datalen) #最大获取数据长度为1023
    scale = str(scale) # 可获取1, 5，15，30，60分钟的数据
    #新浪网数据接口
    url = "https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=" + symbol + "&scale=" + scale + "&ma=no&datalen=" + datalen 
    data = pd.DataFrame(get_jsonparsed_data(url))
    return data

with st.sidebar.header('Welcome！ o(*￣▽￣*)ブ'):
    market = st.sidebar.selectbox("选择股票市场", ("上证","深证"))
    symbol = st.sidebar.text_input('请输入股票代码', 600519)
    datalen = st.sidebar.slider("请选择获取数据长度",1 ,1000, value = 500, step = 1)
    scale = st.sidebar.selectbox("请选择数据频率",("1分钟数据","5分钟数据","15分钟数据","30分钟数据","60分钟数据"))  

#####
if market == "上证":
    market = "sh"
else:
    market = "sz"

#####
if scale == "1分钟数据":
    scale = 1
elif scale == "5分钟数据":
    scale = 5
elif scale == "15分钟数据":
    scale = 15
elif scale == "30分钟数据":
    scale = 30
elif scale == "60分钟数据":
    scale = 60

name, now = get_real_time_data(symbol)


###
st.title('**获取A股市场分钟频率数据**')
#st.subheader('当前选择股票',)
st.write('**当前选择股票 :**', name)
st.write('**股票当前价格 :**', now)
st.write('**数据查询长度 :**', datalen,"**条**")
data = hist_min_data(market=market, symbol=symbol, datalen=datalen,scale =scale)
st.write(data)


###下载数据
download=st.button('下载CSV数据')

###file name
filename = data.iloc[-1, 0] + "--" + str(symbol) + "--" +str(scale)  +  "--" + str(datalen) + ".csv"
st.write("**数据命名格式：** [获取时间] **--** [股票代码] **--** [数据频率]  **--** [数据长度] **.csv**")
if download:
    'Download Started!'
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    linko= f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download csv file</a>'
    #linko=f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ".csv")'
    st.markdown(linko, unsafe_allow_html=True)
