import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame

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
AWSGlueDataCatalog_node1770566285931 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_trusted", transformation_ctx="AWSGlueDataCatalog_node1770566285931")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1770566293146 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_landing", transformation_ctx="AWSGlueDataCatalog_node1770566293146")

# Script generated for node Join
AWSGlueDataCatalog_node1770566293146DF = AWSGlueDataCatalog_node1770566293146.toDF()
AWSGlueDataCatalog_node1770566285931DF = AWSGlueDataCatalog_node1770566285931.toDF()
Join_node1770566298780 = DynamicFrame.fromDF(AWSGlueDataCatalog_node1770566293146DF.join(AWSGlueDataCatalog_node1770566285931DF, (AWSGlueDataCatalog_node1770566293146DF['user'] == AWSGlueDataCatalog_node1770566285931DF['email']), "leftsemi"), glueContext, "Join_node1770566298780")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=Join_node1770566298780, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1770566271843", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1770566571730 = glueContext.getSink(path="s3://andrew-stedi/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], compression="snappy", enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1770566571730")
AmazonS3_node1770566571730.setCatalogInfo(catalogDatabase="stedi",catalogTableName="accelerometer_trusted")
AmazonS3_node1770566571730.setFormat("json")
AmazonS3_node1770566571730.writeFrame(Join_node1770566298780)
job.commit()