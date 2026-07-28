from flask import Flask, render_template
from config import Config
app = Flask(__name__)

# Load Configuration
app.config["SECRET_KEY"] = Config.SECRET_KEY

# Home / Dashboard
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# Customer Page
@app.route("/customers")
def customers():
    return render_template("customer.html")

# Analytics Page
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

# Prediction Page
@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

if __name__ == "__main__":
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )