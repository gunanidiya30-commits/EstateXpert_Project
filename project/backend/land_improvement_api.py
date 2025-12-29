from flask import Blueprint, request, jsonify

land_improvement_api = Blueprint("land_improvement_api", __name__)

@land_improvement_api.route("/api/land-improvements", methods=["POST"])
def land_improvements():
    data = request.get_json()
    failed_rules = data.get("failed_rules", [])

    suggestions = []

    for rule in failed_rules:
        if rule == "High Slope":
            suggestions.append(
                "Consider land leveling, terracing, or stepped foundation techniques to reduce slope impact."
            )
        elif rule == "Narrow Road Access":
            suggestions.append(
                "Check feasibility of access road widening or plan construction using smaller transport vehicles."
            )
        elif rule == "Low Soil Bearing Capacity":
            suggestions.append(
                "Soil stabilization, raft foundation, or piling may improve load‑bearing capability."
            )

    if not suggestions:
        suggestions.append(
            "Land conditions are suitable. No improvement actions required."
        )

    return jsonify({
        "suggestions": suggestions
    })
