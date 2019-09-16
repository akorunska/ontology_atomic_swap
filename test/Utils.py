import json
from binascii import b2a_hex


def GetDeployedContractAddress(contractName):
    with open('./contracts/build/DeployedContracts.json') as file:  
        data = json.load(file)
        return data[contractName]


def FormatOntIdParam(ontId):
    return "Hex:" + b2a_hex(ontId.encode('utf-8')).decode('ascii')


def GetDefaultNetwork():
    with open('./tests/TestsConfig.json') as file:  
        data = json.load(file)
        defaultNetwork = data["defaultNet"]
        return data["networks"][defaultNetwork]


def GetDefaultNetworkName():
    with open('./tests/TestsConfig.json') as file:  
        data = json.load(file)
        return data["defaultNet"]


def GasPrice():
    network = GetDefaultNetwork()
    return network["gasPrice"]


def GasLimit():
    network = GetDefaultNetwork()
    return network["gasLimit"]


def NetworkUrl():
    network = GetDefaultNetwork()
    return network["networkUrl"]


def RejectRequestsPenaltyReasonCode():
    return 0x1