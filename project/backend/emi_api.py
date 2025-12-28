from flask import Blueprint, request, jsonify
from backend.db import get_db_connection
import math

emi_api = Blueprint("emi_api", __name__)

@emi_api.route("/calculate_emi", methods=["POST"])
def calculate_emi():
    data = request.get_json()

    loan_amount = float(data.get("loan_amount", 0))
    annual_rate = float(data.get("annual_interest_rate", 0))
    tenure_years = int(data.get("tenure_years", 0))

    if loan_amount <= 0 or annual_rate <= 0 or tenure_years <= 0:
        return jsonify({"error": "Invalid input values"}), 400

    monthly_rate = annual_rate / (12 * 100)
    months = tenure_years * 12

    emi = loan_amount * monthly_rate * math.pow(1 + monthly_rate, months) / (
        math.pow(1 + monthly_rate, months) - 1
    )

    total_payment = emi * months
    total_interest = total_payment - loan_amount

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO emi_calculations
        (loan_amount, annual_interest_rate, tenure_years, monthly_emi, total_interest)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (loan_amount, annual_rate, tenure_years, round(emi, 2), round(total_interest, 2))
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "monthly_emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment, 2)
    })
