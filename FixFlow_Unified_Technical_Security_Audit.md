# FixFlow — Unified Technical, Security & Production-Readiness Audit

**Project:** FixFlow / FixSoftRepair Pro  
**Audit date:** 2026-11-22  
**Document type:** Consolidated audit combining two static audit reports  
**Primary perspective:** Django 5.2, Django REST Framework, multi-tenant ERP/POS, application security and full-stack engineering  
**Disposition:** **FAIL — not ready for production**

---

## 1. Executive summary

The two source reports agree on the central conclusion: **FixFlow must not be deployed with real customer, employee, inventory, or financial data until tenant isolation and authorization have been repaired and independently tested.**

The most serious concern is not a single endpoint. It is the combination of:

1. API ViewSets that expose tenant-owned records without tenant scoping.
2. Serializers that may allow clients to assign or change `organization` and `branch`.
3. Tenant context that is not reliably populated for authenticated API requests.
4. A default DRF permission policy of `IsAuthenticated`, without effective role-based authorization.
5. A backup system that can expose a database containing multiple organizations.
6. License verification based on a reproducible hash rather than a private-key digital signature.

This creates a plausible path from an ordinary authenticated account to unauthorized access or modification of another organization's data. The attached audit additionally identifies backup and licensing risks that were not covered by the first report.

The application also has significant first-run and runtime defects: a login route/template conflict, missing imports, unresolved URL names, missing templates, a missing `qrcode` dependency, and possible API authentication recursion. These defects can prevent workflows from operating correctly and can obscure security testing.

### Overall disposition

<badge color="danger">FAIL — production deployment not recommended</badge>

The immediate release blockers are:

- Cross-tenant data access and tenant reassignment.
- Missing role/permission enforcement.
- Insecure backup download and restore design.
- Forgeable license verification.
- Broken API tenant-context lifecycle.
- Application startup and runtime blockers.
- Unsafe production-settings defaults.

### Consolidated risk themes

| Area | Consolidated assessment |
|---|---|
| Tenant isolation | Critical |
| Role-based authorization | Critical |
| Backup confidentiality and restore safety | Critical |
| License integrity | Critical |
| API authentication/context lifecycle | High / critical impact |
| Account recovery and authentication UX | High |
| Runtime routing/import/template integrity | High |
| Production configuration and secrets | High |
| Uploads and file access | Medium / High |
| Financial and inventory concurrency | Medium / High |
| Test coverage and release verification | High |

---

## 2. Scope, provenance and limitations

### 2.1 Source reports combined

This document merges the following two reports:

1. **First report:** `FixFlow_Security_Audit_Report.md`, generated from the archive named `Fixflow-main (5).zip`.
2. **Second report:** `FIXFLOW_AUDIT_REPORT.md`, attached by the user. Its header identifies the archive as `194a34ad-Fixflow-main_5.zip`.

Both reports are dated 2026-11-22 and describe a Django 5.2 / DRF multi-tenant repair-shop ERP/POS application. The second report describes 563 files, approximately 33,500 lines of Python excluding migrations, 22 apps, and 172 templates.

**Snapshot caveat:** The archive names differ. The reports appear to concern closely related FixFlow snapshots and agree on several distinctive findings (including 35 missing template references), but this merge does not prove the two ZIP files are byte-for-byte identical. Findings should be rechecked against the exact release candidate before remediation is marked complete.

### 2.2 Method represented by the source reports

The reports describe static source review and scripted checks of settings, URL routing, tenancy/authentication, DRF ViewSets and serializers, HTML views, services/selectors, models, forms, uploads, backups, licensing, templates, tests, and dependencies.

The first report recorded successful Python syntax compilation for 339 Python files. The second report describes scripted AST/regex checks for URL names, template existence, undefined names, and imports.

### 2.3 What was not executed

Neither source report represents a full runtime or penetration test. The attached report explicitly states that Django was unavailable in its audit environment and that no `manage.py check`, migration run, test run, or browser test was performed. The first report likewise did not run the application, migrations, tests, endpoint tests, or browser tests.

Accordingly:

- **Confirmed/static** means the source report describes a direct code observation or scripted source check.
- **Runtime verification required** means the report identifies a likely framework/runtime behavior that should be reproduced in a test environment.
- **Not verified** means the source report explicitly did not inspect or establish the behavior.

No finding should be considered fixed merely because a code change has been made; the acceptance tests in Section 10 must pass.

### 2.4 Business-logic coverage gap

The attached report explicitly says that a line-by-line review of inventory, POS, financial, accounting, CRM, repair, and HR business logic was not completed because parallel review jobs hit a usage limit. Payroll calculations, journal balancing, stock movements, refunds, and workflow transitions therefore remain **unaudited for correctness**. The concurrency observations below are structural risks, not a completed financial correctness audit.

### 2.5 Historical audit

The archive contains `FIXFLOW_DEEP_CODE_AUDIT.md` dated 2026-11-12. Both source reports note that several old findings are stale in the later snapshot, including missing `apps/core/mixins.py`, missing SimpleJWT/`django-filter` dependencies, and missing inventory/suppliers URL configuration. Those old findings are not repeated as current defects here.

---

## 3. Architecture and security model

The project is described as a Django project under `config/` with settings split into `base`, `development`, and `production`, and 22 application modules under `apps/`.

The reported application layering is:

- `models`: persistence and domain entities.
- `selectors`: read/query logic.
- `services`: write/business operations.
- HTML `views`: browser-facing workflows.
- `api_views` and `serializers`: DRF endpoints.

The tenancy hierarchy is `Organization` → `Branch`. HTML requests use organization/branch middleware and context mixins. API requests use JWT/session authentication and `TenantContextAuthentication`, with `TenantScopedMixin` intended to scope ViewSets.

The API's global default permission is `IsAuthenticated`. This proves that a request has an authenticated user; it does **not** prove that the user belongs to the requested organization, has access to the requested branch, or is authorized to perform the requested operation.

This distinction is fundamental to the findings below.

---

# 4. Critical findings

## C-01 — Tenant-owned API ViewSets expose unscoped querysets

**Severity:** Critical  
**Status:** Confirmed by the attached static audit; endpoint exploitability should be regression-tested.

The attached report identifies approximately 30 ViewSets extending plain `viewsets.ModelViewSet` with unrestricted querysets such as `Model.objects.all()` and no tenant-filtering `get_queryset()`.

The first report independently counted 89 ViewSet declarations and found 33 that did not inherit a tenant-scoping mixin. The counts use different criteria: absence of the mixin versus unrestricted queryset behavior. They should not be treated as contradictory or added together.

### Affected resource families identified

**Financial:**
- `InvoiceItemViewSet`
- `InvoicePaymentViewSet`
- `ExpenseAttachmentViewSet`

**POS:**
- `SaleItemViewSet`
- `SalePaymentViewSet`
- `RefundItemViewSet`

**Repair:**
- `RepairOrderHistoryViewSet`
- `RepairPartViewSet`
- `RepairServiceViewSet`
- `RepairChecklistViewSet`
- `RepairAttachmentViewSet`

**Inventory:**
- `StockTransferItemViewSet`
- `StockAdjustmentItemViewSet`

**Suppliers:**
- `SupplierContactViewSet`

