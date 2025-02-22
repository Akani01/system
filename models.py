from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse
from datetime import date
from django.db.models import Q
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.core.files import File
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db.models.signals import post_save

NEWS = "News"
EVENTS = "Event"

POST = (
    (NEWS, "News"),
    (EVENTS, "Event"),
)

#Schools Recorded
DJUNANE = "DJUNANE"
ELIM = "ELIM"
HLALELANI = "HLALELANI"
KETLANI = "KETLANI"
MAHONISI = "MAHONISI"
MASINDI = "MASINDI"
MASUNGULO = "MASUNGULO"
MULWELI = "MULWELI"
MUNZHEDZI = "MUNZHEDZI"
MUTHUHADINI = "MUTHUHADINI"
NKHENSA = "NKHENSA"
RIVONI = "RIVONI"
SHIHLOBYENI = "SHIHLOBYENI"
SHIRLEY = "SHIRLEY"
TRUE_LIFE = "TRUE_LIFE"
TSAKANI = "TSAKANI"
TSHIMONELA = "TSHIMONELA"
TSHIISAPHUNGO = "TSHIISAPHUNGO"
VALDEZIA = "VALDEZIA"
HS_PHILLIPS = "HS_PHILLIPS"
LEMANA = "LEMANA"
MDR = "MDR"
OZIAS_DAVHANA = "OZIAS_DAVHANA"
RIVUBYE = "RIVUBYE"
TSHIAWELO = "TSHIAWELO"
WATERVAL = "WATERVAL"
OTHER = "OTHER"

#name
NAME = (
    (DJUNANE , "DJUNANE"),
    (ELIM , "ELIM"),
    (HLALELANI, "HLALELANI"),
    (KETLANI, "KETLANI"),
    (MAHONISI, "MAHONISI"),
    (MASINDI, "MASINDI"),
    (MASUNGULO, "MASUNGULO"),
    (MULWELI, "MULWELI"),
    (MUNZHEDZI, "MUNZHEDZI"),
    (MUTHUHADINI, "MUTHUHADINI"),
    (NKHENSA, "NKHENSA"),
    (RIVONI, "RIVONI"),
    (SHIHLOBYENI, "SHIHLOBYENI"),
    (SHIRLEY, "SHIRLEY"),
    (TRUE_LIFE, "TRUE_LIFE"),
    (TSAKANI, "TSAKANI"),
    (TSHIMONELA, "TSHIMONELA"),
    (TSHIISAPHUNGO, "TSHIISAPHUNGO"),
    (VALDEZIA, "VALDEZIA"),
    (HS_PHILLIPS, "HS_PHILLIPS"),
    (LEMANA, "LEMANA"),
    (MDR, "MDR"),
    (OZIAS_DAVHANA, "OZIAS_DAVHANA"),
    (RIVUBYE, "RIVUBYE"),
    (TSHIAWELO, "TSHIAWELO"),
    (WATERVAL, "WATERVAL"),
    (OTHER, "OTHER"),
)

#School Type
DEPENDENT_SCHOOL="DEPENDENT_SCHOOL"
INDEPENDENT_SCHOOL="INDEPENDENT_SCHOOL"
SPECIAL_NEEDS="SPECIAL_NEEDS"

SCHOOL_TYPE = (
    (DEPENDENT_SCHOOL,"DEPENDENT_SCHOOL"),
    (INDEPENDENT_SCHOOL,"INDEPENDENT_SCHOOL"),          
    (SPECIAL_NEEDS,"SPECIAL_NEEDS"),          

)

HIGH_SCHOOL = "HIGH_SCHOOL"
PRIMARY_SCHOOL = "PRIMARY_SCHOOL"
COMBINED_SCHOOL = "COMBINED_SCHOOL"
HOME_SCHOOL = "HOME_SCHOOL"

FILTER_BY = (
    (HIGH_SCHOOL,"HIGH_SCHOOL"),
    (PRIMARY_SCHOOL,"PRIMARY_SCHOOL"),
    (COMBINED_SCHOOL,"COMBINED_SCHOOL"),
    (COMBINED_SCHOOL,"HOME_SCHOOL"),
)

ALL = "All"
FIRST = "First"
SECOND = "Second"
THIRD = "Third"
FOURTH = "FOURTH"

TERM = (
    (ALL, "All"),
    (FIRST, "First"),
    (SECOND, "Second"),
    (THIRD, "Third"),
    (FOURTH, "Fourth"),
)

