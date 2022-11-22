from .models import *

def quotationData(request, quotation_id):
    if request.user.is_authenticated:
        user = request.user

        quotation, created = Quotation.objects.get_or_create(id=quotation_id, user=user, client=Client.objects.get(id=259))
        items = quotation.productonquotation_set.all()
        quotation_items = quotation.get_quotation_items

    return {'quotation_items':quotation_items ,'quotation':quotation, 'items':items}