**Reference data called out by the attached audit:**
- `CustomerType`
- `CustomerSource`
- `DeviceCategory`
- `DeviceBrand`
- `DeviceModel`
- `InvoiceStatus`
- `InvoiceType`
- `PaymentMethod`
- `RepairStatus`
- `RepairPriority`
- `RepairCategory`
- `RepairType`
- `ProductBrand`
- `UnitOfMeasure`
- `SupplierCategory`
- `AccountType`
- `EmploymentType`
- `LeaveType`
- `SalaryComponent`

The first report additionally names several ViewSets and modules for review, including HR lookup data and child records. Not every non-tenant ViewSet is necessarily vulnerable: some reference data may intentionally be global. Ownership and access policy must be decided explicitly for each one.

The attached report notes that some docstrings claim child records are “scoped through parent Invoice/Expense”, but the actual queryset code does not implement that scope.

### Impact

An authenticated user may be able to list, retrieve, update, or delete another organization's records. Child-record endpoints are especially dangerous because they can bypass the parent endpoint's tenant filter. Examples include invoice lines, payments, repair attachments, sale items, and stock-transfer items.

Writable global reference tables may also allow ordinary users to alter shared system data.

### Remediation

1. Build a complete inventory of every registered API ViewSet and classify its model as global, organization-owned, branch-owned, or owned through a parent.
2. Scope every tenant-owned queryset by the authenticated organization and, where required, branch.
3. For child models, scope through the owning relation (for example, `invoice__organization`, `sale__branch`, or `repair_order__organization`).
4. Validate parent IDs and all tenant-owned foreign keys on create and update.
5. Make genuinely global lookup resources read-only for ordinary users, or explicitly make them organization-specific.
6. Do not rely on UI filtering or hidden form fields for security.
7. Add cross-tenant tests for list, retrieve, create, update, partial update, and delete.

---

## C-02 — `organization` and `branch` may be client-writable on scoped API resources

**Severity:** Critical  
**Status:** Static evidence in the attached report; confirm serializer behavior and endpoint execution at runtime.

The attached report states:

- `TenantScopedMixin` filters reads but does not enforce create-time ownership.
- `TenantScopedModelViewSet`, which reportedly enforces `perform_create`, is not used by the API ViewSets.
- No `perform_create` method was found in the inspected `api_views.py` files.
- 87 serializer classes across 8 modules use `fields = '__all__'`.
- The reported `read_only_fields` declarations do not include `organization` or `branch`.

### Impact

A client may be able to submit or patch an organization/branch identifier to create an object under another tenant or move an existing object across tenant boundaries. This can defeat queryset filtering if the write path accepts foreign tenant IDs.

### Remediation

1. Set tenant ownership server-side from validated request context.
2. Mark `organization` and `branch` as read-only in serializers when the client must not choose them.
3. Validate every foreign key and parent object against the current tenant.
4. Use a tenant-aware base ViewSet consistently, but do not assume inheritance alone is sufficient.
5. Test malicious POST, PUT, and PATCH requests that submit another organization's IDs.

---

## C-03 — Role-based authorization is not enforced

**Severity:** Critical  
**Status:** Confirmed by the attached static audit.

The attached report states that `Role` and `Permission` models exist in `apps/accounts`, but are not consulted by the inspected views, ViewSets, or services. It also notes that `PermissionRequiredMixin` is imported in CRM, repair, inventory, and supplier views, but no view defines `permission_required`.

The global DRF default is `IsAuthenticated`.

### Impact

Any logged-in user may be able to perform operations beyond their job responsibilities, potentially including:

- Creating, modifying, or deleting customers.
- Changing inventory and stock records.
- Posting financial entries or changing payments.
- Managing users and organization settings.
- Creating or downloading backups.
- Viewing licensing information.
- Modifying shared reference data.

This is a privilege-escalation problem even when tenant isolation is correctly implemented: users inside the same organization still require role- and operation-level authorization.

### Remediation

1. Define an explicit permission matrix by role, resource, and operation.
2. Apply Django permissions or a clearly defined role/permission service to HTML views, DRF ViewSets, and service-layer operations.
3. Use DRF `permission_classes` and object-level permission checks, not only global `IsAuthenticated`.
4. Ensure sensitive services cannot be called through an alternate view or task without authorization.
5. Protect user administration, backups, licensing, payroll, financial posting, refunds, and inventory adjustments with explicit permissions.
6. Add positive and negative tests for every role and sensitive action.
7. Audit permission changes and privileged actions.

---

## C-04 — Backup downloads can disclose the entire multi-tenant database

**Severity:** Critical  
**Status:** Confirmed by the attached static audit.

The attached report describes `BackupService` copying the entire SQLite database file, which contains records for all tenants. `BackupSelector.has_backup_access` in `apps/backups/selectors.py` reportedly grants access to any member of `backup.organization` without a role check. The download path is `backup_download_view` in `apps/backups/views.py`.

### Related defects identified

- `apps/backups/services.py:171`: a path check uses `startswith(os.path.abspath(backup_dir))`. Without a path-separator-aware containment check, a sibling path such as `backups_evil` may pass a prefix test.
- `restore_backup` overwrites the live SQLite file using `shutil.move` while connections may be open.
- Restore behavior is SQLite-specific.
- In an exception path, `backup` may be referenced before assignment if lookup fails.
- Download reads the whole backup into memory using `HttpResponse(f.read())`.

### Impact

An ordinary organization member may be able to download a raw database containing other organizations' data. This is a severe confidentiality failure. Unsafe restore can also cause corruption, downtime, or restoration of an unintended database.

### Remediation

1. Restrict backup creation, download, deletion, and restore to explicitly authorized administrators/superusers.
2. Do not distribute a raw multi-tenant database file to one tenant.
3. Prefer per-organization exports with explicit data ownership and export authorization.
4. Use `os.path.commonpath` or safe path-resolution checks, with strict storage-root validation.
5. Keep backup storage outside the public web root and use private storage permissions.
6. Stream downloads with `FileResponse` rather than reading entire files into memory.
7. Perform restore through a controlled offline/maintenance procedure with verified backups and database-specific tooling.
8. Initialize variables safely and handle missing backup records without leaking internal exceptions.
9. Add tests proving one tenant cannot download, delete, or restore another tenant's backup or a global database dump.

---

## C-05 — License verification is forgeable

**Severity:** Critical  
**Status:** Confirmed by the attached static audit.

The attached report identifies `apps/licensing/services.py:79` as generating a signature using:

`sha256(f"{license_id}:{customer_name}")`

The source reportedly labels this a simplified demo implementation. `LICENSE_PUBLIC_KEY_PATH` is configured but not read by the verification code.

### Impact

A user who knows or can guess the license ID and customer name can reproduce the hash. This is not a secure signature because there is no secret private key required to generate a valid license. License authenticity and entitlement enforcement can therefore be bypassed.

The attached report also notes that `verify_license` returns `str(e)` to the caller, potentially disclosing internal exception details.

### Remediation

1. Sign license payloads using a private key held only by the issuing authority.
2. Verify signatures using the configured public key (for example, Ed25519 or RSA using the existing `cryptography` dependency).
3. Include relevant claims in the signed payload: license ID, customer/organization, product, entitlements, issue time, expiry, and optional machine/installation binding.
4. Define key rotation and revocation procedures.
5. Return generic verification errors to clients; log sanitized diagnostics server-side.
6. Test invalid signatures, modified claims, expired licenses, wrong customer bindings, and key rotation.

