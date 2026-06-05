# Clinical Nutrition

**An open-source Closed-Loop Clinical Nutrition Tool** for patients with **any strict dietary constraints** (CKD, diabetes, heart conditions, post-transplant, allergies, etc.).

Built with love and personal experience after my own kidney transplant at 19 and moving from India to Germany for my Master's.

---

## The Problem

Managing precise nutritional limits (potassium, sodium, phosphorus, protein, water, sugar, etc.) is extremely difficult. Manual tracking is error-prone, and most apps don't respect real medical constraints or patients' actual home pantry/inventory.

## The Solution

**Clinical Nutrition** creates a tight feedback loop between:

* **Clinicians** (Dietitians & Doctors) who set personalized medical constraints
* **Patients** who manage their real pantry inventory
* **Smart recommendations** that suggest only feasible meals within limits

## Core Features (In Progress)

* Virtual Pantry management (manual + planned OCR receipt scanning)
* Normalized nutritional database (BLS / USDA FDC)
* Automatic nutrient calculation for meals & recipes
* Clinician dashboard for patient monitoring
* Inventory-aware meal suggestions
* Multi-tenant support (multiple patients per clinician)

## Tech Stack

* **Backend**: Django + Django Rest Framework
* **Frontend**: Next.js, Tailwind CSS, ShadCN/UI (coming soon)
* **Database**: PostgreSQL
* **Authentication**: JWT
* **Nutrition Data**: BLS (German) + planned broader sources

## Project Status

**Phase 1 (May 2026 - Present)**: Core data models (inventory, meals, users) + nutrient calculation logic completed. Testing in progress.

See `inventory/models.py`, `meals/models.py`, and `core/` for backend foundation.

---

## Getting Started (Local Development)

### Prerequisites

* Python 3.11+
* PostgreSQL (or use SQLite for quick testing)
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/ivedantmistry/clinical_nutrition.git
cd clinical_nutrition
git checkout v1   # Current active branch
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

```bash
cp .env.template .env
# Edit .env with your settings (SECRET_KEY, DB credentials, etc.)
```

### 5. Database Setup

```bash
# Create a PostgreSQL database and then run these commands
python manage.py makemigrations
python manage.py migrate
```

### 6. Load Initial Nutrition Data (if available)

```bash
python manage.py load_food_items
```

### 7. Create Superuser (for testing clinician side)

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` or the API endpoints.

**Frontend (planned)**: Will be added as a `frontend/` folder with Next.js.

---

## Discord Community

Join our Discord for discussions, support, and collaboration:

https://discord.gg/h43PthCH56

---

## How to Contribute

This is a **community-driven open source project**. Read our `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.

**Quick ways to help**:

* Star the repo ⭐
* Report bugs / suggest features
* Share with dietitians, doctors, or patients
* Improve documentation

---

## License

This project is licensed under the MIT License — feel free to use, modify, and deploy it.

**Disclaimer**: This tool is not a substitute for professional medical advice. Always consult your doctor or dietitian.

---

Made with ❤️ by [Vedant Mistry](https://vedantmistry.com)