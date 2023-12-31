# Generated by Django 3.2.19 on 2023-06-05 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_product_id', models.CharField(blank=True, max_length=225, null=True)),
                ('name', models.CharField(max_length=122)),
                ('credit', models.PositiveIntegerField()),
                ('plan_type', models.CharField(choices=[('monthly', 'Per Month'), ('yearly', 'Per Year')], max_length=20)),
                ('plan_cost', models.PositiveIntegerField()),
                ('plan_features', models.TextField(blank=True, help_text='List should be comma separed. Example: ["Feat 1", "Feat 2", "Feat 3"]', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(blank=True, max_length=220, null=True)),
                ('sub_id', models.CharField(blank=True, max_length=220, null=True)),
                ('active', models.BooleanField(default=False)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='users.profile')),
            ],
        ),
    ]
