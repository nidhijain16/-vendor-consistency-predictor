from pydantic import BaseModel, Field
from typing import Optional

class VendorData(BaseModel):
    vendor_id: int = Field(..., description="Unique identifier for the vendor")
    order_hour: int = Field(..., ge=0, le=23, description="Hour of the day (0-23)")
    day_of_week: int = Field(..., ge=0, le=6, description="Day of the week (0=Monday, 6=Sunday)")
    item_count: int = Field(..., gt=0, description="Number of items in the order")
    is_peak_hour: bool = Field(..., description="Whether the order is placed during peak hours")
    historical_delay_avg: float = Field(..., description="Average historical delay for this vendor in minutes")

    model_config = {
        "json_schema_extra": {
            "example": {
                "vendor_id": 12345,
                "order_hour": 19,
                "day_of_week": 4,
                "item_count": 3,
                "is_peak_hour": True,
                "historical_delay_avg": 5.2
            }
        }
    }

class PredictionResponse(BaseModel):
    vendor_id: int
    predicted_prep_time: float = Field(..., description="Predicted preparation time in minutes")
    confidence_interval_95: Optional[tuple[float, float]] = Field(None, description="95% confidence interval for the prediction")
    feature_importance_top: Optional[str] = Field(None, description="Most influential feature for this prediction")
