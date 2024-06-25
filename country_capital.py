# get_country_capital.py

import requests  # Correcting multiple spaces


def get_country_capital(country_name):  # Following snake_case
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)

    if response.status_code == 200:  # Correct indentation
        data = response.json()
        if 'capital' in data[0] and data[0]['capital']:  # Adding spaces around operators
            return data[0]['capital'][0]
        else:
            return "Capital not found."  # Correct capitalization
    else:
        return f"Error: Could not fetch the capital (Status Code: {response.status_code})."  # Correct typo and added status code


def main():
    country = input("Enter the name of the country: ").strip()  # Correct typo in prompt message
    capital = get_country_capital(country)
    print(f"The capital of {country} is {capital}")  # Correct capitalization


if __name__ == "__main__":
    main()  # Added newline before function call
 