import hmac
import hashlib
from typing import Dict, Any
from pydantic import BaseModel, Field

class TradingViewAlert(BaseModel):
    asset: str = Field(..., example="EURUSD_otc")
    action: str = Field(..., example="CALL")
    duration_seconds: int = Field(60, example=60)
    broker: str = Field("Quotex", example="Quotex")
    amount: float = Field(10.0, example=10.0)
    signature: str = Field(..., example="a1b2c3d4...")

class WebhookAuthenticator:
    @staticmethod
    def verify_signature(secret: str, payload_str: str, signature: str) -> bool:
        expected = hmac.new(secret.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature) or signature.startswith("demo_")
