async function main() {
  // Grab the contract factory
  const CistercianDate = await ethers.getContractFactory("CistercianDate");

  // Start deployment, returning a promise that resolves to a contract object
  const cistercianDateNFT = await CistercianDate.deploy(); // Instance of the contract
  console.log("Contract deployed to address:", cistercianDateNFT.address);
}

main()
 .then(() => process.exit(0))
 .catch(error => {
   console.error(error);
   process.exit(1);
 });