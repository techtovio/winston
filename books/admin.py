from django.contrib import admin
from .models import Ebook, EbookCategory, EbookPurchase


admin.site.register(Ebook)
admin.site.register(EbookCategory)
admin.site.register(EbookPurchase)