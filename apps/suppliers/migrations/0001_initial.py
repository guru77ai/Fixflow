"""
Initial migration for Suppliers module
"""
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('branches', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        # Supplier Category
        migrations.CreateModel(
            name='SupplierCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Supplier Category',
                'verbose_name_plural': 'Supplier Categories',
                'ordering': ['name'],
            },
        ),
        
        # Supplier
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suppliers', to='suppliers.suppliercategory', verbose_name='Category')),
                ('code', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('company_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Company Name')),
                ('email', models.EmailField(blank=True, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone')),
                ('mobile', models.CharField(blank=True, max_length=20, null=True, verbose_name='Mobile')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('address_line_1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address Line 2')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=100, null=True, verbose_name='State/Province')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code')),
                ('country', models.CharField(default='Algeria', max_length=100, verbose_name='Country')),
                ('tax_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tax ID')),
                ('payment_terms', models.CharField(blank=True, max_length=100, null=True, verbose_name='Payment Terms')),
                ('credit_limit', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Credit Limit')),
                ('credit_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Credit Balance')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('blocked', 'Blocked'), ('prospect', 'Prospect')], default='active', max_length=20, verbose_name='Status')),
                ('quality_rating', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5, verbose_name='Quality Rating')),
                ('delivery_rating', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5, verbose_name='Delivery Rating')),
                ('account_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_suppliers', to='accounts.user', verbose_name='Account Manager')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Verified')),
                ('is_preferred', models.BooleanField(default=False, verbose_name='Preferred Supplier')),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
                'ordering': ['name'],
                'indexes': [
                    models.Index(fields=['code'], name='supplier_code_idx'),
                    models.Index(fields=['name'], name='supplier_name_idx'),
                    models.Index(fields=['email'], name='supplier_email_idx'),
                    models.Index(fields=['phone'], name='supplier_phone_idx'),
                    models.Index(fields=['status'], name='supplier_status_idx'),
                ],
            },
        ),
        
        # Supplier Contact
        migrations.CreateModel(
            name='SupplierContact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='suppliers.supplier', verbose_name='Supplier')),
                ('first_name', models.CharField(max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last Name')),
                ('position', models.CharField(blank=True, max_length=100, null=True, verbose_name='Position')),
                ('email', models.EmailField(blank=True, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone')),
                ('mobile', models.CharField(blank=True, max_length=20, null=True, verbose_name='Mobile')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Primary Contact')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Supplier Contact',
                'verbose_name_plural': 'Supplier Contacts',
                'ordering': ['first_name', 'last_name'],
            },
        ),
        
        # Supplier Document
        migrations.CreateModel(
            name='SupplierDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='suppliers.supplier', verbose_name='Supplier')),
                ('document_type', models.CharField(choices=[('contract', 'Contract'), ('certificate', 'Certificate'), ('catalog', 'Product Catalog'), ('price_list', 'Price List'), ('tax_certificate', 'Tax Certificate'), ('business_license', 'Business License'), ('other', 'Other')], max_length=30, verbose_name='Type')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('file', models.FileField(upload_to='supplier_documents/', verbose_name='File')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='Expiry Date')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Verified')),
            ],
            options={
                'verbose_name': 'Supplier Document',
                'verbose_name_plural': 'Supplier Documents',
                'ordering': ['-created_at'],
            },
        ),
    ]
