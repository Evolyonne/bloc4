import algokit_utils as au
import algosdk as sdk
from utils import (
    account_creation,
    display_info,
)

algorand = au.AlgorandClient.from_environment()

algod_client = algorand.client.algod
indexer_client = algorand.client.indexer

print(algod_client.block_info(0))
print(indexer_client.health())

alice = account_creation(algorand, "ALICE", au.AlgoAmount(algo=10_000))
bob = account_creation(algorand, "BOB", au.AlgoAmount(algo=100))

sdk.mnemonic.from_private_key(alice.private_key)

pay_txn = algorand.create_transaction.payment(au.PaymentParams(
 sender=alice.address,
 receiver=bob.address,
 amount=au.AlgoAmount(algo=1)
))

pay_txn_signed = pay_txn.sign(alice.private_key)

tx_id = algorand.client.algod.send_transaction(txn=pay_txn_signed)

res = sdk.transaction.wait_for_confirmation(algod_client=algod_client, txid=tx_id)

print(res)

payback_txn = algorand.send.payment(au.PaymentParams(
 sender=bob.address,
 receiver=alice.address,
 amount=au.AlgoAmount(algo=1)
))

print('Transaction confirmed, round: 'f'{payback_txn.confirmation["confirmed-round"]}')