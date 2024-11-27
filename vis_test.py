import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# 加载示例数据集
df = px.data.gapminder()

# 创建 Dash 应用
app = dash.Dash(__name__)

# 定义布局
app.layout = html.Div([
    html.H1("多图表交互示例", style={'text-align': 'center'}),

    # Dropdown 选择年份
    html.Div([
        html.Label("选择年份:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in df['year'].unique()],
            value=2007,  # 默认选中年份
            clearable=False
        ),
    ], style={'width': '50%', 'margin': '0 auto'}),

    # 图表容器
    html.Div([
        html.Div([
            html.H3("交互式散点图"),
            dcc.Graph(id='scatter-plot')  # 散点图
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),

        html.Div([
            html.H3("动态柱状图"),
            dcc.Graph(id='bar-chart')  # 柱状图
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),
    ])
])

# 定义回调函数
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('year-dropdown', 'value')]
)
def update_charts(selected_year):
    # 过滤数据
    filtered_df = df[df['year'] == selected_year]

    # 更新散点图
    scatter_fig = px.scatter(
        filtered_df, x='gdpPercap', y='lifeExp',
        size='pop', color='continent',
        hover_name='country', title=f'散点图: {selected_year}年',
        labels={'gdpPercap': '人均GDP', 'lifeExp': '预期寿命'}
    )

    # 更新柱状图
    bar_fig = px.bar(
        filtered_df, x='continent', y='pop',
        color='continent', title=f'柱状图: {selected_year}年人口分布',
        labels={'pop': '人口', 'continent': '大洲'}
    )

    return scatter_fig, bar_fig


# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
