# Generated by Django 5.0.6 on 2024-08-09 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0008_alter_article_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='carbs',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='article',
            name='chol',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='article',
            name='fat',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='article',
            name='sodium',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='article',
            name='protein',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5),
        ),
    ]
