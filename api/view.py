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
            "payment_type": payload["paymentMethodId"],
            "airport_fee": 1.25,  # Hardcoded (to improve)
            "improvement_surcharge": 0.3,  # Hardcoded (to improve)
            "trip_distance": payload["distanceInMiles"],
        }

        data = pd.DataFrame(data, index=[0])
        df = agregate_columns.agregate_columns_to_input(data)
        df = input_preprocessor.preprocess_input_data(df)

        results_total = total_trip_model.predict(df)
        results_duration = duration_trip_model.predict(df)

        return (
            jsonify(
                {
                    "amount": f"${results_total[0]}",
                    "duration": f"{results_duration[0]} min",
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