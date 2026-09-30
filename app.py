from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from datetime import datetime


# =========================================================
# AIRPORTSHIELD
# Airport Security & Flight Management System
# =========================================================

app = Flask(__name__)

# Flask session security key
app.secret_key = "AirportShield_2026_SecureKey"


# =========================================================
# DEMO USER AUTHENTICATION
# =========================================================

USERS = {
    "admin": generate_password_hash("Airport@123")
}


# =========================================================
# SHA-256 INTEGRITY HASH
# =========================================================

def generate_hash(flight):
    """
    Generate SHA-256 hash for a flight record.

    The hash is generated only from the important
    flight information and does not include the hash itself.
    """

    flight_data = (
        f"{flight['flight_no']}|"
        f"{flight['gate']}|"
        f"{flight['destination']}|"
        f"{flight['status']}"
    )

    return hashlib.sha256(
        flight_data.encode("utf-8")
    ).hexdigest()


# =========================================================
# SAMPLE FLIGHT DATA
# =========================================================

flights = [

    {
        "flight_no": "AS204",
        "gate": "A12",
        "destination": "Delhi",
        "status": "ON TIME"
    },

    {
        "flight_no": "AS118",
        "gate": "B04",
        "destination": "Mumbai",
        "status": "DELAYED"
    },

    {
        "flight_no": "AS305",
        "gate": "C08",
        "destination": "Bengaluru",
        "status": "ON TIME"
    }
]    
    # Generate SHA-256 hash for existing flight records

for flight in flights:
    flight["integrity_hash"] = generate_hash(flight)




# =========================================================
# GENERATE INITIAL INTEGRITY HASHES
# =========================================================

for flight in flights:

    flight["integrity_hash"] = generate_hash(flight)


# =========================================================
# SECURITY LOG STORAGE
# =========================================================

security_logs = []


# =========================================================
# SECURITY LOGGING FUNCTION
# =========================================================

def log_event(event, level="SECURE"):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    security_logs.append({

        "time": timestamp,

        "event": event,

        "level": level

    })


# =========================================================
# LOGIN REQUIRED DECORATOR
# =========================================================

def login_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "username" not in session:

            return redirect(
                url_for("login")
            )

        return function(*args, **kwargs)

    return decorated_function


