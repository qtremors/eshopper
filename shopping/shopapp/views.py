from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib import messages

from .models import*
from django.db.models import Sum

from django.core.mail import send_mail
from django.core.paginator import Paginator
import random
from django.conf import settings
import razorpay
import os




def contact(request):
    context = unicon(request)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Redirect to the same page to clear the form
        else:
            messages.error(request, "Please fill in all required fields (Name, Email, Message).")
    return render(request,"contact.html", context)





# common context
def unicon(request): 
    context = {}
    context["category"] = Category.objects.all().order_by("id")
    context["sub_category"] = Sub_category.objects.all().order_by("-id")

    user_logged_in = False
    user_email = None
    cart_item_count = 0
    wishlist_item_count = 0

    if 'email' in request.session:
        user_logged_in = True
        user_email = request.session.get('email')
        try:
            user = User.objects.get(email=user_email)
            
            cart_total_quantity = Add_to_cart.objects.filter(user_id=user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
            cart_item_count = cart_total_quantity if cart_total_quantity is not None else 0
            
            wishlist_item_count = Wishlist.objects.filter(user_id=user).count()
        except User.DoesNotExist:
            pass

    context['user_logged_in'] = user_logged_in
    context['email'] = user_email
    context['cart_item_count'] = cart_item_count
    context['wishlist_item_count'] = wishlist_item_count

    return context



def index(request):
    context = unicon(request)
    return render(request, "index.html", context)





def register(request):
    context = unicon(request)
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            return render(request, "register.html", {"emsg": "Passwords do not match"})
        elif User.objects.filter(email=email).exists():
            return render(request, "register.html", {"emsg": "Email already registered"})
        else:
            User.objects.create(username=username, email=email, password=password)
            return redirect('login')
    else:
        return render(request, "register.html", context)
    





def login(request):
    context = unicon(request)
    if 'email' in request.session:
        return render(request, "index.html", context)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            context['error_message'] = "Both email and password are required."
            return render(request, "login.html", context)

        try:
            user = User.objects.get(email=email)
            if user.password == password:
                request.session['email'] = user.email
                return redirect("index")
            else:
                context['error_message'] = "Invalid password."
                return render(request, "login.html", context)
        except User.DoesNotExist:
            context['error_message'] = "No account found with that email."
            return render(request, "login.html", context)
        except Exception as e:
            context['error_message'] = f"An unexpected error occurred: {e}"
            return render(request, "login.html", context)
    else:
        return render(request, "login.html", context)





def profile(request):
    # Get common context for the template
    context = unicon(request)

    # Check if the user is logged in
    if 'email' not in request.session:
        return redirect('login')

    try:
        # Retrieve the user object based on the email in the session
        user = User.objects.get(email=request.session['email'])
        context['user'] = user  # Add the user object to the context

        # --- DEBUGGING LINE START ---
        print(f"DEBUG: User profile_picture field: {user.profile_picture}")
        if user.profile_picture:
            print(f"DEBUG: User profile_picture URL: {user.profile_picture.url}")
        else:
            print("DEBUG: User profile_picture is None or empty.")
        # --- DEBUGGING LINE END ---

    except User.DoesNotExist:
        # If user does not exist, log them out and redirect to login
        if 'email' in request.session:
            del request.session['email']
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')

    # For GET requests, render the profile page with user data
    return render(request, "profile.html", context)


    




def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return render(request,"login.html")





def forget(request):
    if request.POST:
        email=request.POST['email']
        otp=random.randint(1000,9999)
        try:
            user=User.objects.get(email=email)
        
            user.otp=otp
            user.save()
            send_mail("django",f"your otp is - {otp}",'quantumtremors@gmail.com',[email])
            contaxt={
                "email":email
            }
            return render(request,"confirm_password.html",contaxt)
        except:
            print("Invalid Email")       
            return render(request,"forget.html") 
    else:
        return render(request,"forget.html")
    




def confirm_password(request):
    if request.POST:
        email = request.POST['email']
        otp = request.POST['otp']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = User.objects.filter(email=email)

        if not user:
            return render(request, "confirm_password.html",
                          {"error_message": "Invalid Email", "email": email})

        if user.otp != int(otp):
            return render(request, "confirm_password.html",
                          {"error_message": "Invalid OTP", "email": email})

        if new_password != confirm_new_password:
            return render(request, "confirm_password.html",
                          {"error_message": "Passwords do not match", "email": email})

        user.password = new_password
        # user.otp = None
        user.save()

        return redirect('login')
    else:
        email = request.GET.get('email')
        return render(request, "confirm_password.html", {"email": email})
    




def update_profile(request):
    # Get common context for the template
    context = unicon(request)

    # Check if the user is logged in
    if 'email' not in request.session:
        return redirect('login')

    try:
        # Retrieve the user object based on the email in the session
        user = User.objects.get(email=request.session['email'])
        context['user'] = user  # Add the user object to the context
    except User.DoesNotExist:
        # If user does not exist, log them out and redirect to login
        if 'email' in request.session:
            del request.session['email']
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')

    if request.method == 'POST':
        # Get updated username and email from the POST request
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        # Update username if provided and different
        if new_username and new_username != user.username:
            user.username = new_username
            messages.success(request, "Username updated successfully!")
        
        # Update email if provided and different
        if new_email and new_email != user.email:
            # Basic email validation (you might want more robust validation)
            if '@' in new_email and '.' in new_email:
                # Check if the new email already exists for another user
                if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                    messages.error(request, "This email is already in use by another account.")
                    return render(request, "profile.html", context) # Render with error message
                user.email = new_email
                # Update session email if the email was changed successfully
                request.session['email'] = new_email
                messages.success(request, "Email updated successfully!")
            else:
                messages.error(request, "Please enter a valid email address.")
                return render(request, "profile.html", context) # Render with error message

        # Handle profile picture update
        if 'profile_picture' in request.FILES:
            # Optional: Delete old profile picture if it exists
            if user.profile_picture:
                old_profile_picture_path = user.profile_picture.path
                if os.path.exists(old_profile_picture_path):
                    os.remove(old_profile_picture_path)
            
            user.profile_picture = request.FILES['profile_picture']
            messages.success(request, "Profile picture updated successfully!")
        
        user.save() # Save the user object with all updated fields

        # Redirect back to the profile page after update
        return redirect('profile')

    # For GET requests, render the profile page with user data
    return render(request, "profile.html", context)







def shop(request, subcategory_name=None):
    #(includes user_logged_in, email, category, sub_category)
    context = unicon(request)

    products = Product.objects.all()

    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)

    if subcategory_name:
        try:
            selected_subcategory = Sub_category.objects.get(name=subcategory_name)
            products = products.filter(subcategory=selected_subcategory)
        except Sub_category.DoesNotExist:
            pass 
    

    selected_price_range = request.GET.get('price_range')
    if selected_price_range:
        if selected_price_range == "0 to 100":
            products = products.filter(price__lt=100)
        elif selected_price_range == "100 to 500":
            products = products.filter(price__gte=100, price__lte=500)
        elif selected_price_range == "500 to 1000":
            products = products.filter(price__gte=500, price__lte=1000)
        elif selected_price_range == "1000 to 2000":
            products = products.filter(price__gte=1000, price__lte=2000)
        elif selected_price_range == "2000 to 3000":
            products = products.filter(price__gte=2000, price__lte=3000)
        elif selected_price_range == "3000 to 5000":
            products = products.filter(price__gte=3000, price__lte=5000)

    user_wishlist = []
    if 'email' in request.session:
        try:
            user = User.objects.get(email=request.session['email'])
            user_wishlist = Wishlist.objects.filter(user_id=user).values_list('product_id', flat=True)
        except User.DoesNotExist:
            pass

    for product in products:
        product.is_wished = product.id in user_wishlist

    paginator=Paginator(products,6)  
    page_number=request.GET.get("page",1)  
    products=paginator.get_page(page_number)
    show_page=paginator.get_elided_page_range(products.number,on_each_side=2,on_ends=1)


    context["pid"] = products
    context["price"] = Price.objects.all()
    context["show_page"] = show_page

    return render(request, 'shop.html', context)








