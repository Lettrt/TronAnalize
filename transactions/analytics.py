import os
import sys
from pathlib import Path

project_path = Path('/home/letterbe/develops/blockchain/tronAnaliz')
sys.path.append(str(project_path))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

import numpy as np
from transactions.models import Transaction

def calculate_transaction_statistics():
    amounts = list(Transaction.objects.filter(amount__gte=10).values_list('amount', flat=True)) # gte - greater than or equal to
    average = np.mean(amounts)
    stddev = np.std(amounts)
    return average, stddev

def find_anomalies(average, stddev, multiplier=3):
    lower_threshold = average - (multiplier * stddev)
    upper_threshold = average + (multiplier * stddev)
    anomalies = Transaction.objects.filter(
        amount__lt=lower_threshold
    ) | Transaction.objects.filter(
        amount__gt=upper_threshold
    )
    return anomalies

if __name__ == "__main__":
    average, stddev = calculate_transaction_statistics()
    anomalies = find_anomalies(average, stddev)
    
    print(f"Среднее значение: {average}")
    print(f"Стандартное отклонение: {stddev}")
    print(f"Найдено аномальных транзакций: {anomalies.count()}")
    
    for anomaly in anomalies:
        print(f"ID транзакции: {anomaly.tx_id}, Сумма: {anomaly.amount}")
