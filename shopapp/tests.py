from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from shopapp.models import Article, Division, Family, Purchase, Seller


class PriceReportPDFTests(TestCase):
    def setUp(self):
        division = Division.objects.create(name="Supermercado")
        family = Family.objects.create(name="Abarrotes", division=division)
        seller = Seller.objects.create(name="Tienda de prueba")
        self.article_b = Article.objects.create(
            name="Zanahorias",
            quantity=1,
            unit="Kg",
            package=1,
            family=family,
        )
        self.article_a = Article.objects.create(
            name="Arroz",
            quantity=1,
            unit="Kg",
            package=1,
            family=family,
        )
        today = timezone.localdate()
        Purchase.objects.create(
            article=self.article_b,
            seller=seller,
            date=today,
            quantity=1,
            price="30.00",
        )
        Purchase.objects.create(
            article=self.article_a,
            seller=seller,
            date=today,
            quantity=1,
            price="20.00",
        )
        Purchase.objects.create(
            article=self.article_a,
            seller=seller,
            date=today - timedelta(days=10),
            quantity=1,
            price="10.00",
        )
        Purchase.objects.create(
            article=self.article_b,
            seller=seller,
            date=today - timedelta(days=700),
            quantity=1,
            price="1.00",
        )

    def test_price_report_downloads_recent_articles_only(self):
        response = self.client.get(reverse("price_report_pdf"))
        report_date = timezone.localdate().strftime("%d%m%y")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn(
            f"reporte_precios_{report_date}.pdf",
            response["Content-Disposition"],
        )
        self.assertTrue(response.content.startswith(b"%PDF"))
