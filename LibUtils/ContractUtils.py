from boa.interop.System.Runtime import CheckWitness, Deserialize, Notify
from ontology.builtins import state, concat
from boa.interop.System.App import RegisterAppCall
from ontology.interop.Ontology.Native import Invoke
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from ontology.interop.Ontology.Contract import Migrate
from ontology.libont import AddressFromVmCode

headContract = RegisterAppCall("6a7636598311a4b9c939d60fe58d3018379bfd87", "operation", "args")

def GetCoinContractAddress(assetId):
    if assetId is 'ONYX':
        return bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
    elif assetId is 'OXG':
        return bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
    else:
        Revert()

def Require(condition):
    if not condition:
        Revert()

def WitnessRequire(witness):
    if not CheckWitness(witness):
        raise Exception("Witness require")

def ConcatKey(key1, key2):
    return concat(key1, key2)


def Revert(str = ""):
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(str) #Exception(0xF1F1F2F2F3F3F4F4)


def DeserializeList(rawList):
    if len(rawList) > 0:
        return Deserialize(rawList)
    return []


def GetContractAddress(contractName):
    return headContract('GetContractAddress', [contractName])


def ParamError():
    Notify(["param error"])
    return False


def FunctionNameError():
    Notify(["Wrong function name"])
    return False


def InitContractAdmin(adminOntID):
    authContractAddr = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06')
    res = Invoke(0, authContractAddr, "initContractAdmin", adminOntID)
    Notify(["Admin has been registered", adminOntID])


def VerifyCaller(operation, caller, keyNo):    
    authContractAddr = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06')
    param = state(GetExecutingScriptHash(), caller, operation, keyNo)
    res = Invoke(0, authContractAddr, "verifyToken", param)
    Require(res)


def Migration(contractName, caller, keyNo, avmCode, needStorage, name, version, author, email, description):
    """
    :param avmCode:
    :param needStorage:
    :param name:
    :param version:
    :param author:
    :param email:
    :param description:
    :return:
    """
    # Only contract owner can migrate contract
    VerifyCaller('MigrateContract', caller, keyNo)

    newContractHash = AddressFromVmCode(avmCode)
    res = Migrate(avmCode, needStorage, name, version, author, email, description)
    if res:
        Notify(["Smart contract has been migrated successfully", contractName, newContractHash])
        return True
    else:
        return False


def IsMainNetworkCoin(assetId):
    return assetId is "ONYX" or assetId is "OXG"


def Transfer(assetId, fromAcct, toAcct, amount):
    if IsMainNetworkCoin(assetId):
        return TransferMainNetworkCoin(assetId, fromAcct, toAcct, amount) 
    else:
        return TransferOnyxPayAsset(assetId, fromAcct, toAcct, amount)   


def TransferOnyxPayAsset(assetId, fromAcct, toAcct, amount):
    contractName = ""
    params = []
    if assetId is "OnyxCash":
        contractName = "OnyxCash"
        params = [fromAcct, toAcct, amount]        
    else:
        contractName = "Assets"
        params = [assetId, fromAcct, toAcct, amount]

    contractAddress = GetContractAddress(contractName)
    return DynamicAppCall(contractAddress, 'transfer', params)


def TransferMainNetworkCoin(assetId, fromAcct, toAcct, amount):
    param = state(fromAcct, toAcct, amount)
    return Invoke(0, GetCoinContractAddress(assetId), 'transfer', [param])


def ContractBalance(assetId):
    if IsMainNetworkCoin(assetId):
        param = GetExecutingScriptHash()
        return Invoke(0, GetCoinContractAddress(assetId), 'balanceOf', param)    
    else:
        return BalanceOfOnyxPayAsset(GetExecutingScriptHash(), assetId)

def BalanceOfOnyxPayAsset(acct, assetId):
    if assetId is "OnyxCash":
        contractName = "OnyxCash"
        params = [acct]        
    else:
        contractName = "Assets"
        params = [acct, assetId]

    contractAddress = GetContractAddress(contractName)
    return DynamicAppCall(contractAddress, 'balanceOf', params)