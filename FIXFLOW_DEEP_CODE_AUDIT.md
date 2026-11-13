# FixFlow Deep Code Audit

**Audited repository:** `https://github.com/guru77ai/Fixflow`  
**Audit date:** 2026-11-12  
**Scope:** Python/Django source, project configuration, URL routing, templates, static assets, API viewsets, security-sensitive patterns, tests and migrations.  
**Method:** Static inspection of the inspected repository snapshot; Python source compilation; inventory of template and static references; URL and import inspection; JavaScript syntax check where available.

> **Important limitation:** This is a source-level audit, not a successful runtime verification. The repository snapshot's declared dependencies are not installed in this inspection environment, so Django checks, migrations, test execution, HTTP integration tests, browser rendering, and database-backed business-flow tests were not run. Python compilation passing only confirms syntax, not importability or runtime correctness.

## Executive summary

**Current assessment: not runnable/release-ready without substantial repairs.** The repository contains a broad Django ERP application, but important pieces are disconnected or absent. The most serious confirmed blockers are:

1. `config/urls.py` imports `rest_framework_simplejwt`, but `djangorestframework-simplejwt` is absent from `requirements.txt`.
2. `django_filters` is configured and imported throughout API modules, but `django-filter` is absent from `requirements.txt`.
3. `config/urls.py` includes `apps.inventory.urls` and `apps.suppliers.urls`, but neither file exists in the inspected repository snapshot.
4. Many class-based views import `apps.core.mixins.OrganizationContextMixin` and `BranchContextMixin`, but `apps/core/mixins.py` does not exist.
5. Inventory and supplier API router modules exist (`api_urls.py`), but the root URL configuration does not include them; it points to missing regular `urls.py` modules instead.
6. The root URL configuration includes `apps.crm.urls`, `apps.repair.urls`, etc. under `/api/v1/`, but these are largely HTML/frontend URLconfs, not the corresponding API router URLconfs.
7. A large part of the Python view layer references templates that are absent or named differently from the templates in the inspected repository snapshot.
8. The shared sidebar contains many `{% url %}` references for namespaces/routes that are not registered in the URL configuration. Rendering the base layout can therefore fail with `NoReverseMatch`.
9. Several DRF `ModelViewSet` classes use unrestricted `.objects.all()` querysets while the global DRF permission policy only guarantees authentication. This is a major cross-organization data exposure risk unless every serializer and custom permission independently enforces tenant boundaries; that enforcement is not evident in these viewsets.
10. CSRF is explicitly disabled on customer and repair quick-create endpoints.

Python source compilation completed without syntax errors. `node --check static/js/main.js` also completed without reporting a syntax error. These checks do not mitigate the runtime blockers above.

---

## 1. Critical startup and dependency blockers

### 1.1 Missing declared Python dependencies — Critical

**Evidence**
- `config/urls.py` imports `rest_framework_simplejwt.views`.
- `config/settings/base.py` installs `rest_framework_simplejwt` and configures `JWTAuthentication`.
- `config/settings/base.py` configures `django_filters.rest_framework.DjangoFilterBackend`.
- Multiple API modules import `django_filters.rest_framework.DjangoFilterBackend`.
- `requirements.txt` lists Django, DRF, spectacular, corsheaders, etc., but does not list `djangorestframework-simplejwt` or `django-filter`.

**Impact**: A clean environment installed strictly from `requirements.txt` cannot import the root URL configuration and API modules. Django startup/checks fail with `ModuleNotFoundError`.

**Fix**: Add pinned, Django/DRF-compatible versions of both packages; ensure lock/constraints and deployment installation instructions agree. Add a clean-environment CI job that installs only declared dependencies and runs `manage.py check`.

### 1.2 Missing core mixins — Critical

**Evidence**: `apps/crm/views.py`, `apps/repair/views.py`, `apps/pos/views.py`, `apps/financial/views.py`, `apps/accounting/views.py`, and `apps/hr/views.py` import:

```python
from apps.core.mixins import OrganizationContextMixin, BranchContextMixin
```

But `apps/core/mixins.py` is absent. `apps/core/` contains models, context processors, pagination, app config, signals and tests only.

**Impact**: Importing these view modules fails. Since their URLconfs import the views, URL resolution/startup fails even after dependencies are installed.

**Fix**: Implement and test the mixins or remove the dependency in favor of a consistent, tested request context/service pattern. The implementation must fail closed when organization/branch context is missing, scope all object querysets, and validate object ownership on detail/update/delete operations. Do not simply attach arbitrary request attributes without membership validation.

### 1.3 Missing URLconfs for inventory and suppliers — Critical

**Evidence**: `config/urls.py` includes `apps.inventory.urls` and `apps.suppliers.urls` twice (under `/api/v1/` and as frontend paths), but those modules do not exist. The apps contain `api_urls.py`, `api_views.py`, models, serializers, services/selectors, tests, and templates, but no regular `urls.py` or `views.py`.

**Impact**: URL configuration import fails. Inventory/supplier HTML pages are not wired to their existing templates, and their API routers are not exposed.

