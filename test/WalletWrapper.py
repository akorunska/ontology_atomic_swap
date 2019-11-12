from SDKWrapper import SdkWrapper

sdkWrapper = SdkWrapper.GetInstance()


class WalletManager():
    def __init__(self):
        self.alice = Alice()
        self.aliceAddr = AliceAddress()
        self.bobAddr = BobAddress()
        self.bob = Bob()
        self.eveAddr = EveAddress()
        self.eve = Eve()
        


def Alice():
    return sdkWrapper.GetSdk().wallet_manager.get_account(AliceAddress(), 'password')

def Bob():
    return sdkWrapper.GetSdk().wallet_manager.get_account(BobAddress(), 'password')

def Eve():
    return sdkWrapper.GetSdk().wallet_manager.get_account(EveAddress(), 'test')



def AliceAddress():
    # return 'AecaeSEBkt5GcBCxwz1F41TvdjX3dnKBkJ'
    return 'AUr5QUfeBADq6BMY6Tp5yuMsUNGpsD7nLZ'

def BobAddress():
    return 'AQvZMDecMoCi2y4V6QKdJBtHW1eV7Vbaof'

def EveAddress():
    return "AVW5gqPewjmZ5W1osaU2CmMB2iamBHY2CA"