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
    name = models.CharField(max_length=64)
    date = models.DateField()
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'Benefit {self.investment} - {self.date}: {self.amount}'


class OperatingCost(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField()
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MaxValueValidator(0)])

    def __str__(self):
        return f'Operating Cost {self.investment} - {self.date}: {self.amount}'


class ImplementationCost(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField()
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MaxValueValidator(0)])

    def __str__(self):
        return f'Implementation Cost {self.investment} - {self.date}: {self.amount}'


class Asset(models.Model):
    DEPRECIATION_CHOICES = [
        (1, '1 year'),
        (2, '2 years'),
        (5, '5 years'),
        (10, '10 years'),
    ]

    name = models.CharField(max_length=64)
    date = models.DateField()
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    depreciation_period = models.IntegerField(choices=DEPRECIATION_CHOICES)

    def __str__(self):
        return f'Asset {self.investment} - {self.date}: {self.amount}'


class Depreciation(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MaxValueValidator(0)])

    def __str__(self):
        return f'Depreciation of {self.asset} - {self.date}: {self.amount}'
