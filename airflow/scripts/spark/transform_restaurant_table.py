from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T

spark = SparkSession.builder.enableHiveSupport().getOrCreate()

df = spark.read.csv('/home/spark/restaurant_detail/part-m-00000', header=False)
rename = {
    '_c0' : 'id',
    '_c1' : 'restaurant_name',
    '_c2' : 'category',
    '_c3' : 'estimated_cooking_time',
    '_c4' : 'latitude',
    '_c5' : 'longitude',
}
df = df.toDF(*[rename[c] for c in df.columns])
df = df.withColumn('estimated_cooking_time', F.col('estimated_cooking_time').cast(T.FloatType()))
df = df.withColumn('latitude', F.col('latitude').cast(T.DecimalType(11,8)))
df = df.withColumn('longitude', F.col('longitude').cast(T.DecimalType(11,8)))
df = df.withColumn('dt', F.lit("latest"))
df.write.parquet('/home/spark/transformed_restaurant_detail', partitionBy='dt', mode='overwrite')

# df.show(1, vertical=True, truncate=False)