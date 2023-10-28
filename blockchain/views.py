from django.shortcuts import render
from web3 import Web3

# Ethereum setup
infura_url = 'https://sepolia.infura.io/v3/069ed309e7484022918cfca9a6d772f3'
web3 = Web3(Web3.HTTPProvider(infura_url))

# Replace 'YOUR_CONTRACT_ADDRESS' with the deployed smart contract address
contract_address = '0x2B6648D0a6503FA07c86f06d8c2c4d38f46F8d3d'
contract_address_bytes = web3.to_checksum_address(contract_address)

# Replace 'YOUR_CONTRACT_ABI' with the ABI (Application Binary Interface) of your smart contract
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "itemId",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "itemData",
                "type": "string"
            }
        ],
        "name": "addItem",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "name": "items",
        "outputs": [
            {
                "internalType": "string",
                "name": "itemData",
                "type": "string"
            },
            {
                "internalType": "bool",
                "name": "verified",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "itemId",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "itemData",
                "type": "string"
            }
        ],
        "name": "verifyItem",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

account = "0xa7255745188F75a23b6e241c69D360AE606B2da2"
private_key = "6214ca32dbc6e81217d6bcdd1f75c618691bc7e7943637d6202b182fed5e2d9d"

contract = web3.eth.contract(address=contract_address_bytes, abi=contract_abi)


def store_data(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        item_data = request.POST['item_data']

        # Set up transaction details
        transaction = contract.functions.addItem(item_id, item_data).build_transaction({
            'chainId': 11155111,  # For Sepolia test network
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'nonce': web3.eth.get_transaction_count(web3.to_checksum_address(account)),
        })

        # Sign the transaction
        private_key_bytes = bytes.fromhex(private_key)
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key_bytes)

        # Send signed transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return render(request, 'success.html', {'item_id': item_id, 'item_data': item_data, 'tx_hash': tx_hash.hex()})

    return render(request, 'add_item.html')


def verify_data(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        item_data = request.POST['item_data']

        # Check data integrity using the smart contract's verifyItem function
        is_verified = contract.functions.verifyItem(item_id, item_data).call()

        return render(request, 'verification_result.html', {'item_id': item_id, 'item_data': item_data, 'is_verified': is_verified})

    return render(request, 'verify_data.html')


def view_items(request):
    # Note: Your smart contract doesn't have a method to retrieve all item IDs.
    # So, for this dummy function, we assume some mechanism or you can enhance the smart contract.
    # This is just a placeholder:
    item_ids = []  # You would need to fill this with the actual item IDs

    # Fetch item details for each item ID
    items = [{'item_id': item_id, 'item_data': contract.functions.items(item_id).call()[0]} for item_id in item_ids]

    return render(request, 'view_items.html', {'items': items})
