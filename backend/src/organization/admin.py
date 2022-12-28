from django.contrib import admin
from .models.org import Organization, OrganizationPersonnel
from .models.schools import Group, School, SchoolPersonnel, AdministrativePersonnel, Teacher, Classroom


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_of', 'slug', 'parent')
    search_fields = ('id', 'name', 'slug')
    list_filter = ('type_of', 'slug', 'student_plan', 'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(OrganizationPersonnel)
class OrganizationPersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization', 'name', 'last_name',
                    'gender', 'date_of_birth', 'identification_number', 'position')
    search_fields = ('id', 'user__username', 'organization__name', 'name', 'last_name', 'identification_number')
    list_filter = ('organization', 'position', 'gender', 'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'internal_code', 'population', 'slug',
                    'grade', 'school_personnel')
    search_fields = ('id', 'name', 'internal_code', 'school_personnel__user__username',
                     'school_personnel__user__first_name', 'school_personnel__user__last_name')
    list_filter = ('area_of_knowledges', 'grade', 'slug', 'population',
                   'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'internal_code', 'type_of', 'organization')
    search_fields = ('id', 'name', 'internal_code', 'organization__name')
    list_filter = ('student_plan', 'type_of', 'slug', 'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(SchoolPersonnel)
class SchoolPersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'discountCode', 'name', 'last_name',
                    'gender', 'date_of_birth', 'identification_number',
                    'position', 'zip', 'country', 'district')
    search_fields = ('id', 'user__username', 'school__name', 'name', 'last_name',
                     'identification_number', 'position', 'zip', 'country', 'district',)
    list_filter = ('school', 'position', 'identification_number', 'gender', 'district', 'country', 'zip')


@admin.register(AdministrativePersonnel)
class AdministrativePersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'discountCode', 'name', 'last_name',
                    'gender', 'date_of_birth', 'identification_number',
                    'position', 'zip', 'country', 'district')
    search_fields = ('id', 'user__username', 'school__name', 'name', 'last_name', 'identification_number',
                     'position', 'zip', 'country', 'district')
    list_filter = ('identification_number', 'position', 'gender', 'school__name', 'zip', 'country', 'district',
                   'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'discountCode', 'name', 'last_name',
                    'gender', 'date_of_birth', 'identification_number',
                    'position', 'zip', 'country', 'district')
    search_fields = ('id', 'user__username', 'school__name', 'name', 'last_name',
                     'identification_number', 'position', 'zip', 'country', 'district')
    list_filter = ('school', 'position', 'identification_number', 'gender', 'district', 'country', 'zip',
                   'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'language', 'audience', 'school', 'teacher', 'enable_games', 'game_cost', 'time_zone',
                    'monday_start', 'monday_end', 'tuesday_start', 'tuesday_end', 'wednesday_start', 'wednesday_end',
                    'thursday_start', 'thursday_end', 'friday_start', 'friday_end', 'saturday_start', 'saturday_end',
                    'sunday_start', 'sunday_end')
    search_fields = ('id', 'name', 'audience__translations__name',
                     'school__name', 'teacher__name', 'teacher__last_name')
    list_filter = ('grade', 'language', 'audience', 'school', 'game_cost',
                   'time_zone', 'is_active', 'create_timestamp', 'update_timestamp')