---

# 5. High-severity findings

## H-01 — First-run login route resolves to Django's default login view and missing template

**Severity:** High  
**Status:** Confirmed by the attached static audit.

The attached report identifies `config/urls.py` including `django.contrib.auth.urls` at `/accounts/`. This provides an un-namespaced `login` route that expects `registration/login.html`. The project's own login view is namespaced as `accounts:login`. `LOGIN_URL = 'login'` reportedly resolves to Django's default view rather than the project login view.

The same issue applies to Django's default password-reset views, which expect templates such as `registration/password_reset_form.html`.

### Impact

The first login/redirect flow can fail with `TemplateDoesNotExist: registration/login.html`, preventing usable first-run access. Password-reset routes may fail similarly.

### Remediation

- Remove the default `django.contrib.auth.urls` include if the project intends to use its own account URLs, or explicitly provide and namespace the expected templates/routes.
- Set `LOGIN_URL = 'accounts:login'`.
- Set `LOGOUT_REDIRECT_URL = 'accounts:login'`.
- Update references identified by the attached report: `redirect('login')` in `apps/accounts/views.py` and `apps/organizations/views.py`, plus `{% url 'logout' %}` in `templates/components/topnav.html`.
- Add login, logout, and password-reset route-resolution tests.

## H-02 — Tenant context is not reliably set for authenticated API requests

**Severity:** High, with critical security implications  
**Status:** Framework-behavior finding requiring runtime proof.

Both reports identify the authentication order in `config/settings/base.py`:

1. `JWTAuthentication`
2. `SessionAuthentication`
3. `TenantContextAuthentication`

DRF stops at the first authenticator that successfully authenticates a request. Therefore, when JWT or session authentication succeeds, the later tenant-context authenticator is not called. The HTML organization/branch middleware skips `/api/` paths, so it does not fill the missing context.

### Impact

Tenant-scoped API endpoints may receive no `request.organization` or `request.branch` and return 403 errors. Meanwhile, unscoped endpoints may remain accessible, creating a dangerous split: properly scoped endpoints fail while unscoped endpoints continue to expose data.

### Remediation

- Resolve tenant context in a DRF hook that runs after successful authentication, such as a carefully designed `initial()`/permission/base-view mechanism.
- Alternatively, use a custom authenticator that delegates to the intended JWT/session authentication and reliably sets tenant context before returning the authenticated tuple.
- Do not depend on a later authenticator running after an earlier one succeeds.
- Test both JWT and session requests, with valid and invalid organization/branch membership.

## H-03 — Anonymous API authentication may recurse infinitely

**Severity:** High  
**Status:** Runtime hypothesis in the attached report; reproduce before classifying as confirmed.

The attached report states that `TenantContextAuthentication.authenticate()` reads `request.user`. In DRF, accessing this property can itself trigger authentication. For an anonymous request where `_user` is not yet set, this may recursively call `_authenticate()` and end in `RecursionError` rather than a normal 401 response.

### Remediation

- Avoid reading `request.user` from inside an authenticator that is participating in setting that user.
- Resolve tenant context after authentication in a permission/base-view hook.
- Add an anonymous API request test asserting a controlled 401/403 response and no server error.

## H-04 — Undefined names cause runtime `NameError` failures

**Severity:** High  
**Status:** Confirmed by the attached report's source/script review.

The attached report lists these application-code defects:

| Location | Missing name | Reported effect |
|---|---|---|
| `apps/backups/views.py:50,53,72,83,97,104` | `messages` | Backup create/download/delete views can crash |
| `apps/crm/services.py:265-266` | `models` (`models.Q`) | Customer follow-up query can crash |
| `apps/repair/services.py:264-267` | `models` (`models.Q`) | Device repair-order query can crash |
| `apps/pos/services.py:303` | `uuid` | POS session opening can crash |
| `apps/pos/selectors.py:78` | `PaymentMethod` | Payment-method listing can crash |

### Remediation

Add the correct imports, then add tests that execute each affected code path. A syntax compilation pass does not detect all undefined runtime names.

## H-05 — 39 URL names do not resolve

**Severity:** High  
**Status:** Confirmed by the attached report's scripted check.

The attached report checked 361 URL-name references and found 39 unresolved references.

Examples include:

- `templates/backups/list.html`: `backups:detail`, `backups:download`, `backups:delete`.
- `apps/backups/views.py`: five redirects to `backups:list`.
- `apps/branches/views.py`: references to `branches:list` and `branches:detail`.
- `apps/organizations/views.py`: references to `organizations:list` and `organizations:detail`.
- Inventory: `*_confirm_delete`, `unitofmeasure_detail`, and `warehouse_form`.
- Suppliers: several `*_confirm_delete` references.
- POS: `pos:sale_delete`.
- Accounts/profile: `organizations:switch`, `accounts:user_detail`, `profile`, and `settings`.

### Impact

Affected pages or actions may raise `NoReverseMatch`, interrupting navigation or workflow execution.

### Remediation

- Reconcile each URL reference with the actual app namespace and registered route name.
- Do not blindly rename routes: update callers and templates consistently.
- Add a test that resolves all named routes and renders key templates.

## H-06 — 35 referenced templates do not exist

**Severity:** High  
**Status:** Confirmed by the static template-reference check in both reports.

The first report and attached report independently identify 35 unresolved template references. The attached report says 158 literal references were checked against 172 templates and 64 templates were not referenced.

Examples include:

- Branch pages: `branches/list.html`, `branches/detail.html`, `branches/edit.html`, `branches/delete.html`.
- Organization pages: `organizations/list.html`, `organizations/create.html`, `organizations/detail.html`, `organizations/edit.html`, `organizations/delete.html`.
- Repair order templates, including naming differences such as `repair/repairorder_list.html` versus `repair/repair_order_list.html`.
- Reports: sales, repairs, inventory, and financial pages.
- Zakat calculator/history.
- CRM device brand/model pages.
- Barcode print page.
- Inventory detail/form pages.
- Licensing view.
- Documents list.

### Impact

Affected views can fail with `TemplateDoesNotExist`. Duplicate and orphaned templates make it harder to know which page is canonical.

### Remediation

- Map each view to the intended existing template.
- Create missing templates only where the page is genuinely required.
- Remove or archive obsolete duplicates after confirming they are unused.
- Add template-loader and page-render smoke tests for all registered HTML views.

## H-07 — Production settings are not the default entrypoint configuration

**Severity:** High  
**Status:** Confirmed by both reports' settings review.

The attached report states that `manage.py`, `config/wsgi.py`, and `config/asgi.py` default to `config.settings.base`. The base settings use SQLite and a hard-coded fallback `SECRET_KEY` when `DJANGO_SECRET_KEY` is absent. The same key is also used for JWT signing in the base settings.

The production settings reportedly set `DEBUG=False`, secure cookies, HSTS/SSL redirect, and require explicit secrets/database credentials. However, the entrypoints do not select production settings by default. The attached report also notes that `.env.example` is not loaded, despite `python-dotenv` being installed.

### Impact

A deployment that fails to set `DJANGO_SETTINGS_MODULE` correctly may run with a known fallback signing key, SQLite, and without production HTTPS protections.

### Remediation

