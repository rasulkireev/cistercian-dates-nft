# converting mint-nft.js to python
# from this tutorial
# https://docs.alchemy.com/alchemy/tutorials/how-to-create-an-nft/how-to-mint-a-nft

import json
import logging
import os
import time

from dotenv import load_dotenv
from utils import get_project_root
from web3 import Web3
from web3._utils.threads import Timeout
from web3.exceptions import TimeExhausted

logger = logging.getLogger(__name__)

load_dotenv()

# Get required env variables
API_URL = os.environ.get("API_URL")
PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
CONTRACT = os.environ.get("CONTRACT")

# Establish Web3 connection
w3 = Web3(Web3.HTTPProvider(API_URL))

# Read the contract file
project_root = get_project_root()
contract_file = os.path.join(
    project_root, "artifacts/contracts/CistercianDate.sol/CistercianDate.json"
)
with open(contract_file, encoding="utf-8") as f:
    contract = json.load(f)

# address of the deployed contract from deploy_contract.js
contract_address = Web3.toChecksumAddress(CONTRACT)
nft_contract = w3.eth.contract(abi=contract["abi"], address=contract_address)


def mintNFT(tokenURI):

    logger.info("Beggining the Minting Process")

    for attempt_num in range(10):

        tx = {
            "from": PUBLIC_KEY,
            "nonce": int(
                w3.eth.get_transaction_count(PUBLIC_KEY, "latest")
                + attempt_num
            ),
            "gasPrice": int(w3.eth.gas_price * 1.15),
            "gas": int(
                nft_contract.functions.mintNFT(
                    PUBLIC_KEY, tokenURI
                ).estimateGas({"from": PUBLIC_KEY})
                * 1.15
            ),
        }

        logging.info("Building Transaction")
        built_txn = nft_contract.functions.mintNFT(
            PUBLIC_KEY, tokenURI
        ).buildTransaction(tx)

        logging.info("Updating Transaction Data")
        built_txn["data"] = nft_contract.encodeABI(
            fn_name="mintNFT", args=[PUBLIC_KEY, tokenURI]
        )

        logging.info("Signing Transaction")
        signed_txn = w3.eth.account.sign_transaction(
            built_txn, private_key=PRIVATE_KEY
        )

        try:
            logging.info("Sending Signed Transactions (Raw)")
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            break
        except ValueError as e:
            logging.error(
                (
                    f"Value Error: {e}."
                    f"(Attempt #{attempt_num})."
                    f"Trying once more."
                    f"Attempted transaction: {tx}"
                )
            )
            time.sleep(1.5)
            continue

    for attempt_num in range(10):
        try:
            logging.info("Waiting for Transaction Receipt")
            response = w3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=1200
            )
            break
        except (Timeout, TimeExhausted) as e:
            logging.error(
                f"Timeout Error: {e}. (Attempt #{attempt_num}). Trying once more."
            )
            continue

    return tx, response
