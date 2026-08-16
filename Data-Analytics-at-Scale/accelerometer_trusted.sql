CREATE EXTERNAL TABLE `accelerometer_trusted`(
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
  's3://andrew-stedi/accelerometer/trusted/'
TBLPROPERTIES (
  'CreatedByJob'='accelerometer_landing_to_trusted', 
  'CreatedByJobRun'='jr_177c48ba71b5ab8e7781501ca9081e6b0f8be9a02058d9df2a62470579b97c0d', 
  'classification'='json')