**Fix**: Create a deliberate frontend URLconf and API URLconf for each module. Include the `api_urls.py` modules under `/api/v1/inventory/` and `/api/v1/suppliers/`. Implement the intended frontend views/forms or remove unsupported navigation/templates until implemented.

### 1.4 Invalid/stray directory in repository snapshot — Medium

**Evidence**: The inspected repository snapshot contains a literal directory named `apps/{core,accounts,organizations,licensing,branches,audit_logs,settings,dashboard,notifications,backups,reports,documents,barcode,zakat}` containing a `signals.py` file.

**Impact**: This appears to be an accidental shell-brace-expansion artifact. It is not a valid Python package path used by the project and creates repository noise/confusion.

**Fix**: Determine whether the file contains any unique signal registrations; merge legitimate code into the intended apps and remove the malformed directory. Add a repository hygiene check.

---

## 2. URL routing and API integration

### 2.1 API root points to frontend URLconfs — Critical

**Evidence**: Under `/api/v1/`, `config/urls.py` includes modules such as `apps.crm.urls`, `apps.repair.urls`, `apps.pos.urls`, `apps.financial.urls`, `apps.accounting.urls`, and `apps.hr.urls`. These URLconfs define HTML pages and hand-written API endpoints; the corresponding DRF routers are in separate `api_urls.py` modules.

**Impact**: The ViewSets registered in `api_urls.py` are not exposed at the expected API paths. Clients and the API schema may see missing routes or the wrong views. This is a functional API integration defect, not merely a naming preference.

**Fix**: Mount each router explicitly, e.g. `path('api/v1/crm/', include('apps.crm.api_urls'))`, and keep frontend routes outside the API prefix. Decide whether the older hand-written endpoints remain supported; avoid duplicate/conflicting API designs.

### 2.2 API and frontend routes are included more than once — High

**Evidence**: The root URLconf includes CRM/repair/POS/financial/accounting/HR at `/api/v1/<module>/` and again at `/<module>/`. Inventory and suppliers are also attempted twice.

**Impact**: The same URL patterns are mounted in different contexts, with ambiguous route names and unexpected URL behavior. A frontend page may appear under an API path, and route reversing may select an unintended pattern.

**Fix**: Establish one canonical route table with separate frontend and API namespaces. Add URL resolver tests for every documented endpoint and every navigation link.

### 2.3 `i18n_patterns` wraps the entire URL configuration — High

**Evidence**: `urlpatterns = i18n_patterns(*urlpatterns)` is applied after admin, schema, JWT, API, auth, and frontend URL patterns have all been assembled.

**Impact**: Admin/API/schema/JWT/static-serving routes become language-prefixed as well, potentially breaking clients, health checks, API docs, and expected paths. The code also uses `LocaleMiddleware` after `CommonMiddleware` and `CorsMiddleware` at the end of the middleware list, which is an unsuitable ordering for locale/CORS handling.

**Fix**: Apply `i18n_patterns` only to user-facing routes that should be language-prefixed. Keep API, admin, schema, token, and machine endpoints stable/unprefixed. Put `LocaleMiddleware` after `SessionMiddleware` and before `CommonMiddleware` per Django guidance; place `CorsMiddleware` high enough to add headers to early responses (before `CommonMiddleware`). Test Arabic/French/English routing.

### 2.4 Namespace and route-name inconsistencies — High

**Evidence**
- `apps/dashboard/urls_frontend.py` declares names such as `organizations:list`, `branches:list`, `licensing:view`, `audit_logs:list`, etc. directly as route names, but the URLconf itself has no matching `app_name` namespace and is included without an explicit namespace.
- Templates call names such as `crm:customer_edit`, `crm:customertype_delete`, `inventory:product_update`, `repair:repair_order_detail`, `pos:index`, `suppliers:supplier_update`, and many generic namespaces (`products:list`, `sales:list`, `employees:list`, `attendance:list`, etc.) that do not correspond to registered URL patterns in the inspected repository snapshot.
- CRM URLs use names such as `customer_update`, `customertype_update`, and `device_update`; templates use `customer_edit`, `customertype_edit`, `device_edit` and delete names that are not all registered.
- Repair URLs use `repairorder_list`, `repairorder_detail`, `repairorder_update`, etc., while templates use `repair_order_list`, `repair_order_detail`, `repair_order_update`, etc.
- POS has `dashboard` and `sale_list`, but the sidebar expects `pos:index`; the sale delete route is referenced in templates but is not registered.

**Impact**: Rendering templates that contain these tags raises `NoReverseMatch`, often breaking the whole page (especially the shared sidebar).

**Fix**: Define app namespaces correctly using `app_name` plus `include()` and consistent route names. Generate a route-name inventory and automatically parse every template `{% url %}` tag in tests. Remove links for features not implemented; do not leave dead links in the global navigation.

### 2.5 Dashboard API URL patterns are not mounted — Medium

**Evidence**: `apps/dashboard/urls.py` defines `urlpatterns_api` separately from `urlpatterns`; only `urlpatterns` is included.

