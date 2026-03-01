"""
Ethereum Wallet for AI Agents
Supports: ETH transfers, ERC-20 tokens, Smart contract interactions
"""
import os
import json
import secrets
from typing import Dict, Optional
from eth_account import Account
from web3 import Web3

class EthereumWallet:
    """Ethereum wallet interface for AI agents"""
    
    NETWORKS = {
        'mainnet': {'rpc': 'https://eth-mainnet.g.alchemy.com/v2/', 'chain_id': 1},
        'sepolia': {'rpc': 'https://eth-sepolia.g.alchemy.com/v2/', 'chain_id': 11155111},
        'goerli': {'rpc': 'https://eth-goerli.g.alchemy.com/v2/', 'chain_id': 5},
    }
    
    def __init__(self, network='sepolia', private_key=None):
        """
        Initialize Ethereum wallet
        
        Args:
            network: 'mainnet', 'sepolia', or 'goerli'
            private_key: Optional private key to import
        """
        self.network = network
        self.address = None
        self.private_key = private_key
        
        # Get Alchemy API key from env
        alchemy_key = os.getenv('ALCHEMY_API_KEY', '')
        rpc_url = self.NETWORKS[network]['rpc'] + alchemy_key
        
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if private_key:
            self._load_from_key(private_key)
    
    def create(self):
        """Create new Ethereum account"""
        # Generate random private key
        priv = secrets.token_hex(32)
        self.private_key = "0x" + priv
        self._load_from_key(self.private_key)
        return {
            'address': self.address,
            'private_key': self.private_key,
            'network': self.network
        }
    
    def _load_from_key(self, private_key):
        """Load account from private key"""
        self.account = Account.from_key(private_key)
        self.address = self.account.address
    
    def get_balance(self) -> Dict:
        """Get ETH balance"""
        if not self.address:
            return {'error': 'Wallet not initialized'}
        
        try:
            balance_wei = self.w3.eth.get_balance(self.address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            return {
                'success': True,
                'address': self.address,
                'balance_eth': float(balance_eth),
                'balance_wei': balance_wei,
                'network': self.network
            }
        except Exception as e:
            return {'error': str(e)}
    
    def send(self, to_address: str, amount_eth: float, gas_price_gwei: int = None) -> Dict:
        """
        Send ETH to address
        
        Args:
            to_address: Recipient Ethereum address
            amount_eth: Amount in ETH
            gas_price_gwei: Optional gas price in gwei
        """
        if not self.private_key:
            return {'error': 'No private key loaded'}
        
        try:
            # Convert ETH to wei
            amount_wei = self.w3.to_wei(amount_eth, 'ether')
            
            # Get nonce
            nonce = self.w3.eth.get_transaction_count(self.address)
            
            # Get gas price
            if gas_price_gwei:
                gas_price = self.w3.to_wei(gas_price_gwei, 'gwei')
            else:
                gas_price = self.w3.eth.gas_price
            
            # Build transaction
            tx = {
                'nonce': nonce,
                'to': to_address,
                'value': amount_wei,
                'gas': 21000,  # Standard ETH transfer
                'gasPrice': gas_price,
                'chainId': self.NETWORKS[self.network]['chain_id']
            }
            
            # Sign transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_hash_hex = tx_hash.hex()
            
            return {
                'success': True,
                'tx_hash': tx_hash_hex,
                'from': self.address,
                'to': to_address,
                'amount_eth': amount_eth,
                'network': self.network,
                'explorer_url': self._get_explorer_url(tx_hash_hex)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_explorer_url(self, tx_hash):
        """Get blockchain explorer URL"""
        explorers = {
            'mainnet': 'https://etherscan.io/tx/',
            'sepolia': 'https://sepolia.etherscan.io/tx/',
            'goerli': 'https://goerli.etherscan.io/tx/'
        }
        return explorers.get(self.network, '') + tx_hash
    
    def export(self) -> Dict:
        """Export wallet data"""
        return {
            'address': self.address,
            'private_key': self.private_key,
            'network': self.network
        }


# AI-friendly interface
class EthereumInterface:
    """JSON interface for AI agents"""
    
    @staticmethod
    def handle_command(command: Dict) -> Dict:
        """Handle JSON commands from AI agents"""
        action = command.get('action')
        
        if action == 'create':
            wallet = EthereumWallet(network=command.get('network', 'sepolia'))
            return wallet.create()
        
        elif action == 'get_balance':
            wallet = EthereumWallet(
                network=command.get('network', 'sepolia'),
                private_key=command.get('private_key')
            )
            return wallet.get_balance()
        
        elif action == 'send':
            wallet = EthereumWallet(
                network=command.get('network', 'sepolia'),
                private_key=command.get('private_key')
            )
            return wallet.send(
                to_address=command.get('to_address'),
                amount_eth=command.get('amount_eth')
            )
        
        elif action == 'import':
            wallet = EthereumWallet(
                network=command.get('network', 'sepolia'),
                private_key=command.get('private_key')
            )
            return {'success': True, 'address': wallet.address}
        
        else:
            return {'error': f'Unknown action: {action}'}
