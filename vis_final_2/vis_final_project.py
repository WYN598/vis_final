START_DATE = "2024-01-11"  # start date for historical data
RSI_TIME_WINDOW = 7  # number of days

import requests
import pandas as pd
import warnings
import datetime as dt
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas_datareader.data as web
from plotly.subplots import make_subplots

warnings.filterwarnings('ignore')

## URLS and names
urls = ["https://www.cryptodatadownload.com/cdd/Bitfinex_EOSUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_BTCUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_ETHUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_LTCUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_BATUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_OMGUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_DAIUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_ETCUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_NEOUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_TRXUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_XLMUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_XMRUSD_d.csv",
        "https://www.cryptodatadownload.com/cdd/Bitfinex_XVGUSD_d.csv",
        ]
crypto_names = ["EOS Coin (EOS)",
                "Bitcoin (BTC)",
                "Ethereum (ETH)",
                "Litecoin (LTC)",
                "Basic Attention Token (BAT)",
                "OmiseGO (OMG)",
                "Dai (DAI)",
                "Ethereum Classic (ETC)",
                "Neo (NEO)",
                "TRON (TRX)",
                "Stellar (XLM)",
                "Monero (XMR)",
                "Verge (XVG)"
                ]


## Data download and loading
def df_loader(urls, start_date="2021-01-01"):
    filenames = []
    all_df = pd.DataFrame()
    for idx, url in enumerate(urls):
        req = requests.get(url, verify=False)
        url_content = req.content
        filename = url[48:]
        csv_file = open(filename, 'wb')
        csv_file.write(url_content)
        csv_file.close()
        filename = filename[:-9]
        filenames.append(filename)
    for file in filenames:
        df = pd.read_csv(file + "USD_d.csv", header=1, parse_dates=["date"])
        df = df[df["date"] > start_date]
        df.index = df.date
        df.drop(labels=[df.columns[0], df.columns[1], df.columns[8]], axis=1, inplace=True)
        all_df = pd.concat([all_df, df], ignore_index=False)

    return all_df, filenames


def computeRSI(data, time_window):
    diff = data.diff(1).dropna()
    up_chg = 0 * diff
    down_chg = 0 * diff
    up_chg[diff > 0] = diff[diff > 0]
    down_chg[diff < 0] = diff[diff < 0]
    up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    rs = abs(up_chg_avg / down_chg_avg)
    rsi = 100 - 100 / (1 + rs)
    return rsi


def computeMA(data, window):
    return data.rolling(window=window).mean()


all_df, filenames = df_loader(urls, start_date=START_DATE)

crypto_df = []
latest_common_date = None
earliest_common_date = None
for file in filenames:
    symbol = file + "/USD"
    temp_df = pd.DataFrame(all_df[all_df["symbol"] == symbol])

    # 检查索引类型
    print(f"\nChecking index for {symbol}:")
    print(f"Index dtype: {temp_df.index.dtype}")

    # 检查是否所有索引都是日期格式
    if not isinstance(temp_df.index, pd.DatetimeIndex):
        print(f"Warning: Index for {symbol} is not DatetimeIndex")
        print("Sample of problematic indices:")
        print(temp_df.index[:5].tolist())  # 打印前5个索引值

    if latest_common_date is None and earliest_common_date is None:
        latest_common_date = temp_df.index.max()
        earliest_common_date = temp_df.index.min()
        print(f"Latest date: {temp_df.index.max()}")
        print(f"Earliest date: {temp_df.index.min()}")
    else:
        print(f"Latest date: {temp_df.index.max()}")
        print(f"Earliest date: {temp_df.index.min()}")
        latest_common_date = min(temp_df.index.max(), latest_common_date)
        earliest_common_date = max(temp_df.index.min(), earliest_common_date)
