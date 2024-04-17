from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

class PatientsAdmin(admin.ModelAdmin):
    list_display = ('admin', 'gender')
    search_fields = ["admin__username"]

class UserModel(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "user_type")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "user_type")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "user_type")
    search_fields = ("username", "first_name", "last_name", "email", "user_type")
    ordering = ("username",)

admin.site.register(CustomUser, UserModel)

admin.site.register(Patients,PatientsAdmin)
admin.site.register(Pharmacist)
admin.site.register(AdminHOD)
admin.site.register(Stock)
admin.site.register(Doctor)
admin.site.register(PharmacyClerk)
admin.site.register(Prescription)
admin.site.register(Dispense)
admin.site.register(PatientFeedback)
admin.site.register(SellInvoice)

class NameAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")

admin.site.register(Manufacturer, NameAdmin)
admin.site.register(Vender, NameAdmin)
admin.site.register(Category, NameAdmin)
admin.site.register(DrugType, NameAdmin)
admin.site.register(DrugUnit, NameAdmin)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'medicine', 'quantity', 'updated_at')
    list_filter = ('updated_at', 'quantity')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
