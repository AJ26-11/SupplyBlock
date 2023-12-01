from django.http import JsonResponse
import json
from .models import Batch
from django.shortcuts import render, redirect
from web3 import Web3
import time
from datetime import datetime

# infura_url = 'https://sepolia.infura.io/v3/069ed309e7484022918cfca9a6d772f3'
infura_url = 'http://127.0.0.1:7545'
web3 = Web3(Web3.HTTPProvider(infura_url))

# contract_address = '0x18ee332e1943524a797Bf58433b2782d58aacA2A'
contract_address = '0x9aC7C272723EFdF140B0c2fFDBeE69093A885e92'
contract_address_bytes = web3.to_checksum_address(contract_address)

contract_abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "string", "name": "batchId", "type": "string"}
        ],
        "name": "BatchAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "string", "name": "batchId", "type": "string"}
        ],
        "name": "BatchUpdated",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "batchId", "type": "string"},
            {"internalType": "string", "name": "farmName", "type": "string"},
            {"internalType": "string", "name": "originCountry", "type": "string"},
            {"internalType": "uint256", "name": "harvestDate", "type": "uint256"}
        ],
        "name": "addBatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "", "type": "string"}
        ],
        "name": "batches",
        "outputs": [
            {"internalType": "string", "name": "batchId", "type": "string"},
            {"internalType": "string", "name": "farmName", "type": "string"},
            {"internalType": "string", "name": "originCountry", "type": "string"},
            {"internalType": "uint256", "name": "harvestDate", "type": "uint256"},
            {"internalType": "string", "name": "processingDetails", "type": "string"},
            {"internalType": "uint256", "name": "roastingDate", "type": "uint256"},
            {"internalType": "string", "name": "packagingDetails", "type": "string"},
            {"internalType": "uint256", "name": "packagingDate", "type": "uint256"},
            {"internalType": "bool", "name": "isShipped", "type": "bool"},
            {"internalType": "bool", "name": "isDelivered", "type": "bool"},
            {"internalType": "string", "name": "currentLocation", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "batchId", "type": "string"}
        ],
        "name": "getBatchDetails",
        "outputs": [
            {
                "components": [
                    {"internalType": "string", "name": "batchId", "type": "string"},
                    {"internalType": "string", "name": "farmName", "type": "string"},
                    {"internalType": "string", "name": "originCountry", "type": "string"},
                    {"internalType": "uint256", "name": "harvestDate", "type": "uint256"},
                    {"internalType": "string", "name": "processingDetails", "type": "string"},
                    {"internalType": "uint256", "name": "roastingDate", "type": "uint256"},
                    {"internalType": "string", "name": "packagingDetails", "type": "string"},
                    {"internalType": "uint256", "name": "packagingDate", "type": "uint256"},
                    {"internalType": "bool", "name": "isShipped", "type": "bool"},
                    {"internalType": "bool", "name": "isDelivered", "type": "bool"},
                    {"internalType": "string", "name": "currentLocation", "type": "string"}
                ],
                "internalType": "struct CoffeeBeanSupplyChain.CoffeeBeanBatch",
                "name": "",
                "type": "tuple"
            },
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "batchId", "type": "string"},
            {"internalType": "string", "name": "newProcessingDetails", "type": "string"},
            {"internalType": "uint256", "name": "newRoastingDate", "type": "uint256"},
            {"internalType": "string", "name": "newPackagingDetails", "type": "string"},
            {"internalType": "uint256", "name": "newPackagingDate", "type": "uint256"},
            {"internalType": "bool", "name": "newIsShipped", "type": "bool"},
            {"internalType": "bool", "name": "newIsDelivered", "type": "bool"},
            {"internalType": "string", "name": "newCurrentLocation", "type": "string"}
        ],
        "name": "updateBatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

account = "0x5A5cE81e835ce18DCaF8CD24CeeE9815dF79a2eC"
private_key = "0x050e639bf8cd717bfe34e7271baafd9f304bbc68ec585d821d5075b14efd7c6c"

contract = web3.eth.contract(address=contract_address_bytes, abi=contract_abi)


