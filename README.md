# AWS Micro ETL pipeline



## Requirements 
- ETL process to match this target data model - https://dbdiagram.io/d/62268eff61d06e6eadbc43bc
  - Given the limited time, I completed the normalization of data in the file using lambda for tables user, user_profile, role_profile and role_profile_type, with the understanding that these could be extended for the remaining tables in the data model. 
  - The reason I chose lambda is because the file is small in size. Depending on the use case, I would recommend a different solution.
  - I scheduled the lambda to run every 15 minutes (an assumption). Again, depending on the use case my answer changes.
  - I made some assumptions about what could go in some of the incrementing primary keys given the limited scope and time as well as certain columns like updated, updated by and created, created_by.
  - I stored the resulting dataframes for these tables as CSV files in separate S3 buckets, so that it would be easier to connect with Athena for querying and AWS Glue for ETL to conform to any constraints or tranformations that may be necessary.
  



## AWS Free Tier offerings used:
- AWS S3: for data lake to Athena pipeline
- AWS Lambda: for micro-ETL
- AWS SAM: for building the environment, and scheduling the Lambda handler
- AWS Athena: to query resulting CSVs
- AWS Glue: just to test out insertions into tables



## License

This library is licensed under the MIT-0 License. See the LICENSE file.
