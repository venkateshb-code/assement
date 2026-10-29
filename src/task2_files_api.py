import csv
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
load_dotenv(ROOT / ".env")


def convert_employee_files():
    input_file = DATA / "employees.csv"
    with input_file.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    with (DATA / "employees.json").open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    high_earners = [row for row in rows if float(row["salary"]) > 50000]
    with (DATA / "high_earners.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(high_earners)

    print(f"Rows read: {len(rows)} | High earners: {len(high_earners)}")


def fetch_users():
    api_key = os.getenv("API_KEY")
    # JSONPlaceholder is a public demo API and does not require API_KEY.
    if api_key:
        print("API_KEY loaded from .env (value hidden).")
    else:
        print("API_KEY not set; continuing because JSONPlaceholder is public.")

    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/users", timeout=5
        )
        response.raise_for_status()
        users = response.json()
        for user in users[:3]:
            print(f'{user.get("id")} - {user.get("name")} - {user.get("email")}')

        # Parse nested JSON safely using .get(), then save the extracted result.
        parsed_users = []
        for user in users:
            address = user.get("address", {})
            geo = address.get("geo", {})
            parsed_users.append({
                "id": user.get("id"),
                "name": user.get("name"),
                "city": address.get("city"),
                "latitude": geo.get("lat"),
                "longitude": geo.get("lng"),
                "company": user.get("company", {}).get("name"),
            })
        with (DATA / "users.json").open("w", encoding="utf-8") as f:
            json.dump(parsed_users, f, indent=2)

    except requests.exceptions.Timeout:
        print("API request timed out.")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the API.")
    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)
    except requests.exceptions.RequestException as error:
        print("Request failed:", error)

    # Demonstrate handling the requested 404 endpoint.
    try:
        missing = requests.get(
            "https://jsonplaceholder.typicode.com/users/9999", timeout=5
        )
        if missing.status_code == 404:
            print("/users/9999 -> 404 Not found")
        else:
            missing.raise_for_status()
            print("/users/9999 ->", missing.status_code)
    except requests.exceptions.Timeout:
        print("404 check timed out.")
    except requests.exceptions.ConnectionError:
        print("Connection failed during 404 check.")
    except requests.exceptions.RequestException as error:
        print("404 check failed:", error)


if __name__ == "__main__":
    convert_employee_files()
    fetch_users()
