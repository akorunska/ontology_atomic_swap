import time
from ontology.ont_sdk import OntologySdk
from SDKWrapper import SdkWrapper
from ontology.smart_contract.native_contract.auth import Auth

sdk = SdkWrapper.GetInstance().GetSdk()
g_auth = sdk.native_vm().auth()

g_gasLimit = 510000
g_gasPrice = 500

def WaitNextBlock():
    currentBlock = sdk.rpc.get_block_count()
    while True:
        time.sleep(1)
        if sdk.rpc.get_block_count() > currentBlock:
            break
        continue


def SendTransaction(contractAddress, acct, payer, gasLimit, gasPrice, abiFunction, preExec):    
    tx = sdk.neo_vm().send_transaction(contractAddress, acct, payer, gasLimit, gasPrice, abiFunction, preExec)
    if not preExec:
        WaitNextBlock()
    return tx


def GetOnyxBalance(accountAddress):
    return sdk.native_vm().asset().query_balance('ONYX', accountAddress)


def TransferOnyx(fromAcct, toAcct, amount):
    asset = sdk.native_vm().asset()
    gasLimit = 210000
    gasPrice = 0
    asset.send_transfer('onyx', fromAcct, toAcct, int(amount), fromAcct, gasLimit, gasPrice)


def BlockHeight():
    return sdk.rpc.get_block_count()


def GasConsumed(tx):
    contractEvent = sdk.rpc.get_smart_contract_event_by_height(tx)
    return contractEvent['GasConsumed']


def ContractEvents(tx):
    contractEvent = sdk.rpc.get_smart_contract_event_by_height(tx)
    return contractEvent['Notify']


def AssignFuncsToRole(identity, password, keyNo, contractAddress, role, functionsList, adminAcct):
    res = g_auth.assign_funcs_to_role(identity, password, keyNo, contractAddress, role, functionsList, adminAcct, g_gasLimit, g_gasPrice)
    WaitNextBlock()
    return res


def AssignOntIdsToRole(identity, password, keyNo, contractAddress, role, ontIdsList, adminAcct):
    res = g_auth.assign_ont_ids_to_role(identity, password, keyNo, contractAddress, role, ontIdsList, adminAcct, g_gasLimit, g_gasPrice)
    # WaitNextBlock()
    return res


def RegisterOntId(identity, password, payer):
    try:
        return sdk.native_vm().ont_id().send_registry_ont_id_transaction(identity, password, payer, g_gasLimit, g_gasPrice)
    except Exception as ex:
        print (ex)