DISTINCTION_RESULTS = "Distinction"
BACHELOR_RESULTS = "Bachelor"
DIPLOMA_RESULTS = "Diploma"
FAILED_RESULTS = "Fail"

LEVEL = (
    (DISTINCTION_RESULTS, "Distinction RESULTS"),
    (BACHELOR_RESULTS, "Bachelor RESULTS"),
    (DIPLOMA_RESULTS, "Diploma RESULTS"),
    (FAILED_RESULTS, "Failed RESULTS"),
)


# QuerySet for NewsAndEvents
class NewsAndEventsQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(summary__icontains=query) | Q(posted_as__icontains=query)
        return self.filter(lookups).distinct()

# Manager for NewsAndEvents
class NewsAndEventsManager(models.Manager):
    def get_queryset(self):
        return NewsAndEventsQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

# NewsAndEvents model
class NewsAndEvents(models.Model):
    title = models.CharField(max_length=200, null=True)
    summary = models.TextField(max_length=200, blank=True, null=True)
    posted_as = models.CharField(choices=POST, max_length=10)
    updated_date = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="news_images/%y/%m/%d/", default="default.png", null=True)
    objects = NewsAndEventsManager()

    # Get the image URL or the default image
    def get_image(self):
        try:
            return self.image.url
        except:
            return settings.MEDIA_URL + "default.png"

    # Resize the image if necessary
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except:
            pass

    # Delete the image file if it's not the default image
    def delete(self, *args, **kwargs):
        if self.image.url != settings.MEDIA_URL + "default.png":
            self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
#End

#Custom User
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


#Session
class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)

#Custom UserSettings
class CustomUser(AbstractUser):
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "Student"), (4,"Principal"), (5,"Educator"), (6,"Circuit_Manager"), (7,"Parent"), (8,"member"))
    GENDER = [("M", "Male"), ("F", "Female")]
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + ", " + self.first_name



#grade
class Grade(models.Model):
    name = models.CharField(max_length=120)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
#Term
class Term(models.Model):
    term = models.CharField(max_length=10, choices=TERM, blank=True)
    is_current_term = models.BooleanField(default=False, blank=True, null=True)
    activity = models.CharField(max_length=120)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, blank=True, null=True
    )
    next_term_begins = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.term
    
#SCHOOL
class School(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schools')
    emis = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=20, choices=NAME, blank=True)
    phase = models.CharField(max_length=200, null=True, blank=True)
    sector = models.CharField(max_length=200, null=True, blank=True)
    educators_on_db =  models.IntegerField()
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, blank=True, null=True
    )
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE, blank=True)
    logo = models.ImageField()
    head_principal = models.CharField(max_length=200, null=True, blank=True)
    deputy = models.CharField(max_length=200, null=True, blank=True)
    filter_by = models.CharField(max_length=20, choices=FILTER_BY, blank=True)
    website_url = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True, blank=False)
    whatsapp_number = models.CharField(max_length=20, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255)
    year = models.IntegerField()
    count = models.IntegerField()

    class Meta:
        unique_together = ('name', 'year')

    def __str__(self):
        return f"{self.name} ({self.year})"

  

#Course
class Course(models.Model):
    name = models.CharField(max_length=120)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#Custom User 2
class Staff(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + " " + self.admin.first_name



#Subject
class Subject(models.Model):
    name = models.CharField(max_length=120)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')  # Added related_name
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#EDUCATOR
class Educator(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True)
    subjects = models.ManyToManyField(Subject)  # Updated to Many-to-Many
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    term = models.ForeignKey(Term, on_delete=models.DO_NOTHING, null=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name
    
    
#Admin
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)



#Custom User 3
class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True, blank=False)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True, blank=False)
    

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


#informal student result
class InformalStudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    informaltest = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#Attendance
class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#attendance report
class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#leavereport student
class LeaveReportStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#leavereport staff
class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#feedback student
class FeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#feedback staff
class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#notifications
class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#notification student
class NotificationStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#STUDENTRESULTS
class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment = models.FloatField(default=0)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



#MEMBER
class Member(models.Model):
   admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
   position = models.CharField(max_length=20, null=True, blank=True)
   #report
   session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
   term = models.ForeignKey(Term, on_delete=models.DO_NOTHING, null=True)

   def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name

#parent
class Parent(models.Model):
   admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
   student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
   grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
   #report
   session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
   term = models.ForeignKey(Term, on_delete=models.DO_NOTHING, null=True)
   #student, studentresult, grade, attendancereport, educator,  subject , course 
   def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name

