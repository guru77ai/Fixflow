# FixSoftRepair Pro

## Complete Repair Shop ERP / POS Management System

FixSoftRepair Pro is a professional, production-quality repair shop management system built with Django, designed to support GSM and smartphone repair shops, computer repair shops, electronics repair workshops, automotive repair workshops, and general maintenance businesses.

## Features

### Core Features
- **Multi-Organization Support**: Manage multiple companies/businesses
- **Multi-Branch Support**: Manage multiple physical locations
- **Role-Based Access Control**: Granular permissions for different user types
- **Internationalization**: Support for French, Arabic, and English
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Modules

#### Customer Relationship Management (CRM)
- Customer management with profiles, history, and statements
- Device registry with IMEI, serial numbers, and photos
- Quick customer creation from repair intake and POS

#### Repair Management
- Complete repair workflow with status tracking
- Automatic stock deduction for used parts
- Repair history and statistics
- Quotation and invoice generation
- Warranty tracking

#### Inventory Management
- Real stock ledger with movement history
- Multiple warehouses and branch transfers
- Serialized product tracking
- Low-stock notifications
- Stock valuation

#### Point of Sale (POS)
- Professional, fast POS interface
- Barcode scanning support
- Multiple payment methods
- Credit sales and installments
- Receipt printing (thermal and A4)

#### Financial Management
- Invoicing system with automatic numbering
- Payment processing with idempotency
- Installment and debt management
- Cash register management
- Expense tracking

#### Accounting
- Chart of accounts
- General ledger
- Journal entries
- Financial statements
- Trial balance

#### Human Resources
- Employee management
- Attendance tracking
- Payroll processing
- Commission calculations

#### Reporting
- Sales reports
- Repair reports
- Inventory reports
- Financial reports
- Technician performance reports
- Custom report builder

#### Advanced Features
- Zakat calculator with configurable methodology
- Document management
- Barcode generation
- Audit logging
- Backup and restore
- License verification (perpetual/lifetime model)
- Notifications system

## Technical Stack

### Backend
- **Python**: 3.12+
- **Django**: 5.2
- **Django REST Framework**: For REST APIs
- **SQLite**: Primary database (can be replaced with PostgreSQL)
- **DRF Spectacular**: API documentation

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling
- **Bootstrap 5**: Responsive UI framework
- **HTMX**: Dynamic server-rendered interactions
- **Alpine.js**: Lightweight client-side state management
- **Vanilla JavaScript**: Specialized components
- **Chart.js**: Data visualization
- **DataTables**: Interactive tables
- **Bootstrap Icons**: Icon library

## Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Git

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gsmlte77-droid/Fixflow.git
   cd Fixflow
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   Open your browser and navigate to `http://localhost:8000`

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```ini
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite is used by default)
# For PostgreSQL:
# DATABASE_ENGINE=django.db.backends.postgresql
# DATABASE_NAME=fixsoftrepair
# DATABASE_USER=postgres
# DATABASE_PASSWORD=your-password
# DATABASE_HOST=localhost
# DATABASE_PORT=5432

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@fixsoftrepair.com

# CORS Settings (for development)
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### Settings

The application uses a modular settings structure:
- `config/settings/base.py`: Base settings
- `config/settings/development.py`: Development-specific settings
- `config/settings/production.py`: Production-specific settings

To use development settings:
```bash
python manage.py runserver --settings=config.settings.development
```

## Project Structure

```
fixsoftrepair-pro/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
│
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/
│   ├── accounts/
│   ├── organizations/
│   ├── licensing/
│   ├── branches/
│   ├── audit_logs/
│   ├── settings/
│   ├── dashboard/
│   ├── notifications/
│   ├── backups/
│   ├── reports/
│   ├── documents/
│   ├── barcode/
│   └── zakat/
│
├── templates/
│   ├── base/
│   ├── components/
│   ├── layouts/
│   └── errors/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── img/
│   └── vendor/
│
├── media/
│
├── locale/
│   ├── fr/
│   ├── ar/
│   └── en/
│
├── tests/
│
└── docs/
```

## API Documentation

The application provides RESTful APIs for all modules. API documentation is available at:
- `/api/docs/`: Swagger UI
- `/api/schema/`: OpenAPI schema

### API Endpoints

All API endpoints are prefixed with `/api/v1/` and follow the pattern:
- `/api/v1/<module>/`: List and create operations
- `/api/v1/<module>/<id>/`: Retrieve, update, and delete operations
- `/api/v1/<module>/<id>/<action>/`: Custom actions

### Authentication

API authentication uses JWT (JSON Web Tokens):
- `POST /api/token/`: Get access and refresh tokens
- `POST /api/token/refresh/`: Refresh access token

Include the access token in the `Authorization` header:
```
Authorization: Bearer <access_token>
```

## Testing

Run tests using pytest:
```bash
pytest
```

Or using Django's test runner:
```bash
python manage.py test
```

## License

This project is proprietary software. For licensing information, please contact the vendor.

## Support

For support and inquiries, please contact:
- Email: support@fixsoftrepair.com
- Website: https://fixsoftrepair.com

## Contributing

This is a proprietary project. Contributions are not accepted at this time.

## Security

If you discover any security vulnerabilities, please report them immediately to security@fixsoftrepair.com.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.
