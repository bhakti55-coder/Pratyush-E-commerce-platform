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

# Pratyush Store — Week 2 Milestone

## 🛍️ Enhanced Product Catalog & Visual Variations

During Week 2, the core product engine was expanded to support advanced cataloging requirements. Instead of simple standalone products, the platform now handles rich text descriptions, flexible multi-image galleries, and distinct variant labels to match specific inventory selections.

---

### ✨ Key Features Implemented

* **Multi-Image Product Galleries:** Added the `ProductImage` model linked via a Foreign Key to allow individual products to showcase an unlimited number of secondary angles and promotional graphics.
* **Color & Variant Customization:** Introduced a specialized `color_name` field within the gallery schema to map explicit thumbnail previews to distinct inventory options (e.g., Royal Blue, Ruby Red).
* **Global E-Commerce Policies:** hardcoded pre-filled vendor standards directly into the product layer, keeping data uniform across the platform:
  * *Quality Policy:* 100% Premium Quality Guaranteed
  * *Shipping Policy:* 🔥 FREE SHIPPING ALL OVER INDIA 🔥
  * *Return Policy:* Strict No-Return Policy applies.
  * *Security Measure:* Compulsory package opening video for damage validation.
* **Dynamic Contact Delegation:** Assigned individual contact attributes (`booking_contact_name` and `booking_contact_number`) to each product item to scale multi-vendor management natively.

---

### 🛠️ Database Schema Upgrades
The `shop` app models were updated and successfully applied using Django’s migration engine:

```bash
python manage.py makemigrations shop
python manage.py migrate

### 📂 Option B: `README.md` Content for Week 3

```markdown
# Pratyush Store — Week 3 Milestone

## 🔐 User Authentication & Intelligent Profile Dashboards

Week 3 focused on user security, state persistence, and automation. This update establishes a fully unified system connecting anonymous store guests, registered buyer profiles, and personalized WhatsApp automated checkouts.

---

### ✨ Key Features Implemented

* **Secure Authentication Engine:** Created dedicated user onboarding sequences covering customer Sign-Up, Login restrictions, and instantaneous Navbar state updates based on session validity.
* **Shipping Profile Dashboard:** Designed the comprehensive `Profile` model tracking localized shipping criteria including House No/Flat, Landmarks, District, State, and Pin Code metrics.
* **Fault-Tolerant Signal Automation:** Integrated automatic lifecycle hooks utilizing Django `post_save` receivers. 
  * *Bug Shielding:* Implemented advanced `try/except` logic mapping against `Profile.DoesNotExist` exceptions. This ensures legacy administrative accounts without preset profiles automatically generate profile configurations mid-session without triggering runtime crashes.
* **Pre-Filled Checkout Integration:** Wired the authenticated user's data structures directly into the store’s interactive hooks. Clicking a product link generates an explicit WhatsApp API layout pre-filling saved profile details directly inside the text payload.

---

# Pratyush Store - E-Commerce Platform

A feature-rich, session-based e-commerce storefront built with Django.

## Project Status: Week 4
We have successfully implemented the **Shopping Cart Module**. Users can now add products (including specific color variants) to a persistent session, update quantities, and generate pre-filled WhatsApp checkout messages that include shipping details pulled from their user profiles.

## Key Features Implemented (Week 4)
- **Session-Based Cart:** Persistent shopping sessions without requiring database hits for every view.
- **Dynamic Product Variants:** Support for custom product attributes (e.g., Color) using a composite key strategy.
- **WhatsApp Checkout:** Automatic conversion of cart data into a formatted, ready-to-send WhatsApp order string.
- **Auto-Fill Profiles:** Integration between user profiles and checkout, pre-filling address and contact details.

## Technologies
- **Backend:** Django 5.x, Python 3.x
- **Frontend:** Bootstrap 5, Django Template Engine
- **Version Control:** Git

## Getting Started
1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd pratyush-store