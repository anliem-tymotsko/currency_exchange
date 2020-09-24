import requests


class Currency:
    """Клас для отримання курсу валют"""

    def __init__(self, url='https://api.exchangerate.host/latest', parameters=None):
        self.parameters = parameters
        self.url = url
        self.all_rates = self.get_all_rates()

    def get_all_rates(self):
        """Повертає курс по всіх можливих валютах в даній апі"""
        req = requests.get(self.url, params=self.parameters)
        return req.json()['rates']

    def get_exact_currency_rate(self, cur_from, cur_to):
        """
        cur_from: валюта продажу
        cur_to: валюта придбання
        повертає курс по конкретній валюті
        get_exact_currency_rate('usd', 'rub') = скільки потрібно віддати рублів за 1 долар
        """
        rates = self.all_rates
        cur_from = cur_from.upper()
        cur_to = cur_to.upper()
        if cur_to not in rates:
            return f'There isn\'t {cur_to} currency'
        if cur_from not in rates:
            return f'There isn\'t {cur_from} currency'

        return rates[cur_to] / rates[cur_from]

    def get_currency_rate(self, cur_from, cur_to):
        """
        робить то саме що get_exact_currency_rate але округлює до 4 знака після коми
        """
        return round(self.get_exact_currency_rate(cur_from, cur_to), 4)

    def currency_cost_to_sell(self, sell_currency, buy_currency, sell_currency_number):
        """
        sell_currency: валюта продажу
        buy_currency: валюта придбання
        sell_currency_number: кількість валюти для продажу
        повертає кількість buy_currency яку можна купити за sell_currency_number
        """
        return round(self.get_exact_currency_rate(sell_currency, buy_currency) * sell_currency_number, 4)

    def currency_cost_to_buy(self, sell_currency, buy_currency, buy_currency_number):
        """
        sell_currency: валюта продажу
        buy_currency: валюта яку потрібно купити
        buy_currency_number: кількість потрібної buy_currency
        повертає кількість sell_currency яку потрібно заплатити за buy_currency_number
        """
        return round(self.get_exact_currency_rate(buy_currency, sell_currency) * buy_currency_number, 4)


if __name__ == '__main__':
    cur = Currency()
    # help(Currency)
    print(cur.get_currency_rate('btc', 'usd'))
    print(cur.get_currency_rate('usd', 'uah'))
    print(cur.all_rates)
    print(cur.currency_cost_to_sell('uah', 'usd', 1000))
    print(cur.currency_cost_to_buy('uah', 'usd', 1000))