- Explicitly set `DJANGO_SETTINGS_MODULE=config.settings.production` in production process configuration.
- Use development settings only in development.
- Fail startup when `DEBUG=False` and a strong secret is missing or a known fallback is used.
- Do not rely on an undocumented environment variable to select production settings.
- Load environment configuration through the deployment platform or a deliberate `.env` loading strategy.
- Add a deployment test asserting the active settings module, database engine, secret presence, and security flags.

## H-08 — Open account registration has no reported approval or abuse controls

**Severity:** High  
**Status:** Confirmed by the attached report's source review; deployment exposure should be checked.

The attached report identifies `/accounts/register/` as creating accounts without approval, rate limiting, or CAPTCHA.

### Impact

Public registration may allow automated account creation. Combined with missing RBAC and tenant isolation defects, new accounts may become a route to unauthorized application access.

### Remediation

- Decide whether registration should be public, invitation-only, or administrator-approved.
- Require verified email/phone or an invitation token as appropriate.
- Add IP/account rate limits and abuse monitoring.
- Ensure newly registered accounts receive only the minimum role and no privileged tenant membership by default.
- Test that registration cannot grant organization ownership or administrative permissions.

## H-09 — Login `next` parameter is an open redirect

**Severity:** High  
**Status:** Confirmed by both reports' source review.

`apps/accounts/views.py` reads `request.GET.get('next', 'dashboard')` and passes it to `redirect()` without validating that the destination is a trusted local URL.

### Impact

A crafted login link may send a user to an attacker-controlled external destination after authentication, enabling phishing and trust abuse.

### Remediation

Use Django's `url_has_allowed_host_and_scheme()` with the current host and HTTPS requirement. Fall back to a fixed internal dashboard when validation fails. Test absolute external URLs, protocol-relative URLs, backslashes, and malformed paths.

## H-10 — Organization, branch, and backup HTML views contain unscoped object lookups

**Severity:** High  
**Status:** Unscoped lookup confirmed; complete downstream authorization behavior was not verified for every view.

The attached report identifies:

- `get_object_or_404(Organization, pk=pk)` in `apps/organizations/views.py`.
- `get_object_or_404(Branch, pk=pk)` in `apps/branches/views.py`.
- `get_object_or_404(Backup, pk=pk)` in `apps/backups/views.py`.

The report notes that later authorization checks were not verified for every view.

### Impact

If a later check is absent or incomplete, a user may view, edit, or delete another organization's or branch's records by changing an object ID. This is a classic insecure direct object reference (IDOR) pattern.

### Remediation

- Query objects through the current user's authorized organization/branch scope.
- Apply object-level permissions before rendering or mutating.
- Test cross-tenant IDs on detail, edit, delete, download, and restore views.
- Return a consistent 404 or 403 without leaking object existence where appropriate.

## H-11 — Stock updates and document-number generation may be race-prone

**Severity:** High for inventory/financial integrity; verify each workflow.

The attached report states that no `select_for_update()` or `F()` expression was found in the source scan. The first report independently found no `select_for_update()` matches, while identifying `transaction.atomic()` in several services.

### Impact

Atomic transactions do not automatically prevent lost updates when two requests read the same value and then write a new value. Concurrent stock adjustments, POS sales, refunds, payment posting, or invoice generation may produce incorrect balances, duplicate numbers, or inconsistent state.

The attached report also says `count()+1`-style document-number generation should be checked, but that check was not completed.

### Remediation

- Review inventory, POS, payment, invoice, purchase-order, repair, and cash-session workflows.
- Use `select_for_update()` for critical read-modify-write rows inside atomic transactions where supported.
- Use `F()` expressions or conditional database updates for simple arithmetic.
- Add unique database constraints for document numbers and business invariants.
- Use idempotency keys for payment/posting operations.
- Add concurrent-request tests against PostgreSQL.

## H-12 — Writable DRF serializer fields with dotted `source` may fail nested writes

**Severity:** High  
**Status:** Runtime hypothesis in the attached report.

The attached report identifies writable fields such as `serializers.UUIDField(source='customer_type.uuid', write_only=True)`. DRF's default create/update behavior does not support arbitrary writable nested relationships without custom handling and may raise an assertion.

### Impact

API create/update operations using those serializers may fail at runtime even if the serializer validates the input.

### Remediation

- Replace dotted writable `source` fields with explicit relationship fields (`PrimaryKeyRelatedField`, slug/UUID related fields, or custom fields).
- Validate the related object against the current tenant.
- Implement explicit `create()`/`update()` only when necessary.
- Add API tests for valid, invalid, foreign-tenant, create, and update cases.

## H-13 — Important application modules lack tests; existing tests may themselves fail

**Severity:** High  
**Status:** Test-coverage observations confirmed by the attached report; actual test outcomes not executed.

The attached report says no tests exist for:

- `accounts`
- `organizations`
- `branches`
- `backups`
- `licensing`
- `documents`
- `settings`
- `zakat`
- `barcode`
- `notifications`
- `reports`
- `dashboard`
- `audit_logs`

It describes approximately 180 tests elsewhere, but says they do not cover tenant isolation or permissions. It also identifies test files referencing names that are not imported, including `Organization`, `Branch`, `OrganizationMembership`, and `BranchUserAccess` in financial/accounting tests.

### Impact

Critical security regressions can pass CI unnoticed. Tests with undefined names may fail before reaching the behavior they are meant to verify.

### Remediation

- Add tenant-isolation and RBAC test suites before feature-specific tests.
- Repair test imports and ensure every test is actually collected and executed.
- Add service, API, HTML, and permission tests for critical workflows.
- Run the complete suite from a clean dependency installation against PostgreSQL.

## H-14 — `qrcode` dependency is missing from requirements

**Severity:** High functional/deployment risk  
**Status:** Confirmed by the attached dependency comparison.

`apps/barcode/services.py:6` reportedly imports `qrcode`, but `qrcode` is absent from `requirements.txt`.

### Impact

Importing the barcode service on a clean install may fail with `ModuleNotFoundError`.

### Remediation

Add the correct package and any required extras to the dependency manifest, pin a compatible version, and test a clean installation.

## H-15 — Password-reset confirmation is a placeholder

**Severity:** High  
**Status:** Confirmed by the first report's source review.

`apps/accounts/views.py` contains `password_reset_confirm_view()` as a placeholder that renders a template rather than validating a reset token and setting a new password.

The attached report separately identifies the default Django password-reset routes as pointing to missing `registration/...` templates. These are related but distinct defects: the project's own confirmation flow is incomplete, and the default auth URL flow may also resolve to missing templates.

### Impact

Users may be unable to complete account recovery, and the UI may imply that a recovery flow exists when it does not.

### Remediation

- Use Django's built-in password-reset views or a fully tested equivalent.
- Validate token, user, expiry, and one-time use.
- Apply configured password validators.
- Do not disclose whether an email address is registered.
- Test valid, expired, malformed, reused, and user-mismatched tokens.

## H-16 — Password-change URL is wired to the password-reset request view

**Severity:** High  
**Status:** Confirmed by the first report's source review.

`apps/accounts/urls_frontend.py` reportedly routes `account/password/change/` to `password_reset_view`, rather than an authenticated password-change view.

### Impact

The password-change route does not provide the expected authenticated change-password behavior.

### Remediation

- Implement a dedicated authenticated password-change form/view.
- Require the current password.
- Apply password validators.
- Call `update_session_auth_hash()` after successful change to preserve the current session safely.
- Add tests for wrong current password, weak new password, and successful change.

