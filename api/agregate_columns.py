import pandas as pd


def agregate_columns_to_input(data: pd.DataFrame):
    # Replace tpep_pickup_datetime and tpep_dropoff_datetime columns with new columns
    data["pickup_year"] = data["tpep_pickup_datetime"].dt.year # si
    data["pickup_day"] = data["tpep_pickup_datetime"].dt.day # si
    data["pickup_hour"] = data["tpep_pickup_datetime"].dt.hour # si
    data["pickup_minute"] = data["tpep_pickup_datetime"].dt.minute # si
    data["pickup_day_of_week"] = data["tpep_pickup_datetime"].dt.dayofweek # si

    #data["average_speed_mph"] = 2 # si esta mal!

    def drop_column_if_exists(data, column_name):
        if column_name in data.columns:
         data.drop(column_name, inplace=True, axis=1)

    # Luego puedes llamar a esta función para cada columna que quieras eliminar
        drop_column_if_exists(data, "tip_amount")
        drop_column_if_exists(data, "extra")
        drop_column_if_exists(data, "improvement_surcharge")
        drop_column_if_exists(data, "fare_amount")
        drop_column_if_exists(data, "VendorID")
        drop_column_if_exists(data, "store_and_fwd_flag")
        #drop_column_if_exists(data, "trip_distance")
        drop_column_if_exists(data, "RatecodeID")
        drop_column_if_exists(data, "tolls_amount")
        drop_column_if_exists(data, "tpep_pickup_datetime")


    return data
