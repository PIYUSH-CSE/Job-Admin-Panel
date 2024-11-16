from django.db import models

# Create your models here.


class JobListing(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100, null=True, blank=True)  # Store salary as string initially
    yearly_avg_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title
