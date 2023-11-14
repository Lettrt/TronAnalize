from django.db.models import Avg, StdDev
from .models import Transaction

def calculate_transaction_statistics():
    transactions = Transaction.objects.filter(amount__gte=10)
    
    average = transactions.aggregate(Avg('amount'))['amount__avg']
    stddev = transactions.aggregate(StdDev('amount'))['amount__stddev']
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
