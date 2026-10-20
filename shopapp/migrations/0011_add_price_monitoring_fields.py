from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0010_alter_division_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="price_tracking",
            field=models.BooleanField(default=False, verbose_name="Seguimiento de precio"),
        ),
        migrations.AddField(
            model_name="article",
            name="lower_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                editable=False,
                max_digits=7,
                null=True,
                verbose_name="Precio mínimo histórico",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="median_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                editable=False,
                max_digits=7,
                null=True,
                verbose_name="Precio mediano histórico",
            ),
        ),
    ]
