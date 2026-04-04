from django.contrib import admin

from shopapp.models import Seller, Article, Purchase, Division, Family

# Register your models here.

class SellerAdmin(admin.ModelAdmin):
    list_display = ["name"]

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["name", "package"]
    list_filter = ("unit" , "package", "family")


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["date", "quantity", "article", "price", "seller"]
    date_hierarchy = "date"

class DivisionAdmin(admin.ModelAdmin):
    list_display = ["name"]

class FamilyAdmin(admin.ModelAdmin):
    list_display = ["name", "division"]

admin.site.register(Seller, SellerAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Family, FamilyAdmin)
