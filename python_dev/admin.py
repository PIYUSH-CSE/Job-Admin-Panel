from django.contrib import admin
from .models import JobListing
import numpy as np
from .utils import calculate_average_salary


class JobListingAdmin(admin.ModelAdmin):
    # Removed 'salary' column and added 'average_salary' column to the list display
    list_display = (
        'title', 'company', 'location', 'yearly_avg_salary', 'average_salary_per_region')  # Only show 'average_salary'

    search_fields = ('title', 'company', 'location')  # Fields to search for
    ordering = ('-yearly_avg_salary',)
    list_per_page = 20  # Items per page in the admin panel

    def average_salary_per_region(self, obj):
        """
        This method will calculate the average salary for the specific location of the current object
        and display it in the admin panel with a rupee symbol (₹).
        """
        city = obj.location  # Get the city from the job listing
        avg_salary = calculate_average_salary(city)  # Call the function to calculate the average salary
        if avg_salary:
            return f'₹ {avg_salary:,.2f}'  # Format the salary to 2 decimal places with ₹ symbol
        else:
            return "No Data"  # If no data is found

    # Optional: You can use this as a custom admin action or column in the list display


admin.site.register(JobListing, JobListingAdmin)
