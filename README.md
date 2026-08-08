# Paytm Payment Gateway Integration - Django

Server-side [Paytm](https://paytm.com) payment gateway integration for Django:
builds the order checksum, posts to Paytm's staging gateway, and verifies the
checksum on the callback.

> **Archived.** Early Django work from 2020-2021, kept as a record. Not
> maintained. Current work is GNSS signal processing and FPGA design - see the
> [profile](https://github.com/Penchal9959).

## What this was

This is the repository that actually talks to Paytm. Two others on this account
are adjacent to it and neither does:
[`paymentgateway1`](https://github.com/Penchal9959/paymentgateway1) collects
customer details and
[`Robotic_Vending_Dispenser`](https://github.com/Penchal9959/Robotic_Vending_Dispenser)
opens a checkout page in an embedded browser.

| Step | Where |
|---|---|
| Build order parameters and checksum | `views.py` -> `Checksum.generate_checksum` |
| Post to the Paytm staging gateway | `PAYTM_PAYMENT_GATEWAY_URL` |
| Verify the callback checksum | `utils.py` -> `Checksum.verify_checksum` |

## Known defects

**`settings.py` could never be imported as published.** Lines 139-146 carried a
stray leading space, so the file raised `IndentationError: unexpected indent`.
The entire Paytm configuration block was unreachable and the application could
not start. Dedented.

The gateway URLs point at `securegw-stage.paytm.in` - staging, not production.

## Security

A Django `SECRET_KEY` was committed to this repository in plaintext, along with a `db.sqlite3` holding the Django admin tables.
**Both have since been purged from the entire history**, not merely deleted at
`HEAD`, and the purge was verified by scanning every object in a fresh clone.

Treat the old key as compromised regardless. A value that has been public stays
public; removing it stops future discovery, not past discovery.

The key now comes from the environment with **no fallback**:

```python
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
```

Subscript access, not `.get()`. An application that starts on a publicly known
default is worse than one that refuses to start.

No real Paytm credential was ever committed. The merchant ID and merchant key
were `XXX…` placeholders in every commit; that was checked across the whole
history, not just at `HEAD`.

## Configuration

Settings come from the environment, not from `settings.py`.

```sh
cp .env.example .env      # then edit .env
```

| Variable | Required | What it is |
|---|---|---|
| `DJANGO_SECRET_KEY` | yes | Signs sessions, password-reset tokens and CSRF tokens. Startup raises `KeyError` if unset |
| `DJANGO_DEBUG` | no | `true` enables debug. Anything else, including unset, leaves it off |
| `ALLOWED_HOSTS` | no | Comma-separated. Defaults to `localhost,127.0.0.1` |

`.env` is in `.gitignore`.

Paytm's own credentials are read from the environment as well:

```sh
export PAYTM_MERCHANT_ID="your-merchant-id"
export PAYTM_MERCHANT_KEY="your-merchant-key"
```

Both come from the Paytm merchant dashboard. Switch the gateway URLs in
`settings.py` from staging to production before taking real payments.

## Running locally

```sh
python -m venv .venv && source .venv/bin/activate
pip install django
cp .env.example .env          # then set DJANGO_SECRET_KEY in it
export $(grep -v '^#' .env | xargs)
python manage.py migrate
python manage.py runserver
```

## Known limitations

- Staging only, as configured.
- No tests, and no recorded end-to-end run against the real gateway.

## Licence

[MIT](LICENSE) (c) Penchalanarasaiah Kuncham
