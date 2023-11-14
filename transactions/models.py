from django.db import models

class Transaction(models.Model):
    tx_id = models.CharField(max_length=100, primary_key=True)
    block_number = models.BigIntegerField()
    timestamp = models.DateTimeField()
    contract_ret = models.CharField(max_length=100)
    amount = models.BigIntegerField()
    owner_address = models.CharField(max_length=100)
    to_address = models.CharField(max_length=100)

    def __str__(self):
        return self.tx_id
