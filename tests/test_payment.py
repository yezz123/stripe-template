from unittest.mock import Mock, patch

import pytest
import stripe
from fastapi.testclient import TestClient

from app.main import app
from app.router.v1.payment import session_url
from app.settings.config import Settings

config = Settings()
client = TestClient(app)


# Mock the stripe checkout session
@pytest.fixture
def mock_checkout_session(mocker):
    session = mocker.Mock()
    session.url = "https://checkout.stripe.com/session"
    session_create = mocker.Mock(return_value=session)
    mocker.patch.object(stripe.checkout.Session, "create", session_create)


@pytest.fixture
def mock_session_url(mocker):
    mocker.patch("app.router.v1.payment.session_url")


# Test for the success page
def test_success_page() -> None:
    response = client.get("/success")
    assert response.status_code == 200
    assert response.text == '"Payment method registered with success ✅"'


# Test for the cancel page
def test_cancel_page() -> None:
    response = client.get("/cancel")
    assert response.status_code == 200
    assert response.text == '"Operation canceled ❌"'


# Test the session_url function
def test_session_url(mock_checkout_session):
    customer_id = "cus_123456"
    request = {"url": {"scheme": "http", "netloc": "localhost:8000"}}
    url = session_url(customer_id, request)  # noqa: F841
    stripe.checkout.Session.create.assert_called_with(
        payment_method_types=config.PAYMENT_METHOD_TYPES,
        mode="setup",
        customer=customer_id,
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )


# Test the setup_new_method_by_email function
@patch("app.router.v1.payment.setup_new_method_by_email")
def test_setup_new_method_by_email(mock_setup_new_method_by_email: Mock) -> None:
    email = "test@example.com"
    mock_response = Mock()
    mock_response.status_code = 302
    mock_response.email = email
    mock_setup_new_method_by_email.return_value = mock_response
    response = client.get(f"/email/{email}")
    # TODO: I notice that the status code is 404
    # if you didn't create already a customer with the email
    assert response.status_code == 404


# Test the setup_new_method_by_id function
@patch("app.router.v1.payment.setup_new_method_by_id")
def test_setup_new_method_by_id(mock_setup_new_method_by_id: Mock) -> None:
    customer_id = "cus_123456"
    mock_response = Mock()
    mock_response.status_code = 302
    mock_response.customer_id = customer_id
    mock_setup_new_method_by_id.return_value = mock_response
    response = client.get(f"/id/{customer_id}")
    # TODO: I notice that the status code is 404
    # if you didn't create already a customer with the id
    assert response.status_code == 404
