# Generated by Django 4.1.1 on 2023-05-05 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_%(class)ss', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CostMainHead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(default='')),
                ('balance', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TenderProject',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tender.basemodel')),
                ('project_name', models.CharField(max_length=200)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('job_no', models.CharField(blank=True, max_length=200, null=True)),
                ('project_location', models.CharField(max_length=200)),
                ('procuring_entity_name', models.CharField(max_length=200)),
                ('contact_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('number_of_infrastructure', models.PositiveIntegerField()),
                ('infrastructure_description', models.TextField()),
                ('project_complete', models.BooleanField(default=False)),
            ],
            bases=('tender.basemodel',),
        ),
        migrations.CreateModel(
            name='CostSubHead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(default='')),
                ('balance', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('main_head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_head', to='tender.costmainhead')),
            ],
        ),
        migrations.CreateModel(
            name='TenderPg',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tender.basemodel')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('is_withdraw', models.BooleanField(default=False)),
                ('maturity_date', models.DateField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('tender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tender.tenderproject')),
            ],
            bases=('tender.basemodel',),
        ),
        migrations.CreateModel(
            name='SecurityMoney',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tender.basemodel')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('is_withdraw', models.BooleanField(default=False)),
                ('maturity_date', models.DateField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('tender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tender.tenderproject')),
            ],
            bases=('tender.basemodel',),
        ),
        migrations.CreateModel(
            name='RetensionMoney',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tender.basemodel')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('is_withdraw', models.BooleanField(default=False)),
                ('maturity_date', models.DateField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tender.tenderproject')),
            ],
            bases=('tender.basemodel',),
        ),
        migrations.CreateModel(
            name='DailyExpendiature',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tender.basemodel')),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=20)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_method', models.CharField(choices=[('cash', 'Cash'), ('bank', 'Bank'), ('due', 'Due')], max_length=30)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('deposit_bank_name', models.CharField(blank=True, max_length=150, null=True)),
                ('deposit_branch_name', models.CharField(blank=True, max_length=150, null=True)),
                ('deposit_account_no', models.CharField(blank=True, max_length=150, null=True)),
                ('issue_cheque_no', models.CharField(blank=True, max_length=150, null=True)),
                ('issue_bank_name', models.CharField(blank=True, max_length=150, null=True)),
                ('main_head', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='main_head_expendiature', to='tender.costmainhead')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='daily_expendiature', to='tender.tenderproject')),
                ('sub_head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_head_expendiature', to='tender.costsubhead')),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=('tender.basemodel',),
        ),
    ]
