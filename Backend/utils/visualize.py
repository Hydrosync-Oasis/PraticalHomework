import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import warnings

# 关闭警告提示，防止绘图时出现警告信息
warnings.filterwarnings('ignore')

# 设置中文支持（全局有效）
plt.rcParams['font.family'] = 'SimHei'           # 显示中文
plt.rcParams['axes.unicode_minus'] = False       # 显示负号正常

# 设置整体画风和调色板
plt.style.use('fivethirtyeight')
colors = ['#011f4b', '#03396c', '#005b96', '#6497b1', '#b3cde0']
sns.set_palette(sns.color_palette(colors))


def plot_age_distribution(df):
    """
    可视化年龄分布：包括密度图、带标签的直方图和箱型图
    """
    fig, ax = plt.subplots(1, 3, figsize=(20, 6))
    sns.histplot(df['AGE'], kde=True, ax=ax[0], color='blue')
    sns.histplot(data=df, x='AGE', hue='LUNG_CANCER', kde=True, ax=ax[1])
    sns.boxplot(x='LUNG_CANCER', y='AGE', data=df, ax=ax[2])
    plt.suptitle("年龄（AGE）相关可视化", size=20)
    plt.show()

def plot_categorical_counts(df, cat_cols):
    """
    绘制类别变量的分布和与肺癌标签的关系
    """
    fig, ax = plt.subplots(len(cat_cols), 2, figsize=(30, 5 * len(cat_cols)))
    for idx, col in enumerate(cat_cols):
        sns.countplot(data=df, x=col, ax=ax[idx, 0])
        sns.countplot(data=df, x=col, hue='LUNG_CANCER', ax=ax[idx, 1])
        ax[idx, 0].set_title(f'{col} 分布')
        ax[idx, 1].set_title(f'{col} 与肺癌关系')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.suptitle("类别特征可视化", fontsize=40)
    plt.show()

def plot_correlation_heatmap(df):
    """
    绘制特征相关性热力图（遮罩上三角，防止重复）
    """
    corr_matrix = df.corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', mask=mask,
                cmap='coolwarm', cbar_kws={'shrink': 0.3},
                annot_kws={'size': 8}, linewidths=0.1)
    plt.title("特征相关性热力图", fontsize=20)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.show()

def plot_gender_cancer_counts(df):
    """
    绘制不同性别肺癌与非肺癌患者人数统计柱状图
    """
    plt.rcParams['font.family'] = 'SimHei'  # 适配中文字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    gender_cancer_counts = df.groupby(['GENDER', 'LUNG_CANCER']).size().unstack(fill_value=0)
    colors = ['#4CAF50', '#F44336']  # 绿色和红色

    gender_cancer_counts.plot(kind='bar', figsize=(8, 6), color=colors)
    plt.title('不同性别的肺癌与非肺癌患者统计')
    plt.xlabel('性别（0 = 女，1 = 男）')
    plt.ylabel('人数')
    plt.xticks(rotation=0)
    plt.legend(title='是否患肺癌')
    plt.tight_layout()
    plt.show()

def plot_age_group_stacked_bar(df):
    """
    按年龄分组，绘制堆叠柱状图展示肺癌与非肺癌患者数
    """
    lung_cancer_numeric = df['LUNG_CANCER']
    age_bins = range(20, 100, 10)
    age_groups = pd.cut(df['AGE'], bins=age_bins, right=False)

    grouped = pd.DataFrame({'AGE_GROUP': age_groups, 'LUNG_CANCER': lung_cancer_numeric})
    age_group_counts = grouped.groupby(['AGE_GROUP', 'LUNG_CANCER']).size().unstack(fill_value=0)
    age_group_counts.columns = ['非肺癌', '肺癌']
    colors = ['#2196F3', '#FF5722']

    age_group_counts.plot(kind='bar', stacked=True, figsize=(12, 6), color=colors)
    plt.title('不同年龄段的肺癌与非肺癌患者统计')
    plt.xlabel('年龄段')
    plt.ylabel('人数')
    plt.legend(title='是否患肺癌')
    plt.tight_layout()
    plt.show()

def plot_smoking_boxplot(df):
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.rcParams['font.family'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df, x='SMOKING', y='AGE')
    plt.title("吸烟与年龄的箱型图")
    plt.xlabel("是否吸烟")
    plt.ylabel("年龄")
    plt.show()


def plot_sample_counts_before_after_sampling(df):
    """
    绘制采样前后肺癌与非肺癌患者数量对比柱状图
    """
    import matplotlib.pyplot as plt
    from sklearn.utils import resample

    # 设置中文字体
    plt.rcParams['font.family'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False

    # 原始样本数统计（假设LUNG_CANCER为0和1）
    df_lung = df[df['LUNG_CANCER'] == 1]
    df_nonlung = df[df['LUNG_CANCER'] == 0]

    original_counts = {'肺癌-原始': len(df_lung), '非肺癌-原始': len(df_nonlung)}

    # 过采样非肺癌患者至与肺癌数量一致
    df_nonlung_upsampled = resample(df_nonlung, replace=True, n_samples=len(df_lung), random_state=42)
    sampled_counts = {'肺癌-采样后': len(df_lung), '非肺癌-采样后': len(df_nonlung_upsampled)}

    # 合并统计结果
    all_counts = {**original_counts, **sampled_counts}

    # 画图
    plt.figure(figsize=(8, 6))
    plt.bar(all_counts.keys(), all_counts.values(),
            color=['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd'])
    plt.title('肺癌与非肺癌患者数量对比（采样前后）')
    plt.ylabel('样本数量')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

