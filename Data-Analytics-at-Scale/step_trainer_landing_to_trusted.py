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
AWSGlueDataCatalog_node1770568974742 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_curated", transformation_ctx="AWSGlueDataCatalog_node1770568974742")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1770568976089 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_landing", transformation_ctx="AWSGlueDataCatalog_node1770568976089")

# Script generated for node SQL Query
SqlQuery0 = '''
select distinct step_trainer_landing.*
from step_trainer_landing
join customer_curated
on step_trainer_landing.serialnumber = customer_curated.serialnumber
'''
SQLQuery_node1770568979844 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"step_trainer_landing":AWSGlueDataCatalog_node1770568976089, "customer_curated":AWSGlueDataCatalog_node1770568974742}, transformation_ctx = "SQLQuery_node1770568979844")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1770568979844, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1770568652447", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1770569238544 = glueContext.getSink(path="s3://andrew-stedi/step_trainer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], compression="snappy", enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1770569238544")
AmazonS3_node1770569238544.setCatalogInfo(catalogDatabase="stedi",catalogTableName="step_trainer_trusted")
AmazonS3_node1770569238544.setFormat("json")
AmazonS3_node1770569238544.writeFrame(SQLQuery_node1770568979844)
job.commit()