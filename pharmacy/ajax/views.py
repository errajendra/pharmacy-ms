from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from ..models import Stock



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
