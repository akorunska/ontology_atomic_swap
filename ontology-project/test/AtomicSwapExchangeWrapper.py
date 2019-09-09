from punica.invoke.invoke_contract import Invoke
from punica.test.test import Test
from ontology.utils.util import parse_neo_vm_contract_return_type_integer, parse_neo_vm_contract_return_type_string, parse_neo_vm_contract_return_type_bool
import WalletWrapper
# import SdkUtils
from Utils import GetDeployedContractAddress, FormatOntIdParam


gas_limit = 500000
gas_price = 0
abi_path = 'contracts/build/ASExchange_abi.json'
contract_address = bytes.fromhex(GetDeployedContractAddress("ASExchange"))
abi_info = Test.get_abi_info(abi_path)
alice = WalletWrapper.alice

def initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock):
    preExec = False
    params = {
        "amountOfOntToSell": amountOfOntToSell,
        "amountOfEthToBuy": amountOfEthToBuy,
        "hashlock": hashlock,
        "acct": alice,
    }
    abiFunction = Invocation.get_function(params, 'intiate_order', abi_info)
    return SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)

def get_orders():
    preExec = True
    params = dict()
    abiFunction = Invoke.get_function(params, 'get_orders', abi_info)
    return SdkUtils.SendTransaction()


