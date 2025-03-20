import os
import algosdk as sdk
import algokit_utils as au
from algokit_utils.models.account import SigningAccount

import client as cl

import algokit_utils.transactions.transaction_composer as att

from utils import (
    account_creation,
    display_info,
    box_abi,
    get_min_balance_required,
    sha256_encode,
    sha256_digest
)



mnemonic = "achieve cook carry estate combine cycle wave flag husband rather manage join catalog sugar clown clay survey impact begin three mass dry arrow ability assume"
#recuperer la clé privée en local
private_key = sdk.mnemonic.to_private_key(mnemonic)
#recuperer l'account en local
account = sdk.account.address_from_private_key(private_key)

print (account)

# os.system("algokit compile py --out-dir ./app app.py")
# os.system("algokit generate client app/Eval.arc32.json --output client.py")


if __name__ == "__main__":
    algorand = au.AlgorandClient.from_environment()

    #recuperer le client
    client = algorand.client
    algod_client = algorand.client.algod
    indexer_client = algorand.client.indexer

    print(algod_client.block_info(0))
    print(indexer_client.health())

    #cree le compte
    laury = account_creation(algorand, "laury", au.AlgoAmount(algo=10000))
    with open(".env", "w") as file:
        file.write(sdk.mnemonic.from_private_key(laury.private_key))

    #recuperer le factory
    factory = algorand.client.get_typed_app_factory(
        cl.EvalFactory, default_sender=laury.address
    )

    if len(algorand.account.get_information(laury.address).created_apps) > 0:
        app_id = algorand.account.get_information(laury.address).created_apps[0]["id"]
    else:

        result, _ = factory.send.create.bare()
        app_id = result.app_id
    ac = factory.get_app_client_by_id(app_id, default_sender=laury.address)
    print(f"App {app_id} deployed with address {ac.app_address}")

    #avoir la box key
    box_key = laury.public_key

    args = cl.AddStudentsArgs(account=laury.address)

    param = au.CommonAppCallParams(sender=laury.address, signer=laury.signer)

    # mettre de l'argent sur le compte laury
    algorand.account.ensure_funded(ac.app_address, laury, min_spending_balance=au.AlgoAmount(micro_algo=3_000_000), min_funding_increment=au.AlgoAmount(micro_algo=1_000_000))


    #ajouter un etudiant
    ac.send.add_students(args, send_params=au.SendParams(
            populate_app_call_resources=True
        )
    )

    #claim algo
    ac.send.claim_algo(param, send_params=au.SendParams(
            populate_app_call_resources=True
        )
    )

    #creer asset
    asset = algorand.send.asset_create(
        au.AssetCreateParams(
            sender=laury.address,
            signer=laury.signer,
            total=15,
            decimals=0,
            default_frozen=False,
            unit_name="PY-CL-FD",  # 8 Max
            asset_name="Proof of Attendance Py-Clermont",
            url="https://pyclermont.org/",
            note="Hello Clermont",
        )
    )

    print(f"Asset {asset.asset_id} created")

    mbr_pay_txn = algorand.create_transaction.payment(
            au.PaymentParams(
                sender=laury.address,
                receiver=ac.app_address,
                amount=au.AlgoAmount(algo=0.2),
                extra_fee=au.AlgoAmount(micro_algo=algorand.get_suggested_params().min_fee)
            )
        )

    ac.send.opt_in_to_asset(
        cl.OptInToAssetArgs(
            mbr_pay=att.TransactionWithSigner(mbr_pay_txn, laury.signer),
            asset=asset.asset_id
        ),
        send_params=au.SendParams(populate_app_call_resources=True)
    )











