from ape_safe import ApeSafe
from brownie import accounts, Contract

# Contract deployed and verified on Goerli
# https://goerli.etherscan.io/address/0x2b7a5a5923eca5c00c6572cf3e8e08384f563f93#code
GOERLI_BASE_FEE_CONTRACT_ADDRESS = "0x2b7a5a5923eca5c00c6572cf3e8e08384f563f93"
GOERLI_BASE_FEE_CONTRACT_ABI = [{"inputs": [], "stateMutability":"nonpayable", "type":"constructor"}, {"inputs": [], "name":"getCurrentBaseFee", "outputs":[{"internalType": "uint256", "name": "", "type": "uint256"}],
                                                                                                       "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"storeCurrentBaseFee", "outputs":[{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}]

# https://app.safe.global/gor:0x044b8A68ed54BCD1BBd1a315e97CC8594d098aaE/home
# Deployer EOA account is added as a delegate to the multisig
# so it can queue up transactions
GOERLI_MULTISIG_ADDRESS = "0x044b8A68ed54BCD1BBd1a315e97CC8594d098aaE"


def main():
    """
    This script tries to call a contract using `block.basefee` OPCODE.
    Contract is read from the explorer.
    """

    multisig = ApeSafe(GOERLI_MULTISIG_ADDRESS)

    # Getting the contract from the explorer fails regardless of the hardfork setting
    base_fee_contract = Contract.from_explorer(
        GOERLI_BASE_FEE_CONTRACT_ADDRESS, owner=multisig.account)

    # This view will fail because block.basefee is not available
    current_base_fee = base_fee_contract.getCurrentBaseFee()
    print(f"Current base fee: {current_base_fee}")

    # This write call will also fail
    reciept = base_fee_contract.storeCurrentBaseFee()

    # combine history into multisend txn
    safe_tx = multisig.tx_from_receipt(reciept)
    safe_tx.safe_nonce = 21

    multisig.preview(safe_tx)

    safe_tx.sign(accounts.load("deployer").private_key)
    multisig.post_transaction(safe_tx)
