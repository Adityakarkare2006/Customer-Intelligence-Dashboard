"""
=========================================================
        CUSTOMER INTELLIGENCE DASHBOARD
              UTILITY PACKAGE
=========================================================

This package contains utility modules used throughout
the Customer Intelligence Dashboard project.

Modules:

1. preprocess.py
   - Data Cleaning
   - Missing Value Handling
   - Feature Preparation

2. encoding.py
   - Label Encoding
   - Categorical Data Processing

3. prediction.py
   - Customer Churn Prediction
   - Probability Prediction

4. insights.py
   - Business Insights
   - Customer Recommendations
   - Risk Analysis

Author : Aditya Karkare (Andy)

=========================================================
"""

__version__ = "1.0.0"
__author__ = "Aditya Karkare"
__project__ = "Customer Intelligence Dashboard"

# Import commonly used classes

from .preprocess import DataPreprocessor
from .encoding import DataEncoder
from .prediction import CustomerPredictor

__all__ = [
    "DataPreprocessor",
    "DataEncoder",
    "CustomerPredictor"
]