**Impact**: Dashboard stats/recent-activity endpoints are unreachable unless mounted elsewhere (no such inclusion was found in the root config).

**Fix**: Mount them under the dashboard API prefix or merge them into an explicit `api_urls.py`.

---

## 3. Templates and frontend rendering

### 3.1 Many Python views reference templates that are absent — Critical/High

The inspected repository snapshot has 55 files under the global `templates/` directory. The view layer references many more. `APP_DIRS=True` is enabled, but no app-local `templates/` trees were found, so the missing references are not supplied by app template discovery.

Confirmed examples:

| Python view reference | Existing repository snapshot state |
|---|---|
| `accounts/login.html`, `accounts/register.html`, profile/settings/users and password-reset templates | Missing |
| `organizations/list.html`, `create.html`, `detail.html`, `edit.html`, `delete.html` | Missing |
| `branches/list.html`, `create.html`, `detail.html`, `edit.html`, `delete.html` | Missing |
| `audit_logs/list.html` | Missing |
| `backups/list.html`, `create.html`, `delete.html` | Missing |
| `notifications/list.html`, `detail.html` | Missing |
| `reports/dashboard.html`, sales/repairs/inventory/financial | Missing |
| `licensing/view.html` | Missing |
| `zakat/calculator.html`, `history.html` | Missing |
| `documents/list.html` | Missing |
| `settings/general.html` | Missing |
| `barcode/generator.html`, `barcode/print.html` | Missing |
| `financial/dashboard.html`, `accounting/dashboard.html`, `hr/dashboard.html` | Present |
| `pos/dashboard.html` | Missing |
| `pos/sale_list.html`, `sale_detail.html`, `sale_form.html` | Present |
| `repair/repairorder_list.html`, `repairorder_detail.html`, `repairorder_form.html`, `repairorder_confirm_delete.html`, `repairorder_status_change.html`, `repair/dashboard.html` | Missing under these exact names |

**Impact**: Requests to these views return `TemplateDoesNotExist` even after import/startup blockers are fixed.

**Fix**: For every view, choose a canonical template path. Either create the missing templates or update view references to the intended existing templates. Add a test that discovers all `template_name` and `render()` references and verifies that Django's template loader can resolve each one.

### 3.2 Existing template naming does not match repair view names — High

**Evidence**: Existing files are named `repair_order_list.html`, `repair_order_detail.html`, `repair_order_form.html`, `repair_order_confirm_delete.html`, and category/priority/status/type templates with underscores. The repair view classes refer to `repairorder_list.html`, `repairorder_detail.html`, `repairorder_form.html`, `repairorder_confirm_delete.html`, `repairorder_status_change.html`, and `repair/dashboard.html`.

**Impact**: The repair UI cannot render using the current view references. Several existing category/priority/status/type templates appear to have no corresponding registered view routes in `apps/repair/urls.py`.

**Fix**: Standardize naming and ensure every template has a corresponding view/URL and every view has a corresponding template. Avoid duplicate template variants with inconsistent names.

### 3.3 Template URL tags reference missing/unimplemented modules — Critical/High

The shared sidebar and page templates contain routes for modules absent from the URL configuration, including examples such as:

- `technicians:list`, `products:list`, `products:create`, `categories:list`, `inventory:list`, `warehouses:list`, `purchasing:list`
- `sales:list`, `invoices:list`, `payments:list`, `installments:list`, `cash_register:list`, `expenses:list`
- `employees:list`, `attendance:list`, `payroll:list`, `commissions:list`
- `customers:list`, `devices:list`, `repairs:list`, `repairs:workflow`

Some data domains exist in other apps, but these particular namespaces/routes are not registered. The sidebar also references route names that differ from the actual CRM, repair, POS, and supplier route names.

**Impact**: The base layout can fail before page-specific content is displayed. Users cannot reliably navigate the application.

**Fix**: Reconcile navigation against actual implemented endpoints. Use a navigation configuration tested with `reverse()`; gate menu items by permissions and feature availability. Do not expose links for features that have no implemented views.

### 3.4 Template references use inconsistent identifiers — High

**Evidence**: Several templates pass `object.uuid`, `product.uuid`, `sale.uuid`, etc., while many view routes use `<uuid:pk>` and the model primary key conventions need to be checked. Some views use `pk` while templates use `.uuid`; other views use `customer.pk` and similar. CRM route names also differ from template names.

**Impact**: Even after route names are fixed, missing attributes or mismatched UUID/PK types can break reversing or object lookup.

**Fix**: Standardize model identifiers and route converter usage. Test every detail/edit/delete link with real model instances, not only route-name existence.

### 3.5 Template correctness and UX tests are absent — High

No automated template-rendering or browser tests were identified. The inspected repository snapshot includes a number of HTML templates but no evidence of comprehensive tests for base layout, sidebar, forms, error states, Arabic RTL, responsive layout, or HTMX interactions.

