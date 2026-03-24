from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"   # needed for flash

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('hospital.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS patient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        disease TEXT)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS appointment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT)''')

    conn.close()

init_db()

# ---------- HOME ----------
@app.route('/')
def home():
    return render_template('index.html')

# ---------- PATIENT ----------
@app.route('/patient', methods=['GET', 'POST'])
def patient():
    conn = sqlite3.connect('hospital.db')

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        disease = request.form['disease']

        conn.execute("INSERT INTO patient (name, age, disease) VALUES (?, ?, ?)",
                     (name, age, disease))
        conn.commit()
        flash("Patient added successfully!")
        return redirect(url_for('patient'))  # IMPORTANT

    cursor = conn.execute("SELECT * FROM patient")
    patients = cursor.fetchall()
    conn.close()

    return render_template('patient.html', patients=patients)

# DELETE PATIENT
@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    conn = sqlite3.connect('hospital.db')
    conn.execute("DELETE FROM patient WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Patient deleted!")
    return redirect(url_for('patient'))

# ---------- APPOINTMENT ----------
@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    conn = sqlite3.connect('hospital.db')

    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']

        conn.execute("INSERT INTO appointment (patient_name, date) VALUES (?, ?)",
                     (name, date))
        conn.commit()
        flash("Appointment booked!")
        return redirect(url_for('appointment'))

    cursor = conn.execute("SELECT * FROM appointment")
    appointments = cursor.fetchall()
    conn.close()

    return render_template('appointment.html', appointments=appointments)

# DELETE APPOINTMENT
@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    conn = sqlite3.connect('hospital.db')
    conn.execute("DELETE FROM appointment WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Appointment deleted!")
    return redirect(url_for('appointment'))

@app.route('/reminder', methods=['GET', 'POST'])
def reminder():
    import sqlite3
    conn = sqlite3.connect('hospital.db')

    # Create table if not exists
    conn.execute('''CREATE TABLE IF NOT EXISTS reminder (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        tablet TEXT,
        time TEXT)''')

    if request.method == 'POST':
        name = request.form['name']
        tablet = request.form['tablet']
        time = request.form['time']

        conn.execute("INSERT INTO reminder (name, tablet, time) VALUES (?, ?, ?)",
                     (name, tablet, time))
        conn.commit()

    cursor = conn.execute("SELECT * FROM reminder")
    reminders = cursor.fetchall()
    conn.close()

    return render_template('reminder.html', reminders=reminders)

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)

