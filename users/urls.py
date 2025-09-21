from django.urls import path, include
from users import admin
urlpatterns = [
    path('', admin.index, name='system_users'),
    path('save_user', admin.save, name='system_users_save'),
    path('roles/', admin.role, name='system_groups'),
    path('roles/save_role', admin.save_role, name='system_groups_save'),
    path('assign-role-permission', admin.assign_role_permission, name='system_role_assign_permission'),
    path('assign-user-permission', admin.assign_user_permission, name='system_user_assign_permission'),
    path('users/save-role-permission', admin.save_role_permission, name='system_assign_group_permission_save'),
    path('users/save-user-permission', admin.save_user_permission, name='system_assign_user_permission_save'),
    path('users/check-dublicate', admin.check_dublicate, name='system_users_check'),
    path('profile', admin.profile, name='system_users_profile'),
    path('update-profile', admin.update_profile, name='system_users_update_profile'),
    path('change-password', admin.change_password, name='system_users_change_password'),
    path('update-change-password', admin.update_change_password, name='system_users_update_change_password'),


]