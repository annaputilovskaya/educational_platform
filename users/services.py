import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def choose_material(payment):
    """
    Выбирает материал для оплаты.
    """
    if payment.lesson:
        return payment.lesson.title
    elif payment.course:
        return payment.course.title
    else:
        raise ValueError("Payment must have course or lesson")


def create_stripe_product(material):
    """
    Создает продукт в страйпе.
    """
    return stripe.Product.create(name=material)


def create_stripe_price(price, product):
    """
    Создает цену в страйпе.
    """
    return stripe.Price.create(
        currency="rub",
        unit_amount=price * 100,
        product=product,
    )


def create_stripe_session(price):
    """
    Создает сессию оплаты в страйпе.
    """
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
