# Add discount codes to checkout

Support percentage and fixed-amount discount codes at checkout. Codes have expiry dates and usage limits. Apply before tax. New endpoint POST /checkout/apply-discount.

_Swarm run `run_2c124ed6` · 15425 tokens · $0.0294_

## Decisions
- **discount-type-enum** — Discount codes store type as enum: PERCENTAGE | FIXED_AMOUNT, not string or boolean. (95%)
- **discount-application-timing** — Apply discount codes to subtotal *before* tax calculation; tax is computed on (subtotal - discount). (92%)
- **code-validation-endpoint-response** — POST /checkout/apply-discount returns {code, type, value, discountAmount, newSubtotal, expiresAt, remainingUses} with 400 if code invalid/expired/exhausted. (90%)
- **usage-limit-enforcement** — Enforce usage limits with atomic database decrement (e.g. SQL UPDATE ... WHERE uses_remaining > 0) at apply-time, not at order-creation. (88%)
- **expiry-check-scope** — Check code expiry date (expiresAt <= NOW()) on every apply-discount call and at order-finalization; reject if expired at either point. (85%)

## Review: PASS

## Contradictions resolved
- **discount-application-timing**: Architect's decision stands as the primary design choice, but skeptic's risk is valid and requires mitigation. Implementation must include: (1) configurable tax-calculation mode per jurisdiction, (2) documentation that pre-discount taxation is default but post-discount taxation must be available for compliance, (3) legal review before production deployment. Skeptic's concern does not contradict the decision itself but identifies a compliance gap requiring additional controls. (policy 2)
- **usage-limit-enforcement-timing**: Architect's decision specifies *when* to enforce (apply-time) but does not specify *scope* (per-user/global). These are orthogonal concerns. Architect's atomic decrement approach is sound for preventing overselling at the chosen enforcement point. Skeptic correctly identifies that scope must be explicitly defined in implementation. No contradiction; skeptic identifies missing specification detail. (policy 2)
- **expiry-check-scope**: Architect's decision specifies the logic (check at two points); skeptic identifies an implementation risk (clock skew). These are not contradictory. Architect's decision is correct; skeptic's risk requires mitigation via: (1) UTC-only server timestamps, (2) NTP synchronization, (3) test coverage for timezone edge cases. No contradiction detected. (policy 2)