# Clinical Nutrition

An open-source **Closed-Loop Clinical Nutrition Tool** designed for patients with chronic kidney disease (CKD), kidney transplant recipients, and other patients with strict dietary needs.

Built with love and personal experience after my own kidney transplant at 19 and moving from India to Germany for my Master's.

---

## The Problem

Managing precise nutritional limits (potassium, sodium, phosphorus, protein, etc.) is extremely difficult. Manual tracking is error-prone, and most apps don't respect real medical constraints or actual inventory/pantry at home.

## The Solution

**Clinical Nutrition** is a multi-tenant platform that creates a tight feedback loop between:
- **Clinicians** (Dietitians & Nephrologists) who set medical constraints
- **Patients** who manage their real pantry inventory
- **Smart recommendations** that only suggest meals possible with available ingredients while staying strictly within prescribed limits

## Core Features (In Progress)

- Virtual Pantry management (manual entry + planned OCR receipt scanning)
- Normalized nutritional database (BLS / FDC integration)
- Automatic nutrient calculation for meals
- Doctor/clinician dashboard for monitoring vitals
- Inventory-based recipe suggestions

## Tech Stack

- **Backend**: Django, Django Rest Framework
- **Frontend**: Next.js, TailwindCSS and ShadCN/UI
- **Database**: PostgreSQL
- **Nutrition Data**: BLS (Bundeslebensmittelschlüssel)

## Project Status

**Phase 1 (Current)**: As of June 4th, 2026 core data models and nutrient calculation logic completed. Testing is remaning.

See `inventory/models.py` and `meals/models.py`.

## How to Contribute

This is a **community-driven open source project**.

I (Vedant) will lead the overall architecture and direction, but **everyone is welcome** to:
- Suggest features
- Open issues
- Submit PRs
- Join discussions

**Ways to contribute:**
1. Star the repo ⭐
2. Join the Discord (link coming soon)
3. Pick up an issue
4. Share with doctors, dietitians, or patients who might benefit

## Getting Started

```bash
# Clone the repo
git clone https://github.com/ivedantmistry/clinical-nutrition.git