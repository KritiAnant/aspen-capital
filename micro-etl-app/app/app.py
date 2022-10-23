#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#


import boto3
import logging
import pandas as pd
import os
import requests
import io
import boto3
import datetime

# Environment variables
S3_BUCKET = os.environ['S3Bucket']
LOG_LEVEL = os.environ['LogLevel']

# Log settings
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


# Lambda function handler
def lambda_handler(event, context):
    logger.info('## EVENT')
    logger.info(event)


    # ## Read file

    # In[2]:

    s3 = boto3.client(
        's3',
        aws_access_key_id='*********',
        aws_secret_access_key='**************'
    )

    # In[3]:

    obj = s3.get_object(
        Bucket='aspen-capital-raw-data',
        Key='data_engineer_raw_data.xlsx')

    # In[4]:

    data = obj['Body'].read()
    # print(data)
    borrower = pd.read_excel(data, engine='openpyxl', sheet_name='borrower')
    # display(borrower.head())

    # In[5]:

    role_profile = pd.read_excel(data, engine='openpyxl', sheet_name='role_profile')
    # display(role_profile.head())

    # # ETL

    # ### USER_PROFILE

    # In[6]:

    user_profile_df = borrower.copy()
    user_profile_df = user_profile_df.rename(columns={"id": "user_profile_id"})
    user_profile_df = user_profile_df[user_profile_df['user_profile_id'].notna()]
    user_profile_df = user_profile_df[user_profile_df['full_name'].notna()]
    user_profile_df[['first_name', 'last_name']] = user_profile_df.full_name.str.split(n=1, expand=True)
    user_profile_df['created_date'] = datetime.datetime.now()
    user_profile_df['created_by'] = 'Kriti'
    user_profile_df.drop(['full_name', 'street', 'city', 'state', 'zip_code', 'phone_cell', 'email'], axis=1,
                         inplace=True)
    user_profile_df['updated_date'] = datetime.datetime.now()
    user_profile_df['updated_by'] = 'Kriti'
    # user_profile_df.head()

    # In[7]:

    csv_buffer = io.StringIO()
    user_profile_df.to_csv(csv_buffer)

    s3_resource = boto3.resource('s3')
    s3_resource.Object('aspen-capital-user-profile', 'user_profile.csv').put(Body=csv_buffer.getvalue());

    # ### USER

    # In[8]:

    user_df = user_profile_df.copy()
    user_df['user_id'] = user_df.index
    user_df.drop(['first_name', 'last_name'], axis=1, inplace=True)
    user_df = user_df.rename(columns={"created_date": "created", "updated_date": "updated"})
    # user_df.head()

    # In[9]:

    csv_buffer = io.StringIO()
    user_df.to_csv(csv_buffer)

    s3_resource = boto3.resource('s3')
    s3_resource.Object('aspen-capital-user', 'user.csv').put(Body=csv_buffer.getvalue());

    # ### ROLE_PROFILE_TYPE
    #
    #

    # In[10]:

    role_profile_type_df = role_profile.copy()
    role_profile_type_df = role_profile_type_df.rename(
        columns={"borrower_id": "role_profile_type_id", "role_profile": "type"})
    role_profile_type_df['created'] = datetime.datetime.now()
    role_profile_type_df['created_by'] = 'Kriti'
    role_profile_type_df['updated'] = datetime.datetime.now()
    role_profile_type_df['updated_by'] = 'Kriti'
    # role_profile_type_df.head()

    # In[11]:

    csv_buffer = io.StringIO()
    role_profile_type_df.to_csv(csv_buffer)

    s3_resource = boto3.resource('s3')
    s3_resource.Object('aspen-capital-role-profile-type', 'role-profile_type.csv').put(Body=csv_buffer.getvalue());

    # ### ROLE_PROFILE

    # In[12]:

    role_profile_df = pd.DataFrame(user_df.loc[:, ['user_profile_id', 'user_id']].set_index('user_profile_id')
                                   ).join(role_profile_type_df.set_index('role_profile_type_id'), how='outer')
    # pd.concat([user_df.loc[:,['user_profile_id','user_id']].set_index('user_profile_id'), role_profile_type_df.set_index('role_profile_type_id')], axis=1).reset_index()
    role_profile_df['role_profile_type_id'] = role_profile_df.index
    role_profile_df = role_profile_df.reset_index()
    role_profile_df['role_profile_id'] = role_profile_df.index
    role_profile_df = role_profile_df.drop(['type', 'created', 'created_by', 'updated', 'updated_by', 'index'], axis=1)
    role_profile_df['created'] = datetime.datetime.now()
    role_profile_df['created_by'] = 'Kriti'
    role_profile_df['updated'] = datetime.datetime.now()
    role_profile_df['updated_by'] = 'Kriti'
    # role_profile_df.head()

    # In[13]:

    csv_buffer = io.StringIO()
    role_profile_df.to_csv(csv_buffer)

    s3_resource = boto3.resource('s3')
    s3_resource.Object('aspen-capital-role-profile', 'role_profile.csv').put(Body=csv_buffer.getvalue());
    
