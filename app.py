from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "main":
    app.run(debug=True)
