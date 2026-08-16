import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1770570517227 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_trusted", transformation_ctx="AWSGlueDataCatalog_node1770570517227")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1770570516381 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_trusted", transformation_ctx="AWSGlueDataCatalog_node1770570516381")

# Script generated for node SQL Query
SqlQuery0 = '''
select step_trainer_trusted.*, accelerometer_trusted.*
from step_trainer_trusted
inner join accelerometer_trusted
on step_trainer_trusted.sensorreadingtime = accelerometer_trusted.timestamp
'''
SQLQuery_node1770570522446 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"step_trainer_trusted":AWSGlueDataCatalog_node1770570517227, "accelerometer_trusted":AWSGlueDataCatalog_node1770570516381}, transformation_ctx = "SQLQuery_node1770570522446")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1770570522446, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1770570207520", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1770571039014 = glueContext.getSink(path="s3://andrew-stedi/step_trainer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], compression="snappy", enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1770571039014")
AmazonS3_node1770571039014.setCatalogInfo(catalogDatabase="stedi",catalogTableName="machine_learning_curated")
AmazonS3_node1770571039014.setFormat("json")
AmazonS3_node1770571039014.writeFrame(SQLQuery_node1770570522446)
job.commit()