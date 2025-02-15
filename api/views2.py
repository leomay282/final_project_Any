from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import logging

#logging.basicConfig(filename='app.log', level=logging.INFO)


from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    session
)

import joblib
import models_loader, input_preprocessor, agregate_columns
from datetime import datetime
import pandas as pd

total_trip_model = models_loader.load_total_trip_model()
duration_trip_model = models_loader.load_duration_trip_model()

app = Flask(__name__)

class TaxiForm(FlaskForm):
    pickUpDateTime = StringField('Pick Up DateTime', validators=[DataRequired()])
    passengersNumber = IntegerField('Number of Passengers', validators=[DataRequired()])
    pickUpId = IntegerField('Pick Up Location ID', validators=[DataRequired()])
    dropOffId = IntegerField('Drop Off Location ID', validators=[DataRequired()])
    paymentMethodId = IntegerField('Payment Method ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route('/', methods=['GET', 'POST'])
def index():
    form = TaxiForm()
    error_message = None
    data = {}
    if form.validate_on_submit():
        print("Formulario validado")  # Debug print

        data = {
            "tpep_pickup_datetime": datetime.strptime(form.pickUpDateTime.data, "%Y-%m-%d %H:%M:%S"),
            "passenger_count": form.passengersNumber.data,
            "PULocationID": form.pickUpId.data,
            "DOLocationID": form.dropOffId.data,
            "payment_type": form.paymentMethodId.data,
            "trips_per_hour": 1200,
            "average_speed_per_hour":20,
            "trip_distance": 20
            #"airport_fee": 1.25, # Hardcoded (to improve)
            #"improvement_surcharge": 0.3 # Hardcoded (to improve)
        }
            
        try:
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
    # Store the results in the session
            session['results_total'] = [round(num, 2) for num in results_total.tolist()]
            session['results_duration'] = [round(num, 2) for num in results_duration.tolist()]
        

            print("Redirigiendo a resultados")  # Debug print

            return redirect(url_for('app_router.results'))#, total=results_total, duration=results_duration))
        except ValueError as ve:
            print(f"Ocurrió un error de valor: {ve}")
            error_message = f"Ocurrió un error de valor: {ve}"
        except TypeError as te:
            print(f"Ocurrió un error de tipo: {te}")
            error_message = f"Ocurrió un error de tipo: {te}"
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            error_message = f"Ocurrió un error inesperado: {e}"
    
    return render_template('index.html', form=form, error=error_message)

@router.route('/results',methods=['GET'])
def results():
    results_total = session.get('results_total')
    results_duration = session.get('results_duration')

    return render_template('results.html', total=results_total, duration=results_duration)