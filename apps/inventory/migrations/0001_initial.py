"""
Initial migration for Inventory module
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
        ('suppliers', '0001_initial'),
    ]

    operations = [
        # Warehouse
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone')),
                ('email', models.EmailField(blank=True, null=True, verbose_name='Email')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_warehouses', to='accounts.user', verbose_name='Manager')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_central', models.BooleanField(default=False, help_text='Is this the central warehouse?', verbose_name='Central Warehouse')),
            ],
            options={
                'verbose_name': 'Warehouse',
                'verbose_name_plural': 'Warehouses',
                'ordering': ['name'],
                'unique_together': {('organization', 'code')},
            },
        ),
        
        # Product Category
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='inventory.productcategory', verbose_name='Parent Category')),
                ('icon', models.CharField(blank=True, max_length=50, null=True, verbose_name='Icon')),
                ('color', models.CharField(blank=True, max_length=20, null=True, verbose_name='Color')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
                'ordering': ['name'],
                'unique_together': {('organization', 'code')},
            },
        ),
        
        # Product Brand
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='product_brands/logos/', verbose_name='Logo')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Product Brand',
                'verbose_name_plural': 'Product Brands',
                'ordering': ['name'],
            },
        ),
        
        # Unit of Measure
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Unit of Measure',
                'verbose_name_plural': 'Units of Measure',
                'ordering': ['name'],
            },
        ),
        
        # Product
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('code', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Code')),
                ('sku', models.CharField(blank=True, db_index=True, max_length=50, null=True, unique=True, verbose_name='SKU')),
                ('barcode', models.CharField(blank=True, db_index=True, max_length=50, null=True, unique=True, verbose_name='Barcode')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='inventory.productcategory', verbose_name='Category')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='inventory.productbrand', verbose_name='Brand')),
                ('product_type', models.CharField(choices=[('part', 'Part'), ('accessory', 'Accessory'), ('consumable', 'Consumable'), ('tool', 'Tool'), ('equipment', 'Equipment'), ('other', 'Other')], default='part', max_length=20, verbose_name='Product Type')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='inventory.unitofmeasure', verbose_name='Unit of Measure')),
                ('stock_type', models.CharField(choices=[('serialized', 'Serialized'), ('batch', 'Batch Tracked'), ('non_serialized', 'Non-Serialized')], default='non_serialized', max_length=20, verbose_name='Stock Type')),
                ('initial_stock', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Initial Stock')),
                ('current_stock', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Current Stock')),
                ('minimum_stock', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Minimum Stock')),
                ('maximum_stock', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Maximum Stock')),
                ('purchase_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Purchase Price')),
                ('selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Selling Price')),
                ('wholesale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True, verbose_name='Wholesale Price')),
                ('cost_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Cost Price')),
                ('tax_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Tax Rate %')),
                ('is_taxable', models.BooleanField(default=True, verbose_name='Taxable')),
                ('supplier_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Supplier Code')),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='inventory.warehouse', verbose_name='Warehouse')),
                ('location', models.CharField(blank=True, max_length=100, null=True, verbose_name='Location')),
                ('weight', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Weight (kg)')),
                ('dimensions', models.CharField(blank=True, max_length=100, null=True, verbose_name='Dimensions')),
                ('color', models.CharField(blank=True, max_length=50, null=True, verbose_name='Color')),
                ('model', models.CharField(blank=True, max_length=100, null=True, verbose_name='Model')),
                ('part_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Part Number')),
                ('is_serialized', models.BooleanField(default=False, verbose_name='Serialized')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_for_sale', models.BooleanField(default=True, verbose_name='For Sale')),
                ('is_for_purchase', models.BooleanField(default=True, verbose_name='For Purchase')),
                ('is_for_repair', models.BooleanField(default=False, verbose_name='For Repair')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/images/', verbose_name='Image')),
                ('tags', models.JSONField(blank=True, null=True, verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['name'],
                'indexes': [
                    models.Index(fields=['code'], name='inventory_product_code_idx'),
                    models.Index(fields=['sku'], name='inventory_product_sku_idx'),
                    models.Index(fields=['barcode'], name='inventory_product_barcode_idx'),
                    models.Index(fields=['name'], name='inventory_product_name_idx'),
                    models.Index(fields=['category'], name='inventory_product_category_idx'),
                    models.Index(fields=['brand'], name='inventory_product_brand_idx'),
                    models.Index(fields=['organization', 'code'], name='inventory_product_org_code_idx'),
                ],
            },
        ),
        
        # Product Serial Number
        migrations.CreateModel(
            name='ProductSerialNumber',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serial_numbers', to='inventory.product', verbose_name='Product')),
                ('serial_number', models.CharField(db_index=True, max_length=100, verbose_name='Serial Number')),
                ('batch_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Batch Number')),
                ('status', models.CharField(choices=[('in_stock', 'In Stock'), ('sold', 'Sold'), ('used', 'Used in Repair'), ('returned', 'Returned'), ('defective', 'Defective'), ('lost', 'Lost'), ('stolen', 'Stolen')], default='in_stock', max_length=20, verbose_name='Status')),
                ('purchase_date', models.DateField(blank=True, null=True, verbose_name='Purchase Date')),
                ('purchase_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Purchase Price')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='Expiry Date')),
                ('location', models.CharField(blank=True, max_length=100, null=True, verbose_name='Location')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Product Serial Number',
                'verbose_name_plural': 'Product Serial Numbers',
                'ordering': ['serial_number'],
                'unique_together': {('product', 'serial_number')},
                'indexes': [
                    models.Index(fields=['serial_number'], name='inventory_serial_number_idx'),
                    models.Index(fields=['product', 'status'], name='inventory_serial_product_status_idx'),
                ],
            },
        ),
        
        # Stock Movement
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_movements', to='inventory.product', verbose_name='Product')),
                ('movement_type', models.CharField(choices=[('in', 'Stock In'), ('out', 'Stock Out'), ('transfer_in', 'Transfer In'), ('transfer_out', 'Transfer Out'), ('adjustment_plus', 'Adjustment +'), ('adjustment_minus', 'Adjustment -'), ('return', 'Return'), ('damage', 'Damage/Loss')], max_length=20, verbose_name='Movement Type')),
                ('reference_type', models.CharField(blank=True, choices=[('purchase', 'Purchase Order'), ('sale', 'Sale'), ('repair', 'Repair Order'), ('transfer', 'Stock Transfer'), ('adjustment', 'Stock Adjustment'), ('return', 'Return'), ('manual', 'Manual Entry'), ('other', 'Other')], max_length=20, null=True, verbose_name='Reference Type')),
                ('reference_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference Number')),
                ('quantity', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Quantity')),
                ('unit_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Unit Cost')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Cost')),
                ('source_warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_movements_out', to='inventory.warehouse', verbose_name='Source Warehouse')),
                ('destination_warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_movements_in', to='inventory.warehouse', verbose_name='Destination Warehouse')),
                ('related_to', models.CharField(blank=True, max_length=100, null=True, verbose_name='Related To')),
                ('serial_numbers', models.JSONField(blank=True, null=True, verbose_name='Serial Numbers')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('performed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_movements', to='accounts.user', verbose_name='Performed By')),
            ],
            options={
                'verbose_name': 'Stock Movement',
                'verbose_name_plural': 'Stock Movements',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['product'], name='inventory_stock_movement_product_idx'),
                    models.Index(fields=['movement_type'], name='inventory_stock_movement_type_idx'),
                    models.Index(fields=['reference_type'], name='inventory_stock_movement_ref_type_idx'),
                    models.Index(fields=['reference_number'], name='inventory_stock_movement_ref_num_idx'),
                    models.Index(fields=['created_at'], name='inventory_stock_movement_created_at_idx'),
                ],
            },
        ),
        
        # Stock Transfer
        migrations.CreateModel(
            name='StockTransfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('transfer_number', models.CharField(max_length=50, unique=True, verbose_name='Transfer Number')),
                ('source_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock_transfers_out', to='inventory.warehouse', verbose_name='Source Warehouse')),
                ('destination_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock_transfers_in', to='inventory.warehouse', verbose_name='Destination Warehouse')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending'), ('in_transit', 'In Transit'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft', max_length=20, verbose_name='Status')),
                ('transfer_date', models.DateTimeField(blank=True, null=True, verbose_name='Transfer Date')),
                ('received_date', models.DateTimeField(blank=True, null=True, verbose_name='Received Date')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_transfers', to='accounts.user', verbose_name='Created By')),
                ('received_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_transfers', to='accounts.user', verbose_name='Received By')),
            ],
            options={
                'verbose_name': 'Stock Transfer',
                'verbose_name_plural': 'Stock Transfers',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['transfer_number'], name='inventory_transfer_number_idx'),
                    models.Index(fields=['source_warehouse'], name='inventory_transfer_source_idx'),
                    models.Index(fields=['destination_warehouse'], name='inventory_transfer_dest_idx'),
                    models.Index(fields=['status'], name='inventory_transfer_status_idx'),
                ],
            },
        ),
        
        # Stock Transfer Item
        migrations.CreateModel(
            name='StockTransferItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('transfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.stocktransfer', verbose_name='Transfer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_items', to='inventory.product', verbose_name='Product')),
                ('quantity', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Quantity')),
                ('quantity_received', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Quantity Received')),
                ('unit_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Unit Cost')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Cost')),
                ('serial_numbers', models.JSONField(blank=True, null=True, verbose_name='Serial Numbers')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Stock Transfer Item',
                'verbose_name_plural': 'Stock Transfer Items',
                'ordering': ['-created_at'],
            },
        ),
        
        # Stock Adjustment
        migrations.CreateModel(
            name='StockAdjustment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('adjustment_number', models.CharField(max_length=50, unique=True, verbose_name='Adjustment Number')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('reason', models.CharField(choices=[('count_error', 'Counting Error'), ('damage', 'Damage'), ('loss', 'Loss'), ('theft', 'Theft'), ('found', 'Found'), ('other', 'Other')], max_length=20, verbose_name='Reason')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('performed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_adjustments', to='accounts.user', verbose_name='Performed By')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_adjustments', to='accounts.user', verbose_name='Approved By')),
            ],
            options={
                'verbose_name': 'Stock Adjustment',
                'verbose_name_plural': 'Stock Adjustments',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['adjustment_number'], name='inventory_adjustment_number_idx'),
                    models.Index(fields=['date'], name='inventory_adjustment_date_idx'),
                    models.Index(fields=['reason'], name='inventory_adjustment_reason_idx'),
                ],
            },
        ),
        
        # Stock Adjustment Item
        migrations.CreateModel(
            name='StockAdjustmentItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('adjustment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.stockadjustment', verbose_name='Adjustment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjustment_items', to='inventory.product', verbose_name='Product')),
                ('old_quantity', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Old Quantity')),
                ('new_quantity', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='New Quantity')),
                ('difference', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Difference')),
                ('unit_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Unit Cost')),
                ('total_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Value')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Stock Adjustment Item',
                'verbose_name_plural': 'Stock Adjustment Items',
                'ordering': ['-created_at'],
            },
        ),
        
        # Service
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('service_type', models.CharField(choices=[('labor', 'Labor'), ('diagnostic', 'Diagnostic'), ('installation', 'Installation'), ('maintenance', 'Maintenance'), ('consultation', 'Consultation'), ('other', 'Other')], default='labor', max_length=20, verbose_name='Service Type')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Price')),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Cost')),
                ('estimated_duration', models.PositiveIntegerField(default=60, verbose_name='Estimated Duration (minutes)')),
                ('tax_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Tax Rate %')),
                ('is_taxable', models.BooleanField(default=True, verbose_name='Taxable')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='inventory.productcategory', verbose_name='Category')),
                ('tags', models.JSONField(blank=True, null=True, verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'ordering': ['name'],
                'unique_together': {('organization', 'code')},
                'indexes': [
                    models.Index(fields=['code'], name='inventory_service_code_idx'),
                    models.Index(fields=['name'], name='inventory_service_name_idx'),
                ],
            },
        ),
        
        # Service Category
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='inventory.servicecategory', verbose_name='Parent Category')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Service Category',
                'verbose_name_plural': 'Service Categories',
                'ordering': ['name'],
                'unique_together': {('organization', 'code')},
            },
        ),
    ]
