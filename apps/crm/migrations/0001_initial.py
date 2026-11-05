"""
Initial migration for CRM module
"""
from django.db import migrations, models
import django.db.models.deletion
import uuid
import apps.crm.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('branches', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        # Customer Type
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(help_text='Type of customer', max_length=100, unique=True, verbose_name='Name')),
                ('code', models.CharField(help_text='Short code for customer type', max_length=10, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('color', models.CharField(blank=True, help_text='Color for UI representation', max_length=20, null=True, verbose_name='Color')),
            ],
            options={
                'verbose_name': 'Customer Type',
                'verbose_name_plural': 'Customer Types',
                'ordering': ['name'],
            },
        ),
        
        # Customer Source
        migrations.CreateModel(
            name='CustomerSource',
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
                'verbose_name': 'Customer Source',
                'verbose_name_plural': 'Customer Sources',
                'ordering': ['name'],
            },
        ),
        
        # Device Category
        migrations.CreateModel(
            name='DeviceCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('icon', models.CharField(blank=True, help_text='Icon class for UI', max_length=50, null=True, verbose_name='Icon')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Device Category',
                'verbose_name_plural': 'Device Categories',
                'ordering': ['name'],
            },
        ),
        
        # Device Brand
        migrations.CreateModel(
            name='DeviceBrand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='device_brands/logos/', verbose_name='Logo')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Device Brand',
                'verbose_name_plural': 'Device Brands',
                'ordering': ['name'],
            },
        ),
        
        # Device Model
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='crm.devicebrand', verbose_name='Brand')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('image', models.ImageField(blank=True, null=True, upload_to='device_models/images/', verbose_name='Image')),
                ('specifications', models.JSONField(blank=True, help_text='Device specifications in JSON format', null=True, verbose_name='Specifications')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Device Model',
                'verbose_name_plural': 'Device Models',
                'ordering': ['brand__name', 'name'],
                'unique_together': {('brand', 'name')},
            },
        ),
        
        # Customer Group
        migrations.CreateModel(
            name='CustomerGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0.0, help_text='Default discount percentage for this group', max_digits=5, verbose_name='Discount %')),
                ('credit_limit', models.DecimalField(decimal_places=2, default=0.0, help_text='Maximum credit allowed for customers in this group', max_digits=19, verbose_name='Credit Limit')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Customer Group',
                'verbose_name_plural': 'Customer Groups',
                'ordering': ['name'],
                'unique_together': {('organization', 'code')},
            },
        ),
        
        # Customer
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('customer_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customers', to='crm.customertype', verbose_name='Customer Type')),
                ('customer_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customers', to='crm.customergroup', verbose_name='Customer Group')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customers', to='crm.customersource', verbose_name='Source')),
                ('code', models.CharField(db_index=True, help_text='Unique customer code', max_length=20, unique=True, verbose_name='Code')),
                ('first_name', models.CharField(max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last Name')),
                ('company_name', models.CharField(blank=True, help_text='Company name for business customers', max_length=200, null=True, verbose_name='Company Name')),
                ('email', models.EmailField(blank=True, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone')),
                ('mobile', models.CharField(blank=True, max_length=20, null=True, verbose_name='Mobile')),
                ('whatsapp', models.CharField(blank=True, max_length=20, null=True, verbose_name='WhatsApp')),
                ('address_line_1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address Line 2')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=100, null=True, verbose_name='State/Province')),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code')),
                ('country', models.CharField(default='Algeria', max_length=100, verbose_name='Country')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('unknown', 'Unknown')], default='unknown', max_length=10, verbose_name='Gender')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('tax_id', models.CharField(blank=True, help_text='Tax identification number', max_length=50, null=True, verbose_name='Tax ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('blocked', 'Blocked'), ('prospect', 'Prospect'), ('vip', 'VIP')], default='active', max_length=20, verbose_name='Status')),
                ('is_verified', models.BooleanField(default=False, help_text='Customer identity verified', verbose_name='Verified')),
                ('verification_date', models.DateTimeField(blank=True, null=True, verbose_name='Verification Date')),
                ('credit_balance', models.DecimalField(decimal_places=2, default=0.0, help_text='Current credit balance (positive = owes money, negative = prepaid)', max_digits=19, verbose_name='Credit Balance')),
                ('total_purchases', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Purchases')),
                ('total_repairs', models.PositiveIntegerField(default=0, verbose_name='Total Repairs')),
                ('loyalty_points', models.PositiveIntegerField(default=0, verbose_name='Loyalty Points')),
                ('facebook', models.URLField(blank=True, null=True, verbose_name='Facebook')),
                ('twitter', models.URLField(blank=True, null=True, verbose_name='Twitter')),
                ('instagram', models.URLField(blank=True, null=True, verbose_name='Instagram')),
                ('referred_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referrals', to='crm.customer', verbose_name='Referred By')),
                ('referral_code', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Referral Code')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='customers/profile_images/', verbose_name='Profile Image')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['code'], name='crm_customer_code_idx'),
                    models.Index(fields=['first_name', 'last_name'], name='crm_customer_name_idx'),
                    models.Index(fields=['phone'], name='crm_customer_phone_idx'),
                    models.Index(fields=['email'], name='crm_customer_email_idx'),
                    models.Index(fields=['status'], name='crm_customer_status_idx'),
                    models.Index(fields=['organization', 'code'], name='crm_customer_org_code_idx'),
                ],
            },
        ),
        
        # Device
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='crm.customer', verbose_name='Customer')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', to='crm.devicecategory', verbose_name='Category')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_devices', to='crm.devicebrand', verbose_name='Brand')),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_devices', to='crm.devicemodel', verbose_name='Model')),
                ('name', models.CharField(help_text='Custom name for the device', max_length=200, verbose_name='Name')),
                ('serial_number', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Serial Number')),
                ('imei_1', models.CharField(blank=True, db_index=True, max_length=20, null=True, verbose_name='IMEI 1')),
                ('imei_2', models.CharField(blank=True, db_index=True, max_length=20, null=True, verbose_name='IMEI 2')),
                ('mac_address', models.CharField(blank=True, max_length=20, null=True, verbose_name='MAC Address')),
                ('color', models.CharField(blank=True, max_length=50, null=True, verbose_name='Color')),
                ('storage', models.CharField(blank=True, help_text='Storage capacity (e.g., 128GB, 1TB)', max_length=50, null=True, verbose_name='Storage')),
                ('ram', models.CharField(blank=True, max_length=50, null=True, verbose_name='RAM')),
                ('os_version', models.CharField(blank=True, max_length=50, null=True, verbose_name='OS Version')),
                ('purchase_date', models.DateField(blank=True, null=True, verbose_name='Purchase Date')),
                ('purchase_price', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True, verbose_name='Purchase Price')),
                ('warranty_expiry', models.DateField(blank=True, null=True, verbose_name='Warranty Expiry')),
                ('status', models.CharField(choices=[('new', 'New'), ('used', 'Used'), ('refurbished', 'Refurbished'), ('broken', 'Broken'), ('lost', 'Lost'), ('stolen', 'Stolen')], default='used', max_length=20, verbose_name='Status')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('front_image', models.ImageField(blank=True, null=True, upload_to='customer_devices/images/', verbose_name='Front Image')),
                ('back_image', models.ImageField(blank=True, null=True, upload_to='customer_devices/images/', verbose_name='Back Image')),
                ('tag', models.CharField(blank=True, help_text='Custom tag or ID for the device', max_length=50, null=True, verbose_name='Tag/ID')),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['customer', 'serial_number'], name='crm_device_customer_serial_idx'),
                    models.Index(fields=['customer', 'imei_1'], name='crm_device_customer_imei1_idx'),
                    models.Index(fields=['customer', 'imei_2'], name='crm_device_customer_imei2_idx'),
                    models.Index(fields=['serial_number'], name='crm_device_serial_idx'),
                    models.Index(fields=['imei_1'], name='crm_device_imei1_idx'),
                    models.Index(fields=['imei_2'], name='crm_device_imei2_idx'),
                ],
            },
        ),
        
        # Customer Communication
        migrations.CreateModel(
            name='CustomerCommunication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communications', to='crm.customer', verbose_name='Customer')),
                ('communication_type', models.CharField(choices=[('phone', 'Phone Call'), ('email', 'Email'), ('sms', 'SMS'), ('whatsapp', 'WhatsApp'), ('in_person', 'In Person'), ('social_media', 'Social Media'), ('other', 'Other')], max_length=20, verbose_name='Type')),
                ('direction', models.CharField(choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')], default='inbound', max_length=10, verbose_name='Direction')),
                ('subject', models.CharField(max_length=200, verbose_name='Subject')),
                ('message', models.TextField(verbose_name='Message')),
                ('response', models.TextField(blank=True, null=True, verbose_name='Response')),
                ('related_to', models.CharField(blank=True, help_text='What this communication is related to (e.g., Repair #123, Invoice #456)', max_length=100, null=True, verbose_name='Related To')),
                ('status', models.CharField(choices=[('open', 'Open'), ('pending', 'Pending'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='open', max_length=20, verbose_name='Status')),
                ('follow_up_required', models.BooleanField(default=False, verbose_name='Follow-up Required')),
                ('follow_up_date', models.DateTimeField(blank=True, null=True, verbose_name='Follow-up Date')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_communications', to='accounts.user', verbose_name='Assigned To')),
            ],
            options={
                'verbose_name': 'Customer Communication',
                'verbose_name_plural': 'Customer Communications',
                'ordering': ['-created_at'],
            },
        ),
        
        # Customer Document
        migrations.CreateModel(
            name='CustomerDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='crm.customer', verbose_name='Customer')),
                ('document_type', models.CharField(choices=[('id_card', 'ID Card'), ('passport', 'Passport'), ('driving_license', 'Driving License'), ('business_license', 'Business License'), ('tax_certificate', 'Tax Certificate'), ('contract', 'Contract'), ('receipt', 'Receipt'), ('warranty', 'Warranty'), ('other', 'Other')], max_length=30, verbose_name='Type')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('file', models.FileField(upload_to='customer_documents/', verbose_name='File')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='Expiry Date')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Verified')),
            ],
            options={
                'verbose_name': 'Customer Document',
                'verbose_name_plural': 'Customer Documents',
                'ordering': ['-created_at'],
            },
        ),
    ]
