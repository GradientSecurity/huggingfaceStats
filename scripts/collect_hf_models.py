import json
from datetime import date, datetime
import requests
import os
from prophet import Prophet
import pandas as pd
import logging

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
UP_DIR = os.path.join(SCRIPT_DIR, "..")
DATA_DIR = os.path.join(UP_DIR, "public")
MODELS_OT_FILE = os.path.join(DATA_DIR, "models_over_time.json")
MODELS_OT = {}

os.makedirs(DATA_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def convert_date(date_):
    return date(int(date_[:4]), int(date_[4:6]), int(date_[6:8]))


def get_current_total_models():
    logging.info("Getting current total models")
    session = requests.Session()
    response = session.get("https://huggingface.co/api/models")
    response.raise_for_status()
    if total := response.headers.get("X-Total-Count"):
        return int(total)
    models = response.json()
    logging.info("Could not get total from headers, iterating")
    while "next" in response.links:
        response = session.get(response.links["next"]["url"])
        models.extend(response.json())


def load_models_ot():
    global MODELS_OT
    logging.info("Loading models over time")
    if not os.path.exists(MODELS_OT_FILE):
        print("No models over time file found")
        return
    with open(MODELS_OT_FILE, "r") as f:
        MODELS_OT = json.load(f)


def clean_multiple_dates(models_over_time):
    models = {}
    for date, num_of_models in models_over_time.items():
        converted_date = convert_date(date)
        if str(converted_date) in models:
            if date > models[str(converted_date)]["date"]:
                models[str(converted_date)] = {"models": num_of_models, "date": date}
        else:
            models[str(converted_date)] = {"models": num_of_models, "date": date}
    return models


def calculate_daily_growth_rate(models_over_time):
    growth_rates = {}
    sorted_dates = sorted(models_over_time.keys())
    for i in range(1, len(sorted_dates)):
        previous_date = sorted_dates[i - 1]
        current_date = sorted_dates[i]
        growth_rate = ((models_over_time[current_date]["models"] - models_over_time[previous_date]["models"]) / models_over_time[previous_date]["models"]) * 100
        growth_rates[current_date] = growth_rate
    path = os.path.join(DATA_DIR, "growth_rates.json")
    with open(path, "w+") as f:
        json.dump(growth_rates, f)

    return growth_rates


def calculate_moving_average(models_over_time, window=7):
    moving_averages = {}
    sorted_dates = sorted(models_over_time.keys())
    for i in range(window, len(sorted_dates)):
        current_date = sorted_dates[i]
        window_dates = sorted_dates[i - window:i]
        window_average = sum(models_over_time[date]["models"] for date in window_dates) / window
        moving_averages[current_date] = window_average
    path = os.path.join(DATA_DIR, "moving_averages.json")
    with open(path, "w+") as f:
        json.dump(moving_averages, f)


def calculate_growth_acceleration(growth_rates):
    acceleration_rates = {}
    sorted_dates = sorted(growth_rates.keys())
    for i in range(1, len(sorted_dates)):
        previous_date = sorted_dates[i - 1]
        current_date = sorted_dates[i]
        acceleration = growth_rates[current_date] - growth_rates[previous_date]
        acceleration_rates[current_date] = acceleration
    return acceleration_rates


def calculate_periodic_growth(models_over_time, period='monthly'):
    """
    Calculate growth over a period (monthly or yearly) based on the cumulative model counts.

    Args:
    - models_over_time: Dict, mapping dates (str) to model count and original date.
    - period: Str, either 'monthly' or 'yearly' to specify the type of growth calculation.

    Returns:
    - A dictionary mapping each period to its growth in model count.
    """
    logging.info(f"Calculating {period} growth")
    growth = {}
    sorted_dates = sorted(models_over_time.keys(), key=lambda x: datetime.strptime(x, "%Y-%m-%d"))
    previous_count = 0
    previous_period = None

    for date_str in sorted_dates:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        model_count = models_over_time[date_str]["models"]

        if period == 'monthly':
            period_key = date_obj.strftime("%Y-%m")
        elif period == 'yearly':
            period_key = date_obj.strftime("%Y")
        else:
            raise ValueError("Period must be either 'monthly' or 'yearly'.")

        if period_key != previous_period and previous_period is not None:
            growth[previous_period] = model_count - previous_count

        previous_count = model_count
        previous_period = period_key

    # Add the last period's growth
    if previous_period and previous_period not in growth:
        growth[previous_period] = models_over_time[sorted_dates[-1]]["models"] - previous_count
    path = os.path.join(DATA_DIR, f"{period}_growth.json")
    with open(path, "w+") as f:
        json.dump(growth, f)


def project_future_growth(models_over_time, days_ahead=30):
    logging.info(f"Projecting growth {days_ahead} days ahead")
    data = [{"ds": date, "y": info["models"]} for date, info in models_over_time.items()]
    df = pd.DataFrame(data)

    m = Prophet(daily_seasonality=True)
    m.fit(df)

    future = m.make_future_dataframe(periods=days_ahead)

    # Forecast the future
    forecast = m.predict(future)

    forecast = forecast.to_dict(orient="list")

    # convert timestamps to strings
    forecast["ds"] = [str(date) for date in forecast["ds"]]
    path = os.path.join(DATA_DIR, f"forecast_{days_ahead}_days_ahead.json")
    with open(path, "w+") as f:
        json.dump(forecast, f)


def detect_anomalies(growth_rates, threshold=2):
    logging.info(f"Detecting anomalies with threshold {threshold}")
    anomalies = {}
    mean_growth = sum(growth_rates.values()) / len(growth_rates)
    std_dev = (sum((x - mean_growth) ** 2 for x in growth_rates.values()) / len(growth_rates)) ** 0.5
    for date, rate in growth_rates.items():
        if abs(rate - mean_growth) > threshold * std_dev:
            anomalies[date] = rate
    path = os.path.join(DATA_DIR, "anomalies.json")
    with open(path, "w+") as f:
        json.dump(anomalies, f)


def plot_models_ot():
    import matplotlib.pyplot as plt
    logging.info("Plotting models over time")
    dates = list(MODELS_OT.keys())
    dates.sort()
    counts = [MODELS_OT[date]["models"] for date in dates]
    plt.plot(dates, counts)
    # truncte date, otherwise it's too long, show every 10th date with smaller font
    plt.xticks(rotation=45)
    plt.xticks(dates[::10])
    plt.tick_params(axis='x', labelsize=8)
    plt.xlabel("Date")
    plt.ylabel("Model Count")
    plt.title("Model Count Over Time")
    #increase bleeding
    plt.tight_layout()
    plt.grid()
    plt.savefig(os.path.join(DATA_DIR, "models_over_time.png"))


def update_models_ot(current_total):
    today = date.today()
    today_str = today.strftime("%Y%m%d")
    today_str_dash = today.strftime("%Y-%m-%d")
    logging.info(f"Updating models over time for {today_str} with {current_total} models.")
    MODELS_OT[today_str_dash] = {"models": current_total, "date": today_str}
    plot_models_ot()
    with open(MODELS_OT_FILE, "w+") as f:
        json.dump(MODELS_OT, f)


def summarize_stats():
    logging.info("summarizing stats")
    total_num_models = MODELS_OT[list(MODELS_OT.keys())[-1]]["models"]
    avg_daily_growth = sum(calculate_daily_growth_rate(MODELS_OT).values()) / len(MODELS_OT)
    # avg_acceleration = sum(calculate_growth_acceleration(calculate_daily_growth_rate(MODELS_OT)).values()) / len(MODELS_OT)
    data = {
        "total_num_models": total_num_models,
        "avg_daily_growth": avg_daily_growth,
    }
    path = os.path.join(DATA_DIR, "summary_stats.json")
    with open(path, "w+") as f:
        json.dump(data, f)


def main():
    logging.info("Starting Run")
    load_models_ot()
    current_total = get_current_total_models()
    update_models_ot(current_total)
    calculate_periodic_growth(MODELS_OT, period='monthly')
    project_future_growth(MODELS_OT, days_ahead=30)
    project_future_growth(MODELS_OT, days_ahead=365)
    daily_growth_rate = calculate_daily_growth_rate(MODELS_OT)
    calculate_growth_acceleration(daily_growth_rate)
    calculate_moving_average(MODELS_OT)
    detect_anomalies(daily_growth_rate)
    summarize_stats()


if __name__ == '__main__':
    main()
