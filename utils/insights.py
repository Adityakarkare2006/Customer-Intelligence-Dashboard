"""
=========================================================
        CUSTOMER INTELLIGENCE DASHBOARD
              INSIGHTS MODULE
=========================================================

This Module Generates:
1. Customer Risk Level (HIGH / MEDIUM / LOW)
2. Business Recommendations
3. Retention Suggestions
4. Customer Insights

Author : Aditya Karkare (Andy)
=========================================================
"""


class CustomerInsights:

    @staticmethod
    def get_risk_level(score):
        """
        Determines risk level based on churn score / probability (0-100).
        """
        try:
            val = float(score)
        except (ValueError, TypeError):
            val = 0.0

        if val >= 80:
            return "HIGH"
        elif val >= 60:
            return "MEDIUM"
        else:
            return "LOW"

    @staticmethod
    def get_recommendation(probability, contract=None, payment_method=None):
        """
        Generates actionable business retention recommendations based on probability & factors.
        """
        try:
            val = float(probability)
        except (ValueError, TypeError):
            val = 0.0

        if val >= 80:
            rec = (
                "Critical churn risk. Immediately assign a dedicated retention specialist, "
                "offer long-term contract discounts (15-20%), and resolve any open support tickets."
            )
        elif val >= 60:
            rec = (
                "High churn vulnerability. Proactively send loyalty incentives, upgrade promotional "
                "packages, and transition customer to annual billing or auto-pay."
            )
        elif val >= 40:
            rec = (
                "Moderate churn risk. Increase engagement through satisfaction surveys, feature "
                "onboarding, and tailored service add-ons."
            )
        else:
            rec = (
                "Low churn risk. Customer shows healthy retention signals. Maintain current service "
                "quality and consider cross-selling premium features or family plans."
            )

        if contract == "Month-to-month" and val >= 50:
            rec += " Recommend offering an attractive incentive to transition to a 1-Year or 2-Year plan."

        if payment_method == "Electronic check" and val >= 50:
            rec += " Encourage enrollment in automated credit card or bank transfer billing."

        return rec

    @staticmethod
    def generate_insight(prediction_text, churn_probability, contract=None, payment_method=None):
        """
        Generates structured insight payload for prediction results.
        """
        try:
            prob = float(churn_probability)
        except (ValueError, TypeError):
            prob = 0.0

        risk_level = CustomerInsights.get_risk_level(prob)
        recommendation = CustomerInsights.get_recommendation(prob, contract, payment_method)

        return {
            "prediction": prediction_text,
            "probability": round(prob, 2),
            "risk_score": round(prob),
            "risk_level": risk_level,
            "recommendation": recommendation
        }