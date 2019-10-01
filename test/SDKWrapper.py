from ontology.ont_sdk import OntologySdk

wallet_path= 'wallet/wallet.json'

class SdkWrapper:
    instance = None
    @staticmethod
    def GetInstance():
        if SdkWrapper.instance == None:
            SdkWrapper()
        return SdkWrapper.instance 

    def __init__(self):
        if SdkWrapper.instance == None:
            self.sdk = OntologySdk()
            self.sdk.set_rpc('http://127.0.0.1:20336')
            self.sdk.wallet_manager.open_wallet(wallet_path)
            SdkWrapper.instance = self

    def GetSdk(self):
        return self.sdk
        