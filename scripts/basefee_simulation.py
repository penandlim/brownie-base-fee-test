from ape_safe import ApeSafe
from brownie import accounts, network

# Contract deployed and verified on Goerli
# https://goerli.etherscan.io/address/0x2b7a5a5923eca5c00c6572cf3e8e08384f563f93#code
GOERLI_BASE_FEE_TEST_CONTRACT = "0x2b7a5a5923eca5c00c6572cf3e8e08384f563f93"

# https://app.safe.global/gor:0x044b8A68ed54BCD1BBd1a315e97CC8594d098aaE/home
# Deployer account is added as a delegate to the multisig
# so it can queue up transactions
GOERLI_MULTISIG_ADDRESS = "0x044b8A68ed54BCD1BBd1a315e97CC8594d098aaE"


def main():
    """
    This script tries to call a contract using `block.basefee` OPCODE.
    Contract is read from the explorer.
    """

    multisig = ApeSafe(GOERLI_MULTISIG_ADDRESS)
    baseFeeContract = multisig.contract(GOERLI_BASE_FEE_TEST_CONTRACT)

    storedBaseFee = baseFeeContract.storedBaseFee()
    print(f"Stored base fee: {storedBaseFee}")

    # This view will fail because block.basefee is not available
    currentBaseFee = baseFeeContract.getCurrentBaseFee()

    # This write call will also fail
    reciept = baseFeeContract.storeCurrentBaseFee()

    # combine history into multisend txn
    safe_tx = multisig.tx_from_receipt(reciept)
    safe_tx.safe_nonce = 21

    multisig.preview(safe_tx)

    safe_tx.sign( accounts.load("deployer").private_key)
    multisig.post_transaction(safe_tx)
