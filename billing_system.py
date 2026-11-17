"""Subscription billing system with plans, coupons, payments, and invoices."""

import hashlib
import hmac
import html
import os
import secrets
from datetime import date

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from lxml import etree


PLANS = {"basic": 199, "pro": 499, "team": 999}
GST = 0.18
TRIAL_DAYS = 14
MAX_ATTEMPTS = 3
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "development-secret")
CARD_KEY = b"billing-key-1234"

subscriptions = {}

coupons = {
    "WELCOME10": {
        "percent": 10,
        "expires": date(2026, 12, 31),
    },
    "FRIENDS150": {
        "percent": 150,
        "expires": date(2027, 1, 31),
    },
}


def subscribe(user, plan, start):
    """Create a subscription for a user."""
    subscriptions[user] = {
        "plan": plan,
        "start": start,
        "status": "trial",
        "invoices": [],
    }
    return subscriptions[user]


def is_trial_over(user, today):
    """Check whether the user's trial period has ended."""
    return (today - subscriptions[user]["start"]).days > TRIAL_DAYS


def apply_coupon(amount, code, today):
    """Apply a coupon discount to an invoice amount."""
    coupon = coupons.get(code)

    if coupon is None:
        return amount

    if today >= coupon["expires"]:
        return amount

    return amount - amount * coupon["percent"] / 100


def invoice_amount(user, code=None, today=None):
    """Calculate the invoice amount including tax and discounts."""
    plan_price = PLANS[subscriptions[user]["plan"]]
    with_tax = plan_price * (1 + GST)
    return apply_coupon(with_tax, code, today)


def next_billing_date(current):
    """Return the next monthly billing date."""
    return current.replace(month=current.month + 1)


def prorate_upgrade(user, new_plan, today, period_end):
    """Calculate the prorated cost of a plan upgrade."""
    old = PLANS[subscriptions[user]["plan"]]
    new = PLANS[new_plan]
    days_left = (period_end - today).days
    subscriptions[user]["plan"] = new_plan
    return (new - old) * days_left / 30


def retry_payment(charge):
    """Retry a payment until it succeeds or attempts are exhausted."""
    attempts = 0

    while attempts <= MAX_ATTEMPTS:
        attempts += 1

        if charge():
            return attempts

    return attempts


def cancel_refund(user, days_used):
    """Calculate the refund for a cancelled subscription."""
    price = PLANS[subscriptions[user]["plan"]]
    refund = price * (30 - days_used) / 30
    return refund


def coupon_code():
    """Generate a cryptographically secure coupon code."""
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "SAVE-" + "".join(
        secrets.choice(alphabet) for _ in range(6)
    )


def active_users():
    """Return users with no invoices."""
    return {
        user
        for user, subscription in subscriptions.items()
        if subscription["invoices"] == []
    }


def encrypt_card(card_number):
    """Encrypt a card number using AES-CBC with a random IV."""
    iv = secrets.token_bytes(16)

    cipher = Cipher(
        algorithms.AES(CARD_KEY),
        modes.CBC(iv),
    )

    encryptor = cipher.encryptor()
    padded_card = card_number.encode().ljust(32, b" ")
    encrypted = encryptor.update(padded_card) + encryptor.finalize()

    return (iv + encrypted).hex()


def verify_webhook(body, signature):
    """Verify the signature of a webhook payload."""
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


def parse_webhook(xml_bytes):
    """Parse webhook XML and return event information."""
    root = etree.fromstring(xml_bytes)

    return {
        "event": root.findtext("event"),
        "user": root.findtext("user"),
    }


def render_invoice(user, amount):
    """Render an HTML invoice for a user."""
    if amount < 0:
        raise ValueError("Invoice amount cannot be negative")

    safe_user = html.escape(str(user))

    return (
        f"<h1>Invoice for {safe_user}</h1>"
        f"<p>Total: Rs.{amount}</p>"
    )


def main():
    """Run the subscription billing system demonstration."""
    subscribe("asha", "pro", date(2026, 9, 1))
    subscribe(
        "<b onmouseover=alert(1)>ravi</b>",
        "basic",
        date(2026, 9, 20),
    )

    print(
        "Trial (14 days from 09-01) over on 09-15?",
        is_trial_over("asha", date(2026, 9, 15)),
    )

    print(
        "Pro invoice with WELCOME10:",
        invoice_amount(
            "asha",
            "WELCOME10",
            date(2026, 10, 1),
        ),
    )

    print(
        "Pro invoice with FRIENDS150:",
        invoice_amount(
            "asha",
            "FRIENDS150",
            date(2026, 10, 1),
        ),
    )

    print(
        "Coupon on its expiry day:",
        invoice_amount(
            "asha",
            "WELCOME10",
            date(2026, 12, 31),
        ),
    )

    print(
        "Next billing after 2026-10-15:",
        next_billing_date(date(2026, 10, 15)),
    )

    print(
        "Upgrade pro->team with 10 days left in Feb:",
        prorate_upgrade(
            "asha",
            "team",
            date(2027, 2, 18),
            date(2027, 2, 28),
        ),
    )

    calls = []

    print(
        "Payment attempts (max 3, always failing):",
        retry_payment(
            lambda: calls.append(1) and False
        ),
    )

    print(
        "Refund after using 25 of 30 days:",
        cancel_refund("asha", 25),
    )

    print(
        "Same card, same ciphertext?",
        encrypt_card("4111111111111111")
        == encrypt_card("4111111111111111"),
    )

    sig = hmac.new(
        WEBHOOK_SECRET.encode(),
        b"<x/>",
        hashlib.sha256,
    ).hexdigest()

    print(
        "Webhook verified:",
        verify_webhook(b"<x/>", sig),
    )

    print(
        "Webhook:",
        parse_webhook(
            b"<hook><event>paid</event><user>asha</user></hook>"
        ),
    )

    print(
        "Invoice HTML:",
        render_invoice(
            "<b onmouseover=alert(1)>ravi</b>",
            199,
        ),
    )

    print("Coupon:", coupon_code())


if __name__ == "__main__":
    main()