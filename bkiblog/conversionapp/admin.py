from django.contrib import admin
from .models import UserHolding, NetWorthHistory


@admin.register(UserHolding)
class UserHoldingAdmin(admin.ModelAdmin):
    list_display = ('user', 'gold18', 'gold24', 'usd', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('updated_at', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(NetWorthHistory)
class NetWorthHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'net_worth', 'timestamp')
    search_fields = ('user__username',)
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        # Prevent manual creation through admin
        return False
