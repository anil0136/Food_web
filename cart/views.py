from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart, Order, OrderItem
from vendors.models import menubuilding


@login_required
def add_to_cart(request):
    if request.method != "POST":
        return redirect("cart:displaycart")

    food_id = request.POST.get("foodid")
    if not food_id:
        return render(request, "cart/add.html", {"error": "No food selected."})

    food = get_object_or_404(menubuilding, pk=food_id)
    requested_qty = request.POST.get("qty")
    try:
        requested_qty = int(requested_qty) if requested_qty else None
    except ValueError:
        requested_qty = None

    try:
        cart_obj, created = Cart.objects.get_or_create(
            user=request.user,
            fooditem=food,
            defaults={"Qty": requested_qty or 1},
        )

        if not created:
            cart_obj.Qty = requested_qty or ((cart_obj.Qty or 0) + 1)
            cart_obj.save()
    except IntegrityError:
        existing = Cart.objects.filter(user=request.user).first()
        if existing:
            if existing.fooditem_id == food.id:
                existing.Qty = requested_qty or ((existing.Qty or 0) + 1)
            else:
                existing.fooditem = food
                existing.Qty = requested_qty or 1
            existing.save()
            cart_obj = existing
            created = False
        else:
            raise

    return render(request, "cart/add.html", {"cart_item": cart_obj, "created": created})


@login_required
def display_cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related("fooditem", "fooditem__ver")
    total_items = sum(item.Qty for item in cart_items)
    total_price = sum(item.fooditem.price * item.Qty for item in cart_items)

    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart_items,
            "total_items": total_items,
            "total_price": total_price,
        },
    )


@login_required
def update_cart(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    cart_id = request.POST.get("cart_id")
    qty = request.POST.get("qty")

    if not cart_id or qty is None:
        return HttpResponseBadRequest("Missing parameters")

    try:
        qty_val = int(qty)
    except ValueError:
        return HttpResponseBadRequest("Invalid quantity")

    cart_obj = get_object_or_404(Cart, pk=cart_id, user=request.user)

    if qty_val <= 0:
        cart_obj.delete()
        messages.info(request, "Item removed from cart.")
    else:
        cart_obj.Qty = qty_val
        cart_obj.save()

    return redirect("cart:displaycart")


@login_required(login_url="login")
def checkout(request):
    items = Cart.objects.filter(user=request.user).select_related("fooditem", "fooditem__ver")
    grand_total = 0
    total_qty = 0
    item_count = items.count()
    for item in items:
        item.item_total = item.fooditem.price * item.Qty
        grand_total += item.item_total
        total_qty += item.Qty
    return render(
        request,
        "cart/checkout.html",
        {
            "items": items,
            "grand_total": grand_total,
            "total_qty": total_qty,
            "item_count": item_count,
        },
    )


@login_required
def payment(request):
    cart_items = Cart.objects.filter(user=request.user).select_related("fooditem")

    if not cart_items.exists():
        return redirect("cart:displaycart")

    grand_total = sum(item.fooditem.price * item.Qty for item in cart_items)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        valid_methods = [choice[0] for choice in Order.PAYMENT_CHOICES]
        if payment_method not in valid_methods:
            messages.error(request, "Please select a valid payment method.")
            return redirect("cart:payment")

        order = Order.objects.create(
            user=request.user,
            total_amount=grand_total,
            payment_method=payment_method,
            is_paid=True,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food_item=item.fooditem,
                qty=item.Qty,
                price=item.fooditem.price,
            )

        cart_items.delete()
        messages.success(request, "Your order will arrive within 30 minutes.")
        return redirect("home")

    return render(request, "cart/payment.html", {"grand_total": grand_total})
