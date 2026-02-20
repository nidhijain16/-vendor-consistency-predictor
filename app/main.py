from fastapi import FastAPI, Depends, HTTPException
import pandas as pd
import time
from app.schemas import VendorData, PredictionResponse
from app.model import get_model, VendorConsistencyModel

app = FastAPI(
    title="Vendor Consistency Predictor",
    description="Predicts food preparation time variance using XGBoost.",
    version="0.1.0"
)

# Using XGBoost for initial rollout to prioritize interpretability.
# Stakeholders need to see feature importance (e.g., historical vendor delay)
# before moving to black-box PyTorch models.
@app.post("/predict/prep-time", response_model=PredictionResponse)
async def predict_delay(data: VendorData, model: VendorConsistencyModel = Depends(get_model)):
    """
    Predicts the preparation time delay for a given vendor and order context.
    """
    start_time = time.time()
    
    # Feature engineering simulation (convert Pydantic model to DataFrame)
    # In production, this might involve fetching real-time features from a feature store
    input_df = pd.DataFrame([data.model_dump()])
    
    # Ensure correct column ordering for XGBoost
    feature_cols = ['order_hour', 'day_of_week', 'item_count', 'is_peak_hour', 'historical_delay_avg']
    input_df = input_df[feature_cols]

    try:
        prediction = model.predict(input_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model inference failed: {str(e)}")

    # Calculate latency (simulated monitoring)
    latency_ms = (time.time() - start_time) * 1000
    
    # In a real system, we would log latency_ms to Prometheus/Datadog here
    print(f"Inference latency: {latency_ms:.2f}ms")

    return PredictionResponse(
        vendor_id=data.vendor_id,
        predicted_prep_time=prediction,
        confidence_interval_95=None,  # Placeholder for future implementation
        feature_importance_top="historical_delay_avg" # Placeholder
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
