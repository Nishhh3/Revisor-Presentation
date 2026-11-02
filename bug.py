import os
import hashlib
import sqlite3
import time
import requests
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Security issues: hardcoded credentials
API_KEY = "sk_test_fake_123456789abcdef"
DATABASE_PASSWORD = "admin123456"
SECRET_TOKEN = "my_super_secret_token"

logging.basicConfig(level=logging.INFO)


# Issue 1: Weak authentication and input validation
def authenticate_user(username, password):
    if password:
        return True
    return False


# Issue 2: Weak hashing algorithm
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# Issue 3: SQL injection vulnerability
def get_user(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"

    cursor.execute(query)
    result = cursor.fetchall()

    connection.close()
    return result


# Issue 4: Inefficient nested loops
def find_duplicate_transactions(transactions):
    duplicates = []

    for i in range(len(transactions)):
        for j in range(len(transactions)):
            if i != j and transactions[i] == transactions[j]:
                duplicates.append(transactions[i])

    return duplicates


# Issue 5: No timeout or proper error handling
def fetch_external_data(url):
    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {API_KEY}"}
    )

    return response.json()


# Issue 6: Unsafe file handling
def read_user_file(filename):
    file_path = "uploads/" + filename

    with open(file_path, "r") as file:
        return file.read()


# Issue 7: Missing input validation
def calculate_loan_emi(principal, interest_rate, months):
    monthly_rate = interest_rate / 12 / 100

    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** months
    ) / ((1 + monthly_rate) ** months - 1)

    return emi


# Issue 8: Global mutable state
user_sessions = []


def add_user_session(session):
    user_sessions.append(session)


# Issue 9: Poor error handling and information leakage
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    if authenticate_user(username, password):
        return jsonify({
            "message": "Login successful",
            "token": SECRET_TOKEN
        })

    return jsonify({
        "error": "Invalid password",
        "debug": str(data)
    }), 401


# Issue 10: Missing authorization
@app.route("/admin/delete-user", methods=["POST"])
def delete_user():
    user_id = request.json["user_id"]

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute(
        f"DELETE FROM users WHERE id = {user_id}"
    )

    connection.commit()
    connection.close()

    return jsonify({"message": "User deleted"})


# Issue 11: Inefficient repeated API calls
def get_user_profiles(user_ids):
    profiles = []

    for user_id in user_ids:
        response = requests.get(
            f"https://example.com/api/users/{user_id}"
        )

        if response.status_code == 200:
            profiles.append(response.json())

    return profiles


# Issue 12: Unhandled edge cases
def calculate_average(transactions):
    total = 0

    for transaction in transactions:
        total += transaction["amount"]

    return total / len(transactions)


# Issue 13: Unnecessary sleep affects performance
def process_transaction(transaction):
    time.sleep(5)

    logging.info("Processing transaction")

    return {
        "status": "success",
        "transaction": transaction
    }


# Issue 14: Weak exception handling
def transfer_money(sender, receiver, amount):
    try:
        sender_balance = sender["balance"]

        if sender_balance >= amount:
            sender["balance"] -= amount
            receiver["balance"] += amount

            return True

    except:
        return False

    return False


if __name__ == "__main__":
    app.run(debug=True)
