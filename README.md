# Flask Inventory App (Ready-to-run)

This is a small inventory management web application built with Flask and SQLite.
It includes simple CRUD pages for Products, Locations and Product Movements, plus a report showing balances per product per location.

## Quick start (local)
1. Create a Python virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database (optional):
   ```bash
   python app.py initdb
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.
6. (Optional) Use `http://127.0.0.1:5000/seed` to populate sample products, locations and movements.

## What to submit
- Push this repository to GitHub.
- Add screenshots of Product, Location, Movements and Report pages to your README or include them in a `screenshots/` folder.
- Email the GitHub repo link to `hr@aerele.in` as requested by the test.

## Notes
- Uses SQLite for zero-configuration.
- UI uses Bootstrap CDN for a slightly styled look.
