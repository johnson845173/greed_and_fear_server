from setu import Deeplink
from setu.contract import RefundRequestItem, SetuAPIException

dl = Deeplink(
    scheme_id="c4f57443-dc1e-428f-8c4e-e5fd531057d2",
    secret="5b288618-473f-4193-ae1b-8c42f223798e",
    product_instance_id="861023031961584801",
    auth_type="OAUTH",
    mode="SANDBOX",
)

bill_amount = 120
try:
    link = dl.create_payment_link(
        amount_value=bill_amount,
        biller_bill_id="test_transaction_1234",
        amount_exactness="EXACT",
        payee_name="Python SDK unittest",
        transaction_note="unittest transaction",
    )
    print(link.payment_link.upi_link)
    assert link.payment_link.upi_id == "7899404714@ybl"
except SetuAPIException as e:
    assert False