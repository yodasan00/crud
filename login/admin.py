from django.contrib import admin
from .models import UserDetails, LicenseDetails

# Register UserDetails model with full field access
@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    # Display all fields in the list view
    list_display = ['user_profile', 'date_of_birth', 'user_status', 'phone_number']
    # Add a search bar for the user profile username and phone number
    search_fields = ['user_profile__username', 'phone_number']
    # Add filters by user status
    list_filter = ['user_status']
    # Enable fields to be edited on the form
    fields = ['user_profile', 'date_of_birth', 'user_status', 'phone_number']


# Register LicenseDetails model with full field access
@admin.register(LicenseDetails)
class LicenseDetailsAdmin(admin.ModelAdmin):
    # Display all fields in the list view
    list_display = ['user_profile', 'license_number', 'district_name', 'licensee_name', 'establishment_name', 
                    'license_category', 'license_type', 'license_nature', 'yearly_license_fee']
    # Add a search bar for the username, license number, and district name
    search_fields = ['user_profile__username', 'license_number', 'district_name']
    # Add filters by license category and type
    list_filter = ['license_category', 'license_type']
    # Enable fields to be edited on the form
    fields = ['user_profile', 'license_number', 'district_name', 'licensee_name', 'establishment_name', 
              'license_category', 'license_type', 'license_nature', 'yearly_license_fee']
    