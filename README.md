# sahara
Daily Check-in

# venv
```
# Create venv
python3 -m venv venv
# Activate venv
source venv/bin/activate
# Exit venv
deactivate
```

# Install
```
pip install --upgrade pip
pip install -r requirements.txt
```

# Prerequisite
## Get SAHARA from the official faucet
```
https://faucet.saharalabs.ai/

You will receive 0.1 SAH token from this Testnet Faucet request.
Faucet resets every 24 hours.

To prevent bots and abuse, this faucet requires a minimum Ethereum mainnet balance of 0.01ETH on the wallet address being used.
```

## Log in to Galxe using the EVM wallet address and set the Galxe username
```
https://app.galxe.com/
```

# Run
```
cd sahara_auto/
cp conf.py.sample conf.py
cp datas/purse/purse.csv.sample datas/purse/purse.csv
# modify datas/purse/purse.csv
python3 sahara.py
```
