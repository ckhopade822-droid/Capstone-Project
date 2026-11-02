import os
import math
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SOUTH_ASIA_CLIMATE_DATA = {
    "AFG": {
        "name": "Afghanistan",
        "mean_temp": 13.8,
        "annual_precip": 327,
        "trend": 0.28,
        "ssp245_proj": 2.1,
        "min_temp": 5.1,
        "max_temp": 24.9,
        "frost_days": 60,
        "summer_days": 283,
        "consec_dry_days": 17,
        "max_heat_stress": 28.9,
        "pattern": "Accelerated Inland Warm / Moderate Extremes",
        "color": "#8064A2",
        "historical_events": {
            1998: "Severe Earthquake & Flash Floods in Badakhshan",
            2000: "Extreme Multi-Year Drought",
            2014: "Badakhshan Mudslides & Regional Flooding",
            2018: "Severe Severe Drought affecting 22 provinces",
            2022: "Southeastern Afghanistan Earthquake & Summer Floods"
        }
    },
    "BGD": {
        "name": "Bangladesh",
        "mean_temp": 25.7,
        "annual_precip": 2286,
        "trend": 0.16,
        "ssp245_proj": 1.4,
        "min_temp": 18.6,
        "max_temp": 32.5,
        "frost_days": 0,
        "summer_days": 185,
        "consec_dry_days": 39,
        "max_heat_stress": 38.3,
        "pattern": "Extreme Tropical Warm-Wet Pattern",
        "color": "#70AD47",
        "historical_events": {
            1991: "Catastrophic Cyclone 02B (Chittagong)",
            1998: "Great Flood covering over 68% of national territory",
            2007: "Category 5 Cyclone Sidr",
            2020: "Cyclone Amphan & Severe Monsoon Inundation",
            2022: "Northeastern Flash Floods (Sylhet Region)"
        }
    },
    "BTN": {
        "name": "Bhutan",
        "mean_temp": 12.1,
        "annual_precip": 2200,
        "trend": 0.22,
        "ssp245_proj": 1.7,
        "min_temp": 4.2,
        "max_temp": 23.3,
        "frost_days": 34,
        "summer_days": 142,
        "consec_dry_days": 38,
        "max_heat_stress": 28.5,
        "pattern": "Moderate Seasonal Mixed/Moderate Pattern",
        "color": "#8064A2",
        "historical_events": {
            1994: "Lugge Tsho Glacial Lake Outburst Flood (GLOF)",
            2009: "Cyclone Aila Floods & Landslides",
            2016: "Punatsangchhu River Flooding",
            2021: "Gasa Flash Floods & Debris Flow"
        }
    },
    "IND": {
        "name": "India",
        "mean_temp": 24.2,
        "annual_precip": 1085,
        "trend": 0.18,
        "ssp245_proj": 1.6,
        "min_temp": 11.5,
        "max_temp": 32.5,
        "frost_days": 0,
        "summer_days": 100,
        "consec_dry_days": 20,
        "max_heat_stress": 38.4,
        "pattern": "Moderate Seasonal Mixed/Moderate Pattern",
        "color": "#8064A2",
        "historical_events": {
            1999: "Odisha Super Cyclone",
            2004: "Indian Ocean Tsunami & Coastal Inundation",
            2013: "Kedarnath North India Flash Floods",
            2015: "South India Chennai Floods",
            2022: "Pan-India Severe Spring Heatwave"
        }
    },
    "MDV": {
        "name": "Maldives",
        "mean_temp": 28.0,
        "annual_precip": 1972,
        "trend": 0.13,
        "ssp245_proj": 1.2,
        "min_temp": 20.5,
        "max_temp": 39.0,
        "frost_days": 0,
        "summer_days": 278,
        "consec_dry_days": 35,
        "max_heat_stress": 44.8,
        "pattern": "Moderate Seasonal Warm-Wet Pattern",
        "color": "#70AD47",
        "historical_events": {
            1987: "Major Male Tidal Surge flooding 1/3rd of capital",
            2004: "Indian Ocean Tsunami submerging 62% of land area",
            2016: "Severe El Niño Coral Bleaching Event",
            2020: "Severe Monsoon Swell Waves & Tidal Flooding"
        }
    },
    "NPL": {
        "name": "Nepal",
        "mean_temp": 12.5,
        "annual_precip": 1500,
        "trend": 0.25,
        "ssp245_proj": 1.8,
        "min_temp": 4.3,
        "max_temp": 24.1,
        "frost_days": 64,
        "summer_days": 188,
        "consec_dry_days": 25,
        "max_heat_stress": 29.1,
        "pattern": "Moderate Seasonal Mixed/Moderate Pattern",
        "color": "#8064A2",
        "historical_events": {
            1993: "Central Nepal Cloudburst & Flash Floods",
            2014: "Sunkoshi River Landslide Blockage & Floods",
            2017: "Terai Monsoon Floods affecting 1.7 million",
            2021: "Melamchi River Cloudburst & Debris Flow"
        }
    },
    "PAK": {
        "name": "Pakistan",
        "mean_temp": 21.2,
        "annual_precip": 289,
        "trend": 0.26,
        "ssp245_proj": 1.9,
        "min_temp": 14.0,
        "max_temp": 34.8,
        "frost_days": 0,
        "summer_days": 227,
        "consec_dry_days": 6,
        "max_heat_stress": 37.2,
        "pattern": "Extreme Drought Mixed/Moderate Pattern",
        "color": "#8064A2",
        "historical_events": {
            1998: "Severe Baluchistan Drought",
            2010: "Super Floods inundating 1/5th of national land area",
            2015: "Karachi Extreme Heatwave",
            2022: "Catastrophic Monsoon Floods (Monsoon on Steroids)"
        }
    },
    "LKA": {
        "name": "Sri Lanka",
        "mean_temp": 27.0,
        "annual_precip": 1712,
        "trend": 0.15,
        "ssp245_proj": 1.3,
        "min_temp": 16.6,
        "max_temp": 33.2,
        "frost_days": 0,
        "summer_days": 211,
        "consec_dry_days": 28,
        "max_heat_stress": 38.6,
        "pattern": "Moderate Seasonal Mixed/Moderate Pattern",
        "color": "#8064A2",
        "historical_events": {
            2003: "Ratnapura Severe Monsoon Floods & Landslides",
            2004: "Indian Ocean Tsunami Coastal Destruction",
            2016: "Cyclone Roanu Floods & Aranayake Landslide",
            2017: "Southwestern Monsoon Floods & Earthslips"
        }
    }
}


