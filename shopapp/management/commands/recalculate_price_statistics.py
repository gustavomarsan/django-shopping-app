from decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand

from shopapp.models import MonitoredArticle, Purchase


CENT = Decimal("0.01")


def median(values):
    ordered = sorted(values)
    middle = len(ordered) // 2

    if len(ordered) % 2:
        return ordered[middle]

    return (ordered[middle - 1] + ordered[middle]) / Decimal("2")


class Command(BaseCommand):
    help = "Recalculate historical minimum and median prices for articles."

    def add_arguments(self, parser):
        parser.add_argument(
            "--article-id",
            type=int,
            help="Recalculate only one article.",
        )
        parser.add_argument(
            "--tracking-only",
            action="store_true",
            help="Deprecated; all records in this command are monitored articles.",
        )

    def handle(self, *args, **options):
        monitored_articles = MonitoredArticle.objects.select_related("article").order_by("article_id")

        if options["article_id"]:
            monitored_articles = monitored_articles.filter(
                article_id=options["article_id"]
            )

        updated = 0
        empty = 0

        for monitored_article in monitored_articles:
            prices = list(
                Purchase.objects
                .filter(article=monitored_article.article)
                .values_list("price", flat=True)
            )

            if prices:
                lower_price = min(prices).quantize(CENT, rounding=ROUND_HALF_UP)
                median_price = median(prices).quantize(CENT, rounding=ROUND_HALF_UP)
                latest_low_purchase = (
                    Purchase.objects
                    .filter(article=monitored_article.article, price=min(prices))
                    .order_by("-date", "-id")
                    .first()
                )
                lower_price_date = latest_low_purchase.date
                updated += 1
            else:
                lower_price = None
                median_price = None
                lower_price_date = None
                empty += 1

            MonitoredArticle.objects.filter(pk=monitored_article.pk).update(
                lower_price=lower_price,
                lower_price_date=lower_price_date,
                median_price=median_price,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {updated} article(s); cleared {empty} article(s) without purchases."
            )
        )
