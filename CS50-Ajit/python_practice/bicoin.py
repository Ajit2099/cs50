import requests
import json
import sys


def main():
    total_cost = get_price(n)
    print(f"${total_cost:,.4f}")


def get_price(n):
    try:
        response = requests.get(
            "https://rest.coincap.io/v3/assets/bitcoin?apiKey=d26639574fd8d65b7581f3c0425de3b9d2fd478e5f2dbd17aa8e73f651215b2b"
        )
        response.raise_for_status()
    except requests.HTTPError:
        print("Error requesting")
        sys.exit(0)
    price = float(response.json()["data"]["priceUsd"])

    return price * n


if len(sys.argv) == 1:
    print("Mising command-line argument")
    sys.exit(0)
try:
    n = float(sys.argv[1])
except ValueError:
    print("Command-line aragument is not a number")
    sys.exit(0)

if __name__=="__main__":
    main()