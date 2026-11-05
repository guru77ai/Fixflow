"""
Initial migration for Repair module
"""
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0001_initial'),
        ('organizations', '0001_initial'),
        ('branches', '0001_initial'),
        ('accounts', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        # Repair Status
        migrations.CreateModel(
            name='RepairStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('color', models.CharField(blank=True, help_text='Color for UI representation', max_length=20, null=True, verbose_name='Color')),
                ('is_initial', models.BooleanField(default=False, help_text='Is this the initial status for new repair orders?', verbose_name='Initial Status')),
                ('is_final', models.BooleanField(default=False, help_text='Is this a final status (cannot be changed)?', verbose_name='Final Status')),
                ('sequence', models.PositiveIntegerField(default=0, help_text='Order in which statuses appear', verbose_name='Sequence')),
            ],
            options={
                'verbose_name': 'Repair Status',
                'verbose_name_plural': 'Repair Statuses',
                'ordering': ['sequence', 'name'],
            },
        ),
        
        # Repair Priority
        migrations.CreateModel(
            name='RepairPriority',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('level', models.PositiveIntegerField(default=1, help_text='Higher level = higher priority', verbose_name='Level')),
                ('color', models.CharField(blank=True, max_length=20, null=True, verbose_name='Color')),
                ('estimated_hours', models.PositiveIntegerField(default=24, help_text='Target resolution time in hours', verbose_name='Estimated Hours')),
            ],
            options={
                'verbose_name': 'Repair Priority',
                'verbose_name_plural': 'Repair Priorities',
                'ordering': ['-level'],
            },
        ),
        
        # Repair Category
        migrations.CreateModel(
            name='RepairCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='repair.repaircategory', verbose_name='Parent Category')),
                ('icon', models.CharField(blank=True, max_length=50, null=True, verbose_name='Icon')),
                ('color', models.CharField(blank=True, max_length=20, null=True, verbose_name='Color')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Repair Category',
                'verbose_name_plural': 'Repair Categories',
                'ordering': ['name'],
            },
        ),
        
        # Repair Type
        migrations.CreateModel(
            name='RepairType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_types', to='repair.repaircategory', verbose_name='Category')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('estimated_cost', models.DecimalField(blank=True, decimal_places=2, help_text='Estimated cost for this repair type', max_digits=19, null=True, verbose_name='Estimated Cost')),
                ('estimated_duration', models.PositiveIntegerField(default=60, help_text='Estimated repair duration in minutes', verbose_name='Estimated Duration (minutes)')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Repair Type',
                'verbose_name_plural': 'Repair Types',
                'ordering': ['name'],
            },
        ),
        
        # Repair Order
        migrations.CreateModel(
            name='RepairOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('order_number', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Order Number')),
                ('order_type', models.CharField(choices=[('standard', 'Standard Repair'), ('express', 'Express Repair'), ('warranty', 'Warranty Repair'), ('premium', 'Premium Service'), ('diagnostic', 'Diagnostic Only')], default='standard', max_length=20, verbose_name='Order Type')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='repair_orders', to='crm.customer', verbose_name='Customer')),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_orders', to='crm.device', verbose_name='Device')),
                ('device_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Device Name')),
                ('device_imei', models.CharField(blank=True, max_length=20, null=True, verbose_name='Device IMEI')),
                ('device_serial', models.CharField(blank=True, max_length=50, null=True, verbose_name='Device Serial')),
                ('device_brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_orders', to='crm.devicebrand', verbose_name='Device Brand')),
                ('device_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_orders', to='crm.devicemodel', verbose_name='Device Model')),
                ('repair_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_orders', to='repair.repairtype', verbose_name='Repair Type')),
                ('repair_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_orders', to='repair.repaircategory', verbose_name='Repair Category')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='repair_orders', to='repair.repairstatus', verbose_name='Status')),
                ('priority', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='repair_orders', to='repair.repairpriority', verbose_name='Priority')),
                ('issue_description', models.TextField(help_text='Detailed description of the problem', verbose_name='Issue Description')),
                ('reported_issue', models.TextField(blank=True, help_text='What the customer reported', null=True, verbose_name='Reported Issue')),
                ('diagnosis', models.TextField(blank=True, help_text='Technician diagnosis', null=True, verbose_name='Diagnosis')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_repairs', to='accounts.user', verbose_name='Assigned To')),
                ('received_date', models.DateTimeField(auto_now_add=True, verbose_name='Received Date')),
                ('promised_date', models.DateTimeField(blank=True, help_text='Date promised to the customer', null=True, verbose_name='Promised Date')),
                ('started_date', models.DateTimeField(blank=True, null=True, verbose_name='Started Date')),
                ('completed_date', models.DateTimeField(blank=True, null=True, verbose_name='Completed Date')),
                ('delivered_date', models.DateTimeField(blank=True, null=True, verbose_name='Delivered Date')),
                ('quotation_amount', models.DecimalField(decimal_places=2, default=0.0, help_text='Amount quoted to the customer', max_digits=19, verbose_name='Quotation Amount')),
                ('labor_cost', models.DecimalField(decimal_places=2, default=0.0, help_text='Labor cost for the repair', max_digits=19, verbose_name='Labor Cost')),
                ('parts_cost', models.DecimalField(decimal_places=2, default=0.0, help_text='Cost of parts used', max_digits=19, verbose_name='Parts Cost')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0.0, help_text='Total repair cost', max_digits=19, verbose_name='Total Cost')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, help_text='Discount applied', max_digits=19, verbose_name='Discount')),
                ('tax_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Tax Amount')),
                ('final_amount', models.DecimalField(decimal_places=2, default=0.0, help_text='Final amount to be paid', max_digits=19, verbose_name='Final Amount')),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Amount Paid')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, help_text='Remaining balance to be paid', max_digits=19, verbose_name='Balance')),
                ('payment_method', models.CharField(blank=True, max_length=50, null=True, verbose_name='Payment Method')),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('partial', 'Partial'), ('paid', 'Paid'), ('refunded', 'Refunded'), ('cancelled', 'Cancelled')], default='pending', max_length=20, verbose_name='Payment Status')),
                ('warranty_type', models.CharField(choices=[('none', 'No Warranty'), ('standard', 'Standard Warranty'), ('extended', 'Extended Warranty'), ('lifetime', 'Lifetime Warranty')], default='none', max_length=20, verbose_name='Warranty Type')),
                ('warranty_period', models.PositiveIntegerField(default=0, help_text='Warranty period in months', verbose_name='Warranty Period (months)')),
                ('warranty_expiry', models.DateField(blank=True, null=True, verbose_name='Warranty Expiry')),
                ('internal_notes', models.TextField(blank=True, help_text='Notes visible only to staff', null=True, verbose_name='Internal Notes')),
                ('customer_notes', models.TextField(blank=True, help_text='Notes to show to the customer', null=True, verbose_name='Customer Notes')),
                ('is_urgent', models.BooleanField(default=False, verbose_name='Urgent')),
                ('is_warranty_claim', models.BooleanField(default=False, verbose_name='Warranty Claim')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('approval_date', models.DateTimeField(blank=True, null=True, verbose_name='Approval Date')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_repairs', to='accounts.user', verbose_name='Approved By')),
                ('status_changed_at', models.DateTimeField(auto_now=True, verbose_name='Status Changed At')),
                ('status_changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_status_changes', to='accounts.user', verbose_name='Status Changed By')),
                ('tags', models.JSONField(blank=True, help_text='JSON array of tags', null=True, verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Repair Order',
                'verbose_name_plural': 'Repair Orders',
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['order_number'], name='repair_order_number_idx'),
                    models.Index(fields=['customer'], name='repair_order_customer_idx'),
                    models.Index(fields=['device'], name='repair_order_device_idx'),
                    models.Index(fields=['status'], name='repair_order_status_idx'),
                    models.Index(fields=['priority'], name='repair_order_priority_idx'),
                    models.Index(fields=['assigned_to'], name='repair_order_assigned_to_idx'),
                    models.Index(fields=['order_type'], name='repair_order_type_idx'),
                    models.Index(fields=['organization', 'order_number'], name='repair_order_org_number_idx'),
                    models.Index(fields=['created_at'], name='repair_order_created_at_idx'),
                    models.Index(fields=['promised_date'], name='repair_order_promised_date_idx'),
                ],
            },
        ),
        
        # Repair Order History
        migrations.CreateModel(
            name='RepairOrderHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('repair_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='repair.repairorder', verbose_name='Repair Order')),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_history_changes', to='accounts.user', verbose_name='Changed By')),
                ('change_type', models.CharField(choices=[('status_change', 'Status Change'), ('assignment', 'Assignment'), ('cost_update', 'Cost Update'), ('note_added', 'Note Added'), ('approval', 'Approval'), ('payment', 'Payment'), ('other', 'Other')], max_length=50, verbose_name='Change Type')),
                ('field_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Field Name')),
                ('old_value', models.TextField(blank=True, null=True, verbose_name='Old Value')),
                ('new_value', models.TextField(blank=True, null=True, verbose_name='New Value')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
            ],
            options={
                'verbose_name': 'Repair Order History',
                'verbose_name_plural': 'Repair Order Histories',
                'ordering': ['-created_at'],
            },
        ),
        
        # Repair Part
        migrations.CreateModel(
            name='RepairPart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('repair_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='repair.repairorder', verbose_name='Repair Order')),
                ('part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_parts', to='inventory.product', verbose_name='Part')),
                ('part_name', models.CharField(max_length=200, verbose_name='Part Name')),
                ('part_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Part Code')),
                ('quantity', models.DecimalField(decimal_places=3, default=1.0, max_digits=10, verbose_name='Quantity')),
                ('unit_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Unit Cost')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Cost')),
                ('serial_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Serial Number')),
                ('is_warranty', models.BooleanField(default=False, verbose_name='Warranty Part')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Repair Part',
                'verbose_name_plural': 'Repair Parts',
                'ordering': ['-created_at'],
            },
        ),
        
        # Repair Service
        migrations.CreateModel(
            name='RepairService',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('repair_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='repair.repairorder', verbose_name='Repair Order')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_services', to='inventory.service', verbose_name='Service')),
                ('service_name', models.CharField(max_length=200, verbose_name='Service Name')),
                ('service_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Service Code')),
                ('quantity', models.DecimalField(decimal_places=3, default=1.0, max_digits=10, verbose_name='Quantity')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Unit Price')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Total Price')),
                ('duration_minutes', models.PositiveIntegerField(default=0, verbose_name='Duration (minutes)')),
                ('technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repair_services_performed', to='accounts.user', verbose_name='Technician')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Repair Service',
                'verbose_name_plural': 'Repair Services',
                'ordering': ['-created_at'],
            },
        ),
        
        # Repair Checklist
        migrations.CreateModel(
            name='RepairChecklist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('repair_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklists', to='repair.repairorder', verbose_name='Repair Order')),
                ('item', models.CharField(max_length=200, verbose_name='Item')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='Completed At')),
                ('completed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='completed_checklists', to='accounts.user', verbose_name='Completed By')),
                ('sequence', models.PositiveIntegerField(default=0, verbose_name='Sequence')),
            ],
            options={
                'verbose_name': 'Repair Checklist',
                'verbose_name_plural': 'Repair Checklists',
                'ordering': ['sequence'],
            },
        ),
        
        # Repair Attachment
        migrations.CreateModel(
            name='RepairAttachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('repair_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='repair.repairorder', verbose_name='Repair Order')),
                ('file', models.FileField(upload_to='repair_attachments/', verbose_name='File')),
                ('file_type', models.CharField(choices=[('photo', 'Photo'), ('document', 'Document'), ('video', 'Video'), ('other', 'Other')], default='photo', max_length=50, verbose_name='File Type')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_attachments', to='accounts.user', verbose_name='Uploaded By')),
            ],
            options={
                'verbose_name': 'Repair Attachment',
                'verbose_name_plural': 'Repair Attachments',
                'ordering': ['-created_at'],
            },
        ),
        
        # Repair Template
        migrations.CreateModel(
            name='RepairTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated at')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_organization', to='organizations.organization', verbose_name='Organization')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_branch', to='branches.branch', verbose_name='Branch')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('repair_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='templates', to='repair.repairtype', verbose_name='Repair Type')),
                ('estimated_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=19, verbose_name='Estimated Cost')),
                ('estimated_duration', models.PositiveIntegerField(default=60, verbose_name='Estimated Duration (minutes)')),
                ('checklist_items', models.JSONField(blank=True, help_text='JSON array of checklist items', null=True, verbose_name='Checklist Items')),
                ('default_parts', models.JSONField(blank=True, help_text='JSON array of default parts', null=True, verbose_name='Default Parts')),
                ('default_services', models.JSONField(blank=True, help_text='JSON array of default services', null=True, verbose_name='Default Services')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Repair Template',
                'verbose_name_plural': 'Repair Templates',
                'ordering': ['name'],
                'unique_together': {('organization', 'code')},
            },
        ),
    ]
