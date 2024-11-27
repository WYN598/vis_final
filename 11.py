# parsed_data = [
#     ("1", 479.55, 481.81, 482.02, 482.41, None, None, None),
#     ("2", 510.96, 512.76, 513.85, 514.19, None, None, None),
#     ("3", 488.04, 489.57, 490.06, 490.41, None, None, None),
#     ("4", 505.12, 507.09, 507.67, 507.71, None, None, None),
#     ("5", 361.37, 362.53, 362.81, 362.93, None, None, None),
#     ("6", 527.39, 529.12, 528.97, 529.37, None, None, None),
#     ("7", 478.27, 479.59, 480.28, 480.46, None, None, None),
#     ("8", 510.26, 511.74, 512.54, 512.50, None, None, None),
#     ("CO-1", 501.23, 502.37, 502.19, 502.34, None, None, None),
#     ("CO-2", 488.19, 489.25, 488.72, 489.13, None, None, None),
#     ("CO-3", 508.23, 509.39, 508.98, 509.24, None, None, None),
#     ("CO-4", 496.44, 498.01, 498.08, 498.15, None, None, None),
#     ("CO-5", 496.04, 497.69, 497.43, 497.49, None, None, None),
#     ("CO-6", 523.82, 525.28, 525.14, 525.46, None, None, None)
# ]


# parsed_data_2 = [
#     ("9", 491.81, 494.19, None, None, None, None, None),
#     ("10", 493.33, 495.24, None, None, None, None, None),
#     ("11", 496.27, 498.21, None, None, None, None, None),
#     ("12", 518.92, 520.96, None, None, None, None, None),
#     ("13", 506.91, 509.09, None, None, None, None, None),
#     ("CO-7", 501.07, 503.81, None, None, None, None, None),
#     ("CO-8", 513.05, 515.76, None, None, None, None, None),
#     ("CO-9", 473.63, 475.29, None, None, None, None, None),
#     ("CO-10", 514.93, 517.44, None, None, None, None, None),
#     ("CO-11", 496.44, 498.91, None, None, None, None, None),
#     ("CO-12", 469.34, 470.49, None, None, None, None, None),
# ]



data_pre = [
        ('9', 491.81, 494.19, 496.57, None, None, None, None),
        ('10', 493.33, 495.24, 497.15, None, None, None, None),
        ('11', 496.27, 498.21, 500.15, None, None, None, None),
        ('12', 518.92, 520.96, 523.0, None, None, None, None),
        ('13', 506.91, 509.09, 511.27, None, None, None, None),
        ('CO-7', 501.07, 503.81, 506.55, None, None, None, None),
        ('CO-8', 513.05, 515.76, 518.47, None, None, None, None),
        ('CO-9', 473.63, 475.29, 476.95, None, None, None, None),
        ('CO-10', 514.93, 517.44, 519.95, None, None, None, None),
        ('CO-11', 496.44, 498.91, 501.38, None, None, None, None),
        ('CO-12', 469.34, 470.49, 471.64, None, None, None, None)
]


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 原始数据
data = [

]


# 将数据转换为DataFrame以便处理
columns = ["Sample"] + [f"Day {i}" for i in range(1, 8)]
df = pd.DataFrame(data, columns=columns)


# 定义用于拟合的增长函数
def growth_model(day, a, b, c):
    return a + b * np.log(c * day + 1)


# 初始化预测结果
predicted_values = []

# 遍历每个样本进行拟合和预测
for _, row in df.iterrows():
    sample = row["Sample"]
    days = np.array([1, 2, 3])  # 已知的天数
    weights = row[1:4].values  # 已知的重量数据

    # 去掉None值
    valid_days = days[~pd.isnull(weights)]
    valid_weights = weights[~pd.isnull(weights)]

    # 拟合数据
    try:
        popt, _ = curve_fit(growth_model, valid_days, valid_weights, maxfev=10000)
        # 使用拟合结果预测剩余天数
        future_days = np.array([4, 5, 6, 7])
        predictions = growth_model(future_days, *popt)
    except:
        predictions = [None, None, None, None]  # 如果拟合失败，返回None

    # 保存预测结果
    predicted_values.append(list(predictions))

# 将预测结果填入DataFrame
for i, predictions in enumerate(predicted_values):
    df.iloc[i, 4:] = [round(pred, 3) if pred is not None else None for pred in predictions]

# 查看更新后的数据
# 查看更新后的数据
print(df)







