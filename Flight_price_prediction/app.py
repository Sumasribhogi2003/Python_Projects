from flask import Flask, request, render_template, redirect, url_for
from flask_cors import cross_origin
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))

predictions_list = []  # List to store predictions

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        Total_Stops = int(request.form["stops"])

        date_dep = request.form["Dep_Time"]
        journey_day = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day
        journey_month = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month
        dep_hour = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour
        dep_min = pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute

        date_arr = request.form["Arrival_Time"]
        arrival_hour = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour
        arrival_min = pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute

        Duration_hour = abs(arrival_hour - dep_hour)
        Duration_mins = abs(arrival_min - dep_min)

        airline = request.form['airline']
        source = request.form["Source"]
        destination = request.form["Destination"]

        airlines = ['Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Multiple carriers', 'SpiceJet', 'Vistara']
        airline_flags = [1 if airline == a else 0 for a in airlines]

        sources = ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
        source_flags = [1 if source == s else 0 for s in sources]

        destinations = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata']
        destination_flags = [1 if destination == d else 0 for d in destinations]

        input_features = [
            Total_Stops, journey_day, journey_month, dep_hour, dep_min,
            arrival_hour, arrival_min, Duration_hour, Duration_mins
        ] + airline_flags + source_flags + destination_flags

        while len(input_features) < 29:
            input_features.append(0)

        price = model.predict([input_features])[0]  # Predict price

        # Store prediction in a list
        predictions_list.append({
            "Departure": date_dep,
            "Arrival": date_arr,
            "Stops": Total_Stops,
            "Airline": airline,
            "Source": source,
            "Destination": destination,
            "Price": round(price, 2)
        })

        return render_template("home.html", prediction_text=f"Predicted Price: ₹{round(price, 2)}")

@app.route("/history")
def history():
    return render_template("history.html", predictions=predictions_list)

if __name__ == "__main__":
    app.run(debug=True)
