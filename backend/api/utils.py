from .models import *

def quotationData(request, quotation_id):
    if request.user.is_authenticated:
        quotation = Quotation.objects.get(id=quotation_id)
        items = quotation.productonquotation_set.all()
        quotation_items = quotation.get_quotation_items

    return {'quotation_items':quotation_items ,'quotation':quotation, 'items':items}