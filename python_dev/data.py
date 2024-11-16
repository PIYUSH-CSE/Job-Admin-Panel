import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indeeds.settings')

# Set up Django
django.setup()

from python_dev.models import JobListing
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['indeed_jobs']  # Your MongoDB database name
collection = db['python_developer_jobs']  # Your MongoDB collection name

# Fetch the data
job_listings = collection.find()

# Import data into Django model
for job in job_listings:
    # Extract values from MongoDB document
    title = job.get('title')
    company = job.get('company')
    location = job.get('location')
    salary = job.get('salary')
    yearly_avg_salary = job.get('yearly_avg_salary')

    # Optional: Check if a job listing already exists (prevent duplicates)
    if not JobListing.objects.filter(title=title, company=company).exists():
        try:
            # Create a new JobListing object
            JobListing.objects.create(
                title=title,
                company=company,
                location=location,
                salary=salary,
                yearly_avg_salary=yearly_avg_salary
            )
            print(f"Job '{title}' from {company} added successfully!")
        except Exception as e:
            print(f"Error while inserting job '{title}': {e}")
    else:
        print(f"Job '{title}' from {company} already exists, skipping.")
