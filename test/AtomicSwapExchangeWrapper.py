from punica.invoke.invoke_contract import Invoke
from punica.test.test import Test
import WalletWrapper
import SdkUtils
from Utils import GetDeployedContractAddress, FormatOntIdParam


gas_limit = SdkUtils.g_gasLimit
gas_price = 0
abi_path = './contracts/build/AtomicSwapExchange_abi.json'
contract_address = bytes.fromhex(GetDeployedContractAddress("AtomicSwapExchange"))
abi_info = Test.get_abi_info(abi_path)
alice = WalletWrapper.Alice()
aliceAddress = WalletWrapper.AliceAddress()

def initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock):
    preExec = False
    params = dict()
    params["amountOfOntToSell"] = amountOfOntToSell
    params["amountOfEthToBuy"] = amountOfEthToBuy
    params["hashlock"] = "String:" + hashlock
    # params["acct"] = "ByteArray:" + aliceAddress
    abiFunction = Invoke.get_function(params, 'intiate_order', abi_info)
    return SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)

def get_orders():
    preExec = True
    params = dict()
    abiFunction = Invoke.get_function(params, 'get_orders', abi_info)
    return SdkUtils.SendTransaction()