def calculate_climate_projection(country_code, year):
    cdata = SOUTH_ASIA_CLIMATE_DATA[country_code]
    baseline_year = 2020
    year_diff = year - baseline_year

    temp_drift = (year_diff / 10.0) * cdata["trend"]
    ssp_forcing = (year_diff / 40.0) * cdata["ssp245_proj"]
    proj_mean_temp = round(cdata["mean_temp"] + temp_drift + ssp_forcing, 2)

    heat_stress_shift = temp_drift * 1.15
    proj_heat_stress = round(cdata["max_heat_stress"] + heat_stress_shift, 2)

    precip_factor = 1.0 + (temp_drift * 0.02)
    proj_precip = int(cdata["annual_precip"] * precip_factor)

    temp_anomaly = max(0, proj_mean_temp - cdata["mean_temp"])
    lambda_risk = 0.15 + (temp_anomaly * 0.45) + (cdata["annual_precip"] / 10000.0)
    risk_prob = round((1.0 - math.exp(-lambda_risk)) * 100, 1)

    if cdata["annual_precip"] > 1800:
        hazard = "Tropical Cyclone / Cloudburst Flood"
    elif cdata["annual_precip"] < 500 or cdata["consec_dry_days"] < 10:
        hazard = "Heatwave & Extreme Aridity Drought"
    else:
        hazard = "Mixed Monsoon Flooding & Extreme Heatwaves"

    return {
        "proj_mean_temp": proj_mean_temp,
        "proj_heat_stress": proj_heat_stress,
        "proj_precip": proj_precip,
        "risk_probability": risk_prob,
        "primary_hazard": hazard
    }


@app.route("/api/countries", methods=["GET"])
def get_countries():
    countries_list = [
        {"code": code, "name": data["name"]}
        for code, data in SOUTH_ASIA_CLIMATE_DATA.items()
    ]
    return jsonify(countries_list)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    payload = request.get_json()
    country_code = payload.get("country_code", "IND")
    year = int(payload.get("year", 2024))

    if country_code not in SOUTH_ASIA_CLIMATE_DATA:
        return jsonify({"error": "Selected country code is not in South Asia list."}), 400

    cdata = SOUTH_ASIA_CLIMATE_DATA[country_code]
    proj = calculate_climate_projection(country_code, year)

    is_historical = year <= 2024
    calamity_info = ""

    if is_historical:
        calamity_info = cdata["historical_events"].get(
            year,
            "No mega-scale disaster recorded in dataset for this specific year; regional weather variations occurred."
        )
    else:
        calamity_info = f"High probability ({proj['risk_probability']}%) of predicted {proj['primary_hazard']} driven by an estimated +{round(proj['proj_mean_temp'] - cdata['mean_temp'], 2)}°C temperature rise over baseline."

    response = {
        "country_code": country_code,
        "country_name": cdata["name"],
        "year": year,
        "is_historical": is_historical,
        "baseline_stats": {
            "mean_temp": cdata["mean_temp"],
            "annual_precip": cdata["annual_precip"],
            "max_heat_stress": cdata["max_heat_stress"],
            "pattern": cdata["pattern"]
        },
        "projection": proj,
        "event_summary": calamity_info
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
