from ontology.wallet.wallet_manager import WalletManager
import os.path

def generateAccount(label, password, walletPath, walletName="wallet.json"):
    wm = WalletManager()
    wm.create_account(label, password)
    wm.open_wallet(os.path.join(walletPath, walletName))
    wm.write_wallet()
