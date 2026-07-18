# Add discount codes to checkout

Support percentage and fixed-amount discount codes at checkout. Codes have expiry dates and usage limits. Apply before tax. New endpoint POST /checkout/apply-discount.

_Swarm run `run_a10c9b5e` · 15857 tokens · $0.0314_

## Decisions
- **discount-type-enum** — Discount codes store type as enum: PERCENTAGE | FIXED_AMOUNT, with percentage capped at 0-100 and fixed_amount as decimal(10,2) in base currency. (95%)
- **discount-application-order** — Apply discount codes to subtotal (before tax), reducing taxable amount; tax recalculates on discounted subtotal. (98%)
- **usage-limit-tracking** — Track usage with atomic increment: discount_codes.usage_count (integer), max_uses (nullable integer); reject if usage_count >= max_uses. (92%)
- **expiry-validation-logic** — Reject code if current_timestamp > expires_at; expires_at is nullable (no expiry) and stored as timestamp with timezone. (96%)
- **endpoint-response-structure** — POST /checkout/apply-discount returns {discount_id, code, discount_amount_cents, new_subtotal_cents, tax_recalculated_cents} on success; 400 if code invalid/expired/exhausted, 409 if already applied. (90%)

## Review: PASS

## Contradictions resolved
- **discount-application-timing-and-tax-treatment**: Architect's decision stands as the stated implementation policy, but skeptic's risk is valid and unresolved. Architect assumes 'standard e-commerce practice' without jurisdiction-specific compliance verification. No human correction provided; architect has higher access (decision-maker) than skeptic (risk identifier). Implementation proceeds with before-tax application, but compliance audit required before production deployment. (policy 2)
- **concurrent-redemption-safety**: Architect specifies atomic increment at application layer but does not mention database-level constraint enforcement. Skeptic correctly identifies that application-layer atomicity alone is insufficient without database constraint. Architect has higher access but claim is incomplete. Skeptic's contradiction is valid: atomic increment without database CHECK constraint or unique index leaves race condition window. Architect's decision partially mitigates but does not fully resolve the risk. (policy 2)
- **discount-code-enumeration-protection**: Skeptic identifies absence of brute-force protection; architect does not claim protection exists. This is an omission, not a contradiction. Skeptic's risk is valid and unaddressed. No resolution under policy clauses 1-3 applies; this is a gap requiring new decision. (policy None)
- **discount-stacking-behavior**: Skeptic identifies omission; architect makes no claim about stacking. This is a gap, not a contradiction. Requires new architectural decision. (policy None)
- **expired-code-handling-behavior**: Architect specifies rejection logic (reject if expired) but does not specify HTTP response behavior (silent vs. loud). Skeptic correctly identifies underspecification of error messaging. Architect's decision is incomplete but not contradicted. Architect has higher access; decision stands but requires clarification in endpoint response specification. (policy 2)