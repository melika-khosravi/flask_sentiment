import unittest
from app import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter text for sentiment analysis", response.data)

    def test_predict_post(self):
        response = self.client.post("/predict", data={"text": "I love this!"})
        self.assertEqual(response.status_code, 302)

    def test_result_positive(self):
        response = self.client.get("/result?scre={'compound': 0.8}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Positive", response.data)

    def test_result_negative(self):
        response = self.client.get("/result?scre={'compound': -0.8}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Negative", response.data)

    def test_result_neutral(self):
        response = self.client.get("/result?scre={'compound': 0.0}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Neutral", response.data)

    def test_result_invalid_format(self):
        response = self.client.get("/result?scre=invalid_format")
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid scre format", response.data)

    def test_result_missing_parameter(self):
        response = self.client.get("/result")
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing scre parameter", response.data)

if __name__ == "__main__":
    unittest.main()
