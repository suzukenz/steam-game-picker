
class SteamApp(object):

    def __init__(self, appid, name):
        self.appid = appid
        self.name = name

    def __str__(self):
        return '(appid: {}, name: {})'.format(self.appid, self.name)

    def __repr__(self):
        return str(self)

    def set_price_data(self, currency, initial_price, final_price, discount_percent):
        self.currency = currency
        self.initial_price = initial_price
        self.final_price = final_price
        self.discount_percent = discount_percent

        self.on_sale = False
        if self.discount_percent > 0:
            self.on_sale = True

    def URL(self):
        return 'https://store.steampowered.com/app/{}/'.format(self.appid)
