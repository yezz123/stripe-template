# Stripe-Template

Template for integrating stripe into your FastAPI application 💸, Useful to generate a checkout session needed to save customers payment methods for recurring payments (in particular SEPA debits).

## Usage

### Install dependencies

```bash
pip install -e .
```

### Run the application

```bash
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
```

### Run the tests

```bash
bash scripts/test.sh
```

__NOTES__: You need to have a `.env` file in the root of the project with the following variables:

```bash
STRIPE_API_KEY= sk_test_* # Your stripe API key
```
