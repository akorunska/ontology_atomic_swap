import os
import sys
import json
from punica.invoke.invoke_contract import Invoke
from compile import Compile, GetBuildFolderPath, GetContractsFolderPath, GetDestAbiFilePath, GetDeployedContractsJson


def BuildAndDeploy(contractName):
    Compile(contractName)
    try:
        os.system("punica deploy --avm " + os.path.join(GetBuildFolderPath(), contractName) + ".avm --config " + os.path.join(GetContractsFolderPath(), contractName) + "-config.json")
    except:
        print(sys.exc_info()[0])
    
    with open(GetDestAbiFilePath(contractName), "r") as f:
        dict_abi = json.loads(f.read())
        contract_address_tmp = dict_abi['hash'].replace('0x', '')
        contract_address = [contract_address_tmp[i:i+2] for i in range(0, len(contract_address_tmp), 2)]
        
    return contract_address


def CreateBuildDir():
    dirName = GetBuildFolderPath()        
    try:
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")


def DeployAllContracts():
    CreateBuildDir()
    deployedContractsAddress = dict()
    contracts = [
        "AtomicSwapExchange"
    ]
    for contract in contracts:
        address = BuildAndDeploy(contract)
        deployedContractsAddress[contract] = "".join(reversed(address))
    return deployedContractsAddress

def WriteAddressesToFile(data):
    with open(GetDeployedContractsJson(), 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    addresses = DeployAllContracts()
    WriteAddressesToFile(addresses)
    # print(addresses)