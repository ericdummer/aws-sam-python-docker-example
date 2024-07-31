import json
import os
import re
import boto3
import math
import logging
import time
import uuid
from botocore.exceptions import ClientError  # For handling AWS service-related errors
from datetime import datetime
from datetime import date
import random
# from services.db_service import DbService


logger = logging.getLogger(__name__)  # Create a logger for your function
logger.setLevel(os.environ.get("APPLICATION_LOG_LEVEL", "INFO"))

def lambda_handler(event, context):
    # if it is not the begining of a quarter, do nothing
    event_bus_name = os.environ.get("EVENT_BUS")
    # detail_type = "NEW_QUARTER"
    # logger.debug(event_bus_name)
    # bodies = get_event_bodies(event_bus_name, detail_type)
    # logger.debug(json.dumps(bodies, indent=4))
    # response = push_events_to_event_bus(bodies)
    # print(json.dumps(response, indent=4))

    today = date.today()
    # if not is_begining_of_quarter(today):
    #     return {
    #         "statusCode": 200,
    #         "body": json.dumps({
    #             "message":  "Not the begining of a quarter"
    #         })
    #     }

    last_qtr = last_month_of_previous_quarter(today.month)
    last_year = today.year - 1 if today.month < 4 else today.year
    tax_periods_query = get_query([last_qtr], [last_year])

    print(tax_periods_query)

    return {"TESTING": "TESTING"}

    lambda_response_message = "Transcripts created successfully"
    return {
        "statusCode": 200,
        "body": json.dumps({    
            "message":  lambda_response_message
        })
    }

def is_begining_of_quarter(today):
    if today.month == 1 or today.month == 4 or today.month == 7 or today.month == 10:
        return True
    return False

def last_month_of_previous_quarter(current_month):
    if current_month < 1 or current_month > 12:
        raise ValueError("Invalid month. Must be between 1 and 12.")
    # Define the quarters
    quarters = {
        1: 12,  # December of the previous year
        2: 12,  # December of the previous year
        3: 12,  # December of the previous year
        4: 3,   # March
        5: 3,   # March
        6: 3,   # March
        7: 6,   # June
        8: 6,   # June
        9: 6,   # June
        10: 9,  # September
        11: 9,  # September
        12: 9   # September
    }
    # Return the last month of the previous quarter
    return quarters[current_month]



def push_events_to_event_bus(event_bodies):
    event_bus = boto3.client('events')
    response = None
    print (json.dumps(event_bodies, indent=4))
    batch_size = 10
    for i in range(0, len(event_bodies), batch_size):
        batch = event_bodies[i:i+batch_size]
        response = event_bus.put_events(
            Entries=batch
        )
        print(json.dumps(batch, indent=4))
        print(json.dumps(response, indent=4))
    return response

def get_event_bodies(event_bus_name, event_name):
    event_bodies = []
    years = [2020,2021,2022,2023]
    tax_periods = [3,6,9,12]
    random_entry_count = 200
    all_details = []
    for _ in range(random_entry_count):
        random_year = years[math.floor(random.random() * len(years))]
        random_tax_period = tax_periods[math.floor(random.random() * len(tax_periods))]
        detail = {
            "account_uuid": str(uuid.uuid4()),
            "irs_product": 'ACTR',
            "irs_form": "941",
            "tax_period": random_tax_period,
            "year": random_year
        }
        all_details.append(detail)
    
    for event_details in all_details:
        event_bodies.append({
            'EventBusName': event_bus_name,
            'Source': 'com.tm.daily.transcripts.create',
            'DetailType': event_name,
            'Detail': json.dumps(event_details)
        })
    return event_bodies

def build_tax_periods_query(years, tax_periods):
    if not years:
        raise ValueError("The years list cannot be empty")
    if not tax_periods:
        raise ValueError("The tax periods list cannot be empty")

    # Generate the SQL query
    select_statements = []
    for year in years:
        for period in tax_periods:
            select_statements.append(f"SELECT {year} AS year, {period} AS tax_period")
    
    sql_query = "WITH tax_periods AS (\n  " + " UNION\n  ".join(select_statements) + "\n)"

    return sql_query

def get_query(years, tax_periods):
    tax_periods_query = build_tax_periods_query(years, tax_periods)
    return tax_periods_query

def get_subscriptions_without_transcripts():
    # dbService = DbService.instance()
    pass