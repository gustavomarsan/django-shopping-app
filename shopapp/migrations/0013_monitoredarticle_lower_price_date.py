from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0012_monitored_article"),
    ]

    operations = [
        migrations.AddField(
            model_name="monitoredarticle",
            name="lower_price_date",
            field=models.DateField(
                blank=True,
                editable=False,
                null=True,
                verbose_name="Fecha del precio mínimo",
            ),
        ),
    ]
