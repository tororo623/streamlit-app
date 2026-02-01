import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_tourism_data.csv')

latlon_data = {
    '韓国': [37.5665, 126.9780],
    '台湾': [23.6978, 120.9605],
    '香港': [22.3193, 114.1694],
    '中国': [35.8617, 104.1954],
    'タイ': [15.8700, 100.9925],
    '米国': [37.0902, -95.7129],
    '英国': [55.3781, -3.4360],
    'フランス': [46.2276, 2.2137],
    'オーストラリア': [-25.2744, 133.7751],
    'ベトナム': [14.0583, 108.2772]
}
def add_latlon(country_name):
    return latlon_data.get(country_name, None)

# データフレームに緯度(lat)と経度(lon)を追加
df['lat'] = df['国籍'].map(lambda x: latlon_data[x][0] if x in latlon_data else None)
df['lon'] = df['国籍'].map(lambda x: latlon_data[x][1] if x in latlon_data else None)

st.title('🇯🇵 訪日外国人 消費動向＆マップ')
st.caption('出典：e-Stat 訪日外国人消費動向調査')

st.sidebar.header('検索条件')
selected_countries = st.sidebar.multiselect(
    '表示する国・地域を選択',
    options=df['国籍'].unique(),
    default=['韓国', '台湾', '米国', '中国', '香港'] # 初期表示
)