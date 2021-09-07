Process to deplo NFTs

1. Deploy Contract

```
npx hardhat compile
npx hardhat run scripts/deploy_contract.js --network rinkeby
```

2. Take the address of the contract and put it into `mint_nft.py` file
3. Set the dates you want to run script for in `main.py`
4. Start the script `poetry run python scripts/main.py`.