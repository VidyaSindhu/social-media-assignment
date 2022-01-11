from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'name',  'is_active',)
    list_filter = ('email', 'name',  'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        # ('Permissions', {'fields': ('is_active', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        if request.user.is_superuser or request.user.is_staff:
            return User.objects.filter(is_superuser=False)
        

admin.site.register(User, UserAdmin)