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
filtered_df = df[df['国籍'].isin(selected_countries)]

if not filtered_df.empty:
    top_country = filtered_df.sort_values('旅行消費単価', ascending=False).iloc[0]
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="選択した国の平均単価", value=f"{filtered_df['旅行消費単価'].mean():,.0f} 円")
    with col2:
        st.metric(label="最も使う国 (No.1)", value=f"{top_country['国籍']}", delta=f"{top_country['旅行消費単価']:,.0f} 円")
else:
    st.error("サイドバーで国を選んでください")

tab1, tab2, tab3 = st.tabs(["グラフ比較", "世界地図", "データ詳細"])

with tab1:
    st.subheader('国別の消費単価ランキング')
    if not filtered_df.empty:
        # 棒グラフ
        st.bar_chart(filtered_df.set_index('国籍')['旅行消費単価'])
        st.caption("棒グラフ：国ごとの消費額の違い")

with tab2:
    st.subheader('来訪元の国をマップで確認')
    map_df = filtered_df.dropna(subset=['lat', 'lon'])
    if not map_df.empty:
        st.map(map_df, size=2000, color='#ff0000') # 赤い点で表示
        st.caption("※主要な国のみ位置を表示")
    else:
        st.warning("選択された国の位置情報データがありません。")