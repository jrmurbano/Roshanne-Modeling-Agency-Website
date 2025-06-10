from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import Model, Magazine, Photoshoot, Runway, Campaign, ModelCategory, MagazineCategory, Customer, Order, OrderItem
from django.contrib.auth.decorators import login_required
from decimal import Decimal

# Create your views here.
def home(request):
    # Get featured models and latest magazines
    featured_models = Model.objects.filter(user_profile__user__is_active=True)[:3]
    latest_magazines = Magazine.objects.all().order_by('-created_at')[:4]
    context = {
        'featured_models': featured_models,
        'latest_magazines': latest_magazines,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def models(request):
    # Get all active models and categories
    models = Model.objects.filter(user_profile__user__is_active=True)
    categories = ModelCategory.objects.all()
    
    # Get category filter from query parameters
    category_filter = request.GET.get('category')
    if category_filter:
        models = models.filter(category__name=category_filter)
    
    context = {
        'models': models,
        'categories': categories,
        'current_category': category_filter,
    }
    return render(request, 'models.html', context)

def contact(request):
    return render(request, 'contact.html')

def photoshoots(request):
    # Get all photoshoots ordered by date
    photoshoots = Photoshoot.objects.all().order_by('-date')
    context = {
        'photoshoots': photoshoots,
    }
    return render(request, 'photoshoots.html', context)

def magazines(request):
    # Get all magazines and categories
    magazines = Magazine.objects.all()
    categories = MagazineCategory.objects.all()
    
    # Get category filter from query parameters
    category_filter = request.GET.get('category')
    if category_filter:
        magazines = magazines.filter(category__name=category_filter)
    
    context = {
        'magazines': magazines,
        'categories': categories,
        'current_category': category_filter,
    }
    return render(request, 'magazines.html', context)

def runways(request):
    # Get all runways ordered by date
    runways = Runway.objects.all().order_by('-date')
    context = {
        'runways': runways,
    }
    return render(request, 'runways.html', context)

def campaigns(request):
    # Get all active campaigns
    campaigns = Campaign.objects.filter(end_date__gte=timezone.now()).order_by('start_date')
    context = {
        'campaigns': campaigns,
    }
    return render(request, 'campaigns.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Check if user is a customer, if not create one
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={
                    'phone': '',
                    'address': ''
                }
            )
            if created:
                messages.info(request, 'Please complete your customer profile.')
            else:
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register.html')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        # Create customer profile
        Customer.objects.create(
            user=user,
            phone=phone,
            address=address
        )

        # Log the user in
        login(request, user)
        messages.success(request, 'Registration successful! Welcome to Roshanne Modeling Agency.')
        return redirect('home')

    return render(request, 'register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def shopping_bag(request):
    # Get the customer's bag from session
    bag = request.session.get('bag', {})
    bag_items = []
    total = Decimal('0.00')
    items_to_remove = []

    for item_key, item_data in bag.items():
        item_type = item_data.get('type')
        item_id = item_data.get('id')
        quantity = item_data.get('quantity', 1)

        # Only process magazines
        if item_type == 'magazine':
            try:
                item = Magazine.objects.get(id=item_id)
                item_total = item.price * quantity
                total += item_total

                bag_items.append({
                    'id': item_id,
                    'name': item.title,
                    'price': item.price,
                    'quantity': quantity,
                    'total_price': item_total,
                    'type': item_type
                })
            except Magazine.DoesNotExist:
                items_to_remove.append(item_key)
                continue
        else:
            # Remove non-magazine items
            items_to_remove.append(item_key)
            continue

    # Remove any items that no longer exist or are not magazines
    for item_key in items_to_remove:
        del bag[item_key]
    
    # Update the session if any items were removed
    if items_to_remove:
        request.session['bag'] = bag
        messages.warning(request, 'Only magazines can be added to the bag. Other items have been removed.')

    context = {
        'bag_items': bag_items,
        'total': total
    }
    return render(request, 'shopping_bag.html', context)

@login_required
def add_to_bag(request, item_id):
    item_type = request.POST.get('type')
    
    # Only allow magazines to be added to bag
    if item_type != 'magazine':
        messages.error(request, 'Only magazines can be added to the bag!')
        return redirect('magazines')
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Get the bag from session or create new one
    bag = request.session.get('bag', {})
    
    # Create a composite key using item type and ID
    item_key = f"{item_type}_{item_id}"
    
    # Add or update item in bag
    if item_key in bag:
        bag[item_key]['quantity'] += quantity
    else:
        bag[item_key] = {
            'type': item_type,
            'id': item_id,
            'quantity': quantity
        }
    
    # Save bag back to session
    request.session['bag'] = bag
    messages.success(request, 'Magazine added to your bag!')
    
    return redirect('shopping_bag')

@login_required
def update_bag(request, item_id):
    quantity = int(request.POST.get('quantity', 1))
    bag = request.session.get('bag', {})
    
    # Find the item in the bag using the composite key
    item_key = None
    for key, value in bag.items():
        if value.get('id') == item_id:
            item_key = key
            break
    
    if item_key and item_key in bag:
        if quantity > 0:
            bag[item_key]['quantity'] = quantity
        else:
            del bag[item_key]
    
    request.session['bag'] = bag
    return redirect('shopping_bag')

@login_required
def remove_from_bag(request, item_id):
    bag = request.session.get('bag', {})
    
    # Find the item in the bag using the composite key
    item_key = None
    for key, value in bag.items():
        if value.get('id') == item_id:
            item_key = key
            break
    
    if item_key and item_key in bag:
        del bag[item_key]
        request.session['bag'] = bag
        messages.success(request, 'Item removed from your bag!')
    
    return redirect('shopping_bag')

@login_required
def checkout(request):
    # Get the customer's bag from session
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Your bag is empty!')
        return redirect('shopping_bag')

    # Get or create customer profile
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': '',
            'address': ''
        }
    )

    if request.method == 'POST':
        # Update customer information
        customer.phone = request.POST.get('phone', '')
        customer.address = request.POST.get('shipping_address', '')
        customer.save()

        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        # Create order
        order = Order.objects.create(
            customer=customer,
            total_amount=Decimal(request.POST.get('total_amount', 0)),
            shipping_address=request.POST.get('shipping_address', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            notes=request.POST.get('notes', '')
        )

        # Create order items (only magazines)
        for item_key, item_data in bag.items():
            item_type = item_data.get('type')
            item_id = item_data.get('id')
            quantity = item_data.get('quantity', 1)

            if item_type == 'magazine':
                item = get_object_or_404(Magazine, id=item_id)
                OrderItem.objects.create(
                    order=order,
                    item_type=item_type,
                    item_id=item.id,
                    name=item.title,
                    price=item.price,
                    quantity=quantity
                )

        # Clear the bag
        request.session['bag'] = {}
        messages.success(request, 'Order placed successfully!')
        return redirect('order_confirmation', order_number=order.order_number)

    # Calculate total
    total = Decimal('0.00')
    bag_items = []
    for item_key, item_data in bag.items():
        item_type = item_data.get('type')
        item_id = item_data.get('id')
        quantity = item_data.get('quantity', 1)

        if item_type == 'magazine':
            item = get_object_or_404(Magazine, id=item_id)
            item_total = item.price * quantity
            total += item_total

            bag_items.append({
                'id': item_id,
                'name': item.title,
                'price': item.price,
                'quantity': quantity,
                'total_price': item_total,
                'type': item_type
            })

    context = {
        'bag_items': bag_items,
        'total': total,
        'customer': customer
    }
    return render(request, 'checkout.html', context)

@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, customer__user=request.user)
    context = {
        'order': order
    }
    return render(request, 'order_confirmation.html', context)