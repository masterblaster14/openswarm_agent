from typing import Optional, Tuple
from models.discount_code import DiscountCode

class DiscountService:
    def __init__(self):
        self.codes: dict[str, DiscountCode] = {}

    def register_code(self, discount_code: DiscountCode) -> None:
        """Register a new discount code."""
        self.codes[discount_code.code] = discount_code

    def validate_and_apply(
        self,
        code: str,
        subtotal: float
    ) -> Tuple[bool, Optional[float], str]:
        """
        Validate discount code and calculate discount.
        Returns: (success, discount_amount, message)
        """
        if code not in self.codes:
            return False, None, "Discount code not found"

        discount_code = self.codes[code]

        if not discount_code.is_valid():
            if discount_code.expiry_date < __import__('datetime').datetime.now():
                return False, None, "Discount code has expired"
            else:
                return False, None, "Discount code usage limit exceeded"

        discount_amount = discount_code.calculate_discount(subtotal)
        discount_code.usage_count += 1

        return True, discount_amount, "Discount applied successfully"
