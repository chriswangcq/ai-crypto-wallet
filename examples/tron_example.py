#!/usr/bin/env python3
"""TRON Wallet Example for AI Agents"""
import sys
sys.path.insert(0, '/home/ubuntu/ai-crypto-wallet')
from ai_wallet.chains.tron_wallet import TronWallet

wallet = TronWallet.generate_wallet(network="nile")
print(f"Address: {wallet['address']}")
print(f"Explorer: https://nile.tronscan.org/#/address/{wallet['address']}")
