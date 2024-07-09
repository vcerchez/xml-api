# Generated by Django 5.0.7 on 2024-07-14 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Doc",
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
                ("DOCUMENT_REF_DATE", models.DateField()),
                ("PUBLICATION_REF_FILE", models.CharField(max_length=50)),
                ("PUBLICATION_REF_LG_OJ", models.CharField(max_length=3)),
                ("SOURCE", models.CharField(max_length=6)),
                ("CELEX", models.CharField(max_length=11)),
                ("CONTENU_TITRE", models.TextField()),
                ("CONTENU_PREAMBULE", models.TextField()),
                ("CONTENU_ARTICLES", models.TextField()),
                ("CONTENU_SIGNATURE", models.TextField()),
                ("ANNEXES", models.TextField()),
            ],
        ),
    ]