## H-17 — Branch middleware does not enforce `can_access=True`

**Severity:** High  
**Status:** Confirmed by the first report's comparison of middleware and API checks; runtime authorization should be tested.

`apps/core/middleware.py` reportedly queries `BranchUserAccess` using user, branch, and `is_active=True`, but does not require `can_access=True`. The API tenant-context code includes `can_access=True`.

### Impact

A branch assignment that remains active but explicitly denies access may still be accepted by browser middleware. This creates inconsistent authorization between browser and API paths.

### Remediation

- Require `can_access=True` consistently.
- Centralize branch-membership authorization to avoid divergent rules.
- Test active/denied, inactive/allowed, revoked, and valid branch assignments through both HTML and API paths.

## H-18 — Tenant-scoping helper may silently skip models without direct organization/branch fields

**Severity:** High  
**Status:** Confirmed by the first report's source review.

`apps/core/api_mixins.py` helper methods such as `filter_by_organization()`, `filter_by_branch()`, `validate_organization()`, and `validate_branch()` reportedly skip filtering/validation when the model does not expose the expected direct field.

### Impact

A developer may assume that inheriting `TenantScopedMixin` guarantees tenant isolation even when the model is owned indirectly through a parent relation. This is particularly relevant to invoice lines, repair parts, attachments, and other child records.

### Remediation

- Require every tenant-scoped ViewSet to declare its ownership path.
- Support explicit relation paths such as `invoice__organization` or `repair_order__branch`.
- Fail closed when a tenant-scoped resource has no declared tenant ownership path.
- Add a system check or test that flags tenant-owned ViewSets without an explicit scope definition.

## H-19 — MFA secrets and backup codes are stored in ordinary model fields

**Severity:** High  
**Status:** Confirmed model-design observation from the first report; full MFA flow not validated.

`apps/accounts/models.py` reportedly stores `User.mfa_secret` as a `CharField` and `User.mfa_backup_codes` as a `TextField`. The model declaration does not show encryption at rest or one-way hashing for backup codes.

### Impact

A database read, backup disclosure, or overly broad admin/API exposure could reveal TOTP seed material and reusable recovery codes.

### Remediation

- Encrypt TOTP secrets using an application-managed encryption key or KMS.
- Store backup codes as salted password hashes.
- Invalidate each backup code after successful use.
- Ensure MFA fields are excluded from serializers, admin forms, logs, and exports.
- Add key rotation, recovery, and replay-prevention tests.

## H-20 — Logout is a GET-capable state-changing action

**Severity:** High  
**Status:** Confirmed by the first report's source review.

`apps/accounts/views.py` reportedly calls `logout(request)` without restricting the method, and the frontend URL exposes the view as a normal route.

### Impact

A cross-site link or embedded resource may trigger logout without an intentional user POST. This is generally lower impact than unauthorized financial changes, but violates safe HTTP method semantics and can disrupt user workflows.

### Remediation

- Require POST for logout.
- Use a CSRF-protected form.
- Ensure navigation does not trigger logout through a GET link.
- Test that GET does not terminate the session.

---

# 6. Medium-severity findings

## M-01 — Uploads lack consistently applied extension, size, and content validation

**Severity:** Medium / High depending on exposure  
**Status:** The attached report says configured validation settings are not applied; first report called for endpoint-by-endpoint verification.

The attached report identifies approximately 20 `FileField`/`ImageField` fields across CRM, HR, financial, repair, suppliers, documents, accounts, organizations, and inventory. It says `ALLOWED_FILE_EXTENSIONS` and `MAX_FILE_UPLOAD_SIZE` are defined but never applied.

The first report notes that a 10 MB limit and extension allowlist in settings do not prove that every serializer/form/storage path enforces them.

### Impact

Uploads may accept oversized or unexpected files, trust client-supplied MIME types/extensions, or expose files across tenant boundaries if download authorization is missing.

### Remediation

- Enforce size limits in every upload path or a shared validation layer.
- Validate actual file signatures/content, not only file extensions or browser MIME type.
- Generate opaque storage names and prevent path traversal.
- Store files outside the executable web root or in private object storage.
- Authorize every download against the owning tenant and user permission.
- Use short-lived signed URLs where appropriate.
- Scan risky document types where operationally appropriate.

## M-02 — Exception details are returned or logged to clients

**Severity:** Medium  
**Status:** Confirmed by the attached report's scan.

The attached report identifies `str(e)` being returned or logged to clients in approximately 12 places, including licensing services.

### Impact

Exception messages may reveal database details, file paths, internal implementation, or other information useful to an attacker.

### Remediation

Return generic client-facing errors with stable error codes. Log sanitized diagnostic information server-side with correlation IDs. Do not return stack traces or raw exception text in production.

## M-03 — Silent exception handling hides failures

**Severity:** Medium  
**Status:** Confirmed by the attached report's scan.

Approximately 10 `except ...: pass` blocks are identified, including `apps/reports/selectors.py:144-321` and `apps/licensing/selectors.py:30`.

### Impact

Reports may be incomplete or incorrect without any visible failure. Silent exception handling also makes security and data-integrity incidents difficult to detect.

### Remediation

Catch only expected exceptions, log them with context, expose an appropriate failure state, and add tests for failed data retrieval.

## M-04 — Inventory service may create tenant-less products when context is missing

**Severity:** Medium / High  
**Status:** Confirmed source observation in the attached report.

`apps/inventory/services.py:70-73` reportedly sets organization/branch only “if available”, allowing a product to be created without tenant context.

### Impact

Tenant-less inventory records may become invisible, globally visible, or inconsistent with tenant ownership assumptions.

### Remediation

Require organization and branch context for tenant-owned inventory writes. Fail closed if context is absent. Add service-level tests for missing, invalid, and unauthorized tenant context.

## M-05 — Incorrect or obsolete security header settings

**Severity:** Medium  
**Status:** Confirmed settings observations in the attached report.

The attached report notes:

- `SECURE_BROWSER_XSS_FILTER` is removed/has no effect in modern Django.
- `REFERRER_POLICY` is not the Django setting; `SECURE_REFERRER_POLICY` is the relevant setting.

### Impact

The intended browser security policy may not be applied. The obsolete XSS filter setting should not be treated as a substitute for output encoding and CSP.

### Remediation

Use supported Django security settings and validate actual response headers in staging. Consider a carefully tested Content Security Policy. Continue relying on context-aware escaping and safe DOM APIs for XSS defense.

## M-06 — Production reverse-proxy SSL configuration may be incomplete

**Severity:** Medium  
**Status:** Confirmed configuration observation; impact depends on deployment topology.

The attached report says `config/settings/production.py` lacks `SECURE_PROXY_SSL_HEADER`. If TLS terminates at a trusted reverse proxy and Django does not recognize the forwarded HTTPS scheme, `SECURE_SSL_REDIRECT=True` may cause redirect loops.

### Remediation

Configure `SECURE_PROXY_SSL_HEADER` only when the proxy is trusted and strips/sets the header safely. Configure proxy behavior and test HTTPS redirects end-to-end.

## M-07 — Development CORS settings are unsafe if deployed

**Severity:** Medium  
**Status:** Confirmed by the attached report.

`config/settings/development.py` reportedly sets `CORS_ALLOW_ALL_ORIGINS=True` with `CORS_ALLOW_CREDENTIALS=True`.

