from decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand

from shopapp.models import Article, Purchase


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
            help="Recalculate only articles with price tracking enabled.",
        )

    def handle(self, *args, **options):
        articles = Article.objects.all().order_by("id")

        if options["article_id"]:
            articles = articles.filter(pk=options["article_id"])

        if options["tracking_only"]:
            articles = articles.filter(price_tracking=True)

        updated = 0
        empty = 0

        for article in articles:
            prices = list(
                Purchase.objects
                .filter(article=article)
                .values_list("price", flat=True)
            )

            if prices:
                lower_price = min(prices).quantize(CENT, rounding=ROUND_HALF_UP)
                median_price = median(prices).quantize(CENT, rounding=ROUND_HALF_UP)
                updated += 1
            else:
                lower_price = None
                median_price = None
                empty += 1

            Article.objects.filter(pk=article.pk).update(
                lower_price=lower_price,
                median_price=median_price,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {updated} article(s); cleared {empty} article(s) without purchases."
            )
        )
