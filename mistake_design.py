import pandas as pd
import matplotlib.pyplot as plt

# 读取本地CSV文件
denver_df = pd.read_csv(r'avgtemps/denver_avgtemp.csv')
okc_df = pd.read_csv(r'avgtemps/okc_avgtemp.csv')
seattle_df = pd.read_csv(r'avgtemps/seattle_avgtemp.csv')
dallas_df = pd.read_csv(r'avgtemps/dallas_avgtemp.csv')

# Denver - 使用Cut-off Axes（截断轴）
plt.figure(figsize=(7, 5))  # 单独的图表
plt.plot(denver_df['year'], denver_df['avg_temp'], label='Avg Temp', color='blue')
plt.plot(denver_df['year'], denver_df['10y_ma'], label='10Y Moving Avg', color='red', linestyle='--')
plt.title('Denver Average Temperature (Cut-off Axes)')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.ylim(8, 10)  # 故意截断Y轴，给出不完整的温度范围
plt.tight_layout()
plt.show()  # 显示Denver图表

# Oklahoma City - 使用Glass Slippers（不合适的轴刻度）
plt.figure(figsize=(7, 5))  # 单独的图表
plt.plot(okc_df['year'], okc_df['avg_temp'], label='Avg Temp', color='blue')
plt.plot(okc_df['year'], okc_df['10y_ma'], label='10Y Moving Avg', color='red', linestyle='--')
plt.title('Oklahoma City Average Temperature (Glass Slippers)')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.yticks([0, 5, 10, 15, 20])  # 不合适的刻度，误导观众
plt.tight_layout()
plt.show()  # 显示Oklahoma City图表

# Seattle - 使用Bad Color Scale（不恰当的颜色使用）和屎黄色内部背景
fig, ax = plt.subplots(figsize=(7, 5))  # 单独的图表
ax.set_facecolor('#9B870C')  # 设置内部背景颜色为屎黄色
ax.plot(seattle_df['year'], seattle_df['avg_temp'], label='Avg Temp', color='#FF00FF')  # 过度鲜艳的颜色
ax.plot(seattle_df['year'], seattle_df['10y_ma'], label='10Y Moving Avg', color='#00FFFF', linestyle='--')  # 另一个刺眼的颜色
plt.title('Seattle Average Temperature (Bad Color Scale)')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.tight_layout()
plt.show()  # 显示Seattle图表

# Dallas - Perspective Distortion（透视扭曲）
fig = plt.figure(figsize=(7, 5))  # 单独的图表
ax = fig.add_subplot(111, projection='3d')  # 创建3D图形
ax.plot(dallas_df['year'], dallas_df['avg_temp'], zs=0, zdir='y', label='Avg Temp', color='blue')
ax.plot(dallas_df['year'], dallas_df['10y_ma'], zs=0, zdir='y', label='10Y Moving Avg', color='red', linestyle='--')
plt.title('Dallas Average Temperature (Perspective Distortion)')
ax.set_xlabel('Year')
ax.set_ylabel('Temperature (°C)')
ax.legend()
plt.tight_layout()
plt.show()  # 显示Dallas图表
