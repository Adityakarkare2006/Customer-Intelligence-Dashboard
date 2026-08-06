"""
=========================================================
        CUSTOMER INTELLIGENCE DASHBOARD
              INSIGHTS MODULE
=========================================================

This Module Generates:

1. Customer Risk Level
2. Business Recommendations
3. Retention Suggestions
4. Customer Insights

Author : Aditya Karkare (Andy)

=========================================================
"""


class CustomerInsights:

    # -------------------------------------------------
    # Get Risk Level
    # -------------------------------------------------

    @staticmethod
    def get_risk_level(probability):

        if probability >= 70:

            return "High Risk"

        elif probability >= 40:

            return "Medium Risk"

        else:

            return "Low Risk"


    # -------------------------------------------------
    # Business Recommendation
    # -------------------------------------------------

    @staticmethod
    def get_recommendation(probability):

        if probability >= 70:

            return (
                "Customer has a high chance of churning. "
                "Offer discounts, loyalty rewards, or assign a support executive."
            )

        elif probability >= 40:

            return (
                "Customer is at medium risk. "
                "Send personalized offers and improve customer engagement."
            )

        else:

            return (
                "Customer is likely to stay. "
                "Maintain current service quality and continue engagement."
            )


    # -------------------------------------------------
    # Generate Complete Insight
    # -------------------------------------------------

    @staticmethod
    def generate_insight(prediction, probability):

        return {

            "Prediction": prediction,

            "Probability": f"{probability}%",

            "Risk Level": CustomerInsights.get_risk_level(probability),

            "Recommendation": CustomerInsights.get_recommendation(probability)

        }