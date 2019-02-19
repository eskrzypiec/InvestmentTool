from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Investment(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    approved = models.BooleanField(default=False)
    approver = models.ManyToManyField(User, related_name="approver")

    def __str__(self):
        return f'Investment {self.name}'


class Benefit(models.Model):
    description = models.TextField()
    date = models.DateField()
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'Benefit {self.investment} - {self.date}: {self.amount}'


class OperatingCost(models.Model):
    description = models.TextField()
    date = models.DateField()
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MaxValueValidator(0)])

    def __str__(self):
        return f'Operating Cost {self.investment} - {self.date}: {self.amount}'


class ImplementationCost(models.Model):
    description = models.TextField()
    date = models.DateField()
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MaxValueValidator(0)])

    def __str__(self):
        return f'Implementation Cost {self.investment} - {self.date}: {self.amount}'
