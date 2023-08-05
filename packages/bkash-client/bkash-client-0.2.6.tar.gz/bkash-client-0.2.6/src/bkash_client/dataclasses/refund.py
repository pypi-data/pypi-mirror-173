from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .base import BasePaymentIDRequest


class RefundRequest(BaseModel):
    amount: Decimal
    paymentID: str
    trxID: str
    sku: str
    reason: str


class RefundResponse(BaseModel):
    completedTime: str
    originalTrxID: str
    refundTrxID: str
    transactionStatus: str
    amount: Decimal
    currency: str
    charge: Optional[str]


class RefundStatusRequest(BasePaymentIDRequest):
    trxID: str


class RefundStatusResponse(RefundResponse):
    pass