**Fix**: Add Django template-render tests for every page and browser-level smoke tests for the critical user journeys. Test French, English and Arabic, including `dir="rtl"`, date/number/currency formatting, and form validation messages.

---

## 4. Static files, CSS, JavaScript, and external assets

### 4.1 Referenced local assets are missing — High

Only three static files exist in the inspected repository snapshot:

- `static/js/main.js`
- `static/css/styles.css`
- `static/css/rtl.css`

But templates reference local files that do not exist:

- `img/logo.png` (sidebar)
- `img/favicon.ico` (base layout)
- `css/datatables.min.css` and `js/datatables.min.js` (multiple list pages)

**Impact**: Broken logo/favicon and 404 requests for DataTables assets. The base template also loads DataTables from a CDN, so the local references may be redundant or an incomplete migration; the project must choose one source and use it consistently.

**Fix**: Add the missing assets or remove/replace the references. Avoid loading duplicate DataTables builds from both CDN and local static paths. Run `collectstatic` and assert all template static references resolve.

### 4.2 Static/media URL settings are relative — High

**Evidence**: `STATIC_URL = 'static/'` and `MEDIA_URL = 'media/'` are relative paths rather than root-relative `/static/` and `/media/`.

**Impact**: Relative URLs can resolve incorrectly under nested or language-prefixed routes (e.g. `/fr/repair/orders/static/...`).

**Fix**: Use canonical URL prefixes beginning with `/` (or explicit absolute CDN URLs where appropriate) and test under prefixed language routes and reverse-proxy deployments.

### 4.3 Production static storage configuration needs modernization — Medium/High

**Evidence**: Production uses `STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'`. Django 5.2 uses the `STORAGES` setting for modern storage configuration; the legacy setting may be deprecated/ignored depending on version behavior.

**Impact**: Static asset manifest generation may not use the intended backend, and deployment behavior can differ from expectations.

**Fix**: Configure `STORAGES['staticfiles']` explicitly for the project's Django version and run `collectstatic --noinput` in CI/deployment.

### 4.4 External CDN dependencies have availability and integrity risks — Medium

**Evidence**: The base template loads Bootstrap, Bootstrap Icons, DataTables, HTMX, Alpine.js, and Chart.js from external CDNs. Bootstrap has an integrity attribute; several other external script/style references do not.

**Impact**: CDN outage, supply-chain compromise, content-security-policy limitations, or network restrictions can break core UI behavior. Versions are hardcoded in templates and not managed through a dependency manifest.

**Fix**: Pin versions, add Subresource Integrity where supported, define a restrictive CSP compatible with the app, and decide which libraries should be vendored/self-hosted. Test with external network blocked to identify hard runtime dependencies.

### 4.5 JavaScript toast rendering is an XSS sink — High

**Evidence**: `static/js/main.js` builds HTML using interpolated `title` and `message` values and inserts it with `container.insertAdjacentHTML('beforeend', toastHtml)`.

**Impact**: If a server response or user-controlled string is passed to `showToast()`, markup/script injection may occur. Django template autoescaping does not protect strings inserted later by JavaScript.

**Fix**: Build DOM nodes and assign untrusted values using `textContent`; do not interpolate arbitrary values into HTML strings. If rich HTML is truly required, use a maintained sanitizer with a strict allowlist and test malicious payloads.

### 4.6 HTMX/Alpine initialization and lifecycle concerns — Medium

**Evidence**: `main.js` initializes some plugins on `DOMContentLoaded` and again on HTMX content loads. The code adds handlers to dynamically inserted forms and uses delegated event handling inconsistently. Base HTML uses `hx-boost="true"` globally.

**Impact**: Duplicate DataTables/Chart initialization, duplicate event handlers, stale widgets, and broken behavior after boosted navigation are possible. Global HTMX boosting can also interact badly with full-page navigation, file downloads, language changes, and forms without correct CSRF handling.

**Fix**: Make each initializer idempotent, destroy existing plugin instances before reinitializing, use delegated listeners where appropriate, and define explicit HTMX behavior for forms/downloads/navigation. Add browser tests for repeated partial updates.

### 4.7 Frontend theme and form enhancement edge cases — Medium

**Evidence**: `initFormEnhancements()` attaches a submit listener only when a click target has class `needs-validation`, which is not the normal way to bind form submit validation. It also resets all modal forms on `hidden.bs.modal`, potentially discarding user input unexpectedly. `printDocument()` assumes `window.open()` succeeds and returns a window object.

**Impact**: Validation may not run for keyboard submission; modal data may be lost; print popup blockers can cause a JavaScript exception.

**Fix**: Bind validation directly to `form.needs-validation` submit events during initialization/delegation; reset only when explicitly intended; null-check popup handles and provide an error path.

---

## 5. Python application design and correctness

### 5.1 Organization/branch scoping is not enforced consistently in DRF viewsets — Critical

**Evidence**: API viewsets in `apps/pos/api_views.py`, `apps/financial/api_views.py`, `apps/accounting/api_views.py`, `apps/hr/api_views.py`, `apps/inventory/api_views.py`, `apps/suppliers/api_views.py`, and other modules declare class-level querysets such as `Sale.objects.all()`, `Invoice.objects.all()`, `Account.objects.all()`, `Product.objects.all()`, and `Supplier.objects.all()`.

