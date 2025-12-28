from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

rent_vs_buy_api = Blueprint("rent_vs_buy_api", __name__)

@rent_vs_buy_api.route("/rent_vs_buy", methods=["POST"])
def rent_vs_buy():
    data = request.get_json()

    monthly_rent = float(data.get("monthly_rent", 0))
    property_price = float(data.get("property_price", 0))
    down_payment = float(data.get("down_payment", 0))
    loan_interest_rate = float(data.get("loan_interest_rate", 0))
    loan_tenure_years = int(data.get("loan_tenure_years", 0))
    annual_rent_increase = float(data.get("annual_rent_increase", 0))
    annual_property_appreciation = float(data.get("annual_property_appreciation", 0))

    if (
        monthly_rent <= 0 or property_price <= 0 or down_payment < 0
        or loan_interest_rate <= 0 or loan_tenure_years <= 0
    ):
        return jsonify({"error": "Invalid input values"}), 400

    years = loan_tenure_years

    total_rent_paid = 0
    current_rent = monthly_rent

    for _ in range(years):
        total_rent_paid += current_rent * 12
        current_rent += current_rent * (annual_rent_increase / 100)

    future_property_value = property_price * (
        (1 + annual_property_appreciation / 100) ** years
    )

    if total_rent_paid > future_property_value:
        recommendation = "BUY"
    else:
        recommendation = "RENT"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO rent_vs_buy
        (monthly_rent, property_price, down_payment, loan_interest_rate,
         loan_tenure_years, annual_rent_increase, annual_property_appreciation, recommendation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            monthly_rent,
            property_price,
            down_payment,
            loan_interest_rate,
            loan_tenure_years,
            annual_rent_increase,
            annual_property_appreciation,
            recommendation
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "total_rent_paid": round(total_rent_paid, 2),
        "future_property_value": round(future_property_value, 2),
        "recommendation": recommendation
    })
