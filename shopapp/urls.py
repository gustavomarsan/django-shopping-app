"""

URL SHOPAPP

"""
from django.urls import path
from shopapp.views import home, article_list, article_create, article_edit, article_delete, article_purchases, seller_list, seller_create, seller_edit, seller_delete, purchase_list, purchase_create, purchase_edit, purchase_delete,  consult_articles, consult_families



urlpatterns = [
    path('', home, name="home"),
    # ------------ PURCHASE --------------
    path("articles/", article_list, name="article_list"),
    path("articles/create/", article_create, name="article_create"),
    path("articles/<int:pk>/edit/", article_edit, name="article_edit"),
    path("articles/<int:pk>/delete/", article_delete, name="article_delete"),
    path("articles/<int:article_id>/purchases/", article_purchases, name="article_purchases"),
    # ------------ SELLERS --------------
    path("sellers/", seller_list, name= "seller_list"),
    path("sellers/create/", seller_create, name="seller_create"),                     
    path("sellers/<int:pk>/edit/", seller_edit, name="seller_edit"),                    
    path("sellers/<int:pk>/delete/", seller_delete, name="seller_delete"),              
    # ------------ PURCHASE --------------
    path("purchases/", purchase_list, name= "purchase_list"),
    path("purchases/create", purchase_create, name="purchase_create"),
    path("purchases/<int:pk>/edit/", purchase_edit, name="purchase_edit"),
    path("purchases/<int:pk>/delete/", purchase_delete, name="purchase_delete"),
    # ------------ CONSULT --------------
    path('consult_articles/', consult_articles, name="consult_articles"),
    path('consult_families/', consult_families, name="consult_familes"),
    
]





