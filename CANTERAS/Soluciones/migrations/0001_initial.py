# Generated by Django 4.0.3 on 2023-04-23 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='franjas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tamiz', models.FloatField(blank=True, null=True)),
                ('MSA38', models.FloatField(blank=True, null=True)),
                ('MIA38', models.FloatField(blank=True, null=True)),
                ('MSA25', models.FloatField(blank=True, null=True)),
                ('MIA25', models.FloatField(blank=True, null=True)),
                ('TamboMa', models.FloatField(blank=True, null=True)),
                ('TamboCh', models.FloatField(blank=True, null=True)),
                ('MoralesSB', models.FloatField(blank=True, null=True)),
                ('MoralesSC', models.FloatField(blank=True, null=True)),
                ('TotoroSab', models.FloatField(blank=True, null=True)),
                ('TotoroSA', models.FloatField(blank=True, null=True)),
                ('RosasTr', models.FloatField(blank=True, null=True)),
                ('RosasUf', models.FloatField(blank=True, null=True)),
                ('BolivarSR', models.FloatField(blank=True, null=True)),
                ('BolivarCol', models.FloatField(blank=True, null=True)),
                ('Piendamo', models.FloatField(blank=True, null=True)),
                ('PopayanBe', models.FloatField(blank=True, null=True)),
                ('PopayanCer', models.FloatField(blank=True, null=True)),
                ('LaSierra', models.FloatField(blank=True, null=True)),
                ('SotaraHB', models.FloatField(blank=True, null=True)),
                ('SotaraSR', models.FloatField(blank=True, null=True)),
                ('CaldonoEs', models.FloatField(blank=True, null=True)),
                ('CaldonoJa', models.FloatField(blank=True, null=True)),
                ('VillaRicaBP', models.FloatField(blank=True, null=True)),
                ('VillaRicaSB', models.FloatField(blank=True, null=True)),
                ('Guachene', models.FloatField(blank=True, null=True)),
                ('LaVegaCR', models.FloatField(blank=True, null=True)),
                ('LaVegaUv', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'franja',
                'verbose_name_plural': 'franjas',
            },
        ),
    ]
