# Add discount codes to checkout

Support percentage and fixed-amount discount codes at checkout. Codes have expiry dates and usage limits. Apply before tax. New endpoint POST /checkout/apply-discount.

_Swarm run `run_a57e2aca` · 15792 tokens · $0.0312_

## Decisions
- **discount-type-enum** — Discount codes store type as enum: PERCENTAGE | FIXED_AMOUNT, not string or boolean. (95%)
- **discount-application-timing** — Apply discount codes to subtotal *before* tax calculation; tax is computed on (subtotal - discount). (92%)
- **code-validation-endpoint-response** — POST /checkout/apply-discount returns {code, type, value, discountAmount, newSubtotal, expiresAt, remainingUses} with 400 for invalid/expired/exhausted codes. (90%)
- **usage-limit-enforcement** — Enforce usage limits via database row-level lock or atomic decrement during POST /checkout/apply-discount; reject if remaining_uses ≤ 0. (88%)
- **expiry-date-comparison** — Store expires_at as UTC timestamp; reject code if current_time > expires_at (inclusive of expiry date end). (93%)

## Review: PASS
