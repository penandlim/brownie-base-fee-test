Replicating basefee fails using ape-safe and eth-brownie

After applying the network-config.yaml, runing the below script fails due to `invalid opcode`
```
brownie run --network goerli-fork scripts/basefee_simulation_get_from_explorer.py
```

Using the hardfork london setting still fails with same error
```
brownie run --network goerli-fork-london scripts/basefee_simulation_get_from_explorer.py
```


If we try bypassing compiling by providing the ABI, we encounter a new error.
The transaction gets stuck with `Awaiting transaction in the mempool` and does not proceed.
```
brownie run --network goerli-fork-london scripts/basefee_simulation_from_abi.py
```
