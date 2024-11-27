import pandas as pd
import matplotlib.pyplot as plt

# 替换为你本地CSV文件的路径
denver_df = pd.read_csv(r'avgtemps/denver_avgtemp.csv')
okc_df = pd.read_csv(r'avgtemps/okc_avgtemp.csv')
seattle_df = pd.read_csv(r'avgtemps/seattle_avgtemp.csv')
dallas_df = pd.read_csv(r'avgtemps/dallas_avgtemp.csv')

# 生成可视化图表
plt.figure(figsize=(14, 8))

# Plot for Denver
plt.subplot(4, 1, 1)
plt.plot(denver_df['year'], denver_df['avg_temp'], label='Avg Temp', color='blue')
plt.plot(denver_df['year'], denver_df['10y_ma'], label='10Y Moving Avg', color='red', linestyle='--')
plt.title('Denver Average Temperature Over Time')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.legend()

# Plot for Oklahoma City
plt.subplot(4, 1, 2)
plt.plot(okc_df['year'], okc_df['avg_temp'], label='Avg Temp', color='blue')
plt.plot(okc_df['year'], okc_df['10y_ma'], label='10Y Moving Avg', color='red', linestyle='--')
plt.title('Oklahoma City Average Temperature Over Time')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.legend()

# Plot for Seattle
plt.subplot(4, 1, 3)
plt.plot(seattle_df['year'], seattle_df['avg_temp'], label='Avg Temp', color='blue')
plt.plot(seattle_df['year'], seattle_df['10y_ma'], label='10Y Moving Avg', color='red', linestyle='--')
plt.title('Seattle Average Temperature Over Time')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.legend()



plt.subplot(4, 1, 4)
plt.plot(dallas_df['year'], dallas_df['avg_temp'], label='Avg Temp', color='blue')
plt.plot(dallas_df['year'], dallas_df['10y_ma'], label='10Y Moving Avg', color='red', linestyle='--')
plt.title('Dallas Average Temperature Over Time')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.legend()


# 调整布局并显示图表
plt.tight_layout()
plt.show()
