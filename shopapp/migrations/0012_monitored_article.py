from django.db import migrations, models
import django.db.models.deletion


def copy_existing_monitoring(apps, schema_editor):
    Article = apps.get_model("shopapp", "Article")
    MonitoredArticle = apps.get_model("shopapp", "MonitoredArticle")

    for article in Article.objects.filter(price_tracking=True):
        MonitoredArticle.objects.create(
            article_id=article.pk,
            lower_price=article.lower_price,
            median_price=article.median_price,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0011_add_price_monitoring_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="MonitoredArticle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sams_url",
                    models.URLField(blank=True, verbose_name="URL de Sam's Club"),
                ),
                (
                    "lower_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        editable=False,
                        max_digits=7,
                        null=True,
                        verbose_name="Precio mínimo histórico",
                    ),
                ),
                (
                    "median_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        editable=False,
                        max_digits=7,
                        null=True,
                        verbose_name="Precio mediano histórico",
                    ),
                ),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="shopapp.article",
                    ),
                ),
            ],
            options={
                "verbose_name": "Monitored article",
                "verbose_name_plural": "Monitored articles",
                "constraints": [
                    models.UniqueConstraint(
                        fields=("article",),
                        name="unique_monitored_article",
                    ),
                ],
            },
        ),
        migrations.RunPython(copy_existing_monitoring, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="article",
            name="price_tracking",
        ),
        migrations.RemoveField(
            model_name="article",
            name="lower_price",
        ),
        migrations.RemoveField(
            model_name="article",
            name="median_price",
        ),
    ]
