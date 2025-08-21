from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def product_list(request):
       query = request.GET.get('q')
       category_id = request.GET.get('category')
       products = Product.objects.all()
       if query:
           products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
       if category_id:
           products = products.filter(category_id=category_id)
       categories = Category.objects.all()
       return render(request, 'products/list.html', {'products': products, 'categories': categories})

def add_to_cart(request, product_id):
       product = get_object_or_404(Product, id=product_id)
       cart = request.session.get('cart', {})
       cart[str(product_id)] = cart.get(str(product_id), 0) + 1
       request.session['cart'] = cart
       return redirect('product_list')