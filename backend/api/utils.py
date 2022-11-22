from .models import *

def quotationData(request):
	if request.user.is_authenticated:
		user = request.user
		quotation, created = Quotation.objects.get_or_create(user=user, client="")
		items = quotation.orderitem_set.all()
		quotation_items = quotation.get_cart_items

	return {'quotation_items':quotation_items ,'quotation':quotation, 'items':items}