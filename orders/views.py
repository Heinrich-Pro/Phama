from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Order, OrderItem
from products.models import Product
from reportlab.pdfgen import canvas
from django.http import HttpResponse


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        # Redirect to product list if cart is empty
        return redirect('product_list')

    total = 0
    items = []
    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=pid)
        price = product.price * qty
        total += price
        items.append({'product': product, 'quantity': qty, 'price': price})

    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=total)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )
            # Reduce stock
            item['product'].stock -= item['quantity']
            item['product'].save()
        # Email to client and admin
        send_mail(
            'Commande confirmée',
            f'Votre commande {order.id} est prête pour récupération. Téléchargez votre facture ici: http://127.0.0.1:8000/orders/{order.id}/invoice/',
            'admin@pharmacy.com',
            [request.user.email],
            fail_silently=True
        )
        send_mail(
            'Nouvelle commande',
            f'Commande {order.id} de {request.user.username}.',
            'admin@pharmacy.com',
            ['admin@email.com'],
            fail_silently=True
        )
        # Clear cart from session if it exists
        if 'cart' in request.session:
            del request.session['cart']
        return redirect('order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {'items': items, 'total': total})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Facture pour commande {order.id}")
    p.drawString(100, 780, f"Client: {order.user.username}")
    p.drawString(100, 760, f"Date: {order.created_at}")
    p.drawString(100, 740, f"Total: {order.total_price} €")
    y = 720
    for item in order.items.all():
        p.drawString(100, y, f"{item.quantity} x {item.product.name} - {item.price} €")
        y -= 20
    p.drawString(100, y, "À payer sur place lors de la récupération.")
    p.showPage()
    p.save()
    return response