def send_transaction(contract_function, *args):
    transaction = contract_function(*args).build_transaction({
        'chainId': 1337,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(web3.to_checksum_address(account)),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    return web3.eth.send_raw_transaction(signed_txn.rawTransaction)


def convert_date_to_unix(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return int(time.mktime(dt.timetuple()))
    except ValueError:
        return 0


def add_batch(request):
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        if Batch.objects.filter(batch_id=batch_id).exists():
            return render(request, 'add_batch.html', {'error': 'BatchID already exists'})
        farm_name = request.POST.get('farm_name')
        origin_country = request.POST.get('origin_country')
        harvest_date_str = request.POST.get('harvest_date')
        harvest_date = convert_date_to_unix(harvest_date_str)

        tx_hash = send_transaction(contract.functions.addBatch, batch_id, farm_name, origin_country, harvest_date)
        Batch.objects.create(batch_id=batch_id)
        return render(request, 'success.html', {'tx_hash': tx_hash.hex()})
    return render(request, 'add_batch.html')


def view_batch(request):
    batches = Batch.objects.all()
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        if not Batch.objects.filter(batch_id=batch_id).exists():
            return render(request, 'view_batch.html', {'error': 'BatchID does not exist'})
        try:
            result = contract.functions.getBatchDetails(batch_id).call()
            batch_details, is_successful = result
            if not is_successful:
                return render(request, 'view_batch.html', {'error': 'Batch not found'})

            details = {
                'batch_id': batch_details[0],
                'farm_name': batch_details[1],
                'origin_country': batch_details[2],
                'harvest_date': datetime.utcfromtimestamp(batch_details[3]).strftime('%Y-%m-%d'),
                'processing_details': batch_details[4],
                'roasting_date': datetime.utcfromtimestamp(batch_details[5]).strftime('%Y-%m-%d') if batch_details[
                    5] else '',
                'packaging_details': batch_details[6],
                'packaging_date': datetime.utcfromtimestamp(batch_details[7]).strftime('%Y-%m-%d') if batch_details[
                    7] else '',
                'is_shipped': batch_details[8],
                'is_delivered': batch_details[9],
                'current_location': batch_details[10]
            }
        except Exception as e:
            print(e)
            return render(request, 'view_batch.html', {'error': 'An error occurred'})

        return render(request, 'view_batch.html', {'batch_details': details})

    return render(request, 'view_batch.html', {'batches': batches})


def update_batch(request):
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        if not Batch.objects.filter(batch_id=batch_id).exists():
            return render(request, 'update_batch.html', {'error': 'BatchID does not exist'})
        new_processing_details = request.POST.get('processing_details')
        new_packaging_details = request.POST.get('packaging_details')
        new_current_location = request.POST.get('current_location')
        new_is_shipped = request.POST.get('is_shipped') == 'on'
        new_is_delivered = request.POST.get('is_delivered') == 'on'

        new_roasting_date = convert_date_to_unix(request.POST.get('roasting_date'))
        new_packaging_date = convert_date_to_unix(request.POST.get('packaging_date'))

        tx_hash = send_transaction(
            contract.functions.updateBatch,
            batch_id,
            new_processing_details,
            new_roasting_date,
            new_packaging_details,
            new_packaging_date,
            new_is_shipped,
            new_is_delivered,
            new_current_location
        )
        return render(request, 'success.html', {'tx_hash': tx_hash.hex()})
    return render(request, 'update_batch.html')


def check_batch_id(request):
    data = json.loads(request.body)
    batch_id = data.get('batch_id')
    is_available = not Batch.objects.filter(batch_id=batch_id).exists()
    return JsonResponse({'available': is_available})


def fetch_batch_data(request):
    data = json.loads(request.body)
    batch_id = data.get('batch_id')
    if Batch.objects.filter(batch_id=batch_id).exists():
        try:
            result = contract.functions.getBatchDetails(batch_id).call()
            batch_details, is_successful = result
            if not is_successful:
                return JsonResponse({'success': False, 'error': 'Batch not found on the blockchain'})

            details = {
                'batch_id': batch_details[0],
                'farm_name': batch_details[1],
                'origin_country': batch_details[2],
                'harvest_date': datetime.utcfromtimestamp(batch_details[3]).strftime('%Y-%m-%d'),
                'processing_details': batch_details[4],
                'roasting_date': datetime.utcfromtimestamp(batch_details[5]).strftime('%Y-%m-%d') if batch_details[
                    5] else '',
                'packaging_details': batch_details[6],
                'packaging_date': datetime.utcfromtimestamp(batch_details[7]).strftime('%Y-%m-%d') if batch_details[
                    7] else '',
                'is_shipped': batch_details[8],
                'is_delivered': batch_details[9],
                'current_location': batch_details[10]
            }
            return JsonResponse({'success': True, 'batch_data': details})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': 'An error occurred while fetching data'})

    return JsonResponse({'success': False, 'error': 'BatchID does not exist in the local database'})
