from django.contrib import admin
from .models import CustomUser, Transaction, Badge, Professor

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'amount', 'date')  # Specify the fields to display in the list view
    readonly_fields = ('date',)  # Make the date field read-only in the detail view
    list_editable = ('type', 'amount')  # Make the type and amount fields editable in the list view

admin.site.register(CustomUser)
admin.site.register(Badge)
admin.site.register(Professor)
admin.site.register(Transaction, TransactionAdmin) 