# AWS Micro ETL pipeline



## Requirements 
- ETL process to match this target data model - https://dbdiagram.io/d/62268eff61d06e6eadbc43bc
  - Given the limited time, I completed the normalization of data in the file using lambda for tables user, user_profile, role_profile and role_profile_type, with the understanding that these could be extended for the remaining tables in the data model. 
  - The reason I chose lambda is because the file is small in size. Depending on the use case, I would recommend a different solution.
  - I scheduled the lambda to run every 15 minutes (an assumption). Again, depending on the use case my answer changes.
  - I made some assumptions about what could go in some of the incrementing primary keys given the limited scope and time as well as certain columns like updated, updated by and created, created_by.
  - [Code](aws_micro_etl_sample.ipynb): I stored the resulting dataframes for these tables as CSV files in separate S3 buckets, so that it would be easier to connect with Athena for querying and AWS Glue for ETL to conform to any constraints or tranformations that may be necessary.
  
- [Diagram](Kriti-Aspen-capital.png)


## AWS Free Tier offerings used:
- AWS S3: for data lake to Athena pipeline
- AWS Lambda: for micro-ETL
- AWS SAM: for building the environment, and scheduling the Lambda handler
- AWS Athena: to query resulting CSVs
- AWS Glue: to test out inserting rows into tables.


To review these, I am happy to share my screen during the interview or provide access to specific people on an ad-hoc basis. Currently, I have deleted some of the resources to avoid accidentally incurring charges.

## Recommended solution for database migration from on prem:
Since the source database is hosted on SQL Server and not a few Excel files, my code is not the solution. 
I recommend using AWS Database Migration Service to migrate to RDS, which the team may already be using.

For this we would need:
1. To create an SQL Server Database Instance in Amazon RDS.
2. Create a replication instance in DMS.
3. Create source and target endpoints for the migration.
4. Create a replication task: I would recommend a single task of full load plus CDC for the simplicity but since replication on both on-prem and AWS is desirable, we would have to create bidirectional replication tasks from the SQL Server instance to the RDS instance. This can be done by:
    (i)



## License

This library is licensed under the MIT-0 License. See the LICENSE file.
