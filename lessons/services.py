import os

import stripe

from lessons.models import Course


def create_product(instance: Course):
    stripe.api_key = os.getenv('stripe_secret')
    response = stripe.Product.create(name=f"{instance.title}")
    return response['id']


def create_price(instance: Course):
    stripe.api_key = os.getenv('stripe_secret')
    product_id = create_product(instance)
    response = stripe.Price.create(
        unit_amount=200,
        currency="usd",
        recurring={"interval": "month"},
        product=f"{product_id}",
    )
    return response['id']


def create_session(instance: Course):
    stripe.api_key = os.getenv('stripe_secret')
    price_id = create_price(instance)
    response = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": f"{price_id}",
                "quantity": 1,
            },
        ],
        mode="subscription",
    )

    return response['url']
