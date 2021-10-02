/**
* @type import('hardhat/config').HardhatUserConfig
*/
require('dotenv').config();
require("@nomiclabs/hardhat-ethers");
require('@openzeppelin/hardhat-upgrades');

const { API_URL, PRIVATE_KEY } = process.env;

module.exports = {
   solidity: "0.8.0",
   defaultNetwork: "rinkeby",
   networks: {
     hardhat: {},
     polygon_mainnet: {
        url: API_URL,
        accounts: [`0x${PRIVATE_KEY}`]
     },
     matic_testnet: {
        url: API_URL,
        accounts: [`0x${PRIVATE_KEY}`]
     },
     rinkeby: {
        url: API_URL,
        accounts: [`0x${PRIVATE_KEY}`]
     }
   },
}