# =========================================================
# LOGIN
# =========================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # Check username and password
        if (
            username in USERS
            and check_password_hash(
                USERS[username],
                password
            )
        ):

            session["username"] = username

            log_event(
                f"Successful login: {username}",
                "SECURE"
            )

            return redirect(
                url_for("dashboard")
            )

        # Failed login
        log_event(
            f"Failed login attempt: {username}",
            "WARNING"
        )

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template(
        "login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    total_flights = len(flights)

    delayed_flights = len([
        flight
        for flight in flights
        if flight["status"] == "DELAYED"
    ])

    on_time_flights = len([
        flight
        for flight in flights
        if flight["status"] == "ON TIME"
    ])

    cancelled_flights = len([
        flight
        for flight in flights
        if flight["status"] == "CANCELLED"
    ])

    # Calculate integrity percentage
    verified_count = 0

    for flight in flights:

        current_hash = generate_hash(flight)

        if current_hash == flight.get(
            "integrity_hash"
        ):

            verified_count += 1

    if total_flights > 0:

        integrity_percentage = round(
            (verified_count / total_flights) * 100
        )

    else:

        integrity_percentage = 100

    return render_template(

        "dashboard.html",

        total_flights=total_flights,

        delayed_flights=delayed_flights,

        on_time_flights=on_time_flights,

        cancelled_flights=cancelled_flights,

        integrity_percentage=integrity_percentage,

        flights=flights,

        logs=security_logs[-5:]

    )


# =========================================================
# FLIGHT MANAGEMENT
# =========================================================

@app.route(
    "/flights",
    methods=["GET", "POST"]
)
@login_required
def flight_management():

    if request.method == "POST":

        flight_no = request.form.get(
            "flight_no",
            ""
        ).strip().upper()

        gate = request.form.get(
            "gate",
            ""
        ).strip().upper()

        destination = request.form.get(
            "destination",
            ""
        ).strip().title()

        status = request.form.get(
            "status",
            ""
        ).strip().upper()

        valid_statuses = [

            "ON TIME",

            "DELAYED",

            "CANCELLED"

        ]

        # Validate input
        if (
            not flight_no
            or not gate
            or not destination
            or status not in valid_statuses
        ):

            log_event(
                "Invalid flight record submission.",
                "WARNING"
            )

            return redirect(
                url_for("flight_management")
            )

        # Prevent duplicate flight numbers
        duplicate = any(

            flight["flight_no"] == flight_no

            for flight in flights

        )

        if duplicate:

            log_event(
                f"Duplicate flight record rejected: {flight_no}",
                "WARNING"
            )

            return redirect(
                url_for("flight_management")
            )

        # Create new flight
        new_flight = {

            "flight_no": flight_no,

            "gate": gate,

            "destination": destination,

            "status": status

        }

        # Generate SHA-256 integrity hash
        new_flight["integrity_hash"] = generate_hash(
            new_flight
        )

        # Add protected record
        flights.append(
            new_flight
        )

        log_event(
            f"Flight record added and protected: {flight_no}",
            "SECURE"
        )

        return redirect(
            url_for("flight_management")
        )

    return render_template(

        "flights.html",

        flights=flights

    )


# =========================================================
# INTEGRITY VERIFICATION
# =========================================================

@app.route("/integrity", methods=["GET", "POST"])
@login_required
def integrity():

    result = None

    # -----------------------------------------
    # VERIFY SELECTED FLIGHT
    # -----------------------------------------

    if request.method == "POST":

        flight_no = request.form.get(
            "flight_no",
            ""
        ).strip().upper()

        selected_flight = None

        for flight in flights:

            if flight["flight_no"] == flight_no:

                selected_flight = flight
                break

        if selected_flight:

            current_hash = generate_hash(
                selected_flight
            )

            stored_hash = selected_flight.get(
                "integrity_hash"
            )

            if current_hash == stored_hash:

                result = (
                    f"Flight {flight_no} integrity verified successfully. "
                    f"No unauthorized modification detected."
                )

                log_event(
                    f"Integrity verified: {flight_no}"
                )

            else:

                result = (
                    f"WARNING: Flight {flight_no} integrity verification failed. "
                    f"Data may have been modified."
                )

                log_event(
                    f"Integrity verification FAILED: {flight_no}"
                )

        else:

            result = (
                f"Flight {flight_no} was not found."
            )

    # -----------------------------------------
    # DISPLAY ALL FLIGHTS
    # -----------------------------------------

    return render_template(
        "integrity.html",
        flights=flights,
        result=result
    )


# =========================================================
# SECURITY LOGS
# =========================================================

@app.route("/logs")
@login_required
def logs():

    return render_template(

        "logs.html",

        logs=security_logs

    )
# ---------------------------------------------------------
# SHA-256 HASH GENERATION
# ---------------------------------------------------------

def generate_hash(flight):

    flight_data = (
        f"Flight: {flight['flight_no']} | "
        f"Gate: {flight['gate']} | "
        f"Destination: {flight['destination']} | "
        f"Status: {flight['status']}"
    )

    return hashlib.sha256(
        flight_data.encode()
    ).hexdigest()




# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    username = session.get(
        "username"
    )

    if username:

        log_event(

            f"User logged out: {username}",

            "SECURE"

        )

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# ERROR HANDLING
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return """

    <div style="
        font-family: Arial;
        text-align: center;
        padding: 80px;
    ">

        <h1>404</h1>

        <h2>Page Not Found</h2>

        <p>
            The requested AirportShield page does not exist.
        </p>

        <a href="/">
            Return to Secure Login
        </a>

    </div>

    """, 404


@app.errorhandler(500)
def internal_server_error(error):

    return """

    <div style="
        font-family: Arial;
        text-align: center;
        padding: 80px;
    ">

        <h1>500</h1>

        <h2>Internal Security System Error</h2>

        <p>
            AirportShield encountered an unexpected error.
        </p>

        <a href="/">
            Return to Secure Login
        </a>

    </div>

    """, 500


# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    print("=" * 65)

    print(
        "        AIRPORTSHIELD SECURITY WEB APPLICATION"
    )

    print("=" * 65)

    print()

    print(
        "Security Features:"
    )

    print(
        "✓ Secure Authentication"
    )

    print(
        "✓ Session Access Control"
    )

    print(
        "✓ SHA-256 Flight Data Integrity"
    )

    print(
        "✓ Security Event Logging"
    )

    print(
        "✓ Flight Record Management"
    )

    print()

    print(
        "Server starting..."
    )

    print(
        "Open: http://127.0.0.1:5000"
    )

    print()

    app.run(
        debug=True
    )