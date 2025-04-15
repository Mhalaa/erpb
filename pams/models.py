from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Currency Choices (for multi-currency support)
CURRENCY_CHOICES = (
    ('USD', 'US Dollar'),
    ('SAR', 'Saudi Riyal'),
    ('EGP', 'Egyptian Pound'),
    ('EUR', 'Euro'),
)

# Company Model
class Company(models.Model):
    name_en = models.CharField(max_length=100, unique=True, verbose_name=_("Name (English)"))
    name_ar = models.CharField(max_length=100, unique=True, verbose_name=_("Name (Arabic)"))
    description_en = models.TextField(blank=True, verbose_name=_("Description (English)"))
    description_ar = models.TextField(blank=True, verbose_name=_("Description (Arabic)"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_en  # Default to English for admin; bilingual display handled in templates

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

# Media Project Model
class MediaProject(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    name_en = models.CharField(max_length=100, verbose_name=_("Name (English)"))
    name_ar = models.CharField(max_length=100, verbose_name=_("Name (Arabic)"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects')
    description_en = models.TextField(blank=True, verbose_name=_("Description (English)"))
    description_ar = models.TextField(blank=True, verbose_name=_("Description (Arabic)"))
    budget = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_en  # Default to English; bilingual display in templates

    def total_expenses(self):
        po_total = self.purchase_orders.aggregate(models.Sum('total_amount'))['total_amount__sum'] or 0
        bt_total = self.bt_cash_requests.aggregate(models.Sum('total_amount'))['total_amount__sum'] or 0
        return po_total + bt_total

    class Meta:
        verbose_name = _("Media Project")
        verbose_name_plural = _("Media Projects")

# Extended User Profile for User Management and Role-Based Access
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('md', 'MD'),
        ('ceo', 'CEO'),
        ('finance', 'Finance'),
        ('user', 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    language_preference = models.CharField(max_length=2, choices=(('en', 'English'), ('ar', 'Arabic')), default='en')
    preferred_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    last_login = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('inactive', 'Inactive')), default='active')
    activity_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def update_activity_score(self):
        if self.last_login:
            days_since_login = (timezone.now() - self.last_login).days
            self.activity_score = max(0, 100 - days_since_login * 10)
        else:
            self.activity_score = 0
        self.save()

    def can_view(self, section):
        if self.role == 'admin':
            return True
        permissions = {
            'md': ['md_approvals', 'dashboard', 'project_list', 'po_list', 'bt_cash_list'],
            'ceo': ['ceo_approvals', 'dashboard', 'project_list', 'po_list', 'bt_cash_list'],
            'finance': ['finance_approvals', 'dashboard', 'media_expense_sheets', 'bt_cash_reconciliation', 'transaction_log'],
            'user': ['dashboard', 'project_list'],
        }
        return section in permissions.get(self.role, [])

    def can_edit(self, section):
        if self.role == 'admin':
            return True
        edit_permissions = {
            'md': ['md_approvals', 'po_approval_status', 'bt_cash_approval_status'],
            'ceo': ['ceo_approvals', 'po_approval_status', 'bt_cash_approval_status'],
            'finance': ['finance_approvals', 'media_expense_sheets', 'bt_cash_reconciliation'],
            'user': [],
        }
        return section in edit_permissions.get(self.role, [])

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

# Notification Model
class Notification(models.Model):
    TYPE_CHOICES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title_en = models.CharField(max_length=100, verbose_name=_("Title (English)"))
    title_ar = models.CharField(max_length=100, verbose_name=_("Title (Arabic)"))
    message_en = models.TextField(verbose_name=_("Message (English)"))
    message_ar = models.TextField(verbose_name=_("Message (Arabic)"))
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    related_object = models.CharField(max_length=50, blank=True)  # e.g., "PurchaseOrder:PO-2025-001"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_en  # Default to English; bilingual display in templates

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

# Vendor Model
class Vendor(models.Model):
    name_en = models.CharField(max_length=100, verbose_name=_("Name (English)"))
    name_ar = models.CharField(max_length=100, verbose_name=_("Name (Arabic)"))
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    contact_info = models.TextField(blank=True, verbose_name=_("Contact Info"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_en  # Default to English; bilingual display in templates

    class Meta:
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")

# Purchase Order Model
class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    request_number = models.CharField(max_length=20, unique=True)
    media_project = models.ForeignKey(MediaProject, on_delete=models.CASCADE, related_name='purchase_orders')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    request_date = models.DateField()
    md_approval = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ceo_approval = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    finance_approval = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    purpose_en = models.CharField(max_length=100, verbose_name=_("Purpose (English)"))
    purpose_ar = models.CharField(max_length=100, verbose_name=_("Purpose (Arabic)"))
    items_en = models.TextField(verbose_name=_("Items (English)"))
    items_ar = models.TextField(verbose_name=_("Items (Arabic)"))
    notes_en = models.TextField(blank=True, verbose_name=_("Notes (English)"))
    notes_ar = models.TextField(blank=True, verbose_name=_("Notes (Arabic)"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='po_created')
    archived = models.BooleanField(default=False)
    archived_date = models.DateField(null=True, blank=True)
    archived_reason_en = models.TextField(blank=True, verbose_name=_("Archived Reason (English)"))
    archived_reason_ar = models.TextField(blank=True, verbose_name=_("Archived Reason (Arabic)"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request_number

    def approval_progress(self):
        approvals = [self.md_approval, self.ceo_approval, self.finance_approval]
        approved_count = approvals.count('approved')
        return (approved_count / 3) * 100

    class Meta:
        verbose_name = _("Purchase Order")
        verbose_name_plural = _("Purchase Orders")

# BT-Cash Request Model
class BTCashRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    request_number = models.CharField(max_length=20, unique=True)
    media_project = models.ForeignKey(MediaProject, on_delete=models.CASCADE, related_name='bt_cash_requests')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    request_date = models.DateField()
    md_approval = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ceo_approval = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    finance_approval = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    purpose_en = models.CharField(max_length=100, verbose_name=_("Purpose (English)"))
    purpose_ar = models.CharField(max_length=100, verbose_name=_("Purpose (Arabic)"))
    items_en = models.TextField(verbose_name=_("Items (English)"))
    items_ar = models.TextField(verbose_name=_("Items (Arabic)"))
    notes_en = models.TextField(blank=True, verbose_name=_("Notes (English)"))
    notes_ar = models.TextField(blank=True, verbose_name=_("Notes (Arabic)"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bt_cash_created')
    archived = models.BooleanField(default=False)
    archived_date = models.DateField(null=True, blank=True)
    archived_reason_en = models.TextField(blank=True, verbose_name=_("Archived Reason (English)"))
    archived_reason_ar = models.TextField(blank=True, verbose_name=_("Archived Reason (Arabic)"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request_number

    def approval_progress(self):
        approvals = [self.md_approval, self.ceo_approval, self.finance_approval]
        approved_count = approvals.count('approved')
        return (approved_count / 3) * 100

    class Meta:
        verbose_name = _("BT-Cash Request")
        verbose_name_plural = _("BT-Cash Requests")

# Vendor Transaction Model
class VendorTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('po', 'Purchase Order'),
        ('bt_cash', 'BT-Cash'),
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='transactions')
    request_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    request_number = models.CharField(max_length=20)
    media_project = models.ForeignKey(MediaProject, on_delete=models.CASCADE, related_name='vendor_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=BTCashRequest.STATUS_CHOICES, default='pending')
    details_en = models.TextField(blank=True, verbose_name=_("Details (English)"))
    details_ar = models.TextField(blank=True, verbose_name=_("Details (Arabic)"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.request_number} - {self.vendor.name}"

    class Meta:
        verbose_name = _("Vendor Transaction")
        verbose_name_plural = _("Vendor Transactions")

# Transaction Log Model
class TransactionLog(models.Model):
    ACTION_TYPES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('archive', 'Archive'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transaction_logs')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=20)
    description_en = models.TextField(verbose_name=_("Description (English)"))
    description_ar = models.TextField(verbose_name=_("Description (Arabic)"))
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} - {self.model_name} ({self.object_id}) by {self.user.username if self.user else 'Anonymous'}"

    class Meta:
        verbose_name = _("Transaction Log")
        verbose_name_plural = _("Transaction Logs")