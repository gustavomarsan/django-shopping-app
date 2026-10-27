from django.shortcuts import render
from django.contrib import messages
from calendar import monthrange
from datetime import time, datetime
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from shopapp.models import Seller, Article, units, Purchase, Division, Family, MonitoredArticle
from shopapp.forms import ArticleForm, SellerForm, PurchaseForm, MonitoredArticleForm, MonitoredArticleURLForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Sum, F
from django.utils import timezone


PRICE_HISTORY_MONTHS = 18
PRICE_CENT = Decimal("0.01")


def months_before(value, months):
    month_index = value.year * 12 + value.month - 1 - months
    year, month_index = divmod(month_index, 12)
    month = month_index + 1
    day = min(value.day, monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


def refresh_stale_monitoring_statistics(monitored_articles):
    cutoff_date = months_before(timezone.localdate(), PRICE_HISTORY_MONTHS)

    for monitored_article in monitored_articles:
        if (
            monitored_article.lower_price_date is None
            or monitored_article.lower_price_date < cutoff_date
        ):
            prices = list(
                Purchase.objects
                .filter(article=monitored_article.article, date__gte=cutoff_date)
                .values_list("price", flat=True)
            )

            if prices:
                prices.sort()
                middle = len(prices) // 2
                if len(prices) % 2:
                    median_price = prices[middle]
                else:
                    median_price = (prices[middle - 1] + prices[middle]) / 2

                lowest_price = prices[0]
                lowest_purchase = (
                    Purchase.objects
                    .filter(
                        article=monitored_article.article,
                        date__gte=cutoff_date,
                        price=lowest_price,
                    )
                    .order_by("-date", "-id")
                    .first()
                )
                monitored_article.lower_price = lowest_price.quantize(
                    PRICE_CENT, rounding=ROUND_HALF_UP
                )
                monitored_article.lower_price_date = lowest_purchase.date
                monitored_article.median_price = median_price.quantize(
                    PRICE_CENT, rounding=ROUND_HALF_UP
                )
            else:
                monitored_article.lower_price = None
                monitored_article.lower_price_date = None
                monitored_article.median_price = None

            monitored_article.save(
                update_fields=["lower_price", "lower_price_date", "median_price"]
            )

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


def family_purchases(request, family_id):
    family = get_object_or_404(Family, id=family_id)
    purchases = (
        Purchase.objects
        .filter(article__family=family)
        .select_related("article", "seller")
        .order_by("-date", "-id")
    )
    return render(
        request,
        "family_purchases.html",
        {"purchases": purchases, "family": family},
    )

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


# MONITORING

def monitored_article_list(request):
    monitored_articles = list(
        MonitoredArticle.objects
        .select_related("article")
        .order_by("article__name")
    )
    refresh_stale_monitoring_statistics(monitored_articles)
    form = MonitoredArticleForm()
    return render(
        request,
        "monitored_articles.html",
        {"monitored_articles": monitored_articles, "form": form},
    )


@require_POST
def monitored_article_create(request):
    form = MonitoredArticleForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Artículo agregado al monitoreo correctamente")
    else:
        messages.error(request, "Error al agregar el artículo al monitoreo")
    return redirect("monitored_article_list")


def monitored_article_edit(request, pk):
    monitored_article = get_object_or_404(MonitoredArticle, pk=pk)

    if request.method == "POST":
        form = MonitoredArticleURLForm(request.POST, instance=monitored_article)
        if form.is_valid():
            form.save()
            messages.success(request, "URL del artículo monitoreado se ha actualizado correctamente")
            return redirect("monitored_article_list")
    else:
        form = MonitoredArticleURLForm(instance=monitored_article)

    return render(
        request,
        "edit_monitored_article.html",
        {"form": form, "monitored_article": monitored_article},
    )


@require_POST
def monitored_article_delete(request, pk):
    monitored_article = get_object_or_404(MonitoredArticle, pk=pk)
    monitored_article.delete()
    messages.success(request, "Artículo eliminado del monitoreo correctamente")
    return redirect("monitored_article_list")



    