### Impact

This may be acceptable for isolated local development, but is dangerous if the development settings are accidentally deployed or exposed.

### Remediation

Keep permissive CORS strictly local. Use an explicit production origin allowlist and test credentialed cross-origin behavior.

## M-08 — Settings module performs filesystem operations at import time

**Severity:** Medium  
**Status:** Confirmed by the attached report.

`config/settings/base.py` reportedly creates `logs/` and `license/` directories and opens a `FileHandler` during settings import.

### Impact

Startup may fail in read-only containers, restricted environments, or CI. Import-time side effects also make tests and management commands harder to isolate.

### Remediation

Move filesystem setup into deployment/entrypoint or logging initialization, ensure directories are writable where required, and avoid requiring writable application code directories.

## M-09 — Dead or duplicated settings and unused flags

**Severity:** Medium  
**Status:** Confirmed by the attached report.

The report notes a duplicate `os` import and `LICENSE_VERIFICATION_ENABLED = True` that is not read by the code.

### Impact

Dead configuration creates false expectations and makes security controls difficult to reason about.

### Remediation

Remove unused settings or wire them to explicit, tested behavior. Avoid configuration flags that imply a control is active when no code consumes them.

## M-10 — Dependencies are unpinned and development packages are mixed with production

**Severity:** Medium  
**Status:** Confirmed by the attached report.

`requirements.txt` reportedly uses lower bounds (`>=`), mixes development tools (pytest, black, flake8, factory-boy) with production packages, and mentions `django-db-geventpool` in a comment without declaring it as a dependency.

### Impact

Unpinned dependencies can change between builds, introduce incompatibilities, and complicate vulnerability management. Mixing development tools increases production image size and attack surface.

### Remediation

- Pin production dependencies with a lock/constraints strategy.
- Split runtime and development/test requirements.
- Use automated dependency vulnerability scanning.
- Generate and retain an SBOM for releases.
- Rebuild from a clean environment in CI.

## M-11 — SQLite is the base/default database and production file-based cache is reported

**Severity:** Medium / High for concurrent ERP workloads  
**Status:** Configuration observation; actual deployment selection must be checked.

The base settings use SQLite, and the attached report says production uses a file-based cache. The first report notes that production settings configure PostgreSQL but are not the default entrypoint settings.

### Impact

An accidental base-settings deployment may use SQLite, which is unsuitable for many concurrent ERP/POS workloads. File-based cache behavior may also be inappropriate for horizontally scaled deployments.

### Remediation

Require PostgreSQL in production startup validation. Use a production cache such as Redis where shared cache semantics are needed. Test concurrency and deployment behavior using the actual production services.

## M-12 — Serializers using `fields = '__all__'` may expose sensitive model fields

**Severity:** Medium / High  
**Status:** Confirmed serializer pattern in the attached report; exposure depends on endpoint and field contents.

The attached report identifies 87 serializers across 8 modules using `fields = '__all__'`, including 18 HR serializer classes. It specifically warns about possible exposure of HR/payroll data to authenticated users.

### Impact

Future model fields may automatically become API-readable or writable without an explicit security review. Sensitive fields may be exposed, and writable fields may enable privilege or tenant reassignment.

### Remediation

Use explicit serializer field allowlists. Mark sensitive fields read-only or exclude them entirely. Separate employee self-service serializers from HR/admin serializers. Add tests that assert sensitive fields are absent for unauthorized roles.

## M-13 — Audit-log integrity and administrative visibility were not verified

**Severity:** Medium  
**Status:** Not verified by the attached report.

The attached report notes `AUDIT_LOG_EXCLUDE_MODELS = ['Session','ContentType']`, but did not verify whether audit entries can be modified or deleted through views or APIs. It also did not review admin registrations for cross-tenant visibility.

### Impact

If users can alter or delete audit records, incident investigation and accountability can be undermined. Admin pages may also expose cross-tenant data if not scoped.

### Remediation

- Review all audit-log views, APIs, admin registrations, and deletion paths.
- Make audit records append-only for ordinary application roles.
- Restrict access to audit logs and record access to them.
- Verify tenant scoping in Django admin and custom admin interfaces.
- Consider tamper-evident storage for high-value audit events.

## M-14 — Middleware order may not follow Django's recommended locale ordering

**Severity:** Medium  
**Status:** Configuration observation from the first report.

The first report notes `LocaleMiddleware` after `CommonMiddleware`; Django's recommended order places it after `SessionMiddleware` and before `CommonMiddleware`.

### Impact

Language negotiation and localized URL behavior may be inconsistent, especially around redirects and middleware-generated responses.

### Remediation

Align middleware order with the supported Django guidance and add locale-prefixed/unprefixed URL tests.

## M-15 — Global reference-data ViewSets may be writable by every authenticated user

**Severity:** Medium / High depending on data criticality  
**Status:** Confirmed pattern in the attached report; endpoint permissions require runtime validation.

The attached report lists global reference-data ViewSets among the unscoped endpoints. Some may be intentionally global, but the use of `ModelViewSet` can expose create/update/delete operations if no further permission restrictions exist.

### Impact

An ordinary user may alter shared payment methods, statuses, categories, account types, units, or other lookup data.

### Remediation

Use read-only ViewSets for shared immutable reference data. Restrict global changes to authorized administrators. If values should differ by tenant, model them as tenant-owned records and scope them accordingly.

---

# 7. Low-severity findings and maintainability issues

## L-01 — Stray literal directory under `apps/`

The attached report identifies a literal directory named:

`apps/{core,accounts,organizations,licensing,branches,audit_logs,settings,dashboard,notifications,backups,reports,documents,barcode,zakat}/`

It reportedly contains a stray `signals.py` and `__pycache__`. The report attributes this to a failed shell brace expansion.

**Remediation:** Inspect the directory, confirm no required source is present, then remove it from the repository/archive.

## L-02 — Compiled Python files included in the archive

The attached report identifies 337 `.pyc` files and `__pycache__` directories in the archive.

**Impact:** Unnecessary repository/archive noise, possible stale bytecode confusion, and larger artifacts.

**Remediation:** Build release archives from a clean checkout and exclude `__pycache__` and `.pyc` files.

## L-03 — Python `__init__.py` files inside template directories

The attached report identifies `templates/components/__init__.py` and `templates/dashboard/__init__.py`.

**Remediation:** Remove these if they are accidental; Django templates do not need Python package initializers.

## L-04 — Orphaned and duplicated templates

The attached report says 64 of 172 templates are not referenced and identifies duplicate families such as:

- `inventory/brand_*` versus `productbrand_*`
- `unit_*` versus `unitofmeasure_*`
- `stock_adjustment*` versus `stockadjustment_*`
- `backups/list.html` versus `backup_list.html`

**Remediation:** Establish canonical template names, update references, and remove duplicates only after confirming they are unused.

## L-05 — Translation `.mo` files are not compiled

The attached report says locale `.po` files exist but compiled `.mo` files do not, so French/Arabic/English translations may not load until `compilemessages` is run.

**Remediation:** Compile translations in the build pipeline and verify locale behavior in staging.

## L-06 — Project documentation is outdated

The attached report identifies `IMPLEMENTATION_PROGRESS.md`, `IMPLEMENTATION_SUMMARY.md`, and `FIXFLOW_DEEP_CODE_AUDIT.md` as outdated and contradictory to the code.

