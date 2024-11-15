import logging
import azure.functions as func
from azure.functions.decorators.core import DataType
import uuid
import json

app = func.FunctionApp()


@app.timer_trigger(schedule="*/10 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
@app.generic_output_binding(arg_name="vehicle", type="sql", CommandText="dbo.vehicle", ConnectionStringSetting="SqlConnectionString",data_type=DataType.STRING)
def write_vehicle_info(myTimer: func.TimerRequest, vehicle: func.Out[func.SqlRow]) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    vehicle.set(func.SqlRow({"Id": str(uuid.uuid4()), "car": "Porsche", "colour": "blue", "licenceplate": "MS1435", "speed": 100.3}))

@app.sql_trigger(arg_name="sqlchange", table_name="vehicle", connection_string_setting="SqlConnectionString")
def analyse_vehicle_info(sqlchange: str) -> None:
    logging.info("SQL Changes: %s", json.loads(sqlchange))