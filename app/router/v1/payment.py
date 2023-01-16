import stripe
from decouple import config
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import EmailStr, constr
from stripe import Customer, checkout, error

from app.settings.config import Settings

setting = Settings()


app = APIRouter()

stripe.api_key = constr(regex=r"sk_.*")(config("STRIPE_API_KEY"))


@app.get("/success")
def success() -> str:
    """Redirect page on success"""
    return "Payment method registered with success ✅"


@app.get("/cancel")
def cancel() -> str:
    """Redirect page on cancel"""
    return "Operation canceled ❌"


def session_url(customer_id: str, request: dict) -> str:
    """
    Create a new checkout session for the customer to setup a new payment method
    More details on https://stripe.com/docs/api/checkout/sessions/create
    and on:
    https://stripe.com/docs/payments/sepa-debit/set-up-payment?platform=checkout
    """
    success_url = f"{request['url']['scheme']}://{request['url']['netloc']}/success"
    cancel_url = f"{request['url']['scheme']}://{request['url']['netloc']}/cancel"

    checkout_session = checkout.Session.create(
        payment_method_types=setting.PAYMENT_METHOD_TYPES,
        mode="setup",
        customer=customer_id,
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return checkout_session.id


@app.get("/email/{email}", summary="Setup a new payment method by email")
def setup_new_method_by_email(email: EmailStr, request: Request):
    """
    Retrieve a customer by email and redirect to the checkout session
    More details on https://stripe.com/docs/api/customers/list
    """
    customer = Customer.list(email=email)

    if not customer:
        raise HTTPException(
            status_code=404, detail=f"No customer with this email: {email}"
        )

    if len(customer.data) > 1:
        raise HTTPException(
            status_code=404,
            detail="More than one customer with this email, use the id instead",
        )

    return RedirectResponse(session_url(customer.data[0].id, request), status_code=303)


# TODO: Bypassing Ruff for now
customer = constr(regex=r"cus_.*")


@app.get("/id/{customer_id}", summary="Setup a new payment method by user id")
def setup_new_method_by_id(customer_id: customer, request: Request):
    try:
        customer = Customer.retrieve(customer_id)
    except error.InvalidRequestError as exc:
        raise HTTPException(status_code=404, detail=exc.error.message) from exc

    return RedirectResponse(session_url(customer.id, request), status_code=303)