def detail(request, id):
    # (includes user_logged_in, email, category, sub_category)
    context = unicon(request)

    try:
        pid = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found") 

    context["pid"] = pid

    return render(request, 'detail.html', context)





def cart(request):
    #(user_logged_in, email, category, sub_category)
    context = unicon(request)

    cart_items = []
    total_cart_price = 0
    discount_amount = 0
    final_total_price = 0

    if not context['user_logged_in']:
        return redirect("login")
    
    try:
        # Use the email from the common_context (which comes from request.session)
        user = User.objects.get(email=context['email']) 
        
        cart_items = Add_to_cart.objects.filter(user_id=user)
        
        for item in cart_items:
            total_cart_price += item.total_price

        
        # Apply discount if present in session
        if 'coupon_discount' in request.session:
            discount_percentage = request.session['coupon_discount']
            discount_amount = (total_cart_price * discount_percentage) / 100
            final_total_price = total_cart_price - discount_amount
            # del request.session['coupon_discount']
        else:
            final_total_price = total_cart_price

            
    except User.DoesNotExist:
        # request.session.flush()
        return redirect("login")

    context["cart_items"] = cart_items
    context["total_cart_price"] = total_cart_price

    context["discount_amount"] = discount_amount
    context["final_total_price"] = final_total_price

    return render(request, "cart.html", context)






