from django.core.management.base import BaseCommand
import csv
import os
from django.db import connection, transaction
from django.db.utils import DataError, IntegrityError

class Command(BaseCommand):
    help = 'Import Punjab university data from CSV file to PostgreSQL database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('--encoding', type=str, default='utf-8', help='CSV file encoding')
        parser.add_argument('--delimiter', type=str, default=',', help='CSV delimiter')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        encoding = options['encoding']
        delimiter = options['delimiter']

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Starting import from {csv_file_path}'))
        
        # Open the CSV file
        try:
            with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                # Create CSV reader
                csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
                
                # Prepare data for bulk insert
                universities = []
                skipped_rows = 0
                processed_rows = 0
                
                # Process each row
                for row_num, row in enumerate(csv_reader, start=2):  # Start from 2 to account for header row
                    try:
                        # Clean and validate the ID field
                        sr_no = row.get('Sr No ', '').strip()
                        if not sr_no or not sr_no.strip().isdigit() or sr_no.strip() == '':
                            self.stdout.write(self.style.WARNING(f'Skipping row {row_num}: Invalid Sr No "{sr_no}"'))
                            skipped_rows += 1
                            continue
                        
                        
                        university = {
                            'id': int(sr_no),
                            'name': row.get('University Name', '').strip(),
                            'course': row.get('courses', '').strip(),
                            'national_ranking': self._clean_ranking(row.get('National Ranking', '')),
                            'global_ranking': self._clean_ranking(row.get('Global Ranking', '')),
                            'application_form': self._clean_boolean(row.get('Application Form', '')),
                            'number_of_student': self._clean_student_count(row.get('Number of Students', '')),
                            'course_count': self._clean_course_count(row.get('Number of Courses', '')),
                            'scholarships': self._clean_boolean(row.get('Scholarships', '')),
                            'bank_loan': self._clean_boolean(row.get('Bank Loan', '')),
                            'about': row.get('About College', '').strip(),
                            'foreign_affiliations': row.get('Foreign University Affiliations', '').strip(),
                            'achievements': row.get('Achievements', '').strip(),
                            'naac_rating': self._clean_naac_rating(row.get('NAAC Rating', '')),
                            'website': row.get('Website', '').strip()
                        }
                        
                        universities.append(university)
                        processed_rows += 1
                        
                        # Process in batches of 1000
                        if len(universities) >= 1000:
                            self._bulk_insert_universities(universities)
                            self.stdout.write(self.style.SUCCESS(f'Inserted batch of {len(universities)} records'))
                            universities = []
                    
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error processing row {row_num}: {str(e)}'))
                        skipped_rows += 1
                
                # Insert any remaining records
                if universities:
                    self._bulk_insert_universities(universities)
                    self.stdout.write(self.style.SUCCESS(f'Inserted final batch of {len(universities)} records'))
                
                self.stdout.write(self.style.SUCCESS(
                    f'Import completed: {processed_rows} records imported, {skipped_rows} records skipped'
                ))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to import data: {str(e)}'))
    
    def _clean_ranking(self, ranking_str):
        """Clean and normalize ranking value"""
        if not ranking_str or ranking_str.strip().lower() == 'not listed':
            return None
        
        # Handle ranges like "30-50" or "100-150"
        if '-' in ranking_str:
            parts = ranking_str.split('-')
            if len(parts) == 2 and parts[0].strip().isdigit():
                return int(parts[0].strip())
        
        # Handle simple numeric values
        cleaned = ''.join(c for c in ranking_str if c.isdigit())
        if cleaned:
            return int(cleaned)
        
        return None
    
    def _clean_boolean(self, value):
        """Convert text values to boolean"""
        if not value:
            return False
        
        value = value.strip().lower()
        return value == 'available' or value == 'yes' or value == 'true'
    
    def _clean_student_count(self, count_str):
        """Clean and normalize student count"""
        if not count_str or count_str.strip().lower() == 'not listed':
            return None
        
        # Handle ranges like "Approx. 5,000"
        count_str = count_str.lower().replace('approx.', '').replace(',', '').strip()
        
        # Handle values with plus sign like "1000+"
        if count_str.endswith('+'):
            count_str = count_str[:-1].strip()
        
        # Extract numeric part
        cleaned = ''.join(c for c in count_str if c.isdigit())
        if cleaned:
            return int(cleaned)
        
        return None
    
    def _clean_course_count(self, count_str):
        """Clean and normalize course count"""
        if not count_str or count_str.strip().lower() == 'not listed' or 'varies' in count_str.lower():
            return None
        
        # Extract numeric part
        cleaned = ''.join(c for c in count_str if c.isdigit())
        if cleaned:
            return int(cleaned)
        
        return None
    
    def _clean_naac_rating(self, rating):
        """Clean and normalize NAAC rating"""
        if not rating:
            return None
        
        # Just return the cleaned string
        return rating.strip()
    
    @transaction.atomic
    def _bulk_insert_universities(self, universities):
        """
        Performs a bulk insert of university records using raw SQL for better performance
        """
        with connection.cursor() as cursor:
            for university in universities:
                try:
                    cursor.execute(
                        """
                        INSERT INTO meduv1_university
                        (id, name, courses, national_ranking, global_ranking, application_form, 
                        student_count, course_count, scholarships, bank_loan, about, 
                        foreign_affiliations, achievements, naac_rating, website)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
                            name = EXCLUDED.name,
                            courses = EXCLUDED.courses,
                            national_ranking = EXCLUDED.national_ranking,
                            global_ranking = EXCLUDED.global_ranking,
                            application_form = EXCLUDED.application_form,
                            student_count = EXCLUDED.student_count,
                            course_count = EXCLUDED.course_count,
                            scholarships = EXCLUDED.scholarships,
                            bank_loan = EXCLUDED.bank_loan,
                            about = EXCLUDED.about,
                            foreign_affiliations = EXCLUDED.foreign_affiliations,
                            achievements = EXCLUDED.achievements,
                            naac_rating = EXCLUDED.naac_rating,
                            website = EXCLUDED.website
                        """,
                        [
                            university['id'],
                            university['name'],
                            university['courses'],
                            university['national_ranking'],
                            university['global_ranking'],
                            university['application_form'],
                            university['student_count'],
                            university['course_count'],
                            university['scholarships'],
                            university['bank_loan'],
                            university['about'],
                            university['foreign_affiliations'],
                            university['achievements'],
                            university['naac_rating'],
                            university['website'],
                        ]
                    )
                except (DataError, IntegrityError) as e:
                    # Log the error but continue with other records
                    self.stdout.write(self.style.WARNING(
                        f"Skipping university ID {university['id']}: {str(e)}"
                    ))