# Generated by Django 4.2.6 on 2023-12-06 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apphost', '0003_alter_pedido_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='fragmentopedido',
            name='tamano',
            field=models.CharField(choices=[('MD', 'Mediana'), ('FM', 'Familiar'), ('AC', 'Acompañamiento')], default='MD', max_length=2),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('PG', 'No pagado'), ('PD', 'Pendiente'), ('EN', 'Enviado'), ('RC', 'Recibido'), ('CN', 'Cancelado')], default='No pagado', max_length=2),
        ),
    ]