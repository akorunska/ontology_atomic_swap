import os
import sys

rootPath = os.path.join(os.path.join(os.path.abspath(__file__), os.pardir), os.pardir)

def GetContractsFolderPath():
    return os.path.abspath(os.path.join(rootPath, "contracts"))

def GetBuildFolderPath():
    return os.path.abspath(os.path.join(GetContractsFolderPath(), "build"))

def GetTestFolderPath():
    return os.path.abspath(os.path.join(rootPath, "tests"))

def GetUtilsFolderPath():
    return os.path.abspath(os.path.join(rootPath, "LibUtils"))

def GetAbiFilePath(contractName):
    return os.path.join(GetBuildFolderPath(), contractName) + "_abi.json"

def GetDeployedContractsJson():
    return os.path.abspath(os.path.join(GetBuildFolderPath(), "DeployedContracts.json"))