for file in filenames:
    symbol = file + "/USD"
    temp_df = pd.DataFrame(all_df[all_df["symbol"] == symbol])
    temp_df = temp_df[(temp_df.index <= latest_common_date) & (temp_df.index >= earliest_common_date)]

    temp_df.drop(columns=["symbol"], inplace=True)

    # 对数值列进行插值处理
    numeric_columns = ['open', 'high', 'low', 'close', 'Volume USD']
    temp_df[numeric_columns] = temp_df[numeric_columns].interpolate(method='time')

    print(temp_df[numeric_columns].isnull().sum())

    # 如果某列缺失值过多（比如超过20%），可能需要特殊处理
    missing_threshold = 0.2
    missing_ratio = temp_df[numeric_columns].isnull().sum() / len(temp_df)
    if (missing_ratio > missing_threshold).any():
        print(f"Warning: High missing ratio in {file}")

    temp_df["close_rsi"] = computeRSI(temp_df['close'], time_window=RSI_TIME_WINDOW)
    temp_df["ma_7"] = computeMA(temp_df['close'], window=7)
    temp_df["ma_25"] = computeMA(temp_df['close'], window=25)
    temp_df["ma_99"] = computeMA(temp_df['close'], window=99)
    temp_df["high_rsi"] = 30
    temp_df["low_rsi"] = 70
    exec('%s = temp_df.copy()' % file.lower())
    crypto_df.append(temp_df)
## plot
# Update the subplot layout to include the stacked area chart in row 3

# fig = make_subplots(
#     rows=3,
#     cols=2,
#     shared_xaxes=True,
#     specs=[
#         [{"rowspan": 2, "colspan": 2}, None],  # First row
#         [None, None],  # Second row (covered by rowspan)
#         [{"colspan": 1}, {"colspan": 1}]  # Third row
#     ]
# )

fig = make_subplots(
    rows=4,
    cols=2,
    shared_xaxes=True,
    specs=[
        [{"rowspan": 2, "colspan": 2}, None],  # First row
        [None, None],  # Second row (covered by rowspan)
        [{"colspan": 1}, {"colspan": 1}],  # Third row
        [{"colspan": 2}, None]  # Fourth row for the stacked area chart
    ]
)





date_buttons = [
    {'step': "all", 'label': "All time"},  # 显示所有时间范围的数据
    {'count': 1, 'step': "year", 'stepmode': "backward", 'label': "Last Year"},  # 显示最近一年的数据
    {'count': 1, 'step': "year", 'stepmode': "todate", 'label': "Current Year"},  # 显示今年至今的数据
    {'count': 1, 'step': "month", 'stepmode': "backward", 'label': "Last 2 Months"},  # 显示最近一个月的数据
    {'count': 1, 'step': "month", 'stepmode': "todate", 'label': "Current Month"},  # 显示本月至今的数据
    {'count': 7, 'step': "day", 'stepmode': "todate", 'label': "Current Week"},  # 显示本周至今的数据（7天）
    {'count': 4, 'step': "day", 'stepmode': "backward", 'label': "Last 4 days"},  # 显示最近4天的数据
    {'count': 1, 'step': "day", 'stepmode': "backward", 'label': "Today"},  # 显示今天的数据
]
buttons = []
i = 0
j = 0
COUNT = 8
# 蜡烛图
# 成交量柱状图
# 价格线图
# 最低价线
# 最高价线
# RSI指标线
# RSI低线
# RSI高线

vis = [False] * len(crypto_names) * COUNT
for df in crypto_df:
    for k in range(COUNT):
        vis[j + k] = True
    buttons.append({'label': crypto_names[i],
                    'method': 'update',
                    'args': [{'visible': vis},
                             {'title': crypto_names[i] + ' Charts and Indicators'}
                             ]}
                   )
    i += 1
    j += COUNT
    vis = [False] * len(crypto_names) * COUNT
