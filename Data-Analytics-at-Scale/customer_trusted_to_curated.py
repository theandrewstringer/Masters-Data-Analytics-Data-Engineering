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
AWSGlueDataCatalog_node1770567672297 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_trusted", transformation_ctx="AWSGlueDataCatalog_node1770567672297")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1770567675133 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_trusted", transformation_ctx="AWSGlueDataCatalog_node1770567675133")

# Script generated for node SQL Query
SqlQuery0 = '''
select distinct customer_trusted.* 
from customer_trusted
join accelerometer_trusted
on customer_trusted.email = accelerometer_trusted.user
'''
SQLQuery_node1770567681132 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"customer_trusted":AWSGlueDataCatalog_node1770567675133, "accelerometer_trusted":AWSGlueDataCatalog_node1770567672297}, transformation_ctx = "SQLQuery_node1770567681132")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1770567681132, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1770567441834", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1770568143431 = glueContext.getSink(path="s3://andrew-stedi/customer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], compression="snappy", enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1770568143431")
AmazonS3_node1770568143431.setCatalogInfo(catalogDatabase="stedi",catalogTableName="customer_curated")
AmazonS3_node1770568143431.setFormat("json")
AmazonS3_node1770568143431.writeFrame(SQLQuery_node1770567681132)
job.commit()