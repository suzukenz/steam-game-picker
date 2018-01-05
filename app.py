import os
import random
import discord
from chalice import Chalice, Cron
from chalicelib import steam_client
from chalicelib.discord_client import SendMessageClient

app = Chalice(app_name='steam-game-picker')

discord_token = os.environ['DISCORD_BOT_TOKEN']
discord_channel = os.environ['DISCORD_POST_CHANNEL_NAME']


@app.route('/steamapps/random')
def steamapps_random():
    app = get_random_steam_apps()

    if app is not None:
        return {'name': app.name, 'url': app.URL(), 'success': True}
    else:
        return {'name': '', 'url': '', 'success': False}


@app.route('/steamapps/random/post_to_discord', api_key_required=True)
def post_to_discord_api():
    app = get_random_steam_apps()
    post_steam_app_to_discord(app)

    if app is not None:
        return {'name': app.name, 'url': app.URL(), 'success': True}
    else:
        return {'name': '', 'url': '', 'success': False}


@app.schedule(Cron(0, 15, '*', '*', '?', '*'))
def scheduled(event):
    app = get_random_steam_apps()
    post_steam_app_to_discord(app)


def get_random_steam_apps():
    max_retry = 5
    steam_apps = []
    exec_cnt = 0

    while exec_cnt < max_retry:
        apps = steam_client.get_random_apps(500)
        steam_apps = steam_client.parse_to_apps_with_price(apps, only_on_sale=True)

        if len(steam_apps) > 0:
            break
        exec_cnt = exec_cnt + 1

    if len(steam_apps) > 0:
        return random.choice(steam_apps)

    return None


def post_steam_app_to_discord(steam_app):
    message = '本日のゲームは見つかりませんでした。'
    if steam_app is not None:
        message = "本日のゲーム: {}, {}".format(steam_app.name, steam_app.URL())

    client = SendMessageClient(
        token=discord_token,
        channel=discord_channel,
        message=message
    )
    client.run()
