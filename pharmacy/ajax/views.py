from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import Stock, CustomUser as User, Cart



def search_product(request):
    """ Search Product from POS Billing page. """
    if request.method == 'POST':
        stocks = Stock.objects.select_related()
    
        category_id = request.POST.get("category_id", "")
        try:
            if category_id != "":
                stocks = stocks.filter(category__id=category_id)
        except:
            pass
        
        vender_id = request.POST.get("vender_id", "")
        try:
            if vender_id != "":
                stocks = stocks.filter(Q(vender__id=vender_id))
        except:
            pass
        
        keywords = request.POST.get("keywords", "")
        stocks = stocks.filter(Q(drug_name__icontains=keywords)|Q(generic_drug_name__icontains=keywords))
            
        html = render_to_string("pos/product-list.html", {"drugs": stocks.distinct()[:16]})
        return JsonResponse(
            {
                "status": 200,
                "result": html
            },
            safe=False
        )


def get_total_cart_value(user):
    cart_items = user.cart_items.all()
    total_value = 0
    for item in cart_items:
        if item.total_price:
            total_value += item.total_price
    return round(total_value, 2)


def add_to_cart(request):
    """ Add to Cart of perticular user """
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.POST.get('user_id', None))
        med = request.POST.get('product_id', None)
        medicine = get_object_or_404(Stock, id=med)
        Cart.objects.create(
            user = user,
            medicine = medicine,
        )
        return JsonResponse(
            {
                "status": 200,
            },
            safe=False
        )


def load_cart_items(request):
    """ Cart Items of perticular user """
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.POST.get('user_id', None))
        cart_items = user.cart_items.all()
                    
        html = render_to_string("pos/cart-list.html", {"carts": cart_items})
        return JsonResponse(
            {
                "status": 200,
                "result": html,
                "total_cart_price": get_total_cart_value(user),
            },
            safe=False
        )

def cart_item_update(request):
    """ Cart Items of perticular user """
    if request.method == 'POST':
        cart = get_object_or_404(Cart, id=request.POST.get('cart_id', None))
        
        quantity = request.POST.get("quantity")
        discount = request.POST.get("discount")
        batch = request.POST.get("batch")
        print(quantity, discount, batch)
        cart.quantity = quantity
        cart.discount = discount
        cart.batch = batch
        cart.save()
        
        cart = Cart.objects.get(id=cart.id)
        user = cart.user
        user_cart_total_price = get_total_cart_value(user)
        print(cart.total_price)
        return JsonResponse(
            {
                "status": 200,
                "quantity": quantity,                
                "discount": discount,                
                "batch": batch,
                "price": cart.total_price,   
                "total_cart_price": user_cart_total_price,            
                "message": "Successfully Updated",
            },
            safe=False
        )
