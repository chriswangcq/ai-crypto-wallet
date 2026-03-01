"""
Unified Multi-Chain Wallet for AI Agents
Supports: Bitcoin, Ethereum, Solana, TRON
"""

from typing import Dict, Any, Optional
from ai_wallet.chains.bitcoin_wallet import BitcoinWallet
from ai_wallet.chains.ethereum_wallet import EthereumWallet
from ai_wallet.chains.solana_wallet import SolanaWallet
from ai_wallet.chains.tron_wallet import TronWallet


class AICryptoWallet:
    """
    Universal wallet interface for AI Agents
    One interface, multiple chains
    """
    
    SUPPORTED_CHAINS = {
        "bitcoin": BitcoinWallet,
        "btc": BitcoinWallet,
        "ethereum": EthereumWallet,
        "eth": EthereumWallet,
        "solana": SolanaWallet,
        "sol": SolanaWallet,
        "tron": TronWallet,
        "trx": TronWallet,
    }
    
    def __init__(self, chain: str, private_key: Optional[str] = None, network: str = "testnet"):
        """
        Initialize wallet for specified chain
        
        Args:
            chain: "bitcoin", "ethereum", "solana", or "tron"
            private_key: Optional private key (generates new if not provided)
            network: Network type (varies by chain)
        """
        chain_lower = chain.lower()
        if chain_lower not in self.SUPPORTED_CHAINS:
            raise ValueError(f"Unsupported chain: {chain}. Supported: {list(self.SUPPORTED_CHAINS.keys())}")
        
        wallet_class = self.SUPPORTED_CHAINS[chain_lower]
        self.wallet = wallet_class(private_key=private_key, network=network)
        self.chain = chain_lower
    
    def execute(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Execute wallet command - AI-friendly interface"""
        return self.wallet.execute(command)
    
    def get_address(self) -> str:
        """Get wallet address"""
        return self.wallet.get_address()
    
    @classmethod
    def generate(cls, chain: str, network: str = "testnet") -> Dict[str, Any]:
        """Generate new wallet for specified chain"""
        chain_lower = chain.lower()
        if chain_lower not in cls.SUPPORTED_CHAINS:
            raise ValueError(f"Unsupported chain: {chain}")
        
        wallet_class = cls.SUPPORTED_CHAINS[chain_lower]
        return wallet_class.generate_wallet(network=network)
    
    @classmethod
    def supported_chains(cls) -> list:
        """Get list of supported chains"""
        return list(set(cls.SUPPORTED_CHAINS.values()))
