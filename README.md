# Full Stack Developer Trainee Assignment (Django Version)

## Overview
This Django web application connects **buyers** and **suppliers**.  
Suppliers can create and manage resource listings, while buyers can browse listings and submit purchase requests or RFQs (Request for Quote).

The project focuses on:
- Clear data flow  
- Functional correctness  
- Role-based navigation  
- End-to-end workflow  

Styling is intentionally minimal — functionality is the priority.

---

## Features

### 🔐 Authentication & Roles
- User signup, login, logout
- Role-based actions (Buyer/Supplier)
- Conditional navigation based on role

### 🏭 Supplier Features
- Create, edit, delete listings
- Manage incoming purchase requests
- Update request statuses
- Handle mock payment marking for fixed-price listings

### 🛒 Buyer Features
- Browse all active listings
- Filter by category
- Submit purchase requests / RFQs
- View own request history

### 💳 Mock Payment
- For fixed-price items: auto-calculates total  
- Supplier can mark request as "Paid"

---

## Views & URLs

### Auth
| Action | View | URL |
|--------|------|-----|
| Home | `index` | `/` |
| Register | `register_view` | `/register/` |
| Login | `login_view` | `/login/` |
| Logout | `logout_view` | `/logout/` |

### Supplier
| Action | View | URL |
|--------|------|-----|
| List listings | `supplier_listings` | `/supplier/listings/` |
| Create listing | `create_listing` | `/supplier/listings/create/` |
| Edit listing | `edit_listing` | `/supplier/listings/<id>/edit/` |
| Delete listing | `delete_listing` | `/supplier/listings/<id>/delete/` |
| View requests | `supplier_requests` | `/supplier/requests/` |
| Update request | `update_request_status` | `/supplier/requests/<id>/<action>/` |
| Mark paid | `mark_paid_view` | `/mark_paid/<id>/` |

### Buyer
| Action | View | URL |
|--------|------|-----|
| Browse listings | `buyer_listings` | `/buyer/listings/` |
| Submit request | `create_request` | `/buyer/listings/<id>/request/` |
| View my requests | `buyer_requests` | `/buyer/requests/` |

---

## Data Models

### User
- `username`, `email`, `password`
- `role` (buyer or supplier)
- Optional: company info, phone, country

### Listing
- Supplier (FK)
- Category, name, description
- Quantity, unit
- Location country
- Pricing mode (fixed / rfq_only)
- Unit price (if fixed)
- Optional image
- Activation status & views count

### PurchaseRequest
- Listing, buyer, supplier (FKs)
- Requested quantity, message
- Status: pending / accepted / rejected
- Payment status: unpaid / paid
- Total amount (auto-calculated for fixed price)

---

## Setup Instructions

1. **Install dependencies:**
```bash
pip install -r requirements.txt
## Apply Migrations
python manage.py migrate
Create Superuser (Optional)
python manage.py createsuperuser
Run the Development Server
python manage.py runserver

## Known Issues
- Minimal styling; focus is on functionality
- Mock payment only
- Basic validation; some edge cases may need refinement

---

## Next Improvements
- Full validation & error handling
- Better UI/UX
- Actual payment gateway integration
- Email / in-app notifications for request updates

---

## AI / LLM Use
- AI-assisted code suggestions were used to speed up development
- All AI-generated code was reviewed, tested, and adapted manually

---

## Author
**Haripriya K V**

Open in Browser
👉 http://127.0.0.1:8000/