**Remediation:** Update documentation after fixes and make CI or release checklists verify that documented dependencies, settings, routes, and features match the implementation.

## L-07 — Product naming is inconsistent

The attached report notes `FixSoftRepair Pro` in settings/environment references and `FixFlow` in the repository.

**Remediation:** Choose a canonical product name and align user-facing branding, environment variables, documentation, package metadata, and deployment resources.

## L-08 — README and `.env.example` document settings not consumed by code

The attached report says the documentation lists `CACHE_BACKEND`, `LOG_LEVEL`, and `JWT_*` settings that the settings modules do not read.

**Remediation:** Remove stale variables or implement them. Add a settings validation test to detect documented-but-unused configuration.

---

# 8. Positive findings

The two source reports also identify positive engineering practices worth preserving:

- The project has a meaningful separation between models, selectors, services, HTML views, and API serializers/views.
- HTML class-based views reportedly use `LoginRequiredMixin` and organization/branch context mixins that validate membership and fail closed.
- The global DRF permission default is `IsAuthenticated`, which is preferable to anonymous access as a baseline, although it is insufficient for tenant and role authorization.
- No `csrf_exempt` usage was found in the attached report's scan.
- No `eval`, `exec`, `subprocess`, or raw SQL patterns were found in that scan.
- No unsafe `|safe` template usage was found in the attached report's scan.
- The toast implementation in `static/js/main.js` uses `textContent`, avoiding HTML interpolation in that rendering path.
- Destructive HTML actions reportedly use POST.
- `transaction.atomic()` is used in several service-layer workflows.
- Production settings explicitly configure `DEBUG=False`, secure cookies, HSTS/SSL redirect, and required secrets/database credentials when those settings are actually selected.
- JWT configuration reportedly uses refresh-token rotation and blacklisting.
- Password validators are enabled.
- Python source compilation completed without syntax errors in the first report's check.

These positives do not cancel the critical findings. In particular, login authentication, tenant isolation, object authorization, and role authorization are separate controls.

---

# 9. Consolidated remediation roadmap

The order below is designed to reduce the highest risks first while making the application testable. Fixes should be performed in small, reviewable changes with regression tests.

## Phase 0 — Establish a reproducible build and make core routes work

**Goal:** Make the exact release candidate install, start, and expose its intended routes.

1. Confirm the exact source archive/release commit to be fixed.
2. Fix the login route conflict and `LOGIN_URL`.
3. Fix missing imports and undefined names in backup, CRM, repair, and POS code.
4. Resolve all 39 URL-name references.
5. Resolve all 35 missing template references.
6. Add the missing `qrcode` dependency.
7. Remove generated `.pyc`/`__pycache__` and stray directories from release artifacts.
8. Run a clean dependency installation and Django system checks.

**Exit criteria:** A clean environment can install dependencies, load settings, run checks, migrate, and render the login and core pages without import, URL, or template errors.

## Phase 1 — Close cross-tenant data leaks

**Goal:** Prove that a user cannot access or mutate another organization's or branch's data.

1. Repair API tenant-context resolution.
2. Remove the recursion-prone authenticator behavior.
3. Inventory every registered ViewSet and classify ownership.
4. Scope all tenant-owned ViewSets, including child/attachment endpoints.
5. Make `organization` and `branch` server-controlled/read-only.
6. Validate all tenant-owned foreign keys and parent IDs.
7. Make global reference data read-only or admin-only.
8. Fail closed when a scoped model has no declared tenant relationship.
9. Fix organization/branch/backup HTML object lookups.
10. Enforce `can_access=True` consistently.

**Exit criteria:** Cross-tenant tests pass for list, retrieve, create, update, partial update, delete, nested objects, file downloads, and branch switching under both JWT and session authentication.

## Phase 2 — Enforce roles and protect privileged capabilities

**Goal:** Ensure users can perform only actions permitted by their roles.

1. Define a resource/action permission matrix.
2. Enforce permissions in HTML views, DRF ViewSets, and sensitive service entrypoints.
3. Protect user management, backups, licensing, payroll, accounting, financial posting, refunds, inventory adjustments, and organization administration.
4. Restrict public registration or add approval/invitation controls.
5. Add rate limits and abuse monitoring for registration, login, and password reset.
6. Protect MFA secrets and hash backup codes.
7. Implement password reset and authenticated password change.
8. Make logout POST-only.
9. Validate login redirects.

**Exit criteria:** Tests prove that each role is allowed and denied the correct operations, including direct API calls that bypass the UI.

## Phase 3 — Repair backup and license trust boundaries

**Goal:** Protect data confidentiality and licensing integrity.

1. Replace raw whole-database tenant backup downloads with authorized per-organization exports or a tightly restricted infrastructure backup process.
2. Restrict backup/restore to privileged operators.
3. Correct path validation and stream large downloads.
4. Make restore an offline/maintenance operation with verified recovery procedures.
5. Replace forgeable license hashes with asymmetric digital signatures.
6. Use the configured public key for verification.
7. Remove raw exception details from license responses.

**Exit criteria:** A tenant cannot obtain another tenant's data through backups, and modified or forged license payloads fail verification.

## Phase 4 — Protect uploads and improve operational security

**Goal:** Close file, configuration, and information-disclosure weaknesses.

1. Validate upload size, file signatures, extensions, and ownership.
2. Store private files outside the public web root.
3. Authorize every download.
4. Replace `fields='__all__'` serializers with explicit field allowlists.
5. Remove `str(e)` responses and silent exception swallowing.
6. Correct security headers and proxy SSL configuration.
7. Restrict CORS in production.
8. Remove settings import-time filesystem side effects.
9. Validate production settings, PostgreSQL, cache, and secrets at startup.
10. Pin dependencies and scan them in CI.

**Exit criteria:** Upload/download tests, production header checks, clean deployment checks, and dependency scans pass.

## Phase 5 — Verify financial and inventory correctness

**Goal:** Protect balances, quantities, and business invariants under concurrency.

The attached report explicitly states that detailed business-logic review of inventory, POS, financial, accounting, CRM, repair, and HR was incomplete. This phase must therefore include a fresh domain review, not just implementation of the concurrency suggestions.

1. Review stock movements and adjustment rules.
2. Review POS sale/refund/payment state transitions.
3. Review invoice and purchase-order numbering.
4. Review journal balancing and accounting posting rules.
5. Review payroll calculations and access boundaries.
6. Review repair workflow transitions and part consumption.
7. Use row locks, conditional updates, uniqueness constraints, and idempotency where appropriate.
8. Test concurrent transactions against PostgreSQL.
9. Verify Decimal precision, rounding, and currency rules.

**Exit criteria:** Domain invariants hold under normal, invalid, retried, and concurrent requests.

## Phase 6 — CI, monitoring, and release controls

1. Run the complete test suite from a clean checkout and clean dependency installation.
2. Run Django deployment checks with production settings.
3. Run migrations from an empty PostgreSQL database and test upgrade paths.
4. Add static analysis, secret scanning, dependency scanning, and SBOM generation.
5. Add API security regression tests to required CI checks.
6. Centralize logs and security events; alert on suspicious login, access-denied, backup, and privilege-change activity.
7. Verify backup encryption, restore drills, retention, and incident response.
8. Update README, `.env.example`, implementation summaries, and deployment documentation.

---

