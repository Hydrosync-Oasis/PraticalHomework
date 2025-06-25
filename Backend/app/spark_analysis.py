
import os
from pyspark.sql import SparkSession

def get_spark_rdd():
    # 构建项目根目录路径（即 Backend/）
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    csv_path = os.path.join(BASE_DIR, 'data', 'insurance.csv')  # Backend/data/insurance.csv

    # 启动 Spark 会话
    spark = SparkSession.builder \
        .appName("Insurance Visual Data RDD") \
        .master("local[*]") \
        .getOrCreate()

    # 读取 CSV 文件
    df = spark.read.csv(csv_path, header=True, inferSchema=True)

    # 转为 RDD
    rdd = df.rdd

    return spark, rdd


def get_boxplot_data():
    spark, rdd = get_spark_rdd()
    result = rdd.map(lambda row: (row['smoker'], row['charges'])) \
                .filter(lambda x: None not in x) \
                .groupByKey() \
                .mapValues(list) \
                .collect()
    spark.stop()
    return {k: list(v) for k,v in result}

def get_scatter_bmi_charges():
    spark, rdd = get_spark_rdd()
    result = rdd.map(lambda row: (row['bmi'], row['charges'])) \
                .filter(lambda x: None not in x) \
                .collect()
    spark.stop()
    return [list(x) for x in result]

def get_age_histogram():
    spark, rdd = get_spark_rdd()
    result = rdd.map(lambda row: row['age']) \
                .filter(lambda x: x is not None) \
                .collect()
    spark.stop()
    return result

def get_region_avg_charges():
    spark, rdd = get_spark_rdd()
    result = rdd.map(lambda row: (row['region'], (row['charges'], 1))) \
                .filter(lambda x: None not in x[0] and None not in x[1]) \
                .reduceByKey(lambda a, b: (a[0]+b[0], a[1]+b[1])) \
                .mapValues(lambda x: round(x[0]/x[1], 2)) \
                .collect()
    spark.stop()
    return dict(result)

def get_scatter_age_charges_smoker():
    spark, rdd = get_spark_rdd()
    result = rdd.map(lambda row: (row['age'], row['charges'], row['smoker'])) \
                .filter(lambda x: None not in x) \
                .collect()
    spark.stop()
    return [list(x) for x in result]

def get_correlation_data():
    spark, rdd = get_spark_rdd()
    result = rdd.map(lambda row: (row['age'], row['bmi'], row['children'], row['charges'])) \
                .filter(lambda x: None not in x) \
                .collect()
    spark.stop()
    return [list(x) for x in result]
