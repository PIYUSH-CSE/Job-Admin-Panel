import numpy as np
from .models import JobListing
from bson import Decimal128


def calculate_average_salary(city):
    """
    Calculate the average salary for job listings in locations that contain the specified city.
    """
    city = city.strip()  # Clean up any extra spaces
    #print(f"Searching for jobs in city: '{city}'")

    # Fetch job listings where location contains the city substring (case-insensitive)
    jobs = JobListing.objects.filter(location__icontains=city)
    #print(f"Jobs found for location containing '{city}': {jobs}")

    # Extract the salaries, ensuring they are valid and not NaN
    salaries = []
    for job in jobs:
        try:
            # Check if the salary exists and is not None or empty
            if job.yearly_avg_salary is not None and job.yearly_avg_salary != '':
                # If the salary is of type Decimal128, convert it to Decimal first
                if isinstance(job.yearly_avg_salary, Decimal128):
                    salary = job.yearly_avg_salary.to_decimal()  # Convert to decimal first
                    salary = float(salary)  # Convert to float
                else:
                    salary = float(job.yearly_avg_salary)  # Convert salary to float if it's not Decimal128

                # Only add valid salary values (non-NaN and greater than 0)
                if not np.isnan(salary) and salary > 0:
                    #print(f"Extracted valid salary for job {job.id}: {salary}")
                    salaries.append(salary)
                else:
                    print(f"Invalid salary value for job {job.id}: {salary}")
            else:
                print(f"Salary not found or is empty for job {job.id}")
        except Exception as e:
            print(f"Error converting salary for job {job.id}: {e}")

    # Debugging: Print the list of extracted salaries
    #print(f"Salaries extracted: {salaries}")

    # Calculate the average salary using NumPy (NumPy can handle float objects)
    if salaries:
        avg_salary = np.mean(salaries)
        #print(f"Average salary for jobs in '{city}': {avg_salary}")
        return avg_salary
    else:
        print(f"No jobs found for location containing '{city}' or no valid salaries.")
        return None
