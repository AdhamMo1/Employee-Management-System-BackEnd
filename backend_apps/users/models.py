from django.contrib.auth.models import AbstractUser
from backend_apps.companies.models import Company
from django.db import models


class RoleChoices(models.TextChoices):
    NOT_SELECTED = "NOT_SELECTED", "Not Selected"
    SYSTEM_ADMINISTRATOR = "SYSTEM_ADMINISTRATOR", "System Administrator"
    HR_MANAGER = "HR_MANAGER", "HR Manager"
    EMPLOYEE = "EMPLOYEE", "Employee"


class UserAccounts(AbstractUser):
    role = models.CharField(
        default=RoleChoices.NOT_SELECTED,
        choices=RoleChoices.choices,
        verbose_name="User Role",
    )
    company = models.ForeignKey(
        Company,
        related_name='user_accounts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions ',
        verbose_name='company'
    )
    created_at = models.DateTimeField(
        verbose_name="Created At",
        auto_now_add=True,
        blank=True, null=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated At",
        auto_now=True,
        blank=True, null=True
    )
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"User account {self.first_name} ID: {self.id}  Email: {self.email} ({self.role}) - {status}"

    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"
        ordering = ['-updated_at', '-created_at']
        get_latest_by = "updated_at"
        unique_together = [('username', 'email')]