def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")

    email = request.session.get("email")
    if not email:
        return redirect("login")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponseNotFound("User not found")

    cart_item, created = Add_to_cart.objects.get_or_create(
        user_id=user,
        product_id=product,
        defaults={ # These values are used only if a new object is created
            'name': product.name,
            'price': product.price,
            'image': product.image,
            'quantity': 1,
            'total_price': product.price
        }
    )

    if not created:
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * cart_item.price
        cart_item.save()

    return redirect("cart")




def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            request.session['coupon_discount'] = float(coupon.discount_percentage)
            request.session['coupon_message'] = "Coupon applied successfully!"
        except Coupon.DoesNotExist:
            request.session['coupon_message'] = "Invalid or expired coupon code."
        return redirect('cart')
    return redirect('cart')




def inc_product(request,id):
    inc=Add_to_cart.objects.get(id=id)
    if inc:
        inc.quantity += 1
        inc.total_price = inc.quantity * inc.price
        inc.save()
    return redirect("cart")





def dec_product(request,id):
    dec=Add_to_cart.objects.get(id=id)
    if dec:
        dec.quantity -= 1
        dec.total_price = dec.quantity * dec.price
        dec.save()
    if dec.quantity == 0:
        dec.total_price = dec.quantity * dec.price
        dec.delete()
    return redirect("cart")





def del_product(request,id):
    delp=Add_to_cart.objects.get(id=id)
    delp.delete()
    return redirect("cart")




def add_to_wishlist(request, product_id):

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")

    email = request.session.get("email")
    if not email:
        return redirect("login")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponseNotFound("User not found")


    wishlist_item = Wishlist.objects.filter(user_id=user, product_id=product).first()

    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(
            user_id=user,
            product_id=product,
            name=product.name,
            price=product.price,
            image=product.image,
        )

    return redirect("shop")





def wishlist(request):
    # (user_logged_in, email, category, sub_category)
    context = unicon(request)

    wishlist_items = []

    if not context['user_logged_in']:
        return redirect("login")

    try:
        # Use the email from the common_context (which comes from request.session)
        user = User.objects.get(email=context['email'])
        
        wishlist_items = Wishlist.objects.filter(user_id=user) 
        
    except User.DoesNotExist:
        return redirect("login")

    context["wishlist_items"] = wishlist_items

    return render(request, "wishlist.html", context)





