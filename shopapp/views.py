from django.shortcuts import render
from django.contrib import messages
from datetime import time, datetime
from datetime import datetime
from shopapp.models import Seller, Article, units, Purchase, Division, Family
from shopapp.forms import ArticleForm, SellerForm, PurchaseForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Sum, F

# Create your views here.

def home(request):
    global time
    global today_str
    time = datetime.now()
    today_str = time.strftime("%Y-%m-%d")
    return render(request, "home.html")


# SELLERS

def seller_list(request):
    sellers =  Seller.objects.order_by("name")
    form = SellerForm()

    return render(
        request,
        "sellers.html",
        {
            "sellers": sellers,
            "form": form,
        }
    )

@require_POST
def seller_create(request):
    form = SellerForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "Supermercado creada correctamente")
    else:
        messages.error(request, "Error al crear el supermercado")

    return redirect("seller_list")

def seller_edit(request, pk):
    seller = get_object_or_404(Seller, pk=pk)

    if request.method == "POST":
        form = SellerForm(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            form.save()
            messages.success(request, "Cambios guardados correctamente")
            return redirect("seller_list")
    else:
        form = ArticleForm(instance=seller)

    return render(
        request,
            "edit_seller.html",
        {
            "form": form,
            "seller": seller,
            }
    )

@require_POST
def seller_delete(request, pk):
    seller = get_object_or_404(Seller, pk=pk)
    seller.delete()
    messages.success(request, "Supermercado eliminado correctamente")

    return redirect("seller_list")


# ARTICLES

def article_list(request):
    articles = Article.objects.order_by("name")
    form = ArticleForm()

    return render(
        request,
        "articles.html",
        {
            "articles": articles,
            "form": form,
        }
    )

@require_POST
def article_create(request):
    form = ArticleForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Artículo creado correctamente")
    else:
        messages.error(request, "Error al crear el artículo")

    return redirect("article_list")

def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect("article_list")
    else:
        form = ArticleForm(instance=article)

    return render(
        request,
        "edit_article.html",
        {
            "form": form,
            "article": article,
        }
    )

@require_POST
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    messages.success(request, "Artículo eliminado correctamente")

    return redirect("article_list")


def article_purchases(request, article_id):
        article = get_object_or_404(Article, id=article_id)
        purchases = Purchase.objects.filter(article = article).order_by("-date")
        return render(request, "article_purchases.html", {"purchases": purchases, "article": article})

# PURCHASE

def purchase_list(request):
    purchases = Purchase.objects.order_by("-date")
    form = PurchaseForm()

    return render(
        request,
        "purchase.html",
        {
            "purchases": purchases,
            "form": form,
        }
    )

def purchase_create(request):
    form = PurchaseForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Compra creada correctamente")
    else:
        messages.error(request, "Error al crear la compra")

    return redirect("purchase_list")

def purchase_edit(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == "POST":
        form = PurchaseForm(request.POST, request.FILES, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect("purchase_list")
    else:
        form = PurchaseForm(instance=purchase)

    return render(
        request,
        "edit_purchase.html",
        {
            "form": form,
            "purchase": purchase,
        }
    )

@require_POST
def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    purchase.delete()
    messages.success(request, "Compra eliminada correctamente")

    return redirect("purchase_list")



# VERIFICACION
def purchase_verification(request):
    sellers = Seller.objects.order_by("name")
    total = None
    selected_date = None
    selected_seller = None
    last_purchase = Purchase.objects.order_by("-date").first()
    default_date = last_purchase.date if last_purchase else datetime.now().date()

    if request.method == "POST":
        date_str = request.POST.get("date")
        seller_id = request.POST.get("seller")
        if date_str and seller_id:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            selected_seller = get_object_or_404(Seller, pk=seller_id)
            result = Purchase.objects.filter(
                date=selected_date, seller=selected_seller
            ).aggregate(total=Sum(F("quantity") * F("price")))
            total = result["total"]

    return render(request, "purchase_verification.html", {
        "sellers": sellers,
        "total": total,
        "selected_date": selected_date,
        "selected_seller": selected_seller,
        "default_date": default_date,
    })


# CONSULTS
def consult_articles(request):
    articles_list = Article.objects.order_by("name")
    return render(request, "consult_articles.html", {"articles": articles_list})

def consult_families(request):
    articles_list = Family.objects.order_by("name")
    return render(request, "consult_families.html", {"families": articles_list})



    
