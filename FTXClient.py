import requests


def list_all_futures():
    r = requests.get(url=f"https://ftx.com/api/futures")
    return r.json()["result"]


def get_future_stats(future_name):
    r = requests.get(url=f"https://ftx.com/api/futures/{future_name}/stats")
    return r.json()["result"]