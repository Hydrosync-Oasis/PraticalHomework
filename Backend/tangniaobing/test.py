from Backend.diabetes_model import train_model, predict_samples
import matplotlib


# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 中文
matplotlib.rcParams['axes.unicode_minus'] = False    # 负号

# 第一次运行时训练模型
train_model()

# 测试样本
test_samples = [
    [1, 85, 66, 29, 0, 26.6, 0.351, 31],     # 正常
    [3, 145, 78, 35, 130, 33.0, 0.5, 45],     # 高风险
    [10, 190, 70, 33, 200, 35.0, 1.2, 50]     # 极高风险
]

# 进行预测
results = predict_samples(test_samples)

# 打印结果
for res in results:
    print(f"测试样本 {res['样本编号']}: 预测结果 = {res['预测结果']}，概率 = {res['概率']}")
