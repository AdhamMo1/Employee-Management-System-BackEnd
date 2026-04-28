from django.db import models

from backend_apps.companies.models import Company


class Department(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='company'
    )
    name = models.CharField(max_length=255, verbose_name='name', help_text='The name of the department')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "departments"
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f"Department ID: {self.id} - Department Name: {self.name}"