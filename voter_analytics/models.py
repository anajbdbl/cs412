from django.db import models
import csv
from django.utils.dateparse import parse_date

# Create your models here.
class Voter(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=20)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def load_data():
    # Delete all existing Voter records
    Voter.objects.all().delete()

    filename = '/Users/anajuliabortolossi/Desktop/django/voter_analytics/newton_voters.csv'
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                # Convert fields to appropriate types
                date_of_birth = parse_date(row['Date of Birth'])
                date_of_registration = parse_date(row['Date of Registration'])

                # Map 'TRUE'/'FALSE' strings to Boolean values
                v20state = row['v20state'].strip().upper() == 'TRUE'
                v21town = row['v21town'].strip().upper() == 'TRUE'
                v21primary = row['v21primary'].strip().upper() == 'TRUE'
                v22general = row['v22general'].strip().upper() == 'TRUE'
                v23town = row['v23town'].strip().upper() == 'TRUE'

                # Convert voter score to an integer
                voter_score = int(row['voter_score'].strip())

                # Create Voter instance
                voter = Voter(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row.get('Residential Address - Apartment Number', None),
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=date_of_birth,
                    date_of_registration=date_of_registration,
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'],
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    voter_score=voter_score,
                )

                # Save Voter to the database
                voter.save()
                print(f'Created voter: {voter}')

            except (ValueError, IndexError, KeyError) as e:
                print(f"Exception occurred while processing row: {row}. Error: {e}")

    print("Data load complete.")