# 10. Production acceptance checklist

A release must not be marked production-ready until every applicable item below is demonstrated in CI or a controlled staging environment.

## Startup and deployment

- [ ] Clean dependency installation succeeds.
- [ ] `qrcode` and all runtime dependencies are declared.
- [ ] Production settings are selected explicitly by the deployment.
- [ ] Startup fails when production secrets are missing or weak.
- [ ] Production uses PostgreSQL, not the base SQLite configuration.
- [ ] Django deployment checks pass.
- [ ] Migrations apply successfully from an empty database.
- [ ] Login, logout, password reset, and core page routes resolve.
- [ ] All referenced templates resolve.

## Authentication and authorization

- [ ] JWT-authenticated API requests receive validated organization/branch context.
- [ ] Session-authenticated API requests receive validated organization/branch context.
- [ ] Anonymous API requests return controlled 401/403 responses, not recursion or 500 errors.
- [ ] Login redirects cannot target untrusted external hosts.
- [ ] Logout accepts POST only.
- [ ] Password reset validates token, expiry, and one-time use.
- [ ] Password change requires authentication and the current password.
- [ ] Registration cannot create privileged accounts or unauthorized tenant memberships.
- [ ] Role permissions are enforced in HTML, API, and service-layer operations.
- [ ] Active branch assignments with `can_access=False` are rejected.

## Tenant isolation

- [ ] Every tenant-owned ViewSet has an explicit ownership scope.
- [ ] Child resources are scoped through their parent.
- [ ] Organization and branch identifiers are server-controlled where required.
- [ ] All foreign-key and parent IDs are validated against the current tenant.
- [ ] A user cannot enumerate another tenant's customers, repairs, invoices, payments, stock, employees, or documents.
- [ ] Cross-tenant create, update, and delete attempts are rejected.
- [ ] Admin pages and exports respect tenant boundaries.

## Backup and licensing

- [ ] Ordinary organization members cannot download raw database backups.
- [ ] Tenant exports contain only authorized tenant data.
- [ ] Backup paths cannot escape the configured storage root.
- [ ] Restore is restricted and tested through an offline procedure.
- [ ] Forged or modified license signatures fail.
- [ ] License verification uses a trusted public key.
- [ ] License errors do not expose internal exception details.

## Files and data exposure

- [ ] Uploads enforce size, type/content, and ownership.
- [ ] Private files are not served directly from a public path.
- [ ] Downloads require authorization.
- [ ] Sensitive serializer fields are explicitly excluded or permission-controlled.
- [ ] MFA seeds are encrypted and backup codes are hashed.
- [ ] Exceptions do not expose internal details to clients.
- [ ] Audit logs cannot be modified or deleted by ordinary users.

## Business integrity and operations

- [ ] Stock updates are safe under concurrent requests.
- [ ] Payment and posting endpoints are idempotent where needed.
- [ ] Document numbers remain unique under concurrency.
- [ ] Financial journals balance and state transitions are validated.
- [ ] Payroll and HR information are role-restricted.
- [ ] Critical workflows pass tests against PostgreSQL.
- [ ] Backup restore drills, monitoring, and incident procedures are documented.

---

# 11. Final conclusion

The two audits converge on a serious architectural concern: **FixFlow currently cannot be trusted to enforce tenant boundaries and user privileges consistently across its API and business operations.**

The attached report contributes several critical findings missing from the first report: absent role-based authorization, whole-database backup exposure, and forgeable license verification. The first report contributes additional account, MFA, branch-access, and tenant-scoping-helper issues that should remain in the remediation backlog.

The most important engineering decision is to treat tenant isolation and authorization as shared infrastructure, not as optional behavior implemented independently in each view. Every API resource, child relationship, file, export, and service operation must have an explicit ownership and permission policy.

The project should proceed through the remediation phases in order. Do not use the number of passing unit tests, a successful server startup, or the presence of a `TenantScopedMixin` as proof of security. The decisive evidence is a comprehensive set of negative authorization tests demonstrating that users cannot cross organization/branch boundaries or exceed their role.

**Final audit disposition: FAIL — production deployment is not recommended until the critical findings are fixed, all high-risk authorization issues are tested, and the incomplete business-logic review is completed.**

---

## Appendix A — Finding index

| ID | Finding | Severity |
|---|---|---|
| C-01 | Unscoped tenant-owned API ViewSets | Critical |
| C-02 | Client-writable organization/branch fields | Critical |
| C-03 | No effective role-based authorization | Critical |
| C-04 | Whole-database backup exposure and unsafe restore | Critical |
| C-05 | Forgeable license verification | Critical |
| H-01 | Login route resolves to missing default template | High |
| H-02 | API tenant context not reliably set | High |
| H-03 | Possible anonymous authentication recursion | High |
| H-04 | Undefined names cause runtime failures | High |
| H-05 | 39 unresolved URL names | High |
| H-06 | 35 missing referenced templates | High |
| H-07 | Production entrypoints default to base settings | High |
| H-08 | Open registration without reported abuse controls | High |
| H-09 | Unvalidated login redirect | High |
| H-10 | Unscoped organization/branch/backup HTML lookups | High |
| H-11 | Race-prone stock/document-number operations | High |
| H-12 | Writable dotted serializer sources may fail nested writes | High |
| H-13 | Missing tests and undefined names in existing tests | High |
| H-14 | Missing `qrcode` dependency | High |
| H-15 | Password-reset confirmation is a placeholder | High |
| H-16 | Password-change URL points to reset-request view | High |
| H-17 | Branch middleware ignores `can_access=False` | High |
| H-18 | Tenant helper may silently skip indirect ownership | High |
| H-19 | MFA secrets and backup codes stored as ordinary fields | High |
| H-20 | Logout is GET-capable | High |
| M-01 | Upload validation not consistently applied | Medium / High |
| M-02 | Raw exception details disclosed | Medium |
| M-03 | Silent exception handling | Medium |
| M-04 | Inventory service may create tenant-less products | Medium / High |
| M-05 | Incorrect/obsolete security header settings | Medium |
| M-06 | Reverse-proxy SSL header may be missing | Medium |
| M-07 | Permissive development CORS configuration | Medium |
| M-08 | Settings import-time filesystem side effects | Medium |
| M-09 | Dead/duplicated settings and unused flags | Medium |
| M-10 | Unpinned and mixed dependencies | Medium |
| M-11 | SQLite default and file-based cache concerns | Medium |
| M-12 | `fields='__all__'` serializers may expose sensitive fields | Medium / High |
| M-13 | Audit-log integrity/admin visibility not verified | Medium |
| M-14 | Middleware ordering for locale handling | Medium |
| M-15 | Global reference ViewSets may be writable | Medium |
| L-01 | Stray literal directory under `apps/` | Low |
| L-02 | Compiled `.pyc` files in archive | Low |
| L-03 | Python `__init__.py` files in template tree | Low |
| L-04 | Orphaned and duplicated templates | Low |
| L-05 | Translation `.mo` files not compiled | Low |
| L-06 | Outdated implementation/audit documentation | Low |
| L-07 | Inconsistent product naming | Low |
| L-08 | Documented environment variables not consumed | Low |

**Note:** Severity labels are the consolidated prioritization for remediation. Runtime hypotheses and explicitly unverified areas are marked in the relevant finding descriptions; the severity label alone does not imply that a live exploit was demonstrated.
