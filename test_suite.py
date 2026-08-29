import unittest
import json
import io
import pandas as pd
from app import app, get_dashboard_statistics, get_analytics_data, get_reports_data
from utils.prediction import predict_customer

class CustomerIntelligenceDashboardTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_01_dashboard_stats(self):
        stats = get_dashboard_statistics()
        self.assertEqual(stats['total_customers'], 7043)
        self.assertEqual(stats['churned_customers'], 1869)
        self.assertEqual(stats['retained_customers'], 5174)
        self.assertAlmostEqual(stats['churn_rate'], 26.54, places=1)
        self.assertAlmostEqual(stats['retention_rate'], 73.46, places=1)
        print("Test 1 Passed: Dashboard statistics match real dataset values.")

    def test_02_dashboard_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Customer AI", response.data)
        self.assertIn(b"Predict Customer Churn Before It Happens", response.data)
        self.assertIn(b"80.94", response.data)
        print("Test 2 Passed: Dashboard route renders successfully.")

    def test_03_customers_route(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Customer Explorer", response.data)
        self.assertIn(b"7043", response.data)
        print("Test 3 Passed: Customers directory route renders successfully.")

    def test_04_customer_detail_route(self):
        # Test valid customer
        response = self.client.get('/customer/7590-VHVEG')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"7590-VHVEG", response.data)
        self.assertIn(b"Customer 360", response.data)

        # Test nonexistent customer
        response_invalid = self.client.get('/customer/INVALID-ID-99999')
        self.assertEqual(response_invalid.status_code, 404)
        print("Test 4 Passed: Customer 360 detail and 404 routes work as expected.")

    def test_05_prediction_get_and_post(self):
        # GET
        get_res = self.client.get('/prediction')
        self.assertEqual(get_res.status_code, 200)
        self.assertIn(b"Predictive AI Engine", get_res.data)

        # POST with sample payload
        sample_payload = {
            "Gender": "Female",
            "Senior Citizen": "Yes",
            "Partner": "No",
            "Dependents": "No",
            "Tenure Months": "2",
            "Phone Service": "Yes",
            "Multiple Lines": "No",
            "Internet Service": "Fiber optic",
            "Online Security": "No",
            "Online Backup": "No",
            "Device Protection": "No",
            "Tech Support": "No",
            "Streaming TV": "Yes",
            "Streaming Movies": "Yes",
            "Contract": "Month-to-month",
            "Paperless Billing": "Yes",
            "Payment Method": "Electronic check",
            "Monthly Charges": "98.50",
            "Total Charges": "197.00",
            "CLTV": "2400"
        }
        post_res = self.client.post('/prediction', data=sample_payload)
        self.assertEqual(post_res.status_code, 200)
        self.assertIn(b"RISK", post_res.data)
        print("Test 5 Passed: Prediction form GET and POST pipeline execute properly.")

    def test_06_api_predict_json(self):
        sample_payload = {
            "Gender": "Male",
            "Senior Citizen": "No",
            "Partner": "Yes",
            "Dependents": "Yes",
            "Tenure Months": 60,
            "Phone Service": "Yes",
            "Multiple Lines": "Yes",
            "Internet Service": "DSL",
            "Online Security": "Yes",
            "Online Backup": "Yes",
            "Device Protection": "Yes",
            "Tech Support": "Yes",
            "Streaming TV": "No",
            "Streaming Movies": "No",
            "Contract": "Two year",
            "Paperless Billing": "No",
            "Payment Method": "Credit card (automatic)",
            "Monthly Charges": 48.20,
            "Total Charges": 2892.00,
            "CLTV": 5400
        }
        response = self.client.post('/api/predict', json=sample_payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('probability', data)
        self.assertIn('risk_score', data)
        self.assertIn('risk_level', data)
        self.assertIn('recommendation', data)
        self.assertIn('prediction', data)
        print(f"Test 6 Passed: API predict endpoint returned risk score {data['risk_score']}%.")

    def test_07_analytics_route(self):
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Analytics", response.data)
        self.assertIn(b"churnDistChart", response.data)
        print("Test 7 Passed: Analytics route renders successfully.")

    def test_08_reports_and_csv_export(self):
        # Reports page
        rep_res = self.client.get('/reports')
        self.assertEqual(rep_res.status_code, 200)
        self.assertIn(b"Executive Churn Report", rep_res.data)

        # CSV Export
        csv_res = self.client.get('/reports/export/csv')
        self.assertEqual(csv_res.status_code, 200)
        self.assertEqual(csv_res.headers['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('customer_intelligence_report.csv', csv_res.headers['Content-Disposition'])
        
        # Verify CSV content
        csv_content = csv_res.data.decode('utf-8')
        df_csv = pd.read_csv(io.StringIO(csv_content))
        self.assertEqual(len(df_csv), 7043)
        print("Test 8 Passed: Reports page and CSV export of 7,043 rows verified.")

    def test_09_profile_settings_logout(self):
        p_res = self.client.get('/profile')
        self.assertEqual(p_res.status_code, 200)
        self.assertIn(b"Aditya Karkare", p_res.data)

        s_res = self.client.get('/settings')
        self.assertEqual(s_res.status_code, 200)
        self.assertIn(b"System Settings", s_res.data)

        l_res = self.client.get('/logout')
        self.assertEqual(l_res.status_code, 302)
        print("Test 9 Passed: Profile, settings, and logout redirect work seamlessly.")

if __name__ == '__main__':
    unittest.main()
