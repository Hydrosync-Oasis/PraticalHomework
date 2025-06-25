from pyspark.sql import SparkSession
import sys, os

python_path = sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['PYSPARK_DRIVER_PYTHON'] = python_path

# 全局变量存储 SparkSession 单例
spark = None


def get_spark_session():
    global spark
    if spark is None:
        # 构建项目根目录路径（即 Backend/）
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        csv_path = os.path.join(BASE_DIR, 'data', 'insurance.csv')  # Backend/data/insurance.csv

        spark = SparkSession.builder \
            .appName("Insurance Visual Data RDD") \
            .master("local[*]") \
            .getOrCreate()

        # 读取 CSV，缓存 DataFrame 以提升后续性能
        spark.df = spark.read.csv(csv_path, header=True, inferSchema=True).cache()

        # 转为 RDD
        spark.rdd = spark.df.rdd
    return spark


def get_boxplot_data():
    spark = get_spark_session()
    result = spark.rdd.map(lambda row: (row['smoker'], row['charges'])) \
        .filter(lambda x: None not in x) \
        .groupByKey() \
        .mapValues(list) \
        .collect()
    return {k: list(v) for k, v in result}


def get_scatter_bmi_charges():
    spark = get_spark_session()
    result = spark.rdd.map(lambda row: (row['bmi'], row['charges'])) \
        .filter(lambda x: None not in x) \
        .collect()
    return [list(x) for x in result]


def get_age_histogram():
    spark = get_spark_session()
    result = spark.rdd.map(lambda row: row['age']) \
        .filter(lambda x: x is not None) \
        .collect()
    return result


def get_region_avg_charges():
    spark = get_spark_session()
    result = spark.rdd.map(lambda row: (row['region'], (row['charges'], 1))) \
        .filter(lambda x: x[0] is not None and x[1][0] is not None) \
        .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) \
        .mapValues(lambda x: round(x[0] / x[1], 2)) \
        .collect()
    return dict(result)


def get_scatter_age_charges_smoker():
    spark = get_spark_session()
    result = spark.rdd.map(lambda row: (row['age'], row['charges'], row['smoker'])) \
        .filter(lambda x: None not in x) \
        .collect()
    return [list(x) for x in result]


def get_correlation_data():
    spark = get_spark_session()
    result = spark.rdd.map(lambda row: (row['age'], row['bmi'], row['children'], row['charges'])) \
        .filter(lambda x: None not in x) \
        .collect()
    return [list(x) for x in result]


def stop_spark():
    global spark
    if spark is not None:
        spark.stop()
        spark = None
