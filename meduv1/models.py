from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager


class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):  # Remove username
    email = models.EmailField(unique=True)  # Use email as unique identifier
    phone_number = models.CharField(max_length=15, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Set email as the login field
    REQUIRED_FIELDS = []  # Only email and password are required

    def __str__(self):
        return self.email


class University(models.Model):
    TYPE_OF_COURSE_CHOICES = (
        ('En', 'Engineering'),
        ('Me', 'Medical'),
        ('Ma', 'Management'),
        ('Ar', 'Architecture'),
        ('La', 'Law'),
        ('Co', 'Commerce'),
        ('Sc', 'Science'),
        ('Ar', 'Arts'),
        ('Ot', 'Other'),
    )
    # admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="university_admin", null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    course = models.TextField(max_length=3000, blank=True, null=True)
    fees = models.TextField(max_length=5000, blank=True, null=True)
    eligibility = models.TextField(blank=True, null=True)
    application_date = models.CharField(max_length=5000, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    highlights = models.TextField(blank=True, null=True)
    departments = models.TextField(blank=True, null=True)
    collaborations = models.TextField(blank=True, null=True)
    ratings = models.CharField(max_length=50, blank=True, null=True)
    stream = models.TextField(max_length=255, blank=True, null=True)
    students_placed = models.TextField(max_length=50, blank=True, null=True)
    air_rank = models.CharField(max_length=50, blank=True, null=True)
    scholarship_amount = models.CharField(max_length=50, blank=True, null=True)
    percentage_marks = models.CharField(max_length=50, blank=True, null=True)
    class_xii_marks = models.CharField(max_length=50, blank=True, null=True)
    
    # Classification Field
    type_of_course = models.CharField(max_length=2, choices=TYPE_OF_COURSE_CHOICES, blank=True, null=True)

    # New fields
    national_ranking = models.CharField(max_length=255, blank=True, null=True)
    global_ranking = models.CharField(max_length=50, blank=True, null=True)
    number_of_students = models.CharField(max_length=50, blank=True, null=True)
    number_of_courses = models.CharField(max_length=50, blank=True, null=True)
    scholarships = models.TextField(max_length=5000, blank=True, null=True)
    bank_loan = models.TextField(max_length=50, blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    entrance_exam = models.CharField(max_length=50, blank=True, null=True)
    counselling = models.CharField(max_length=100, blank=True, null=True)
    number_of_seats = models.CharField(max_length=50, blank=True, null=True)
    round_1_closing_cutoff = models.CharField(max_length=50, blank=True, null=True)
    general = models.CharField(max_length=50, blank=True, null=True)
    obc = models.CharField(max_length=50, blank=True, null=True)
    sc = models.CharField(max_length=50, blank=True, null=True)
    st = models.CharField(max_length=50, blank=True, null=True)
    cutoff_rounds = models.CharField(max_length=50, blank=True, null=True)
    round_1_rank = models.CharField(max_length=50, blank=True, null=True)

    # Additional fields from import script
    affiliations = models.TextField(blank=True, null=True)
    naac_rating = models.CharField(max_length=50, blank=True, null=True)
    application_form = models.CharField(max_length=255, blank=True, null=True)
    scholarship_criteria = models.TextField(blank=True, null=True)
    scholarship_amount = models.CharField(max_length=50, blank=True, null=True)
    eligibility_criteria = models.TextField(blank=True, null=True)
    selection_criteria = models.TextField(max_length=25500, blank=True, null=True)
    foreign_affiliations = models.TextField(blank=True, null=True)


    def __str__(self):
        return f" {self.name}"

class Location(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        from django.utils.timezone import now
        return (now() - self.created_at).seconds < 300  # 5-minute expiry


class Application(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    course = models.CharField(max_length=255)
    statement_of_purpose = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.university.name}"