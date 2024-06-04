import models_loader
import pandas as pd

def preprocess_input_data(data: pd.DataFrame) -> pd.DataFrame:
    # Carga y aplica el encoder
    try:
        encoder = models_loader.load_encoder()
        if encoder is None:
            raise ValueError("El encoder no se cargó correctamente.")
        data = encoder.transform(data)
    except Exception as e:
        print(f"Error al cargar o aplicar el encoder: {e}")
        return None

    # Carga y aplica el imputer
    try:
        imputer = models_loader.load_imputer()
        if imputer is None:
            raise ValueError("El imputer no se cargó correctamente.")
        data = imputer.transform(data)
    except Exception as e:
        print(f"Error al cargar o aplicar el imputer: {e}")
        return None

    # Carga y aplica el scaler
    try:
        scaler = models_loader.load_scaler()
        if scaler is None:
            raise ValueError("El scaler no se cargó correctamente.")
        data = scaler.transform(data)
    except Exception as e:
        print(f"Error al cargar o aplicar el scaler: {e}")
        return None

    return data
