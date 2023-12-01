from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
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