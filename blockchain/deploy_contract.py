from web3 import Web3, HTTPProvider
from solcx import compile_source

# web3 = Web3(HTTPProvider("https://sepolia.infura.io/v3/069ed309e7484022918cfca9a6d772f3"))
web3 = Web3(HTTPProvider("http://127.0.0.1:7545"))


contract_source_code = """
pragma solidity ^0.8.0;

contract CoffeeBeanSupplyChain {
    struct CoffeeBeanBatch {
        string batchId;
        string farmName;
        string originCountry;
        uint256 harvestDate;
        string processingDetails;
        uint256 roastingDate;
        string packagingDetails;
        uint256 packagingDate;
        bool isShipped;
        bool isDelivered;
        string currentLocation;
    }

    mapping(string => CoffeeBeanBatch) public batches;

    event BatchAdded(string batchId);
    event BatchUpdated(string batchId);

    function addBatch(
        string memory batchId,
        string memory farmName,
        string memory originCountry,
        uint256 harvestDate
    ) public {
        require(bytes(batches[batchId].batchId).length == 0, "Batch already exists");
        
        batches[batchId] = CoffeeBeanBatch({
            batchId: batchId,
            farmName: farmName,
            originCountry: originCountry,
            harvestDate: harvestDate,
            processingDetails: "",
            roastingDate: 0,
            packagingDetails: "",
            packagingDate: 0,
            isShipped: false,
            isDelivered: false,
            currentLocation: farmName
        });

        emit BatchAdded(batchId);
    }

    function updateBatch(
        string memory batchId,
        string memory newProcessingDetails,
        uint256 newRoastingDate,
        string memory newPackagingDetails,
        uint256 newPackagingDate,
        bool newIsShipped,
        bool newIsDelivered,
        string memory newCurrentLocation
    ) public {
        require(bytes(batches[batchId].batchId).length != 0, "Batch does not exist");

        CoffeeBeanBatch storage batch = batches[batchId];
        batch.processingDetails = newProcessingDetails;
        batch.roastingDate = newRoastingDate;
        batch.packagingDetails = newPackagingDetails;
        batch.packagingDate = newPackagingDate;
        batch.isShipped = newIsShipped;
        batch.isDelivered = newIsDelivered;
        batch.currentLocation = newCurrentLocation;

        emit BatchUpdated(batchId);
    }

    function getBatchDetails(string memory batchId) public view returns (CoffeeBeanBatch memory, bool) {
    if (bytes(batches[batchId].batchId).length == 0) {
        return (CoffeeBeanBatch("", "", "", 0, "", 0, "", 0, false, false, ""), false);
    }
    return (batches[batchId], true);
}
}
"""

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:CoffeeBeanSupplyChain']

print("Contract ABI:")
print(contract_interface['abi'])

# account = "0xa7255745188F75a23b6e241c69D360AE606B2da2"
# private_key = "6214ca32dbc6e81217d6bcdd1f75c618691bc7e7943637d6202b182fed5e2d9d"
account = "0x10c9855c3F407852B28ec899aa3f5e8AF5D92D5D"
private_key = "0x1c3c37d74213ed8e50966f1a15cfac6320e7552031e05316c09b7b51a0719169"

checksum_address = web3.to_checksum_address(account)
nonce = web3.eth.get_transaction_count(checksum_address)


web3.eth.default_account = web3.to_checksum_address(account)
MyContract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

transaction_data = MyContract.constructor().build_transaction({
    'gas': 3000000,
    'gasPrice': web3.to_wei('50', 'gwei'),
    'nonce': nonce,
})

private_key_bytes = private_key
signed_transaction = web3.eth.account.sign_transaction(transaction_data, private_key_bytes)
account_bytes = bytes.fromhex(account[2:])
tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
print(f"Transaction sent: {tx_hash.hex()}")
print(tx_hash)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
contract_address = tx_receipt['contractAddress']
print(f"Contract deployed at address: {contract_address}")










