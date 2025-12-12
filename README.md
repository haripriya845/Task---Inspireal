# Full Stack Developer Trainee Assignment (Django Version)


## Overview
A Django web application connecting **buyers** and **suppliers**.  
Suppliers can create and manage resource listings, while buyers can browse listings and submit purchase requests or quotes.  

**Focus:** end-to-end functionality, clear data flow, and role-based access.

---

## Features

| Feature | Description |
|---------|-------------|
| User Authentication | Sign up, log in, log out with role-based access (buyer/supplier) |
| Supplier Listings | Create, edit, delete, and view listings |
| Buyer Requests | Browse listings, submit purchase requests or RFQs |
| Request Management | Suppliers can view incoming requests and update status |
| Mock Payment | Mark fixed-price requests as Paid (simulation only) |
| Role-Based Navigation | Different views/actions based on buyer or supplier role |

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
| List supplier’s listings | `supplier_listings` | `/supplier/listings/` |
| Create listing | `create_listing` | `/supplier/listings/create/` |
| Edit listing | `edit_listing` | `/supplier/listings/<id>/edit/` |
| Delete listing | `delete_listing` | `/supplier/listings/<id>/delete/` |
| List incoming requests | `supplier_requests` | `/supplier/requests/` |
| Update request status | `update_request_status` | `/supplier/requests/<id>/<action>/` |

### Buyer
| Action | View | URL |
|--------|------|-----|
| Browse listings | `buyer_listings` | `/buyer/listings/` |
| Submit request | `create_request` | `/buyer/listings/<id>/request/` |
| View requests | `buyer_requests` | `/buyer/requests/` |

### Payment (Mock)
| Action | View | URL |
|--------|------|-----|
| Mark Paid | `mark_paid_view` | `/mark_paid/<id>/` |

---

## Data Models

### User
- `username`, `email`, `password` (hashed)  
- `role` (buyer or supplier)  
- Optional: `company_name`, `phone`, `country`  

### Listing
- `supplier` (FK to User)  
- `category`, `name`, `description`, `quantity_available`, `unit`, `location_country`  
- `pricing_mode`, `unit_price`, optional `image`  
- `is_active`, `views_count`  

### PurchaseRequest
- `listing`, `buyer`, `supplier` (FKs)  
- `requested_quantity`, `message`  
- `status` (pending/accepted/rejected), `payment_status` (unpaid/paid)  
- `total_amount` (calculated automatically)  

---

## Tech Stack
- Python 3.x  
- Django 4.x  
- SQLite (default)  
- HTML/CSS for templates  
- Optional: Pillow (for image upload)

---

## Setup Instructions

1. Clone the repo:  
```bash
git clone <repo-url>
cd <project-folder>
**Install dependencies:**

pip install -r requirements.txt
Apply migrations:
python manage.py migrate
Create superuser (optional):
python manage.py createsuperuser
Run the development server:
python manage.py runserver
Open in browser: http://127.0.0.1:8000/
```
## Known Issues
- Minimal styling; focus is on functionality
- Mock payment only
- Basic validation; edge cases may need improvement

---

## Next Improvements
- Full validation & error handling
- Enhanced UI/UX
- Real payment integration
- Notifications for request updates

---

## AI / LLM Use
- AI-assisted code suggestions were used to speed up development
- All AI-generated code was reviewed and adapted manually

## Author
**Haripriya K V**
