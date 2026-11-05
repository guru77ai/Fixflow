"""
Initial migration for POS module
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
        ('crm', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        # Payment Method
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_cash', models.BooleanField(default=False, verbose_name='Cash')),
                ('is_card', models.BooleanField(default=False, verbose_name='Card')),
                ('is_mobile', models.BooleanField(default=False, verbose_name='Mobile')),
                ('is_online', models.BooleanField(default=False, verbose_name='Online')),
                ('icon', models.CharField(blank=True, max_length=50, null=True, verbose_name='Icon')),
            ],
            options={
                'verbose_name': 'Payment Method',
                'verbose_name_plural': 'Payment Methods',
                'ordering': ['name'],
            },
        ),
        
        # Cash Register
        migrations.CreateModel(
            name='CashRegister',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('initial_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Initial Amount')),
                ('current_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Current Amount')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_open', models.BooleanField(default=False, verbose_name='Open')),
                ('opened_at', models.DateTimeField(blank=True, null=True, verbose_name='Opened At')),
                ('closed_at', models.DateTimeField(blank=True, null=True, verbose_name='Closed At')),
                ('opened_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='opened_registers', to='accounts.user', verbose_name='Opened By')),
                ('closed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='closed_registers', to='accounts.user', verbose_name='Closed By')),
            ],
            options={
                'verbose_name': 'Cash Register',
                'verbose_name_plural': 'Cash Registers',
                'ordering': ['name'],
                'unique_together': {('organization', 'code')},
            },
        ),
        
        # Sale
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('sale_number', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Sale Number')),
                ('sale_type', models.CharField(choices=[('retail', 'Retail'), ('wholesale', 'Wholesale'), ('online', 'Online'), ('phone', 'Phone Order'), ('repair', 'Repair Sale')], default='retail', max_length=20, verbose_name='Sale Type')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('quotation', 'Quotation'), ('confirmed', 'Confirmed'), ('paid', 'Paid'), ('partial', 'Partial'), ('cancelled', 'Cancelled'), ('returned', 'Returned')], default='draft', max_length=20, verbose_name='Status')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to='crm.customer', verbose_name='Customer')),
                ('cash_register', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to='pos.cashregister', verbose_name='Cash Register')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Subtotal')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Discount')),
                ('tax_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Tax Amount')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Amount')),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Amount Paid')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Balance')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to='pos.paymentmethod', verbose_name='Payment Method')),
                ('payment_reference', models.CharField(blank=True, max_length=100, null=True, verbose_name='Payment Reference')),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('partial', 'Partial'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=20, verbose_name='Payment Status')),
                ('is_credit', models.BooleanField(default=False, verbose_name='Credit Sale')),
                ('credit_days', models.PositiveIntegerField(default=0, verbose_name='Credit Days')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due Date')),
                ('is_invoice', models.BooleanField(default=False, verbose_name='Create Invoice')),
                ('invoice_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Invoice Number')),
                ('sold_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_made', to='accounts.user', verbose_name='Sold By')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['sale_number'], name='pos_sale_number_idx'),
                    models.Index(fields=['customer'], name='pos_sale_customer_idx'),
                    models.Index(fields=['status'], name='pos_sale_status_idx'),
                    models.Index(fields=['sale_type'], name='pos_sale_type_idx'),
                    models.Index(fields=['created_at'], name='pos_sale_created_at_idx'),
                ],
            },
        ),
        
        # Sale Item
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pos.sale', verbose_name='Sale')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_items', to='inventory.product', verbose_name='Product')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_items', to='inventory.service', verbose_name='Service')),
                ('product_name', models.CharField(max_length=200, verbose_name='Product Name')),
                ('product_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Product Code')),
                ('quantity', models.DecimalField(decimal_places=3, default=1.0, max_digits=10, verbose_name='Quantity')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Unit Price')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Price')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Discount')),
                ('tax_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Tax Rate %')),
                ('tax_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Tax Amount')),
                ('serial_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Serial Number')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Sale Item',
                'verbose_name_plural': 'Sale Items',
                'ordering': ['-created_at'],
            },
        ),
        
        # Sale Payment
        migrations.CreateModel(
            name='SalePayment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='pos.sale', verbose_name='Sale')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_payments', to='pos.paymentmethod', verbose_name='Payment Method')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Amount')),
                ('reference', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Transaction ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='completed', max_length=20, verbose_name='Status')),
                ('payment_date', models.DateTimeField(auto_now_add=True, verbose_name='Payment Date')),
                ('processed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processed_payments', to='accounts.user', verbose_name='Processed By')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Sale Payment',
                'verbose_name_plural': 'Sale Payments',
                'ordering': ['-created_at'],
            },
        ),
        
        # Receipt
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('sale', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='receipt', to='pos.sale', verbose_name='Sale')),
                ('receipt_number', models.CharField(max_length=50, unique=True, verbose_name='Receipt Number')),
                ('receipt_type', models.CharField(choices=[('thermal', 'Thermal'), ('a4', 'A4'), ('email', 'Email')], default='thermal', max_length=20, verbose_name='Receipt Type')),
                ('is_printed', models.BooleanField(default=False, verbose_name='Printed')),
                ('printed_at', models.DateTimeField(blank=True, null=True, verbose_name='Printed At')),
                ('printed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='printed_receipts', to='accounts.user', verbose_name='Printed By')),
                ('is_emailed', models.BooleanField(default=False, verbose_name='Emailed')),
                ('emailed_at', models.DateTimeField(blank=True, null=True, verbose_name='Emailed At')),
                ('template', models.CharField(blank=True, max_length=100, null=True, verbose_name='Template')),
            ],
            options={
                'verbose_name': 'Receipt',
                'verbose_name_plural': 'Receipts',
                'ordering': ['-created_at'],
            },
        ),
        
        # Refund
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refunds', to='pos.sale', verbose_name='Sale')),
                ('refund_number', models.CharField(max_length=50, unique=True, verbose_name='Refund Number')),
                ('reason', models.CharField(choices=[('defective', 'Defective Product'), ('wrong_item', 'Wrong Item'), ('customer_request', 'Customer Request'), ('other', 'Other')], default='other', max_length=20, verbose_name='Reason')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Amount')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='refunds', to='pos.paymentmethod', verbose_name='Payment Method')),
                ('reference', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('completed', 'Completed')], default='pending', max_length=20, verbose_name='Status')),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_refunds', to='accounts.user', verbose_name='Requested By')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_refunds', to='accounts.user', verbose_name='Approved By')),
                ('processed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processed_refunds', to='accounts.user', verbose_name='Processed By')),
                ('requested_at', models.DateTimeField(auto_now_add=True, verbose_name='Requested At')),
                ('approved_at', models.DateTimeField(blank=True, null=True, verbose_name='Approved At')),
                ('processed_at', models.DateTimeField(blank=True, null=True, verbose_name='Processed At')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Refund',
                'verbose_name_plural': 'Refunds',
                'ordering': ['-created_at'],
            },
        ),
        
        # Refund Item
        migrations.CreateModel(
            name='RefundItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('refund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pos.refund', verbose_name='Refund')),
                ('sale_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='refund_items', to='pos.saleitem', verbose_name='Sale Item')),
                ('product_name', models.CharField(max_length=200, verbose_name='Product Name')),
                ('quantity', models.DecimalField(decimal_places=3, default=1.0, max_digits=10, verbose_name='Quantity')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Unit Price')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Price')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='Reason')),
            ],
            options={
                'verbose_name': 'Refund Item',
                'verbose_name_plural': 'Refund Items',
                'ordering': ['-created_at'],
            },
        ),
        
        # POS Session
        migrations.CreateModel(
            name='POSSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pos_sessions', to='accounts.user', verbose_name='User')),
                ('cash_register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='pos.cashregister', verbose_name='Cash Register')),
                ('session_key', models.CharField(max_length=100, unique=True, verbose_name='Session Key')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='Started At')),
                ('ended_at', models.DateTimeField(blank=True, null=True, verbose_name='Ended At')),
                ('initial_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Initial Amount')),
                ('final_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Final Amount')),
                ('total_sales', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Sales')),
                ('total_refunds', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Refunds')),
                ('total_collected', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Collected')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'POS Session',
                'verbose_name_plural': 'POS Sessions',
                'ordering': ['-started_at'],
            },
        ),
        
        # POS Settings
        migrations.CreateModel(
            name='POSSettings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('receipt_header', models.TextField(blank=True, null=True, verbose_name='Receipt Header')),
                ('receipt_footer', models.TextField(blank=True, null=True, verbose_name='Receipt Footer')),
                ('default_payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_pos_settings', to='pos.paymentmethod', verbose_name='Default Payment Method')),
                ('default_cash_register', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_pos_settings', to='pos.cashregister', verbose_name='Default Cash Register')),
                ('show_customer_display', models.BooleanField(default=True, verbose_name='Show Customer Display')),
                ('auto_print_receipt', models.BooleanField(default=True, verbose_name='Auto Print Receipt')),
                ('auto_email_receipt', models.BooleanField(default=False, verbose_name='Auto Email Receipt')),
                ('tax_included', models.BooleanField(default=False, verbose_name='Tax Included in Prices')),
                ('default_tax_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Default Tax Rate %')),
                ('allow_credit_sales', models.BooleanField(default=True, verbose_name='Allow Credit Sales')),
                ('credit_limit', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Credit Limit')),
            ],
            options={
                'verbose_name': 'POS Settings',
                'verbose_name_plural': 'POS Settings',
                'ordering': ['-created_at'],
                'unique_together': {('organization', 'branch')},
            },
        ),
    ]
