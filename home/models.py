from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')


class Subject(models.Model):
    name = models.CharField(max_length=150, default=None, blank=False,)
    code = models.BigIntegerField(primary_key=True, unique=True)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.first_name


class ExamBlock(models.Model):
    date_of_exam = models.DateField(default=None, blank=True)
    no_of_blocks = models.SmallIntegerField(default=None, blank=True)

    SESSION_CHOICES = (
        ("MORNING", "MORNING"),
        ("EVENING", "EVENING"),
    )
    session = models.CharField(max_length=50, choices=SESSION_CHOICES, default=None)


class AssessmentDetail(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_answer_sheets = models.SmallIntegerField(default=None)
    first_ans_sheet = models.SmallIntegerField(default=None)
    last_ans_sheet = models.SmallIntegerField(default=None)



