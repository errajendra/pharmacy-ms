from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import Stock, CustomUser as User, Cart, BillingPOS



def search_product(request):
    """ Search Product from POS Billing page. """
    if request.method == 'POST':
        stocks = Stock.objects.select_related().filter(status=True)
    
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
            discount = medicine.discount
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
        
        cart.quantity = quantity
        cart.discount = discount
        cart.save()
        
        cart = Cart.objects.get(id=cart.id)
        user = cart.user
        user_cart_total_price = get_total_cart_value(user)
        
        return JsonResponse(
            {
                "status": 200,
                "quantity": quantity,                
                "discount": discount,
                "price": cart.total_price,   
                "total_cart_price": user_cart_total_price,            
                "message": "Successfully Updated",
            },
            safe=False
        )


def cart_item_delete(request):
    """ Cart Items of perticular user """
    if request.method == 'POST':
        cart = get_object_or_404(Cart, id=request.POST.get('cart_id', None))
        cart.delete()
        return JsonResponse(
            {
                "status": 200,         
                "message": "Successfully Deleted.",
            },
            safe=False
        )



""" Place Order from POS Billing Page. """
def place_order_poc_billing(request):
    if request.method == 'POST':
        try:
            data = request.POST
            message = "OK"
            
            custumer = get_object_or_404(User, id=data['customer_id'])
            sub_total = data['sub_total']
            invoice_discount_type = data['invoice_discount_type']
            invoice_discount = data['invoice_discount']
            total_discount = data['total_discount']
            tax_percent = data['tax_percent']
            grand_total = data['grand_total']
            tax = data['tax']
            
            custumer_cart_items = custumer.cart_items.all()
            order_details = []
            medicins = []
            for cart in custumer_cart_items:
                order_details.append(
                    {
                        "medicine_id": cart.medicine.id,
                        "medicine": cart.medicine.drug_name,
                        "price": cart.medicine.price,
                        "medicine_batch": cart.medicine.batch,
                        "quantity": cart.quantity,
                        "discount": f"{cart.discount} %",
                        "total": cart.total_price
                    }
                )
                medicins.append({"med":cart.medicine, "qty":cart.quantity})
            
            order_data = {
                "sub_total": sub_total,
                "invoice_discount_type": invoice_discount_type,
                "invoice_discount_value": invoice_discount,
                "total_discount": total_discount,
                "tax_percent": tax_percent,
                "tax": tax,
                "grand_total": grand_total,
                "item_details": order_details,            
            }
            # Create order here
            order = BillingPOS.objects.create(
                custumer = custumer,
                details = order_data
            ) 
            for i in medicins:
                med = i['med']
                med.quantity = med.quantity - i['qty']
                med.save()
            
            bill_slip_url = f"billing/{order.id}/print/"
            data = {
                "status": 200,
                "message": message,
                "bill_slip_url": bill_slip_url,
            }
            return JsonResponse(data)
        
        except Exception as ex:
            print(ex)
            return JsonResponse({"status":500, "message": "Internal Server Error", "error": f"{ex}"}, status=500)
        
    return JsonResponse({"status":405, "message": "Method Not allowed"}, status=405)
