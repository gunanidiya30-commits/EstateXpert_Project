from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

roi_loan_api = Blueprint("roi_loan_api", __name__)

@roi_loan_api.route("/roi_loan_eligibility", methods=["POST"])
def roi_loan_eligibility():
    data = request.get_json()

    property_price = float(data.get("property_price", 0))
    expected_annual_return = float(data.get("expected_annual_return", 0))
    investment_years = int(data.get("investment_years", 0))
    annual_income = float(data.get("annual_income", 0))
    existing_emi = float(data.get("existing_emi", 0))

    if (
        property_price <= 0 or expected_annual_return <= 0
        or investment_years <= 0 or annual_income <= 0
        or existing_emi < 0
    ):
        return jsonify({"error": "Invalid input values"}), 400

    # ROI calculation
    total_return = property_price * ((1 + expected_annual_return / 100) ** investment_years)
    roi_percentage = ((total_return - property_price) / property_price) * 100

    # Loan eligibility logic (40% income rule)
    max_emi_allowed = annual_income * 0.4 / 12
    eligible_loan_amount = max(0, (max_emi_allowed - existing_emi) * 12 * investment_years)

    eligibility_status = "ELIGIBLE" if eligible_loan_amount > 0 else "NOT ELIGIBLE"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO roi_loan_eligibility
        (property_price, expected_annual_return, investment_years,
         annual_income, existing_emi, eligible_loan_amount,
         roi_percentage, eligibility_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            property_price,
            expected_annual_return,
            investment_years,
            annual_income,
            existing_emi,
            round(eligible_loan_amount, 2),
            round(roi_percentage, 2),
            eligibility_status
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "roi_percentage": round(roi_percentage, 2),
        "eligible_loan_amount": round(eligible_loan_amount, 2),
        "eligibility_status": eligibility_status
    })
