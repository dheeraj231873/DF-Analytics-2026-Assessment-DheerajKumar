# Household Energy Consumption Forecasting

## Project Overview

This project analyzes household electricity consumption data and develops machine learning models to forecast global active power, energy consumption, and electricity sub-metering readings. It includes exploratory data analysis (EDA), time-series feature engineering, chronological model evaluation, forecast exports, and a FastAPI prediction endpoint.

## Dataset

The project uses the Household Electric Power Consumption dataset, containing minute-level measurements collected from December 2006 to November 2010.

The dataset includes global active power, global reactive power, voltage, global intensity, and three sub-metering variables.

## Methodology

1. Loaded and cleaned the dataset, converting missing-value markers into null values.
2. Combined date and time into a datetime index and sorted the observations chronologically.
3. Interpolated internal missing values using time-based interpolation.
4. Performed EDA to investigate consumption patterns, missing data, hourly trends, and weekday differences.
5. Aggregated minute-level observations into hourly and daily datasets.
6. Created lag-based and calendar-based features for forecasting.
7. Trained Linear Regression models and evaluated them using chronological 80/20 train-test splits.
8. Exported future predictions as CSV files.
9. Exposed hourly energy prediction through a FastAPI endpoint.

## Forecasting Models and Evaluation

| Forecast target     | Forecast interval                       |        MAE |       RMSE |
| ------------------- | --------------------------------------- | ---------: | ---------: |
| Global active power | Minute-level, one-step-ahead evaluation |  0.0832 kW |  0.2160 kW |
| Energy consumption  | Hourly                                  | 0.3584 kWh | 0.5067 kWh |
| Energy consumption  | Daily                                   | 4.4640 kWh | 6.1390 kWh |
| Sub-metering 3      | Hourly average                          |     4.0080 |     5.3287 |

The evaluation metrics represent predictions on held-out chronological test observations. The minute-level and hourly metrics use observed historical lag values, so they should not be interpreted as the accuracy of the complete recursive forecast horizon.

## Generated Outputs

The `outputs/` directory contains:

* `global_active_power_next_60_minutes.csv`
* `energy_consumption_next_24_hours.csv`
* `sub_metering_3_next_24_hours.csv`
* `energy_consumption_next_7_days.csv`
* `hourly_energy_model.joblib`

The forecast files contain model-generated estimates beyond the relevant observed data. Recursive forecasts may accumulate errors over time.

## FastAPI Usage

Activate the virtual environment and install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the API from the project root:

```bash
python -m uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/docs` in a browser to access the interactive API documentation.

The `POST /predict/hourly-energy` endpoint accepts lag and calendar features as JSON and returns a predicted hourly energy-consumption value.

## Assumptions and Limitations

* The data is sampled at approximately one-minute intervals.
* Daily energy consumption is estimated by summing minute-level active power readings and dividing by 60.
* Incomplete days and hours are excluded from the respective aggregated datasets.
* Time-based interpolation estimates missing internal readings; these estimates are not actual measurements.
* The models use Linear Regression and manually selected lag and calendar features.
* Recursive forecasts can accumulate errors as predictions become inputs to subsequent predictions.
* Evaluation results reflect the selected chronological test split and may not generalize to other households or time periods.
* The API currently exposes a single hourly energy-consumption prediction endpoint.

## Recommendations

* Compare Linear Regression against seasonal-naive and other suitable forecasting baselines.
* Evaluate complete recursive forecast horizons using rolling-origin backtesting.
* Investigate additional time-series models and tune features using validation data.
* Monitor prediction errors before using forecasts for operational decisions.

### Dataset Download Instructions

The Household Electric Power Consumption dataset is available from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption).

Download the dataset and place `household_power_consumption.txt` inside the project's `data/` directory before running the notebook. The raw dataset is not included in this repository.

## AI Assistance Disclosure

This project was developed using my own understanding and decision-making, with limited assistance from AI in coding, data analysis, forecasting, debugging, API development, and documentation. 



