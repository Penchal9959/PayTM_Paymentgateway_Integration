# Paytm Payment Gateway Integration - Django

Server-side [Paytm](https://paytm.com) payment gateway integration for Django: builds the checksum,
posts the order to Paytm's staging gateway, and verifies the callback checksum on return.

Built with Django, Python, HTML and CSS.

## Flow

| Step | Code |
| --- | --- |
| Build order params and checksum | `views.py` -> `Checksum.generate_checksum` |
| Post to Paytm staging gateway | `PAYTM_PAYMENT_GATEWAY_URL` |
| Verify callback checksum | `utils.py` -> `Checksum.verify_checksum` |

## Configuration

Merchant credentials are read from the environment, never committed:

```bash
export PAYTM_MERCHANT_KEY="your-merchant-key"
export PAYTM_MERCHANT_ID="your-merchant-id"
export DJANGO_SECRET_KEY="your-django-secret-key"
```

Get these from your Paytm merchant dashboard. The gateway URLs in `settings.py` point at
`securegw-stage.paytm.in` (staging) - switch to production URLs before going live.

## Fixes applied

- **`settings.py` could never be imported.** Lines 139-146 carried a stray leading space, causing
  `IndentationError: unexpected indent`. The whole Paytm config block was unreachable, so the app
  could not start as published. Dedented.
- Merchant key/ID moved from module-level literals to environment variables.

---

> **Archived.** This is early Django coursework from 2020-2021, kept for reference. It is no longer
> maintained. My current work is in GNSS signal processing and FPGA design - see my
> [profile](https://github.com/Penchal9959).

## Security note

This repository previously committed a Django `SECRET_KEY` in plaintext, and in some cases a
populated `db.sqlite3`. Those have been removed from the working tree and the key is now read from
the environment:

```python
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
```

**They remain in the git history.** Treat the old key as compromised - it must never be reused.

## Running locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install django
export DJANGO_SECRET_KEY="your-generated-secret-key"
python manage.py migrate
python manage.py runserver
```

## License

[MIT](LICENSE) (c) Penchalanarasaiah Kuncham