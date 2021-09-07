# converting mint-nft.js to python
# from this tutorial https://docs.alchemy.com/alchemy/tutorials/how-to-create-an-nft/how-to-mint-a-nft

import os
from dotenv import load_dotenv
from web3 import Web3
import json
from utils import get_project_root

load_dotenv()

# Get required env variables
API_URL = os.environ.get("API_URL")
PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

# Establish Web3 connection
w3 = Web3(Web3.HTTPProvider(API_URL))

# Read the contract file
project_root = get_project_root()
contract_file = os.path.join(project_root, "artifacts/contracts/CistercianDate.sol/CistercianDate.json")
with open(contract_file) as f:
  contract = json.load(f)

# address of the deployed contract from deploy_contract.js
contract_address = Web3.toChecksumAddress("0x3799E2fe97b43010fBe60E8922D3D3dCf2DdC2d7")
nft_contract = w3.eth.contract(abi=contract['abi'], address=contract_address)

def mintNFT(tokenURI):
  nonce = w3.eth.get_transaction_count(PUBLIC_KEY, 'latest')
  estimated_gas = nft_contract.functions.mintNFT(PUBLIC_KEY, tokenURI).estimateGas({"from": PUBLIC_KEY})
  data = nft_contract.encodeABI(fn_name="mintNFT", args=[PUBLIC_KEY, tokenURI])

  tx = {
    'from': PUBLIC_KEY,
    'nonce': nonce,
    'gasPrice': w3.eth.gas_price,
    'gas': estimated_gas
  }

  built_txn = nft_contract.functions.mintNFT(PUBLIC_KEY, tokenURI).buildTransaction(tx)
  built_txn['data'] = data
  signed_txn = w3.eth.account.sign_transaction(built_txn, private_key=PRIVATE_KEY)
  hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
  response = w3.eth.wait_for_transaction_receipt(hash)

  return response