def del_wishlist_product(request, id):
    try:
        wishlist_item = Wishlist.objects.get(id=id)
        wishlist_item.delete()
    except Wishlist.DoesNotExist:
        return HttpResponseNotFound("Wishlist item not found")
    return redirect("wishlist")






def checkout(request):
    context = unicon(request)

    cart_items_product = []
    subtotal = 0
    shipping_cost = 50

    if not context['user_logged_in']:
        return redirect("login")

    try:
        user = User.objects.get(email=context['email'])
        cart_items_product = Add_to_cart.objects.filter(user_id=user)

        for item in cart_items_product:
            subtotal += item.total_price

        discount_amount = 0
        if 'coupon_discount' in request.session:
            discount_percentage = request.session['coupon_discount']
            discount_amount = (subtotal * discount_percentage) / 100
            subtotal -= discount_amount
            del request.session['coupon_discount']
        
        final_total = subtotal + shipping_cost
        razorpay_amount = int(round(final_total * 100))
        
        client = razorpay.Client(auth=('rzp_test_uqhoYnBzHjbvGF', 'jEhBs6Qp9hMeGfq5FyU45cVi'))
        response = client.order.create({
                'amount': razorpay_amount,
                'currency': 'INR',
                'payment_capture': 1
        })
        print("Razorpay response:",response)

    except User.DoesNotExist:
        return redirect("login")

    context["cart_items_product"] = cart_items_product
    context["subtotal"] = subtotal
    context["shipping_cost"] = shipping_cost
    context["response"] = response
    context["final_total_price"] = final_total
    context["discount_amount"] = discount_amount 

    return render(request, "checkout.html", context)






def order(request):
    context = unicon(request)

    if not context['user_logged_in']:
        return redirect("login")

    user = None
    try:
        user = User.objects.get(email=context['email'])
    except User.DoesNotExist:
        return redirect("login")

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2', '')
        country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        cart_items = Add_to_cart.objects.filter(user_id=user)
        if not cart_items.exists():
            return redirect('cart')

        subtotal = sum(item.total_price for item in cart_items)
        shipping_cost = 50

        discount_amount = 0
        if 'coupon_discount' in request.session:
            discount_percentage = request.session['coupon_discount']
            discount_amount = (subtotal * discount_percentage) / 100
            subtotal -= discount_amount
            del request.session['coupon_discount']

        total_amount = subtotal + shipping_cost


        new_order = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_no=mobile_no,
            address_line1=address_line1,
            address_line2=address_line2,
            country=country,
            city=city,
            state=state,
            zip_code=zip_code,
            total_amount=total_amount,
            order_date=timezone.now()
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=new_order,
                product=item.product_id,
                name=item.name,
                price=item.price,
                quantity=item.quantity,
                total_price=item.total_price
            )

        cart_items.delete()

        return redirect('order')

    else:
        user_orders = Order.objects.filter(user=user).order_by('-order_date')

        context["user_orders"] = user_orders
        return render(request, "order.html", context)





def cancel_order(request,id):
    delp=Order.objects.get(id=id)
    delp.delete()
    return redirect("order")




def add_review(request, product_id):
    if 'email' not in request.session:
        return redirect('login') 

    try:
        product = Product.objects.get(id=product_id)

        if request.method == 'POST':
            rating_str = request.POST.get('rating')
            comment = request.POST.get('comment')
            reviewer_name = request.POST.get('name') 
            
            try:
                user = User.objects.get(email=request.session['email'])
            except User.DoesNotExist:
                return redirect('login') 

            if not rating_str or not comment:
                return redirect('detail', id=product.id)

            try:
                rating = int(rating_str)
                if not (1 <= rating <= 5):
                    return redirect('detail', id=product.id)
            except (ValueError, TypeError):
                return redirect('detail', id=product.id)


            Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                comment=comment,
                reviewer_name=reviewer_name
            )

            product.update_average_rating()
            
            return redirect('detail', id=product.id)

        else:
            return redirect('detail', id=product.id)

    except Product.DoesNotExist:
        return redirect('index')





