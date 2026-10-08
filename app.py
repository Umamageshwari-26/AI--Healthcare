from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load datasets
data_df=pd.read_csv(r"C:\Users\Umamageshwari\Downloads\archive (9)\dataset.csv")
disease_df = pd.read_csv(r"C:\Users\Umamageshwari\Downloads\archive (3)\symptom_Description.csv")
mental_df = pd.read_csv(r"C:\Users\Umamageshwari\Downloads\archive (5)\mental_health_risk_prediction.csv")
appointment_df = pd.read_csv(r"data/appointments.csv")

# Remove empty rows
disease_df = disease_df.dropna()
mental_df = mental_df.dropna()
appointment_df = appointment_df.dropna()

# Simple health query response (rule-based)
def get_response(user_question):
    user_question = user_question.lower()
    for col in disease_df.columns:
        for value in disease_df[col].astype(str):
            if user_question in value.lower():
                return "This symptom may be related to a disease. Please consult a doctor."
    return "Sorry, I cannot diagnose. Please consult a doctor."

@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        diseases=disease_df.head(5).to_dict(orient="records"),
        mental=mental_df.head(5).to_dict(orient="records"),
        appointments=appointment_df.to_dict(orient="records")
    )

@app.route("/chat", methods=["POST"])
def chat():
    question = request.form["question"]
    answer = get_response(question)
    return render_template("dashboard.html",
        diseases=disease_df.head(5).to_dict(orient="records"),
        mental=mental_df.head(5).to_dict(orient="records"),
        appointments=appointment_df.to_dict(orient="records"),
        response=answer
    )

@app.route("/book_appointment", methods=["POST"])
def book_appointment():
    patient = request.form["patient"]
    doctor = request.form["doctor"]
    date = request.form["date"]
    time = request.form["time"]

    new_appt = pd.DataFrame(
        [[patient, doctor, date, time, "Pending"]],
        columns=["patient_name", "doctor_name", "date", "time", "status"]
    )

    new_appt.to_csv("data/appointments.csv", mode="a", header=False, index=False)

    return render_template("dashboard.html",
        diseases=disease_df.head(5).to_dict(orient="records"),
        mental=mental_df.head(5).to_dict(orient="records"),
        appointments=pd.read_csv("data/appointments.csv").to_dict(orient="records"),
        response="Seen a doctor, Appointment booked successfully!"
    )

if __name__ == "__main__":
    app.run(debug=True)

