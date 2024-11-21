import logging
import azure.functions as func
from azure.functions.decorators.core import DataType
import uuid
import json
import random
import string

app = func.FunctionApp()

# Triggers every 1 - 30 seconds using cron
@app.timer_trigger(schedule="*/1 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)

# Connection to Azure SQL database
@app.generic_output_binding(arg_name="vehicle", type="sql", CommandText="dbo.vehicle", ConnectionStringSetting="SqlConnectionString",data_type=DataType.STRING)
def write_vehicle_info(myTimer: func.TimerRequest, vehicle: func.Out[func.SqlRow]) -> None:
    if myTimer.past_due:
        logging.warning('The timer is past due.')

    logging.info('Python timer trigger function executed.')

    # List of data used to generate vehicle information
    car = ["Aston-Martin", "BMW", "Bentley", "Citroen", "Ford", "Ferrari", "Gumpert", "Honda", "Lexus", "Mercedes", 
       "Mclaren", "Morgan","Porsche", "Toyota", "TVR", "Zenvo", "Unidentified"]
    colour = ["Red", "White", "Black", "Purple", "Silver", "Yellow", "Green", "Brown", "Grey", "Cyan", "Teal", "Orange", 
          "Lime", "Unidentified"]
    
    # Number of speed cameras recording to database - currently set at 6
    for i in range(6): 
        vehicle.set(func.SqlRow({"Id": str(uuid.uuid4()), 
                            # Random car and colour     
                            "car": random.choice(car), 
                            "colour": random.choice(colour), 

                            # 3 random captial letters followed by 3 random digits
                            "licenceplate": ''.join(random.choices(string.ascii_uppercase, k=3) + random.choices(string.digits, k=3)),
                            # Speed between 0 and 100 (mph)
                            "speed": random.uniform(0.0, 100.0)}))
    
        logging.info(f"Database write completed - Camera {i}")
    

# Azure SQL trigger - whenever a new row is added, the function triggers
@app.sql_trigger(arg_name="sqlchange", table_name="vehicle", connection_string_setting="SqlConnectionString")

# Azure Blob Storage - read/write from/to blob storage
# https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-blob-output?tabs=python-v2
@app.blob_input(arg_name="inputblob", path="vehicle/speed-ticket.txt", connection="BlobConnectionString")
@app.blob_output(arg_name="outputblob",path="vehicle/speed-ticket.txt",connection="BlobConnectionString")
def analyse_vehicle_info(sqlchange: str, inputblob: str, outputblob: func.Out[str]) -> None:

    logging.info('Python SQL Trigger executed.')

    data = json.loads(sqlchange)

    for change in data:
        logging.info(change)
        newRow = change["Item"]
        logging.info(newRow)

        # Records speeding vehicles
        if (newRow['speed'] > 70.0):
            speedDifference = newRow['speed'] - 70.0
            logging.info(f"car: {newRow['car']} will be issued a speeding fine")

            # Writes to Blob storage
            outputblob.set(
            f"""{inputblob}
        
            Dear driver,
            You have been issued a speeding fine for going {round(speedDifference,2)} mph over the speed limit (70 mph).
            We have the following details about you:
            - Car: {newRow['colour']} {newRow['car']}
            - Licence plate: {newRow['licenceplate']}
                              
            You fine amount is: £100.00. You have 14 days to pay this."""
            )
