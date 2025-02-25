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
admin.site.register(Pathologist)
admin.site.register(Prescription)
admin.site.register(Dispense)
admin.site.register(PatientFeedback)
admin.site.register(SellInvoice)
admin.site.register(PurchasedInvoice)

class NameAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")

admin.site.register(Manufacturer, NameAdmin)
admin.site.register(Vender, NameAdmin)
admin.site.register(Category, NameAdmin)
admin.site.register(DrugType, NameAdmin)
admin.site.register(DrugUnit, NameAdmin)

@admin.register(Language)
class LamguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'medicine', 'quantity', 'updated_at')
    list_filter = ('updated_at', 'quantity')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')


@admin.register(Addmission)
class AddmissionAdmin(admin.ModelAdmin):
    list_display = ("patient", "purpose", "department", "doctor", "reason", "created_at")
    list_filter = ("department", "purpose", "created_at")


@admin.register(HospitalItem)
class HospitalItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'actual_price', 'price', 'discount', 'created_at')
    search_fields = ('name', )
    list_filter = ('unit', 'actual_price', 'price', 'discount', 'created_at')


@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ("admin", "department", "emp_no", "gender", "address", "created_at")
    list_filter = ("created_at", )


@admin.register(Reception)
class NurseAdmin(admin.ModelAdmin):
    list_display = ("admin", "emp_no", "gender", "address", "created_at")
    list_filter = ("created_at", )


@admin.register(ClinicalNote)
class ClinicalNoteAdmin(admin.ModelAdmin):
    list_display = ("note_type", "note", "created_at")
    list_filter = ("note_type", "created_at")


# Inventory related models
@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ('name', )


@admin.register(InventoryStore)
class InventoryStoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "created_at")
    

@admin.register(InventorySupplier)
class InventorySupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email", "contact_person", "contact_person_phone", "address", "created_at")
    search_fields = ("name", "phone", "email", "contact_person", "contact_person_phone", "address",)
    

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "created_at")
    list_filter = ("category", "created_at", )
    search_fields = ("name", )
    

@admin.register(InventoryStock)
class InventoryStockAdmin(admin.ModelAdmin):
    list_display = ("item", "store", "supplier", "quantity", "purchase_price", "date")
    search_fields = ("description", "item__name",)
    list_filter = ("item", "store", "supplier", "date")
