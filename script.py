import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from transactions.views import get_transaction_data

with open('unique_addresses.txt', 'r') as file:
    unique_addresses = [line.strip() for line in file.readlines()]


for address in unique_addresses:
    result = get_transaction_data(address)
    print(result)
