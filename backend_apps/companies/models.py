from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "companies"
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f"Company ID: {self.id} - Company Name: {self.name}"