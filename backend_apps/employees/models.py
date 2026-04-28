from backend_apps.departments.models import Department
from backend_apps.users.models import UserAccounts
from django.db import models
from datetime import date

class Employee(models.Model):
    user = models.OneToOneField(
        UserAccounts,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='user',
        related_name='employee'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='department',
        related_name='employees'
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Employee Name",
        help_text='The name of the employee'
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Employee Title",
        help_text='The title of the employee'
    )
    hire_date = models.DateField(default=date.today)
    mobile = models.BigIntegerField(verbose_name="Employee Phone Number", default=0, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "employees"
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    @property
    def days_employed(self):
        return ((date.today() - self.hire_date).days) + 1

    def __str__(self):
        return f"Employee ID: {self.id}"