# Generated by Django 3.2.4 on 2021-06-27 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_cart_subtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=120)),
                ('status', models.CharField(choices=[('created', 'created'), ('paid', 'paid'), ('shipped', 'shipped'), ('refunded', 'refunded')], default='created', max_length=120)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=10, max_digits=100)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.cart')),
            ],
        ),
    ]