The global DRF default permission is `IsAuthenticated`; that proves the caller is logged in, not that the caller may access a particular organization or branch. Some service/selectors scope records correctly, but these ViewSets do not consistently use those selectors or override `get_queryset()`.

**Impact**: Authenticated users may list, retrieve, update, or delete records across tenant boundaries. Related objects may also be linked across organizations unless serializers validate them. This is a critical confidentiality and integrity risk for customer, payroll, sales, accounting, stock and supplier data.

**Fix**:
- Use a shared, fail-closed tenant-scoping mixin/base ViewSet.
- Scope every queryset by the authenticated user's active organization and authorized branch.
- Enforce object-level permissions on retrieve/update/delete and custom actions.
- Validate every foreign key and many-to-many relation belongs to the same organization (and branch where required).
- Derive organization, branch, created_by, and similar security-sensitive fields from the server-side request context; do not trust client-supplied IDs.
- Add cross-tenant tests for list/retrieve/create/update/delete and custom actions for every module.

### 5.2 ModelViewSets expose broad write operations — High

**Evidence**: Many ViewSets inherit `ModelViewSet`, which enables create, update, partial update, and destroy by default. This includes reference/configuration records and financial entities.

**Impact**: A logged-in user may be able to mutate or delete records that should be read-only, approval-controlled, immutable after posting, or accessible only to managers. The risk compounds with broad querysets.

**Fix**: Replace `ModelViewSet` with read-only or explicitly limited mixins where appropriate. Define role/action-specific permissions, immutable posted records, and audited service-layer commands for state transitions.

### 5.3 Quick-create endpoints disable CSRF — High

**Evidence**: `@csrf_exempt` appears on `quick_create_customer` in `apps/crm/views.py` and `quick_create_repair_order` in `apps/repair/views.py`.

**Impact**: If these endpoints rely on cookie/session authentication, a malicious site may cause authenticated users' browsers to submit unwanted creation requests. The endpoint code also reads request context attributes that must be guaranteed by middleware/mixins.

**Fix**: Remove CSRF exemptions for session-authenticated browser requests. Use proper CSRF token handling in HTMX/fetch. If machine clients need access, use token authentication with explicit permissions and do not silently bypass CSRF for browser sessions. Add method, content-type, input schema, rate-limit and permission validation.

### 5.4 Financial state transitions need stronger invariants — High

**Evidence**: In `apps/accounting/api_views.py`, `JournalEntryViewSet.post` directly sets `entry.is_posted = True` and saves. The action does not visibly call the accounting service, verify debit/credit balance, enforce approval, lock the record, or prevent reposting. Several money services convert incoming values to `Decimal`, but the full set of invariants must be verified.

**Impact**: Unbalanced or unauthorized journal entries may be posted; concurrent updates may cause inconsistent ledgers. Similar review is required for invoice payments, POS sales/refunds, expenses, bank reconciliation and stock movements.

**Fix**: Route posting through a single atomic domain service. Validate total debits equal total credits, period is open, accounts are active, user has approval authority, and entry is in a postable state. Use row locks where concurrency matters, create immutable ledger postings, and record reversal entries rather than editing posted transactions.

### 5.5 Money and quantity inputs require strict validation — High

**Evidence**: Service methods commonly construct `Decimal(data.get(...))` directly from request data. Examples appear in repair, POS, financial and accounting services.

**Impact**: Malformed values may raise exceptions; excessive precision, negative quantities, negative payments, inconsistent totals, and client-controlled totals may be accepted unless serializers/services enforce them. `Decimal(float)` can also preserve binary floating-point artifacts if floats reach these services.

**Fix**: Validate using Decimal-aware serializers/forms, reject floats for monetary inputs, enforce currency precision and positive/nonnegative constraints, calculate totals server-side from line items, apply rounding rules centrally, and add boundary/property tests. Never trust client-submitted subtotal/tax/total/balance as authoritative.

### 5.6 Business services need concurrency and idempotency review — High

**Evidence**: Some services use `transaction.atomic`, which is good, but the codebase's critical workflows must be checked for `select_for_update`, uniqueness/idempotency constraints, and retry-safe operations. Static search found few explicit row-lock patterns in financial/POS/repair service modules.

**Impact**: Concurrent sales, stock transfers, payments, refunds, cash register sessions, and journal posting can race, double-apply movements, or oversell inventory.

**Fix**: Identify aggregate roots and lock rows consistently; add unique idempotency keys for external/retried requests; enforce stock nonnegative constraints where appropriate; use atomic ledger/stock movement records; test concurrent requests against PostgreSQL (SQLite does not provide equivalent row-lock behavior).

### 5.7 Broad exception handling can hide defects — High

**Evidence**: Quick-create view code catches generic `Exception` and returns the raw exception string in JSON.

