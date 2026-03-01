"""
Chain-specific wallet implementations
"""
from .bitcoin import BitcoinWallet
from .ethereum import EthereumWallet

__all__ = ['BitcoinWallet', 'EthereumWallet']