for df in crypto_df:
    print(df.index)
    fig.add_trace(
        go.Candlestick(x=df.index,
                       open=df['open'],
                       high=df['high'],
                       low=df['low'],
                       close=df['close'],
                       name='current_stock_price',
                       showlegend=True,
                       increasing_line_color='#26A69A',  # 上涨时的颜色（绿色）
                       decreasing_line_color='#EF5350',  # 下跌时的颜色（红色）
                       increasing_fillcolor='#26A69A',  # 上涨时的填充颜色
                       decreasing_fillcolor='#EF5350'  # 下跌时的填充颜色
                       ),
        row=1,
        col=1)
    fig.add_trace(
        go.Bar(x=df.index,
               y=df["Volume USD"],
               name='Volume USD',
               showlegend=True,
               marker_color='aqua'),
        row=3,
        col=1)
    # fig.add_trace(
    #     go.Scatter(x=df.index, y=df['close'],
    #                mode='lines',
    #                name='close_Price',
    #               showlegend =True,
    #                line=dict(color="red", width=4)),
    #     row=1,
    #     col=2)
    fig.add_trace(
        go.Scatter(x=df.index, y=df['close_rsi'],
                   mode='lines',
                   name='RSI',
                   showlegend=True,
                   line=dict(color="aquamarine", width=4)),
        row=3,
        col=2)
    fig.add_trace(
        go.Scatter(x=df.index,
                   y=df['low_rsi'],
                   fill='tonexty',
                   mode='lines',
                   name='RSI_low',
                   showlegend=False,
                   line=dict(width=2, color='aqua', dash='dash')),
        row=3,
        col=2)
    fig.add_trace(
        go.Scatter(x=df.index,
                   y=df['high_rsi'],
                   fill='tonexty',
                   mode='lines',
                   name='RSI_high',
                   showlegend=False,
                   line=dict(width=2, color='aqua', dash='dash')),
        row=3,
        col=2)
    fig.add_trace(
        go.Scatter(x=df.index, y=df['ma_7'],
                   mode='lines',
                   name='MA7',
                   line=dict(color="orange", width=1)),
        row=1, col=1)

    fig.add_trace(
        go.Scatter(x=df.index, y=df['ma_25'],
                   mode='lines',
                   name='MA25',
                   line=dict(color="purple", width=1)),
        row=1, col=1)

    fig.add_trace(
        go.Scatter(x=df.index, y=df['ma_99'],
                   mode='lines',
                   name='MA99',
                   line=dict(color="cyan", width=1)),
        row=1, col=1)




# Assuming 'close' and 'Volume USD' columns are present in your DataFrame
all_df['market_cap'] = all_df['close'] * all_df['Volume USD']

# Add traces for the stacked area chart in the fourth row
# btc_market_cap = all_df[all_df['symbol'] == 'BTC/USD']['market_cap']
eth_market_cap = all_df[all_df['symbol'] == 'ETH/USD']['market_cap']
other_market_cap = all_df[~all_df['symbol'].isin(['BTC/USD', 'ETH/USD'])].groupby('date')['market_cap'].sum()

# fig.add_trace(
#     go.Scatter(x=btc_market_cap.index, y=btc_market_cap, mode='lines', name='BTC Market Cap', stackgroup='one'),
#     row=4, col=1
# )

fig.add_trace(
    go.Scatter(x=eth_market_cap.index, y=eth_market_cap, mode='lines', name='ETH Market Cap', stackgroup='one'),
    row=4, col=1
)

fig.add_trace(
    go.Scatter(x=other_market_cap.index, y=other_market_cap, mode='lines', name='Other Market Cap', stackgroup='one'),
    row=4, col=1
)









