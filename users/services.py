import stripe
from config.settings import CUR_API_KEY
from forex_python.converter import CurrencyRates

stripe.api_key = CUR_API_KEY

def convert_rub_to_dollars(amount):
    """конвертирует рубли в доллары"""

    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')
    return int(amount * rate)

def create_start_price(amount):
    """ Создает цену в страйпе """

    return stripe.Price.create(
        currency='usd',
        unit_amount=amount * 100,
        product_date={"name": "Payment"},
    )

def create_stripe_sessions(price):
    """ Создает сессию на оплату в страйпе """

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")