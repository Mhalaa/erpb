from django.contrib import admin
from .models import Company, MediaProject, UserProfile, Notification, Vendor, PurchaseOrder, BTCashRequest, VendorTransaction, TransactionLog

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'created_at', 'updated_at')
    search_fields = ('name_en', 'name_ar')
    list_filter = ('created_at',)

@admin.register(MediaProject)
class MediaProjectAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'company', 'status', 'budget', 'currency', 'start_date', 'end_date', 'created_at')
    search_fields = ('name_en', 'name_ar', 'company__name_en', 'company__name_ar')
    list_filter = ('status', 'company', 'start_date', 'currency')
    readonly_fields = ('total_expenses',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role', 'language_preference', 'preferred_currency', 'status', 'activity_score', 'last_login')
    search_fields = ('user__username', 'company__name_en', 'company__name_ar')
    list_filter = ('role', 'status', 'language_preference', 'preferred_currency')
    actions = ['update_activity_scores']

    def update_activity_scores(self, request, queryset):
        for profile in queryset:
            profile.update_activity_score()
        self.message_user(request, "Activity scores updated successfully.")
    update_activity_scores.short_description = "Update activity scores for selected users"

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title_en', 'title_ar', 'type', 'is_read', 'created_at')
    search_fields = ('title_en', 'title_ar', 'message_en', 'message_ar', 'user__username')
    list_filter = ('type', 'is_read', 'created_at')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'company', 'created_at')
    search_fields = ('name_en', 'name_ar', 'company__name_en', 'company__name_ar')
    list_filter = ('company',)

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'media_project', 'vendor', 'total_amount', 'currency', 'request_date', 'md_approval', 'ceo_approval', 'finance_approval', 'status', 'archived')
    search_fields = ('request_number', 'media_project__name_en', 'media_project__name_ar', 'vendor__name_en', 'vendor__name_ar')
    list_filter = ('md_approval', 'ceo_approval', 'finance_approval', 'status', 'archived', 'request_date', 'currency')
    readonly_fields = ('approval_progress',)

@admin.register(BTCashRequest)
class BTCashRequestAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'media_project', 'total_amount', 'currency', 'request_date', 'md_approval', 'ceo_approval', 'finance_approval', 'status', 'archived')
    search_fields = ('request_number', 'media_project__name_en', 'media_project__name_ar')
    list_filter = ('md_approval', 'ceo_approval', 'finance_approval', 'status', 'archived', 'request_date', 'currency')
    readonly_fields = ('approval_progress',)

@admin.register(VendorTransaction)
class VendorTransactionAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'vendor', 'request_type', 'media_project', 'amount', 'currency', 'date', 'status')
    search_fields = ('request_number', 'vendor__name_en', 'vendor__name_ar', 'media_project__name_en', 'media_project__name_ar')
    list_filter = ('request_type', 'status', 'date', 'currency')

@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'model_name', 'object_id', 'timestamp')
    search_fields = ('user__username', 'model_name', 'object_id', 'description_en', 'description_ar')
    list_filter = ('action_type', 'timestamp')
    readonly_fields = ('timestamp',)