**Impact**: Unexpected internal details may leak to clients, errors become indistinguishable from validation errors, and failures may be swallowed without useful logs.

**Fix**: Catch expected validation/domain exceptions only; return stable error codes/messages; log unexpected exceptions with a correlation ID and return generic 500 responses. Do not expose SQL, paths, tracebacks, or internal exception messages.

### 5.8 Request context dependency is fragile — High

**Evidence**: Views/services access `request.organization` and `request.branch`. No request middleware implementing and validating these attributes was found in `MIDDLEWARE`; the referenced mixins are missing. Context processors only populate template context and do not establish request attributes for API views.

**Impact**: Once imports are patched, requests may fail with `AttributeError`, or developers may add unsafe client-controlled context. Organization and branch selection can become an authorization bypass if not validated against memberships.

**Fix**: Implement a dedicated middleware/context resolver or explicit view-level resolver that authenticates the user, validates organization membership, resolves branch membership, and rejects invalid/missing context. Keep context resolution consistent for HTML and API requests.

### 5.9 Logging configuration can fail or lose logs — Medium/High

**Evidence**: Base settings create `logs/`, but production logging config assumes the directory exists at import time via base side effect. The production settings replace handlers with file handlers and no console handler. Container platforms commonly expect stdout/stderr logging.

**Impact**: Permission/read-only filesystem issues can prevent startup or drop logs; file-only logging is operationally fragile in containers.

**Fix**: Prefer stdout/stderr handlers in container deployments; configure optional rotating file logging only where writable; avoid filesystem side effects during settings import; ensure log directories/permissions are handled by deployment.

### 5.10 Production settings are not production-grade — Critical/High

**Evidence**
- `config/settings/production.py` still uses SQLite.
- Base settings default `DEBUG=True` unless environment overrides it; development settings force `DEBUG=True`.
- Base settings have a predictable insecure fallback `SECRET_KEY`.
- Production `ALLOWED_HOSTS` defaults to an empty list if env is absent.
- Production settings do not configure a PostgreSQL connection from the documented environment variables.
- Production file logging and media/static storage are local filesystem based.

**Impact**: Production can be unavailable or insecure; SQLite is unsuitable for concurrent ERP/POS operations at scale and does not provide PostgreSQL locking/constraint behavior. Missing/incorrect environment variables can cause deployment failure.

**Fix**: Require explicit settings module and required environment variables; fail fast if secret key, allowed hosts, DB credentials, and trusted origins are absent. Configure PostgreSQL via environment. Add `check --deploy`, HTTPS proxy/HSTS configuration appropriate to the deployment, secure cookies, CSRF trusted origins, storage strategy, backups and restore drills.

### 5.11 CORS and middleware ordering — High

**Evidence**: `CorsMiddleware` is last in the base middleware list. `LocaleMiddleware` is also placed after `CommonMiddleware` and after authentication/messages middleware.

**Impact**: CORS headers may not be added to responses produced by earlier middleware; locale selection and URL processing may behave incorrectly. Development settings enable all origins with credentials, which is especially risky if copied into a deployment.

**Fix**: Put CORS middleware near the top (before CommonMiddleware), configure locale middleware in Django's recommended order, and never combine wildcard origins with credentials in production. Validate allowed origins and trusted CSRF origins separately.

### 5.12 JWT refresh token blacklist app not installed — Medium/High

**Evidence**: `SIMPLE_JWT` sets `BLACKLIST_AFTER_ROTATION=True`, but `rest_framework_simplejwt.token_blacklist` is not in `INSTALLED_APPS`.

**Impact**: Token blacklist/rotation behavior may not work as intended or may raise operational errors depending on the token flow.

**Fix**: Install the blacklist app, run its migrations, and test refresh rotation, logout/revocation, expired tokens and concurrent refreshes; alternatively disable blacklist-dependent behavior intentionally.

### 5.13 Custom user and account flows need end-to-end review — High

**Evidence**: A custom `AUTH_USER_MODEL = 'accounts.User'` is configured, but no account templates exist despite views referencing login/register/profile/password reset pages. The Django built-in auth URLs are also included under `/accounts/`, in addition to custom frontend account routes.

**Impact**: Duplicate or conflicting authentication routes, missing templates, password reset email template failures, and incomplete user lifecycle flows are likely.

**Fix**: Choose one coherent auth URL design; verify custom user manager, `USERNAME_FIELD`, required fields, password validators, email uniqueness/normalization, registration authorization, password reset token handling, logout method/CSRF, session invalidation, and staff/superuser creation. Test the full flow.

---

## 6. Static analysis of API and domain modules

### 6.1 Unrestricted queryset review is required across all ViewSets — Critical

The `.objects.all()` pattern was found in multiple API modules, including POS, financial, accounting, HR, inventory and suppliers. Some records may be global reference data (e.g. currency, payment method, account type), but each model must be classified explicitly:

- **Global reference data**: read-only or tightly controlled, not tenant-owned.
- **Organization-owned data**: always scope to organization.
- **Branch-owned data**: scope to organization and authorized branch.
- **Child/transaction data**: scope through parent and validate parent ownership.

