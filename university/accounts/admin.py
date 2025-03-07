import csv
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from .models import Location
from django.contrib import messages

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'lat', 'lon')  # Display fields in the admin list view
    change_list_template = "admin/location_changelist.html"  # Use a custom template for bulk upload

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv, name='upload_csv'),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get('csv_file')
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a CSV file.")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(file_data)
            for row in csv_reader:
                try:
                    name, lat, lon = row
                    Location.objects.create(name=name, lat=float(lat), lon=float(lon))
                except Exception as e:
                    messages.error(request, f"Error processing row {row}: {e}")
                    continue

            messages.success(request, "Bulk upload successful!")
            return HttpResponseRedirect("../")

        return render(request, "admin/csv_upload_form.html")

import csv
from django.contrib import admin
from .models import University
from django.http import HttpResponse

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'total_programs', 'approximate_students', 'naac_grade', 'website', 'contact_number', 'location')

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                self.message_user(request, "Please upload a valid CSV file.")
                return HttpResponse("Invalid File Format", status=400)

            reader = csv.reader(csv_file.read().decode("utf-8").splitlines())
            next(reader)  # Skip header row
            for row in reader:
                University.objects.create(
                    name=row[0],
                    type=row[1],
                    total_programs=row[2],
                    approximate_students=row[3],
                    naac_grade=row[4],
                    website=row[5],
                    contact_number=row[6],
                    location=row[7],
                )
            self.message_user(request, "CSV file successfully uploaded.")
        return HttpResponse("CSV Uploaded Successfully")

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('upload_csv/', self.admin_site.admin_view(self.upload_csv), name='upload_csv'),
        ]
        return custom_urls + urls

admin.site.register(University, UniversityAdmin)
