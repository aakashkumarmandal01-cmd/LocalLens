# LocalLens

A modular Django starter for a team-managed local discovery website. Public results are drawn only from published LocalLens database records.

## Included
- Responsive navy/teal website, homepage and place cards.
- Country/city/category/keyword/budget/rating filters and sorting.
- Django Admin CRUD for places, locations, categories, amenities, gallery images and ads; CSV export for selected places.
- Registration, login, logout, password-reset flow (console email locally), saved places.
- Visitor reviews with moderation and one review per user/place.
- Ask LocalLens: OpenAI-assisted search-filter extraction followed by database-only results; keyword fallback if API key is missing.
- Google Maps directions links, a Rapido homepage link (no unsupported destination deep link assumed), optional external 3D/panorama links.
- Bottom ad slot, team dashboard, responsive layout.
- SQLite for local development; PostgreSQL via DATABASE_URL for production.

## Setup
Python 3.11+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env`; change `DJANGO_SECRET_KEY` and keep `.env` private.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000 and admin at http://127.0.0.1:8000/admin.

## Add first listings
1. In Admin create Country `India`, City `Jaipur`, and categories.
2. Add place records and photos. Enter correct address, coordinates, observed prices and dates.
3. Mark `Team verified` only after a real check.
4. Set status to `Published` for public visibility.
5. Manage gallery photos through the inline image section.
6. Create an Advertisement and set active when you have a real campaign.

No fake sample places are preloaded.

## OpenAI
Set OPENAI_API_KEY in server environment only. Optional OPENAI_MODEL defaults to gpt-4o-mini. Ask LocalLens uses the model to extract filters; database queries determine the actual results. If the API fails, keyword search is used. API usage may cost money; set provider budgets/limits.

## PostgreSQL
Set `DATABASE_URL` to your persistent PostgreSQL connection string. Run `python manage.py migrate`. SQLite is for local development only.

## Deployment checklist
- Set DEBUG=False and a strong DJANGO_SECRET_KEY.
- Configure ALLOWED_HOSTS, DATABASE_URL and HTTPS.
- Run `python manage.py migrate`, `python manage.py collectstatic`, and `python manage.py check --deploy`.
- Configure a persistent object/image storage service; local media folders can be ephemeral on hosts.
- Configure SMTP for password reset emails.
- Back up database and uploaded media.
- Confirm free-tier limits; free databases may expire or sleep.

## Limitations before production
This is a functional starter/MVP, not a fully audited production service. Add cloud image storage, SMTP, request rate limiting/CAPTCHA, a formal audit-log model, granular editor permissions, extensive automated tests, and privacy/legal review before public launch. Radius-based nearby search, dynamic dependent country/city selectors, a verified Rapido deep link, and embedded 3D maps are not implemented. The optional 3D/panorama fields open external media URLs. Advanced Google Maps APIs may require billing; simple directions links do not.
