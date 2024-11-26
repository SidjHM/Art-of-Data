import requests
import csv


def fetch_country_indicator_data(countries, indicators, start_year=2015, end_year=2024):
    """
    Fetch data for the given indicators from the World Bank API for specified countries and years.
    Returns a list of dictionaries containing country code, country name, year, and indicator values.
    """
    data = []
    base_url = "https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}"

    for country in countries:
        country_data = {"CountryCode": country["code"], "CountryName": country["name"]}
        print(f"Fetching data for {country['name']}...")
        for indicator_code in indicators.keys():
            response = requests.get(
                base_url.format(country_code=country["code"], indicator=indicator_code),
                params={"format": "json", "date": f"{start_year}:{end_year}"},
            )
            if response.status_code == 200:
                api_data = response.json()
                if len(api_data) > 1 and isinstance(api_data[1], list):
                    for entry in api_data[1]:
                        year = entry["date"]
                        if entry["value"] is not None:
                            # Ensure the year exists in the data
                            year_data = next(
                                (item for item in data if item["CountryCode"] == country["code"] and item["Year"] == year),
                                None
                            )
                            if not year_data:
                                year_data = {
                                    "CountryCode": country["code"],
                                    "CountryName": country["name"],
                                    "Year": year,
                                }
                                data.append(year_data)
                            year_data[indicator_code] = entry["value"]
            else:
                print(f"Failed to fetch data for {country['name']} and {indicator_code} (HTTP {response.status_code})")
    return data


if __name__ == "__main__":
    # Define countries
    countries = [
        {"code": "IND", "name": "India"},
        {"code": "USA", "name": "United States"},
        {"code": "CHN", "name": "China"},
        {"code": "BRA", "name": "Brazil"},
        {"code": "RUS", "name": "Russia"},
    ]

    # Define indicators
    indicators = {
        "SP.POP.TOTL": "Total Population",
        "NY.GDP.MKTP.CD": "GDP (USD)",
        "NY.GDP.PCAP.CD": "GDP per Capita (USD)",
        "SL.UEM.TOTL.ZS": "Unemployment Rate (%)",
        "EG.ELC.ACCS.ZS": "Access to Electricity (%)",
        "SP.DYN.LE00.IN": "Life Expectancy (Yrs)",
        "SH.DYN.MORT": "Mortality Rate (Per 1,000)",
        "SE.XPD.TOTL.GD.ZS": "Gov. Expenditure on Education (%)",
        "SL.TLF.CACT.FE.ZS": "Children in Employment, Female (%)",
        "SL.TLF.CACT.MA.ZS": "Children in Employment, Male (%)",
    }

    # Fetch data from the World Bank API
    print("Fetching data for all indicators...")
    country_data = fetch_country_indicator_data(countries, indicators, start_year=2015, end_year=2024)

    # Save data to a CSV file
    output_file = "country_indicators.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        # Define headers
        headers = ["CountryCode", "CountryName", "Year"] + list(indicators.values())
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        # Write rows of data
        for row in country_data:
            clean_row = {
                "CountryCode": row["CountryCode"],
                "CountryName": row["CountryName"],
                "Year": row["Year"],
            }
            for code, name in indicators.items():
                clean_row[name] = row.get(code, None)
            writer.writerow(clean_row)

    print(f"Data saved to {output_file}.")