Do not blanket-filter all tables identically; instead define explicit data ownership and access rules for every model.

### 6.2 Nested actions must inherit parent scope — Critical

Custom actions such as `sale.items`, `sale.payments`, `sale.receipt`, `refund.items`, `invoice.items`, `invoice.payments`, `journal-entry.lines`, and `bank-account.transactions` must only expose child rows of a parent already retrieved through a tenant-scoped `get_object()`. If the parent viewset is unrestricted, nested actions inherit that exposure.

### 6.3 Accounting posting and ledger integrity — High

Audit journal entry creation, posting, reversal, trial balance, financial statement generation, bank transactions, and ledger generation as a single coherent accounting domain. Required invariants include balanced entries, immutable posted records, period close controls, account/organization consistency, audit trails, deterministic numbering, and idempotent posting.

### 6.4 POS and inventory consistency — High

Audit POS sale creation, line item changes, payment capture, refund processing, cash register opening/closing, receipt generation, and inventory deductions as one atomic workflow. Ensure:
- Product belongs to the active organization and allowed warehouse/branch.
- Available stock is checked and decremented atomically.
- Refunds cannot exceed refundable sold quantities/amounts.
- Repeated API requests cannot duplicate sales/payments/refunds.
- Cash drawer movements reconcile with payment/refund events.
- Receipt numbering is unique under concurrency.

### 6.5 Repair workflow and parts — High

Audit repair status transitions, quotations, labor/parts costs, customer approvals, technician assignment, warranty, attachments, and stock consumption. Prevent arbitrary status jumps, ensure customer/device/repair order share organization, and ensure used parts create corresponding inventory movements. Do not accept client-provided final totals without server recalculation.

### 6.6 HR and payroll privacy — Critical

HR viewsets include employees, attendance, leave, payroll, commissions, and employee documents. Ensure strict role-based access (employee self-service vs HR vs payroll admin), tenant and branch scope, sensitive field restrictions, audit trails, document download authorization, and no salary/payroll data in broad list serializers.

### 6.7 File/document upload security — High

The settings define a maximum upload size and extension allowlist, but the audit must verify enforcement at every upload endpoint and model field. Extension checks alone are insufficient.

**Fix requirements**: validate content type and file signatures, randomize storage names, prevent executable serving, store private documents outside public static/media paths, enforce per-tenant download permissions, limit file size at proxy and Django layers, scan files where appropriate, and protect against path traversal and decompression bombs. Confirm image processing uses Pillow safely and PDF/Excel exports do not leak tenant data.

---

## 7. Database, migrations, and model consistency

### 7.1 Migration state has not been runtime-validated — High

The inspected repository snapshot contains migrations across most model-bearing apps, but no migration command was run. Static presence of migration files does not prove they apply cleanly or match current models.

**Fix**: Run `makemigrations --check --dry-run`, `migrate --plan`, and a clean database migration in CI. Test both SQLite (if supported) and PostgreSQL. Inspect migration dependencies for cycles and custom user model ordering.

### 7.2 PostgreSQL-specific behavior must be tested — High

The project is intended as a multi-user ERP/POS and needs real concurrency tests. SQLite can mask issues with row locking, constraints, transaction isolation and concurrent writes.

**Fix**: Make PostgreSQL the production/test reference database. Test constraints, indexes, locking, migrations, case-insensitive uniqueness and transaction rollback on PostgreSQL.

### 7.3 Referential and tenant consistency constraints — High

Django foreign keys do not automatically guarantee that related rows belong to the same organization or branch. Enforce this in service/serializer validation and, where feasible, database constraints. Audit all model relationships linking users, organizations, branches, customers, devices, repair orders, products, warehouses, suppliers, invoices, sales and employees.

### 7.4 Numeric field precision and validation — High

Review `DecimalField` precision/scale against DZD and other supported currencies, quantity precision for fractional stock, tax precision, rounding, and maximum values. Ensure forms, serializers, services and database constraints agree.

---

## 8. Tests and quality gates

### 8.1 Test coverage is incomplete — High

Tests exist in accounting, core, CRM, financial, HR, inventory, POS, repair and suppliers. Several other model-bearing apps have no test package (e.g. accounts, audit_logs, backups, barcode, branches, documents, licensing, notifications, organizations, settings, zakat). No comprehensive integration suite was identified.

**Fix**: Add tests for all apps and cross-module flows. Minimum required suites:
- Import/startup and URL resolution.
- Template loading and every URL tag reverse.
- Authentication, permission matrix and tenant isolation.
- Organization/branch membership changes and invalid context.
- API CRUD and serializer cross-tenant foreign-key rejection.
- Accounting balance/post/reversal/period close.
- POS sale/payment/refund/cash register/receipt.
- Stock movement/transfer/adjustment/concurrency.
- Repair lifecycle/parts/warranty.
- Payroll privacy and calculations.
- File upload/download authorization.
- Locale/RTL and frontend HTMX flows.

### 8.2 Add static and dependency checks — Medium/High

