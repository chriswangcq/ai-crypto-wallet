"""
TRON Wallet Module for AI Crypto Wallet
Supports TRX and TRC-20 tokens with AI-friendly interface
"""

import os
from typing import Dict, Any, Optional, List
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider


class TronWallet:
    """TRON wallet with AI-friendly interface for TRX and TRC-20 tokens"""
    
    CHAIN_NAMES = ["tron", "trx"]
    
    # Token contracts (mainnet)
    TOKENS = {
        "USDT": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
        "USDC": "TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8",
        "BTT": "TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4",
    }
    
    def __init__(self, private_key: Optional[str] = None, network: str = "nile"):
        """
        Initialize TRON wallet
        
        Args:
            private_key: Hex private key (optional, generates new if not provided)
            network: "mainnet", "nile" (testnet), or "shasta" (testnet)
        """
        self.network = network
        
        # Setup provider
        if network == "mainnet":
            provider = HTTPProvider("https://api.trongrid.io")
        elif network == "nile":
            provider = HTTPProvider("https://nile.trongrid.io")
        elif network == "shasta":
            provider = HTTPProvider("https://api.shasta.trongrid.io")
        else:
            raise ValueError(f"Unknown network: {network}")
        
        self.client = Tron(provider=provider)
        
        # Setup key
        if private_key:
            self.private_key = PrivateKey(bytes.fromhex(private_key.replace("0x", "")))
        else:
            self.private_key = PrivateKey.random()
        
        self.address = self.private_key.public_key.to_base58check_address()
    
    @classmethod
    def generate_wallet(cls, network: str = "nile") -> Dict[str, str]:
        """Generate a new wallet"""
        private_key = PrivateKey.random()
        address = private_key.public_key.to_base58check_address()
        
        return {
            "address": address,
            "private_key": private_key.hex(),
            "public_key": private_key.public_key.hex(),
            "network": network
        }
    
    def get_address(self) -> str:
        """Get wallet address"""
        return self.address
    
    def get_balance(self, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Get balance for TRX or TRC-20 token
        
        Args:
            token: Token symbol (e.g., "USDT") or None for TRX
        """
        try:
            if token is None or token == "TRX":
                # Get TRX balance
                balance_sun = self.client.get_account_balance(self.address)
                balance_trx = balance_sun / 1_000_000
                
                # Get account info for bandwidth/energy
                account = self.client.get_account(self.address)
                
                return {
                    "success": True,
                    "chain": "tron",
                    "address": self.address,
                    "balance": balance_trx,
                    "symbol": "TRX",
                    "raw_balance": balance_sun,
                    "network": self.network,
                    "resources": {
                        "bandwidth": account.get("net_window_size", 0) if account else 0,
                        "energy": account.get("account_resource", {}).get("energy_window_size", 0) if account else 0
                    }
                }
            else:
                # Get TRC-20 token balance
                token_address = self.TOKENS.get(token.upper())
                if not token_address:
                    return {
                        "success": False,
                        "error": f"Unknown token: {token}. Supported: {list(self.TOKENS.keys())}"
                    }
                
                # Query contract
                contract = self.client.get_contract(token_address)
                balance = contract.functions.balanceOf(self.address)
                decimals = contract.functions.decimals()
                
                return {
                    "success": True,
                    "chain": "tron",
                    "address": self.address,
                    "balance": balance / (10 ** decimals),
                    "symbol": token.upper(),
                    "raw_balance": balance,
                    "decimals": decimals,
                    "contract": token_address,
                    "network": self.network
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chain": "tron",
                "address": self.address
            }
    
    def send(self, to_address: str, amount: float, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Send TRX or TRC-20 tokens
        
        Args:
            to_address: Recipient address (base58)
            amount: Amount to send
            token: Token symbol or None for TRX
        """
        try:
            if token is None or token == "TRX":
                # Send TRX
                amount_sun = int(amount * 1_000_000)
                
                txn = (
                    self.client.trx.transfer(self.address, to_address, amount_sun)
                    .build()
                    .sign(self.private_key)
                )
                
                result = txn.broadcast()
                
                return {
                    "success": True,
                    "chain": "tron",
                    "txid": result["txid"],
                    "from": self.address,
                    "to": to_address,
                    "amount": amount,
                    "symbol": "TRX",
                    "network": self.network,
                    "explorer_url": f"https://{'nile.' if self.network == 'nile' else ''}tronscan.org/#/transaction/{result['txid']}"
                }
            else:
                # Send TRC-20 token
                token_address = self.TOKENS.get(token.upper())
                if not token_address:
                    return {
                        "success": False,
                        "error": f"Unknown token: {token}"
                    }
                
                contract = self.client.get_contract(token_address)
                decimals = contract.functions.decimals()
                amount_raw = int(amount * (10 ** decimals))
                
                txn = (
                    contract.functions.transfer(to_address, amount_raw)
                    .with_owner(self.address)
                    .fee_limit(10_000_000)
                    .build()
                    .sign(self.private_key)
                )
                
                result = txn.broadcast()
                
                return {
                    "success": True,
                    "chain": "tron",
                    "txid": result["txid"],
                    "from": self.address,
                    "to": to_address,
                    "amount": amount,
                    "symbol": token.upper(),
                    "contract": token_address,
                    "network": self.network,
                    "explorer_url": f"https://{'nile.' if self.network == 'nile' else ''}tronscan.org/#/transaction/{result['txid']}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chain": "tron",
                "from": self.address,
                "to": to_address
            }
    
    def get_transaction_history(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent transactions (simplified - returns note about API limitation)"""
        return {
            "success": True,
            "chain": "tron",
            "address": self.address,
            "note": "Use TronScan API for full transaction history",
            "explorer_url": f"https://{'nile.' if self.network == 'nile' else ''}tronscan.org/#/address/{self.address}",
            "transactions": []
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Export wallet data"""
        return {
            "chain": "tron",
            "address": self.address,
            "private_key": self.private_key.hex(),
            "public_key": self.private_key.public_key.hex(),
            "network": self.network
        }
    
    # ============== AI-Friendly Interface ==============
    
    def execute(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-friendly unified interface
        
        Commands:
        - {"action": "get_address"}
        - {"action": "get_balance", "token": "USDT"}  # None for TRX
        - {"action": "send", "to": "T...", "amount": 10.5, "token": "USDT"}
        - {"action": "get_history", "limit": 10}
        """
        action = command.get("action")
        
        if action == "get_address":
            return {"success": True, "chain": "tron", "address": self.get_address()}
        
        elif action == "get_balance":
            token = command.get("token")
            return self.get_balance(token)
        
        elif action == "send":
            to = command.get("to")
            amount = command.get("amount")
            token = command.get("token")
            
            if not to or amount is None:
                return {
                    "success": False,
                    "error": "Missing required params: 'to' and 'amount'"
                }
            
            return self.send(to, float(amount), token)
        
        elif action == "get_history":
            limit = command.get("limit", 10)
            return self.get_transaction_history(limit)
        
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}. Supported: get_address, get_balance, send, get_history"
            }
