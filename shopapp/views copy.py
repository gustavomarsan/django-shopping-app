from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date, time, timedelta, datetime
from django.http import HttpResponse, HttpRequest
from django.utils.encoding import smart_str
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date, timedelta
from operator import itemgetter
from shopapp.models import Seller, Article, units, Purchase, Division, Family

# Create your views here.

def home(request):
    global time
    global today_str
    time = datetime.now()
    today_str = time.strftime("%Y-%m-%d")
    return render(request, "home.html")

def sellers(request):
    if request.method == "POST" :
        name = request.POST["name"]
        image = request.FILES["photo"]
        seller = Seller.objects.filter(name=name)
        if len(seller) == 0 :
            new_seller = Seller.objects.create(name = name, photo = image)
            messages.success(request, "¡Alta exitosa!")
        else:
            messages.success(request, "Tienda ya existente!")
    if request.method == "GET" :
        pass

    sellers_list =  Seller.objects.order_by("name")
    return render(request, "sellers.html", {"sellers": sellers_list})

def edit_sellers(request, id, action) :
    if action == "delete" :
        seller_to_del = Seller.objects.get(id=id)
        seller_to_del.delete()
        sellers_list =  Seller.objects.order_by("name")
        return render(request, "sellers.html", {"sellers": sellers_list})

    if action == "edit" :
        seller_to_edit = Seller.objects.get(id=id)
        #seller_id = seller_to_edit.id
        #seller_name = seller_to_edit.name
        messages.success(request, "Realice los cambios")
        return render(request, "editseller.html", {"seller": seller_to_edit})

def save_sellers(request) :
    id = request.POST["id"]
    name = request.POST["name"]
    seller_to_edit = Seller.objects.get(id=id)
    seller_to_edit.name = name
    seller_to_edit.save()
    sellers_list =  Seller.objects.order_by("name")
    return render(request, "sellers.html", {"sellers": sellers_list})


def articles(request):
    if request.method == "POST" :
        name = request.POST["name"]
        family_id = request.POST["family"]
        family = Family.objects.get(id=family_id)
        quantity = request.POST["quantity"]
        unit = request.POST["unit"]
        package = request.POST["package"]
        ean = request.POST["ean"]
        image = request.FILES["photo"]
        article = Article.objects.filter(name=name)
        if len(article) == 0 :
            new_article = Article.objects.create(name = name, family = family, quantity = quantity, unit = unit, package = package, ean = ean, photo = image)
            messages.success(request, "¡Alta exitosa!")
        else:
            messages.success(request, "Articulo ya existente!")
    if request.method == "GET" :
        pass

    articles_list =  Article.objects.order_by("name")
    families_list = Family.objects.order_by("name")
    return render(request, "articles.html", {"articles": articles_list, "units": units.values, "families": families_list})

def edit_articles(request, id, action) :
    if action == "delete" :
        article_to_del = Article.objects.get(id=id)
        article_to_del.delete()
        articles_list =  Article.objects.order_by("name")
        return render(request, "articles.html", {"articles": articles_list, "units": units.values})

    if action == "edit" :
        article_to_edit = Article.objects.get(id=id)
        messages.success(request, "Realice los cambios")
        return render(request, "edit_article.html", {"article": article_to_edit, "units": units.values})
    
def save_articles(request) :
    id = request.POST["id"]
    name = request.POST["name"]
    quantity = request.POST["quantity"]
    unit = request.POST["unit"]
    package = request.POST["package"]
    ean = request.POST["ean"]
    article_to_edit = Article.objects.get(id=id)
    article_to_edit.name = name
    article_to_edit.quantity = quantity
    article_to_edit.unit = unit
    article_to_edit.package = package
    article_to_edit.ean = ean
    article_to_edit.save()
    articles_list =  Article.objects.order_by("name")
    return render(request, "articles.html", {"articles": articles_list, "units": units.values})



def tickets(request):
    global time
    global today_str
    if request.method == "POST" :
        date = request.POST["date"]
        seller = request.POST["seller"]
        quantity = request.POST["quantity"]
        article = request.POST["article"]
        price = request.POST["price"]
        note = request.POST["note"]
        today_str = date
        seller_obj = Seller.objects.get(id=seller)
        article_obj = Article.objects.get(id=article)
        purchase = Purchase.objects.filter(date=date, article=article_obj, seller=seller_obj)
        if len(purchase) == 0 :
            new_purchase = Purchase.objects.create(date = date, seller=seller_obj, quantity=quantity, article=article_obj, price = price, note=note)
            messages.success(request, "¡Alta exitosa!")
        else:
            messages.success(request, "Compra ya existente!")

    if request.method == "GET" :
        pass

    purchases_list = Purchase.objects.order_by("-date")
    articles_list =  Article.objects.all().order_by("name")
    sellers_list =  Seller.objects.all().order_by("name")
    #time = datetime.now()
    #today_str = time.strftime("%Y-%m-%d")
    return render(request, "tickets.html", {"purchases": purchases_list, "articles": articles_list, "sellers": sellers_list, 
                                                   "today": today_str})
def edit_tickets(request, id, action) :
    global time
    global today_str
    if action == "delete" :
        purchase_to_del = Purchase.objects.get(id=id)
        purchase_to_del.delete()
        articles_list =  Article.objects.order_by("name")
        messages.success(request, "¡Compra dada de baja!")
    
    purchases_list = Purchase.objects.order_by("-date")
    articles_list =  Article.objects.all().order_by("name")
    sellers_list =  Seller.objects.all().order_by("name")
    time = datetime.now()
    today_str = time.strftime("%Y-%m-%d")
    return render(request, "tickets.html", {"purchases": purchases_list, "articles": articles_list, "sellers": sellers_list, 
                                                   "today": today_str})

def consult_articles(request):
    articles_list = Article.objects.order_by("name")
    return render(request, "consult_articles.html", {"articles": articles_list})

def consult_families(request):
    articles_list = Family.objects.order_by("name")
    return render(request, "consult_families.html", {"families": articles_list})

def consult_prices(request, key, id):
    if key == 'article':
        purchases = Purchase.objects.filter(article = id).order_by("-date")
        article = Article.objects.get(id = id)
        return render(request, "display_prices_by_article.html", {"purchases": purchases, "article": article})
    if key == 'family':
        purchases = Purchase.objects.filter(family = id).order_by("-date")
    
    
