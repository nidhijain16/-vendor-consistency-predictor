import xgboost as xgb
import pandas as pd
import numpy as np
import os
import joblib
from functools import lru_cache

class VendorConsistencyModel:
    def __init__(self, model_path: str = "model.json"):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        """
        Loads the XGBoost model. 
        If no model file exists, creates a dummy model for demonstration purposes.
        """
        if os.path.exists(self.model_path):
            self.model = xgb.Booster()
            self.model.load_model(self.model_path)
            print(f"Loaded model from {self.model_path}")
        else:
            print(f"Model file {self.model_path} not found. Initializing dummy model for demo.")
            # Create a simple dummy model
            X = pd.DataFrame(np.random.rand(100, 5), columns=['order_hour', 'day_of_week', 'item_count', 'is_peak_hour', 'historical_delay_avg'])
            y = X['item_count'] * 2 + X['historical_delay_avg'] + np.random.normal(0, 1, 100)
            
            dtrain = xgb.DMatrix(X, label=y)
            params = {
                'objective': 'reg:squarederror',
                'max_depth': 3,
                'eta': 0.1
            }
            self.model = xgb.train(params, dtrain, num_boost_round=10)

    def predict(self, input_data: pd.DataFrame) -> float:
        """
        Runs inference on the input data.
        """
        if not self.model:
            raise RuntimeError("Model not loaded")
        
        # Ensure column order matches training data
        # In a real scenario, this would be strictly enforced via the feature pipeline
        dtest = xgb.DMatrix(input_data)
        prediction = self.model.predict(dtest)
        return float(prediction[0])

@lru_cache()
def get_model():
    return VendorConsistencyModel()
