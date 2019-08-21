from punica.invoke.invoke_contract import Invoke
from punica.test.test import Test
from ontology.utils.util import parse_neo_vm_contract_return_type_integer, parse_neo_vm_contract_return_type_string, parse_neo_vm_contract_return_type_bool
import WalletWrapper
import SdkUtils
from Utils import GetDeployedContractAddress, FormatOntIdParam


gas_limit = 500000
gas_price = 0
abi_path = 'contracts/build/ASExchange_abi.json'
contract_address = bytes.fromhex(GetDeployedContractAddress("ASExchange"))
abi_info = Test.get_abi_info(abi_path)
admin = WalletWrapper.Admin()
adminOntId = WalletWrapper.AdminOntId()

def MintToManually(acctTo, tokenId, amount, preExec = False, caller = adminOntId, keyNo = 1):    
    params = {
        "param": 0,
    }
    abiFunction = Invoke.get_function(params, 'intiate_order', abi_info)
    return SdkUtils.SendTransaction(contract_address, admin, admin, gas_limit, gas_price, abiFunction, preExec)
