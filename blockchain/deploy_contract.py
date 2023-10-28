from web3 import Web3, HTTPProvider
from solcx import compile_source

# Set up Ethereum connection
web3 = Web3(HTTPProvider("https://sepolia.infura.io/v3/069ed309e7484022918cfca9a6d772f3"))

# Compile the smart contract source code
contract_source_code = """
pragma solidity ^0.8.0;

contract SupplyChain {
    struct Item {
        string itemData;
        bool verified;
    }

    mapping(string => Item) public items;

    function addItem(string memory itemId, string memory itemData) public {
        require(!items[itemId].verified, "Item already verified");
        items[itemId] = Item(itemData, false);
    }

    function verifyItem(string memory itemId, string memory itemData) public view returns (bool) {
        return keccak256(abi.encodePacked(items[itemId].itemData)) == keccak256(abi.encodePacked(itemData));
    }
}
"""

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:SupplyChain']

print("Contract ABI:")
print(contract_interface['abi'])

# Deploy the smart contract
account = "0xa7255745188F75a23b6e241c69D360AE606B2da2"
private_key = "6214ca32dbc6e81217d6bcdd1f75c618691bc7e7943637d6202b182fed5e2d9d"

checksum_address = web3.to_checksum_address(account)
nonce = web3.eth.get_transaction_count(checksum_address)


web3.eth.default_account = web3.to_checksum_address(account)
MyContract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

transaction_data = MyContract.constructor().build_transaction({
    'gas': 300000,
    'gasPrice': web3.to_wei('20', 'gwei'),
    'nonce': nonce,
})

private_key_bytes = bytes.fromhex(private_key)
signed_transaction = web3.eth.account.sign_transaction(transaction_data, private_key_bytes)
account_bytes = bytes.fromhex(account[2:])
tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt['contractAddress']
print(f"Contract deployed at address: {contract_address}")







