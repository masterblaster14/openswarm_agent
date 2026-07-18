# Add discount codes to checkout

Support percentage and fixed-amount discount codes at checkout. Codes have expiry dates and usage limits. Apply before tax. New endpoint POST /checkout/apply-discount.

_Swarm run `run_9f0c3c9c` · 15580 tokens · $0.0293_

## Decisions
- **discount-type-enum** — Discount codes store type as enum: PERCENTAGE | FIXED_AMOUNT, with percentage capped at 0-100 and fixed_amount as decimal(10,2) in base currency. (95%)
- **discount-application-order** — Apply discount codes to subtotal (before tax), store applied_discount_amount on checkout, recalculate tax on (subtotal - discount), return final total = subtotal - discount + tax. (92%)
- **usage-limit-enforcement** — Track usage_count (integer) and max_uses (nullable integer) per code; enforce atomically: SELECT FOR UPDATE on code row, check usage_count < max_uses, increment usage_count in same transaction, reject if limit exceeded. (93%)
- **expiry-validation-timing** — Validate expires_at >= NOW() at POST /checkout/apply-discount time only; do not re-validate at payment processing (assume checkout completes within minutes). (88%)
- **invalid-code-response** — POST /checkout/apply-discount returns 400 with error_code field: INVALID_CODE | EXPIRED | USAGE_LIMIT_EXCEEDED | ALREADY_APPLIED, no generic 'not found' to prevent enumeration. (90%)

## Review: PASS

## Contradictions resolved
- **discount_value data type for FIXED_AMOUNT**: Use Decimal type in Python model to match architect's decimal(10,2) database specification and prevent floating-point precision errors in currency calculations (policy 2)
- **expiry validation timing**: Architect's decision stands: validation occurs only at apply-discount endpoint. The is_valid() method is acceptable but must be called exclusively at POST /checkout/apply-discount, not at payment processing (policy 2)
- **usage_count enforcement mechanism**: Architect's atomic database-level enforcement is required. Implementer's in-memory dict approach is insufficient for production. Implementation must use SELECT FOR UPDATE pattern with database transactions (policy 2)