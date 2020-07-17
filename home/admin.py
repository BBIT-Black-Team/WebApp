from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Subject, Faculty, AssessmentDetail, ExamBlock, Assessment


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email',  'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(AssessmentDetail)
admin.site.register(ExamBlock)
admin.site.register(Assessment)

admin.site.unregister(Group)


admin.site.site_header = 'Institute Exam Management System'
admin.site.site_title = 'Institute Exam Management System'
