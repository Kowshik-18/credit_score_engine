from django.db import models

class WalletInfo(models.Model):
    name = models.CharField(max_length=100)
    wallet_no = models.PositiveIntegerField(unique=True)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=10, decimal_places=3)
    age = models.PositiveIntegerField()
    occupation = models.CharField(max_length=50)

    def __str__(self):
        return str(self.wallet_no)
