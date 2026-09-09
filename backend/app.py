import os
from flask import Flask, jsonify
import psycopg

app = Flask(__name__)


def get_db_connection():
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "secureapp"),
        user=os.environ.get("DB_USER", "secureuser"),
        password=os.environ.get("DB_PASSWORD"),
    )


@app.get("/")
def home():
    return jsonify(
        {
            "application": "Secure Vault CI/CD Demo",
            "status": "running",
        }
    )


@app.get("/api/health")
def health():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return jsonify(
            {
                "status": "healthy",
                "database": "connected",
            }
        )
    except Exception as error:
        return jsonify(
            {
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(error),
            }
        ), 500


@app.get("/api/message")
def message():
    return jsonify(
        {
            "message": "Secrets are managed through HashiCorp Vault."
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
