CREATE EXTERNAL TABLE `step_trainer_trusted`(
  `sensorreadingtime` bigint COMMENT 'from deserializer', 
  `serialnumber` string COMMENT 'from deserializer', 
  `distancefromobject` bigint COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
WITH SERDEPROPERTIES ( 
  'paths'='distanceFromObject,sensorReadingTime,serialNumber') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://andrew-stedi/step_trainer/trusted/'
TBLPROPERTIES (
  'CreatedByJob'='step_trainer_landing_to_trusted', 
  'CreatedByJobRun'='jr_bc8277c090e62361d054073b802589c28e90c6ec9e2f3c150a025b3190e92ec9', 
  'classification'='json')