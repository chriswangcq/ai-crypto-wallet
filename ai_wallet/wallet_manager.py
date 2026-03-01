"""
Unified Wallet Manager for AI Agents
Supports: Bitcoin, Ethereum, Solana, TRON
"""
from .chains.bitcoin import BitcoinWallet
from .chains.ethereum import EthereumWallet

class Wallet:
    """Universal wallet for AI agents"""
    
    def __init__(self, config=None):
        self.config = config or {}
    
    def bitcoin(self, testnet=True):
        """Get Bitcoin wallet interface"""
        return BitcoinWallet(testnet=testnet)
    
    def ethereum(self, network="sepolia"):
        """Get Ethereum wallet interface"""
        return EthereumWallet(network=network)
    
    def solana(self, network="devnet"):
        """Get Solana wallet interface (coming soon)"""
        raise NotImplementedError("Solana support coming in v0.3")
    
    def tron(self, network="nile"):
        """Get TRON wallet interface (coming soon)"""
        raise NotImplementedError("TRON support coming in v0.3")
