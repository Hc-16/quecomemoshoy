# Generated by Django 4.2.6 on 2023-12-13 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'ingrediente',
                'verbose_name_plural': 'ingredientes',
            },
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('imagen', models.ImageField(upload_to='recetas/%d/%m/%Y', verbose_name='Imagen de la receta')),
                ('descripcion', models.TextField(default='', verbose_name='Descripción de la receta')),
                ('ingredientes_txt', models.TextField(default='', verbose_name='Ingredientes')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'receta',
                'verbose_name_plural': 'recetas',
            },
        ),
        migrations.CreateModel(
            name='RecetaIngredientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.CharField(max_length=64)),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cantidad', to='GestionRecetas.ingrediente')),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cantidad', to='GestionRecetas.receta')),
            ],
        ),
        migrations.AddField(
            model_name='receta',
            name='ingredientes',
            field=models.ManyToManyField(through='GestionRecetas.RecetaIngredientes', to='GestionRecetas.ingrediente'),
        ),
        migrations.AddField(
            model_name='receta',
            name='likes',
            field=models.ManyToManyField(related_name='receta_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ListaCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.CharField(max_length=64)),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compra', to='GestionRecetas.ingrediente')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compra', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='lista_compra',
            field=models.ManyToManyField(related_name='ingrediente_user', through='GestionRecetas.ListaCompra', to=settings.AUTH_USER_MODEL),
        ),
    ]