#Custom User 4
class Principal(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True)
    #report
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, null=True)
    term = models.ForeignKey(Term, on_delete=models.DO_NOTHING, null=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    #attendancereport, subject, course, session, term, student, studentresult, educator, parent, member

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name

#Circuit manager
class Circuit_Manager(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    circuit = models.CharField(max_length=120)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


#DOWNLOAD QUESTION PAPERS
class QuestionPaperQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = Q(filename__icontains=query) | Q(subject__name__icontains=query)
        return self.filter(lookups).distinct()

class QuestionPaperManager(models.Manager):
    def get_queryset(self):
        return QuestionPaperQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance)
        if instance.user_type == 4:
            Principal.objects.create(admin=instance)
        if instance.user_type == 5:
            Educator.objects.create(admin=instance)
        if instance.user_type == 6:
            Circuit_Manager.objects.create(admin=instance)
        if instance.user_type == 7:
            Parent.objects.create(admin=instance)
        if instance.user_type == 8:
            Member.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
    if instance.user_type == 4:
        instance.principal.save()
    if instance.user_type == 5:
        instance.educator.save()
    if instance.user_type == 6:
        instance.circuit_manager.save()
    if instance.user_type == 7:
        instance.parent.save()
    if instance.user_type == 8:
        instance.member.save()


#Documents

#submits
class Textbook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)
    file = models.FileField(upload_to='textbooks/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#appointments
class Appointment(models.Model):
    DEPARTMENT_CHOICES = [
        ('Admissions', 'Admissions'),
        ('Finance', 'Finance'),
        ('HR', 'Human Resources'),
        ('Academics', 'Academics'),
        ('Advertisement', 'Advertisements'),
        ('Sponsor', 'Sponsors'),
        ('Project', 'Projects'),
        ('Other', 'Others')
    ]

    name= models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.department}"

#subscription
class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

#files
class Files(models.Model):
    filename = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='store/pdfs/')
    cover = models.ImageField(upload_to='store/pdfs/')

    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)
    
#timetable
class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    subjects = models.ManyToManyField(Subject)  # Subjects for the timetable
    educators = models.ManyToManyField(Educator)  # Add educators here
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_timetables')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.created_by_id:
            raise ValueError("The 'created_by' field must be set before saving.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.day} - {self.grade.name} ({self.course.name})"


#testimonial
class Message(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.SET_NULL)  # This field allows replies to other messages

    def __str__(self):
        return self.text[:50]

class MessageMedia(models.Model):
    message = models.ForeignKey(Message, related_name='media', on_delete=models.CASCADE)
    media = models.FileField(upload_to='message_media/')

    def __str__(self):
        return self.media.name


#School Perfomance
class SchoolPerformance(models.Model):
    school_record = models.ForeignKey(School, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)  # New ForeignKey to Session
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True, blank=False)
    school_principal = models.ForeignKey(Principal, on_delete=models.CASCADE)
    performance_score = models.DecimalField(max_digits=5, decimal_places=2)
    total_score = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    overall_performance = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    num_evaluations = models.IntegerField(default=1)
    improvement = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('school_record', 'session', 'subject', 'grade')  # Updated to include session

    def __str__(self):
        return f"{self.school_record.name} - {self.subject} ({self.grade}) Performance ({self.school_record.year})"

    def calculate_total_score(self):
        total = SchoolPerformance.objects.filter(
            school_record=self.school_record,
            session=self.session,
            grade=self.grade,
            subject=self.subject
        ).aggregate(total=Sum('performance_score'))['total']
        self.total_score = total or 0.00
        self.save()

    def calculate_overall_performance(self):
        if self.num_evaluations > 0:
            self.overall_performance = self.total_score / self.num_evaluations
        else:
            self.overall_performance = 0.00
        self.save()

    def calculate_improvement(self, previous_score):
        if previous_score:
            self.improvement = self.performance_score - previous_score
        else:
            self.improvement = self.performance_score
        self.save()

    def save(self, *args, **kwargs):
        self.calculate_total_score()
        self.calculate_overall_performance()
        super(SchoolPerformance, self).save(*args, **kwargs)

#school of specialisation assessment dates

#Jobs model
#Category model
class SosCategory(models.Model):
    class Meta:
        verbose_name = 'SosCategory'
        verbose_name_plural = 'SosCategories'

    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


#sos
class Sos(models.Model):
    class Meta:
        verbose_name = 'Sos'
        verbose_name_plural = 'soss'
    
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True, blank=False)
    date = models.CharField(max_length=20, null=True, blank=True)
    assessment = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
   
    def __str__(self):
        return self.description