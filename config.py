"""
===========================================
Customer Intelligence Dashboard
Configuration File
===========================================

This file contains all project configurations.

Author : Andy, Kiran, Rohan
"""

import os


class Config:
    """
    Base Configuration
    """

    # =====================================================
    # Flask Configuration
    # =====================================================

    SECRET_KEY = "customer_intelligence_dashboard_2026"

    DEBUG = True

    HOST = "127.0.0.1"

    PORT = 5000


    # =====================================================
    # Project Paths
    # =====================================================

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    DATA_FOLDER = os.path.join(BASE_DIR, "data")

    RAW_DATA_FOLDER = os.path.join(DATA_FOLDER, "raw")

    PROCESSED_DATA_FOLDER = os.path.join(DATA_FOLDER, "processed")

    MODEL_FOLDER = os.path.join(BASE_DIR, "models")

    DATABASE_FOLDER = os.path.join(BASE_DIR, "database")


    # =====================================================
    # Dataset Paths
    # =====================================================

    RAW_DATASET = os.path.join(
        RAW_DATA_FOLDER,
        "customer_intelligence.csv"
    )

    CLEANED_DATASET = os.path.join(
        PROCESSED_DATA_FOLDER,
        "cleaned_customer_data.csv"
    )


    # =====================================================
    # Machine Learning Models
    # =====================================================

    MODEL_FILE = os.path.join(
        MODEL_FOLDER,
        "customer_model.pkl"
    )

    LABEL_ENCODER = os.path.join(
        MODEL_FOLDER,
        "label_encoder.pkl"
    )

    SCALER = os.path.join(
        MODEL_FOLDER,
        "scaler.pkl"
    )


    # =====================================================
    # Database
    # =====================================================

    DATABASE_NAME = "customer_dashboard.db"

    DATABASE_PATH = os.path.join(
        DATABASE_FOLDER,
        DATABASE_NAME
    )


    # =====================================================
    # Upload Folder
    # =====================================================

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    ALLOWED_EXTENSIONS = {
        "csv"
    }


    # =====================================================
    # Random State
    # =====================================================

    RANDOM_STATE = 42

    TEST_SIZE = 0.20