# Update layout and show the figure
fig.update_layout(
    width=1800,
    height=1200,  # Adjusted height to accommodate the new row
    font_family='monospace',
    xaxis=dict(rangeselector=dict(buttons=date_buttons)),
    updatemenus=[
        dict(
            type='dropdown',
            x=1.0,
            y=1.108,
            showactive=True,
            active=2,
            buttons=buttons
        ),
        dict(
            type="buttons",
            direction="right",
            buttons=[
                dict(
                    label="Colorblind Mode",
                    method="update",
                    args=[{"increasing": {"line": {"color": "#26A69A"}},
                           "decreasing": {"line": {"color": "#EF5350"}}}],
                    args2=[{"increasing": {"line": {"color": "blue"}},
                            "decreasing": {"line": {"color": "aqua"}}}],
                )
            ],
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.0,
            xanchor="left",
            y=1.15,
            yanchor="top"
        )
    ],
    title=dict(text='<b>Cryptocurrencies Dashboard<b>',
               font=dict(color='#FFFFFF', size=22),
               x=0.50),
    font=dict(color="blue"),
    annotations=[
        dict(text="<b>Volume Traded<b>",
             font=dict(size=20, color="#ffffff"),
             showarrow=False,
             x=0.14,
             y=-0.53,
             xref='paper', yref="paper",
             align="left"),
        dict(text="<b>Relative Strength Index (RSI)<b>",
             font=dict(size=20, color="#ffffff"),
             showarrow=False,
             x=0.94,
             y=-0.53,
             xref='paper', yref="paper",
             align="left")
    ],
    template="plotly_dark"
)





fig.update_xaxes(
    tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
    tickmode='array',
    ticklen=6,
    showline=False,
    showgrid=True,
    gridcolor='#595959',
    ticks='outside')
fig.update_layout(
    spikedistance=100,
    xaxis_rangeslider_visible=False,
    hoverdistance=1000)
fig.update_xaxes(
    showspikes=True,
    spikesnap="cursor",
    spikemode="across"
)
fig.update_yaxes(
    showspikes=True,
    spikesnap='cursor',
    spikemode="across"
)
fig.update_yaxes(
    tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
    tickmode='array',
    showline=False,
    ticksuffix='$',
    showgrid=True,
    gridcolor='#595959',
    ticks='outside')

fig.update_layout(
    width=1800,
    height=900,
    font_family='monospace',
    xaxis=dict(rangeselector=dict(buttons=date_buttons)),
    updatemenus=[
        dict(
            type='dropdown',
            x=1.0,
            y=1.108,
            showactive=True,
            active=2,
            buttons=buttons
        ),
        dict(
            type="buttons",
            direction="right",
            buttons=[
                dict(
                    label="Colorblind Mode",
                    method="update",

                    args=[{"increasing": {"line": {"color": "#26A69A"}},
                            "decreasing": {"line": {"color": "#EF5350"}}}],
                    args2=[{"increasing": {"line": {"color": "blue"}},
                           "decreasing": {"line": {"color": "aqua"}}}],

                )

            ],
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.0,
            xanchor="left",
            y=1.15,
            yanchor="top"
        )

    ],
    title=dict(text='<b>Cryptocurrencies  Dashboard<b>',
               font=dict(color='#FFFFFF', size=22),
               x=0.50),
    font=dict(color="blue"),
    annotations=[
        dict(text="<b>Volume Traded<b>",
             font=dict(size=20, color="#ffffff"),
             showarrow=False,
             x=0.14,
             y=-0.53,
             xref='paper', yref="paper",
             align="left"),
        dict(text="<b>Relative Strength Index (RSI)<b>",
             font=dict(size=20, color="#ffffff"),
             showarrow=False,
             x=0.94,
             y=-0.53,
             xref='paper', yref="paper",
             align="left")
    ],
    template="plotly_dark"
)
for i in range(0, 13 * COUNT):
    fig.data[i].visible = False
for i in range(COUNT):
    fig.data[i].visible = True
fig.layout["xaxis"]["rangeslider"]["visible"] = False
fig.layout["xaxis2"]["rangeslider"]["visible"] = False
fig.layout["xaxis3"]["rangeslider"]["visible"] = False
fig.show()
