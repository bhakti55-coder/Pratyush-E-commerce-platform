# Pratyush E commerce platform

# 🛍️ Pratyush Retails E-Commerce Platform

This project is a robust, full-stack e-commerce web application built using the **Django** web framework. The primary objective is to engineer a high-performance, scalable online storefront mimicking professional platforms like **pratyushstore.com**, allowing seamless category management, dynamic product displays, and customer booking systems.

---

## ⚙️ Initial Setup

* **Virtual Environment Initialization:** Set up an isolated environment (`venv`) to keep all dependency packages securely isolated from the global system.
* **Core Dependency Installation:** Installed the latest **Django** framework alongside **Pillow** to manage media assets and image uploading workflows.
* **Project Architecture Creation:** Initialized the master configuration directory (`ecommerce_config`) and generated the primary modular application module (`shop`).

---

## 📅 Week 1: Foundation & Database Architecture

During this phase, the primary focus was establishing a scalable backend project architecture and setting up the data persistence layers using standard design principles.

### 📐 Project Architecture & Database Modeling

Organized the application database layer inside `shop/models.py` to support dynamic content updates and rich product metadata via the Django ORM:

* **Bilingual Category Blueprint (`Category` Model):**
  * **`name`**: Main category identifier string supporting combined language catalogs.
  * **`name_mr`**: Dedicated Marathi language database field to cleanly house localized script headers (e.g., `ज्वेलरी`).
  * **`slug`**: A unique text token path field used for safe, search-engine-friendly clean browser URLs.
* **Dynamic Catalog Blueprint (`Product` Model):**
  * Configured structural database definitions utilizing key relational constraints including foreign keys to bind products to specific category trees, decimal types for currency fields, booleans for stock visibility controls, and a dedicated image field.

### 🔧 Django Administrative Dashboard Configuration

Registered backend blueprints into `shop/admin.py` to create a production-grade content management dashboard:

* Customized data item layouts utilizing advanced list options (`list_display`, `list_filter`, and `list_editable`) for immediate inventory oversight.
* Activated automated **`prepopulated_fields`** to allow Django to automatically generate web-safe slugs from text entries instantly.

### 🖼️ Local Media Asset Engine

Configured the development web stack to handle physical product images cleanly:

* Declared explicit local routing parameters (`MEDIA_URL` and `MEDIA_ROOT`) inside the main environment `settings.py` file.
* Appended dynamic directory static mapping configurations directly into the main `urls.py` pattern routing lists to allow uploaded assets to serve smoothly during development.

### 📦 Database Synchronization & Inventory Populating

* **Schema Error Mitigation:** Safely tracked down and resolved table structural mismatch anomalies (`OperationalError`) by applying automated code base migrations (`makemigrations`, `migrate`) to safely sync new bilingual columns with the SQLite engine database file.
* **Live Catalog Seeding:** Populated the administrative backend database with real-world product lines spanning key consumer classifications: **Sarees, Jewellery, Kurtis & Dresses, and Coord Sets**.

---

## 💻 Tech Stack
* **Backend Framework:** Python 3.13 / Django
* **Database Management:** SQLite3
* **Graphics Processing:** Pillow Library

---

## 🚀 How to Run the Environment Locally

Follow these precise operational terminal sequences to initiate the development environment:

**1. Activate the isolated workspace:**
```bash
venv\Scripts\activate