Add CI steps for:
- `pip install -r requirements.txt` in a clean environment.
- `python manage.py check` and `python manage.py check --deploy` with production-like env.
- `python manage.py makemigrations --check --dry-run`.
- `python manage.py migrate --noinput` against a fresh PostgreSQL database.
- `pytest` or `manage.py test` with coverage thresholds.
- Ruff/flake8, Black check, isort check, Bandit and dependency vulnerability scan.
- `collectstatic --noinput` and static-reference validation.
- JavaScript linting and browser smoke tests.

---

## 9. Prioritized remediation plan

### P0 — Restore clean startup and routing
1. Add missing dependencies (`djangorestframework-simplejwt`, `django-filter`) with compatible pinned versions.
2. Implement/replace missing core context mixins and validated request organization/branch resolution.
3. Create inventory/supplier URLconfs and mount the existing API routers correctly.
4. Correct root URL routing so frontend URLs are never mounted under `/api/v1/`.
5. Separate language-prefixed UI routes from API/admin/JWT/schema routes.
6. Add URL resolver and import smoke tests.

### P1 — Close security vulnerabilities
1. Tenant-scope every ViewSet and detail action.
2. Validate tenant ownership of every related object on create/update.
3. Remove CSRF exemptions or replace with a correct token-authenticated API design.
4. Add role/action-level permissions and make immutable resources read-only.
5. Fix JavaScript toast XSS sink.
6. Secure HR/payroll and document access.

### P2 — Make every page render
1. Create missing templates or update view paths to existing templates.
2. Fix repair template naming mismatch.
3. Fix every `{% url %}` name/namespace in templates and sidebar.
4. Implement or remove links to unimplemented modules.
5. Add missing logo/favicon/DataTables assets or remove stale references.
6. Test every page render and navigation link.

### P3 — Correct business workflows
1. Enforce accounting posting invariants and immutable ledger behavior.
2. Make POS payments/refunds/cash register flows atomic and idempotent.
3. Make inventory movements concurrency-safe.
4. Recalculate financial totals server-side with strict Decimal validation.
5. Validate repair workflow transitions and parts consumption.
6. Add HR/payroll calculations and privacy tests.

### P4 — Production and operations
1. Configure PostgreSQL and production environment validation.
2. Modernize static storage settings and use absolute static/media URL prefixes.
3. Fix CORS/locale middleware order and secure origin configuration.
4. Configure structured stdout logging, backups, private media storage and restore tests.
5. Add CI, dependency scanning, security checks, monitoring and deployment documentation.

---

## 10. Required acceptance criteria

Do not declare the project fixed until all of the following are demonstrated with command output/test evidence:

- A clean environment installs all dependencies from the committed dependency manifest.
- Django starts and `manage.py check` passes.
- Production `check --deploy` has no unexplained security warnings.
- Root URLconf imports successfully; no missing URL modules or view imports remain.
- Every expected frontend and API endpoint resolves to the intended view.
- API router endpoints are mounted under stable, documented `/api/v1/` paths.
- No frontend template is mounted under an API prefix.
- Every view template exists and can be loaded by Django's template loader.
- Every template `{% url %}` tag resolves; every static reference maps to a real file or an intentional external URL.
- `collectstatic` completes successfully and manifest references resolve.
- All migrations apply to a fresh PostgreSQL database; no uncommitted model changes remain.
- All automated tests pass, including cross-tenant access-denial tests for every tenant-owned resource.
- Unauthenticated requests are rejected; authenticated users cannot access another organization's or unauthorized branch's data.
- CSRF protection works for session-authenticated browser actions.
- Toast notifications cannot inject HTML/script from untrusted strings.
- Accounting, POS, inventory, repair and payroll invariants pass integration and concurrency tests.
- Arabic RTL, French and English UI smoke tests pass.
- File uploads/downloads enforce type, size, tenant and permission checks.
- Deployment documentation covers environment variables, PostgreSQL, static/media, HTTPS, backups, migrations and rollback.

## 11. Audit limitations and next inspection needed

This audit identified high-confidence structural defects and security risks from the inspected repository snapshot. It does **not** claim every business-logic defect has been proven. The following require runtime or deeper model-by-model verification:

- All serializer `create()`/`update()` paths and related-object validation.
- Every model field, constraint, index, `on_delete` policy and migration dependency.
- Exact accounting tax/rounding rules and financial report correctness.
- Inventory stock valuation, reservations, transfers and race conditions.
- POS cash drawer reconciliation and payment provider behavior.
- Repair warranty/quotation/approval state machine.
- Payroll, leave, overtime, commissions and local labor/tax compliance.
- Backup encryption, restore integrity and authorization.
- License signature verification, key management and bypass resistance.
- Actual browser rendering and responsive/RTL behavior.

A follow-up audit should run the application against PostgreSQL, execute all tests, inspect every serializer/model/service, and exercise the critical workflows through HTTP/browser integration tests. Fixes should be made in small, reviewable commits with regression tests rather than applying broad automated rewrites.
