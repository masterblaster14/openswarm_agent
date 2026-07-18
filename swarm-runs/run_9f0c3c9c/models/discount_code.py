from datetime import datetime
from enum import Enum
from typing import Optional

class DiscountType(Enum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"

class DiscountCode:
    def __init__(
        self,
        code: str,
        discount_type: DiscountType,
        discount_value: float,
        expiry_date: datetime,
        usage_limit: Optional[int] = None,
        usage_count: int = 0
    ):
        self.code = code
        self.discount_type = discount_type
        self.discount_value = discount_value
        self.expiry_date = expiry_date
        self.usage_limit = usage_limit
        self.usage_count = usage_count

    def is_valid(self) -> bool:
        """Check if discount code is valid (not expired and within usage limit)."""
        if datetime.now() > self.expiry_date:
            return False
        if self.usage_limit is not None and self.usage_count >= self.usage_limit:
            return False
        return True

    def calculate_discount(self, subtotal: float) -> float:
        """Calculate discount amount based on type."""
        if self.discount_type == DiscountType.PERCENTAGE:
            return subtotal * (self.discount_value / 100)
        elif self.discount_type == DiscountType.FIXED_AMOUNT:
            return self.discount_value
        return 0.0
