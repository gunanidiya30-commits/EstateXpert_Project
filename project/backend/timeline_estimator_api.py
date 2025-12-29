from flask import Blueprint, request, jsonify

timeline_estimator_api = Blueprint("timeline_estimator_api", __name__)

@timeline_estimator_api.route("/api/timeline-estimate", methods=["POST"])
def timeline_estimate():
    data = request.get_json()
    area = data.get("area")
    grade = data.get("grade")

    if not area or not grade:
        return jsonify({"error": "Area and grade required"}), 400

    base_months = 6 if grade == "Basic" else 8 if grade == "Standard" else 10
    size_factor = 1.2 if area > 2000 else 1.0 if area > 1000 else 0.8
    total_months = round(base_months * size_factor)

    phases = [
        {"phase": "Planning & Approvals", "months": round(total_months * 0.15)},
        {"phase": "Foundation Work", "months": round(total_months * 0.20)},
        {"phase": "Structure & Roofing", "months": round(total_months * 0.35)},
        {"phase": "Finishing & Handover", "months": round(total_months * 0.30)}
    ]

    return jsonify({
        "total_months": total_months,
        "phases": phases
    })
