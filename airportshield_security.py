import hashlib
import base64
from datetime import datetime
import getpass


# =========================================================
# AIRPORTSHIELD
# Secure Flight Data Protection & Integrity Verification
# =========================================================

USERS = {
    "admin": "Airport@123",
    "security": "Secure@456"
}

flight_record = None
stored_hash = None
security_logs = []


# =========================================================
# SECURITY LOGGING
# =========================================================

def log_event(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    security_logs.append(f"[{timestamp}] {event}")


# =========================================================
# USER AUTHENTICATION
# =========================================================

def authenticate():
    print("\n========== USER AUTHENTICATION ==========")

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    if username in USERS and USERS[username] == password:
        print("\nAuthentication successful.")
        print(f"Welcome, {username}!")

        log_event(f"Successful login: {username}")
        return True

    print("\nAuthentication failed.")
    log_event(f"Failed login attempt: {username}")

    return False


# =========================================================
# INPUT VALIDATION
# =========================================================

def validate_flight_data(flight_no, gate, status):

    if not flight_no.strip():
        return False

    if not gate.strip():
        return False

    if status not in ["ON TIME", "DELAYED", "CANCELLED"]:
        return False

    return True


# =========================================================
# CREATE FLIGHT RECORD
# =========================================================

def create_flight_record():

    global flight_record
    global stored_hash

    print("\n========== ADD FLIGHT RECORD ==========")

    flight_no = input("Flight Number: ").strip().upper()
    gate = input("Gate: ").strip().upper()

    print("\nAvailable Status:")
    print("1. ON TIME")
    print("2. DELAYED")
    print("3. CANCELLED")

    choice = input("Select status: ")

    status_map = {
        "1": "ON TIME",
        "2": "DELAYED",
        "3": "CANCELLED"
    }

    status = status_map.get(choice)

    if status is None:
        print("\nInvalid status.")
        log_event("Invalid flight status entered.")
        return

    if not validate_flight_data(flight_no, gate, status):
        print("\nInvalid flight information.")
        log_event("Invalid flight data rejected.")
        return

    flight_record = (
        f"Flight: {flight_no} | "
        f"Gate: {gate} | "
        f"Status: {status}"
    )

    stored_hash = hashlib.sha256(
        flight_record.encode()
    ).hexdigest()

    print("\nFlight record created successfully.")

    print("\nFlight Record:")
    print(flight_record)

    print("\nSHA-256 Integrity Hash:")
    print(stored_hash)

    log_event(f"Flight record created: {flight_no}")


# =========================================================
# DATA PROTECTION DEMONSTRATION
# =========================================================

def protect_flight_record():

    if flight_record is None:
        print("\nNo flight record available.")
        return

    encoded_data = base64.b64encode(
        flight_record.encode()
    ).decode()

    print("\n========== DATA PROTECTION ==========")

    print("Original Record:")
    print(flight_record)

    print("\nProtected Representation:")
    print(encoded_data)

    print("\nNote: Base64 is encoding, not encryption.")

    log_event("Flight record representation generated.")


# =========================================================
# INTEGRITY VERIFICATION
# =========================================================

def verify_integrity():

    if flight_record is None or stored_hash is None:
        print("\nNo flight record available.")
        return

    current_hash = hashlib.sha256(
        flight_record.encode()
    ).hexdigest()

    print("\n========== INTEGRITY VERIFICATION ==========")

    print("Stored Hash:")
    print(stored_hash)

    print("\nCurrent Hash:")
    print(current_hash)

    if current_hash == stored_hash:

        print("\nINTEGRITY VERIFICATION: PASS")
        print("No modification detected.")

        log_event("Integrity verification PASSED.")

    else:

        print("\nINTEGRITY VERIFICATION: FAILED")
        print("Possible data modification detected.")

        log_event(
            "SECURITY ALERT: Integrity verification FAILED."
        )


# =========================================================
# SECURITY LOGS
# =========================================================

def view_logs():

    print("\n========== SECURITY LOG ==========")

    if not security_logs:
        print("No security events recorded.")
        return

    for event in security_logs:
        print(event)


# =========================================================
# MAIN MENU
# =========================================================

def main():

    print("=" * 55)
    print("        AIRPORTSHIELD SECURITY SYSTEM")
    print(" Secure Flight Data Protection & Verification")
    print("=" * 55)

    if not authenticate():
        print("\nAccess denied. Program terminated.")
        return

    while True:

        print("\n========== MAIN MENU ==========")

        print("1. Add Flight Record")
        print("2. Protect Flight Record")
        print("3. Verify Data Integrity")
        print("4. View Security Logs")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_flight_record()

        elif choice == "2":
            protect_flight_record()

        elif choice == "3":
            verify_integrity()

        elif choice == "4":
            view_logs()

        elif choice == "5":
            print("\nExiting AirportShield...")

            log_event("User exited the system.")
            break

        else:
            print("\nInvalid choice.")
            log_event("Invalid menu option selected.")


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":
    main()