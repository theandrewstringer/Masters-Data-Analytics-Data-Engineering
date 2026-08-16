CREATE EXTERNAL TABLE `machine_learning_curated`(
  `sensorreadingtime` bigint COMMENT 'from deserializer', 
  `serialnumber` string COMMENT 'from deserializer', 
  `distancefromobject` bigint COMMENT 'from deserializer', 
  `user` string COMMENT 'from deserializer', 
  `timestamp` bigint COMMENT 'from deserializer', 
  `x` float COMMENT 'from deserializer', 
  `y` float COMMENT 'from deserializer', 
  `z` float COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://andrew-stedi/step_trainer/curated/'
TBLPROPERTIES (
  'CreatedByJob'='step_trainer_trusted_to_curated', 
  'CreatedByJobRun'='jr_a9bec193d29d9ea30a0b274e19d6e3ba7bcad20d4b82e931f325125c0953334b', 
  'classification'='json')