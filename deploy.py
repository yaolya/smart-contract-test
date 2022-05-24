from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./voting.sol", "r") as file:
    contract_file = file.read()

# compile solidity
install_solc("0.7.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"voting.sol": {"content": contract_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.7.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["voting.sol"]["Ballot"]["evm"]["bytecode"][
    "object"
]

abi = json.loads(compiled_sol["contracts"]["voting.sol"]["Ballot"]["metadata"])[
    "output"
]["abi"]

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xcA541b2Db42Bbfd557c5b870656A928786CECAc6"
private_key = os.getenv("PRIVATE_KEY")

# create contract
voting_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(my_address)
# transaction that deploys the contract
transaction = voting_contract.constructor(
    [
        "0x08b7675e860FA0483ca1CAc64345b1B1dffaE729",  # candidates addresses
        "0x4A30fd338b38efE692330f82279913BDd93D33Bb",
    ]
).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("deploying contract")

# send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("waiting for transaction to be mined...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)  # transaction receipt
print(f"contract deployed to {tx_receipt.contractAddress}")

# get deployed contract
voting_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
