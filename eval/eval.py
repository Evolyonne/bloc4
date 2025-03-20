import algokit_utils as au

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
algorand = au.AlgorandClient.testnet()

mnemonic = "achieve cook carry estate combine cycle wave flag husband rather manage join catalog sugar clown clay survey impact begin three mass dry arrow ability assume"
#recuperer la clé privée en local
laury = algorand.account.from_mnemonic(mnemonic=mnemonic)


if __name__ == "__main__":
    factory = algorand.client.get_typed_app_factory(
        cl.EvalFactory, default_sender=laury.address
    )

    app_id = 736038676

    ac = factory.get_app_client_by_id(app_id, default_sender=laury.address)


 #claim algo
    # ac.send.claim_algo(au.CommonAppCallParams(sender=laury.address, signer=laury.signer), send_params=au.SendParams(
    #         populate_app_call_resources=True
    #     )
    # )

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

    asset_id = int(asset.confirmation["asset-index"])
    print(f"Asset {asset_id} created")


    # print(f"Asset {asset.asset_id} created")

    mbr_pay_txn = algorand.create_transaction.payment(
            au.PaymentParams(
                sender=laury.address,
                receiver=ac.app_address,
                amount=au.AlgoAmount(algo=0.2),
                extra_fee=au.AlgoAmount(micro_algo=algorand.get_suggested_params().min_fee)
            )
        )

    #opt in to asset
    ac.send.opt_in_to_asset(
        cl.OptInToAssetArgs(
            mbr_pay=att.TransactionWithSigner(mbr_pay_txn, laury.signer),
            asset=asset_id
        ),
        send_params=au.SendParams(populate_app_call_resources=True)
    )

    ac.send.sum(cl.SumArgs(array=bytes([1, 2])), send_params=au.SendParams(
            populate_app_call_resources=True
        )
    )

    ac.send.update_box(cl.UpdateBoxArgs(value="Hello Clermont"), send_params=au.SendParams(
            populate_app_call_resources=True
        )
    )




