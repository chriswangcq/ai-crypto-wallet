#!/usr/bin/env python3
"""
Unified Multi-Chain Wallet Example
One interface controls Bitcoin, Ethereum, Solana, and TRON
"""

import sys
sys.path.insert(0, '/home/ubuntu/ai-crypto-wallet')

from ai_wallet.unified_wallet import AICryptoWallet


def main():
    print("=" * 70)
    print("🤖 AI Crypto Wallet - Unified Multi-Chain Demo")
    print("=" * 70)
    
    chains = [
        ("bitcoin", "testnet"),
        ("ethereum", "sepolia"),
        ("solana", "devnet"),
        ("tron", "nile"),
    ]
    
    print("\n🚀 Generating wallets for all supported chains:\n")
    
    for chain, network in chains:
        print(f"\n{'─' * 70}")
        print(f"🔗 {chain.upper()} ({network})")
        print('─' * 70)
        
        # Generate wallet
        wallet_data = AICryptoWallet.generate(chain, network)
        print(f"   Address: {wallet_data['address']}")
        print(f"   Private: {wallet_data['private_key'][:30]}...")
        
        # Initialize and query
        wallet = AICryptoWallet(chain, wallet_data['private_key'], network)
        
        # AI-friendly command
        result = wallet.execute({"action": "get_balance"})
        if result.get('success'):
            print(f"   Balance: {result.get('balance', 0)}")
        else:
            print(f"   Status: {result.get('error', 'Unknown')}")
    
    print("\n" + "=" * 70)
    print("✅ All chains initialized!")
    print("=" * 70)
    print("\n📝 AI Agent can now control crypto across 4 chains:")
    print("   • Bitcoin (BTC)")
    print("   • Ethereum (ETH + ERC-20)")
    print("   • Solana (SOL + SPL)")
    print("   • TRON (TRX + TRC-20)")


if __name__ == "__main__":
    main()
