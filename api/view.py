from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

import joblib
import models_loader, input_preprocessor, agregate_columns
from datetime import datetime
import pandas as pd
import json
from datetime import datetime
import config 

router = Blueprint("app_router", __name__)
total_trip_model = models_loader.load_total_trip_model()
duration_trip_model = models_loader.load_duration_trip_model()


@router.route("/predict", methods=["POST"])
def predict():
    """
    POST: Used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    error_message = ""

    try:
        payload = request.get_json()

        print("payload1")
        print("payload", payload)
        print("Dictionary attribute names:", list(payload.keys()))
        print("payload.paymentMethodId:", payload["paymentMethodId"])

        """
        payload: 
        pickUpDateTime: string;
        dropOffId: number;
        passengersNumber: number;
        pickUpId: number;
        paymentMethodId: number;
        """
        data = {
            "tpep_pickup_datetime": datetime.strptime(
                payload["pickUpDateTime"], "%Y-%m-%d %H:%M:%S"
            ),
            "passenger_count": payload["passengersNumber"],
            "PULocationID": payload["pickUpId"],
            "DOLocationID": payload["dropOffId"],
            "payment_type": payload["paymentMethodId"]
            
        }

        # Asumiendo que 'pickupdatetime' es una cadena de fecha y hora
        pickupdatetime = data["tpep_pickup_datetime"]
        print('aca')
        print(type(pickupdatetime))
        pickup_hour= pickupdatetime.hour
        # Extrae la hora de 'pickupdatetime'
        #pickup_hour = datetime.strptime(pickupdatetime, "%Y-%m-%d %H:%M:%S").hour

        # Carga el archivo JSON
        with open(config.TRIPS_PER_HOURS, 'r') as f:
            valores_unicos_trips_per_hour = json.load(f)

            # Obtiene 'trips_per_hour' para 'pickup_hour'
        trips_per_hour = valores_unicos_trips_per_hour.get(str(pickup_hour), 0)

        data["trips_per_hour"]=trips_per_hour
        
        # Carga el archivo JSON
        with open(config.AVERAGE_SPEED_PER_HOURS, 'r') as f:
            valores_unicos_average_speed_per_hour = json.load(f)

            # Obtiene 'trips_per_hour' para 'pickup_hour'
        avs_per_hour = valores_unicos_average_speed_per_hour.get(str(pickup_hour), 0)

        data["average_speed_per_hour"]=avs_per_hour

        #"airport_fee": 1.25,  # Hardcoded (to improve)
        #"improvement_surcharge": 0.3,  # Hardcoded (to improve)

        data = pd.DataFrame(data, index=[0])
        data = agregate_columns.agregate_columns_to_input(data)

            # Asumiendo que 'app_train' es tu DataFrame
            # y 'columnas_ordenadas' es una lista con los nombres de las columnas en el orden que deseas

        columnas_ordenadas = ['passenger_count', 'trip_distance', 'PULocationID', 'DOLocationID', 
                                    'payment_type', 'pickup_year','pickup_day', 'pickup_day_of_week', 'pickup_minute', 'trips_per_hour',
                                    'average_speed_per_hour']  # reemplaza esto con tu orden deseado

        data = data.reindex(columns=columnas_ordenadas)

        columns_to_convert = ['VendorID', 'RatecodeID','PULocationID', 'DOLocationID', 'payment_type']
        def convert_columns_to_object2(data: pd.DataFrame, columns_to_convert: list) -> pd.DataFrame:
                for column in columns_to_convert:
                    if column in data.columns:
                        data[column] = data[column].astype('object')
                return data

        data = convert_columns_to_object2(data, columns_to_convert)

        data = input_preprocessor.preprocess_input_data(data)

        results_total = total_trip_model.predict(data)
        results_duration = duration_trip_model.predict(data)

        return (
            jsonify(
                {
                    "amount": f"${round(results_total[0],2)}",

                    "duration": f"{results_duration[0]:.2f}",
                }
            ),
            200,
        )

    except ValueError as ve:
        print(f"Ocurrió un error de valor: {ve}")
        error_message = f"Ocurrió un error de valor: {ve}"
    except TypeError as te:
        print(f"Ocurrió un error de tipo: {te}")
        error_message = f"Ocurrió un error de tipo: {te}"
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        error_message = f"Ocurrió un error inesperado: {e}"
    return (
        jsonify(
            {
                "error": f"${error_message}",
            }
        ),
        500,
    )