from deploy import voting_contract as vc, nonce, chain_id, my_address, w3
from web3 import Web3
import os

# working with deployed contract

print(f"chairperson: {vc.functions.chairperson().call()}")

give_right_to_vote_array = [
    "0x3778a4b1D4aBE795C64bCFAa5EeF72450bAe52C1",
    "0x0fb7a9b4FAD1Ee12d0DF0A736c21e59B56674414",
]

# giving the right to vote
for i in give_right_to_vote_array:
    nonce = nonce + 1
    give_right_to_vote_transaction = vc.functions.giveRightToVote(i).buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    signed_give_right_to_vote_txn = w3.eth.account.sign_transaction(
        give_right_to_vote_transaction, private_key=os.getenv("PRIVATE_KEY")
    )
    tx_give_right_to_vote_hash = w3.eth.send_raw_transaction(
        signed_give_right_to_vote_txn.rawTransaction
    )
    print("chairperson gives a right to vote to ", i)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_give_right_to_vote_hash)

# delegation
d_nonce = w3.eth.getTransactionCount("0x3778a4b1D4aBE795C64bCFAa5EeF72450bAe52C1")
delegate_transaction = vc.functions.delegate(
    "0x0fb7a9b4FAD1Ee12d0DF0A736c21e59B56674414"
).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": "0x3778a4b1D4aBE795C64bCFAa5EeF72450bAe52C1",
        "nonce": d_nonce,
    }
)
signed_delegate_txn = w3.eth.account.sign_transaction(
    delegate_transaction, private_key=os.getenv("PRIVATE_KEY_DELEGATE")
)
tx_delegate_hash = w3.eth.send_raw_transaction(signed_delegate_txn.rawTransaction)
print(
    "0x3778a4b1D4aBE795C64bCFAa5EeF72450bAe52C1",
    " delegates his right to vote to ",
    "0x0fb7a9b4FAD1Ee12d0DF0A736c21e59B56674414",
)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_delegate_hash)

# voting
v_nonce = w3.eth.getTransactionCount("0x0fb7a9b4FAD1Ee12d0DF0A736c21e59B56674414")
vote_transaction = vc.functions.vote(1).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": "0x0fb7a9b4FAD1Ee12d0DF0A736c21e59B56674414",
        "nonce": v_nonce,
    }
)
signed_vote_txn = w3.eth.account.sign_transaction(
    vote_transaction, private_key=os.getenv("PRIVATE_KEY_VOTE")
)
tx__vote_hash = w3.eth.send_raw_transaction(signed_vote_txn.rawTransaction)
print(
    "0x0fb7a9b4FAD1Ee12d0DF0A736c21e59B56674414",
    "votes for ",
    "0x4A30fd338b38efE692330f82279913BDd93D33Bb",
)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx__vote_hash)

print("winner: ", Web3.toHex(vc.functions.winnerName().call()))
