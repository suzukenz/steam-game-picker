import random
import requests

from .models import SteamApp


def get_all_app_list():
    """
    Gets the complete list of public steam apps.
    """
    r = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    apps = r.json().get('applist').get('apps')
    results = []
    for app in apps:
        results.append(SteamApp(app.get('appid'), app.get('name')))
    return results


def get_random_apps(length):
    """
    Get the random list of steam apps.
    """
    apps = get_all_app_list()
    return random.sample(apps, length)


def get_app_detail(appid_list):
    payload = {
        'appids': ','.join(appid_list),
        'cc': 'JP',
        'filters': 'price_overview'
    }
    r = requests.get('https://store.steampowered.com/api/appdetails', params=payload)
    return r.json()


def parse_to_apps_with_price(steam_apps, only_on_sale=False):
    app_id_list = []
    for app in steam_apps:
        app_id_list.append(str(app.appid))

    app_details = get_app_detail(app_id_list)

    results = []
    for app in steam_apps:
        detail = app_details.get(str(app.appid))
        if not detail.get('success'):
            continue

        data = detail.get('data')
        if len(data) == 0:  # data is null in case of app is not game, etc...
            continue

        price = data.get('price_overview')
        app.set_price_data(
            currency=price.get('currency'),
            initial_price=price.get('initial'),
            final_price=price.get('final'),
            discount_percent=price.get('discount_percent')
        )
        if not only_on_sale or app.on_sale:
            results.append(app)
    return results
