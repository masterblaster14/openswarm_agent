from flask import Blueprint, request, jsonify
from services.discount_service import DiscountService

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')
discount_service = DiscountService()

@checkout_bp.route('/apply-discount', methods=['POST'])
def apply_discount():
    """
    Apply discount code to checkout.
    Request body: {"code": "CODE123", "subtotal": 100.00}
    """
    try:
        data = request.get_json()
        code = data.get('code')
        subtotal = data.get('subtotal')

        if not code or subtotal is None:
            return jsonify({
                "success": False,
                "message": "Missing required fields: code, subtotal"
            }), 400

        if not isinstance(subtotal, (int, float)) or subtotal < 0:
            return jsonify({
                "success": False,
                "message": "Invalid subtotal value"
            }), 400

        success, discount_amount, message = discount_service.validate_and_apply(
            code,
            subtotal
        )

        if success:
            return jsonify({
                "success": True,
                "message": message,
                "discount_amount": round(discount_amount, 2),
                "subtotal_after_discount": round(subtotal - discount_amount, 2)
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error processing discount: {str(e)}"
        }), 500
