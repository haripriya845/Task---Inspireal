from django.shortcuts import render
from .models import User, Listing, PurchaseRequest
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from decimal import Decimal

# Create your views here.
def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        company_name = request.POST.get("company_name", "")
        phone = request.POST.get("phone", "")
        country = request.POST.get("country", "")

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already taken."})

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already taken."})

        user = User(
            username=username,
            email=email,
            role=role,
            company_name=company_name,
            phone=phone,
            country=country
        )
        user.set_password(password)
        user.save()
        send_mail(
            subject="Welcome to SkillLink!",
            message=f"Hello {username}, your account has been successfully created!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True,
        )
        return redirect("login")

    return render(request, "register.html")

def buyer_listings(request):
    listings = Listing.objects.filter(is_active=True)
    category = request.GET.get("category")
    if category:
        listings = listings.filter(category=category)
    return render(request, "buyer_listings.html", {"listings": listings})

def create_request(request, listing_id):
    user = User.objects.get(id=request.session["user_id"])
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == "POST":
        requested_quantity = float(request.POST.get("requested_quantity"))
        message = request.POST.get("message", "")
        if requested_quantity > listing.quantity_available:
            return render(request, "create_request.html", {"listing": listing, "error": "Quantity exceeds available stock."})
        PurchaseRequest.objects.create(
            listing=listing,
            buyer=user,
            supplier=listing.supplier,
            requested_quantity=requested_quantity,
            message=message
        )
        return redirect("/buyer/requests/")
    return render(request, "create_request.html", {"listing": listing})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid email or password."})

        if not user.check_password(password):
            return render(request, "login.html", {"error": "Invalid email or password."})

        request.session["user_id"] = user.id

        if user.role == "buyer":
            return redirect("/buyer/listings/")
        return redirect("/supplier/listings/")

    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    return redirect("index")

def supplier_listings(request):
    user = User.objects.get(id=request.session["user_id"])
    listings = Listing.objects.filter(supplier=user)
    return render(request, "supplier_listings.html", {"listings": listings})

def create_listing(request):
    user = User.objects.get(id=request.session["user_id"])
    if request.method == "POST":
        data = request.POST
        unit_price = data.get("unit_price") or None
        if unit_price:
            unit_price = Decimal(unit_price)
        if data["pricing_mode"] == "fixed" and not unit_price:
            return render(request, "create_listing.html", {"error": "Unit price required for fixed pricing."})
        listing = Listing(
            supplier=user,
            category=data["category"],
            name=data["name"],
            description=data["description"],
            quantity_available=float(data["quantity_available"]),
            unit=data["unit"],
            location_country=data["location_country"],
            pricing_mode=data["pricing_mode"],
            unit_price=unit_price
        )
        listing.save()
        return redirect("/supplier/listings/")
    return render(request, "create_listing.html")

def supplier_requests(request):
    user = User.objects.get(id=request.session["user_id"])
    requests = PurchaseRequest.objects.filter(supplier=user)
    return render(request, "supplier_requests.html", {"requests": requests})

def update_request_status(request, request_id, action):
    req = get_object_or_404(PurchaseRequest, id=request_id)
    if action == "accept":
        req.accept()
    elif action == "reject":
        req.reject()
    return redirect("/supplier/requests/")
def buyer_requests(request):
    user = User.objects.get(id=request.session["user_id"])
    requests = PurchaseRequest.objects.filter(buyer=user).order_by('-created_at')
    return render(request, "buyer_requests.html", {"requests": requests})

def mark_paid_view(request, request_id):
    req = get_object_or_404(PurchaseRequest, id=request_id)
    req.mark_paid()
    
    if request.session.get("user_id"):
        user = User.objects.get(id=request.session["user_id"])
        if user.role == "supplier":
            return redirect("/supplier/requests/")
        else:  
            return redirect("/buyer/requests/")
    return redirect("/")  


def edit_listing(request, listing_id):
    user = User.objects.get(id=request.session["user_id"])
    listing = get_object_or_404(Listing, id=listing_id, supplier=user)

    if request.method == "POST":
        data = request.POST
        listing.category = data["category"]
        listing.name = data["name"]
        listing.description = data["description"]
        listing.quantity_available = float(data["quantity_available"])
        listing.unit = data["unit"]
        listing.location_country = data["location_country"]
        listing.pricing_mode = data["pricing_mode"]

        unit_price = data.get("unit_price") or None
        if listing.pricing_mode == "fixed" and not unit_price:
            return render(request, "edit_listing.html", {"listing": listing, "error": "Unit price required"})

        listing.unit_price = unit_price
        listing.save()

        return redirect("/supplier/listings/")

    return render(request, "edit_listing.html", {"listing": listing})


def delete_listing(request, listing_id):
    user = User.objects.get(id=request.session["user_id"])
    listing = get_object_or_404(Listing, id=listing_id, supplier=user)
    listing.delete()
    return redirect("/supplier/listings/")