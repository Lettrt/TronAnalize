from django.http import JsonResponse
from .models import Transaction
import requests
from django.utils import timezone

def get_transaction_data(request, address):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions"
    response = requests.get(url)
    if response.status_code == 200:
        transactions_data = response.json().get('data', [])
        
        for transaction in transactions_data:
            tx_id = transaction.get('txID')
            block_number = transaction.get('blockNumber')
            timestamp = timezone.make_aware(timezone.datetime.fromtimestamp(transaction.get('block_timestamp') / 1000))
            contract_ret = transaction.get('ret')[0].get('contractRet')
            
            raw_data_contract = transaction.get('raw_data', {}).get('contract', [])[0]
            parameter = raw_data_contract.get('parameter', {}).get('value', {})
            amount = parameter.get('amount')
            owner_address = parameter.get('owner_address')
            to_address = parameter.get('to_address')
            
            Transaction.objects.update_or_create(
                tx_id=tx_id,
                defaults={
                    'block_number': block_number,
                    'timestamp': timestamp,
                    'contract_ret': contract_ret,
                    'amount': amount,
                    'owner_address': owner_address,
                    'to_address': to_address,
                }
            )
        
        return JsonResponse({'success': True, 'transactions': len(transactions_data)})
    else:
        return JsonResponse({'error': 'Ошибка запроса к API'}, status=response.status_code)
