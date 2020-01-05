from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

def order_pdf(obj):
	return mark_safe('<a href="{}">PDF</a>'.format(
		reverse('staff:admin_order_pdf', args=[obj.id])))
order_pdf.short_description = 'Invoice'
