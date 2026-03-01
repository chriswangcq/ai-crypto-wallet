"""
AI Crypto Wallet - Basic Usage Example
======================================

This example shows how to give your AI agent economic autonomy.
"""

import asyncio
from ai_wallet import AICryptoWallet

async def main():
    # Initialize the universal wallet
    wallet = AICryptoWallet()
    
    print("🤖 AI Agent Wallet Demo")
    print("=" * 50)
    
    # Check balances across all chains
    print("\n💰 Checking balances...")
    for chain in ["bitcoin", "ethereum", "solana", "tron"]:
        result = await wallet.execute({
            "action": "get_balance",
            "chain": chain
        })
        print(f"  {chain}: {result}")
    
    # Get receiving addresses
    print("\n📬 Receiving addresses:")
    for chain in ["bitcoin", "ethereum", "solana", "tron"]:
        result = await wallet.execute({
            "action": "get_address",
            "chain": chain
        })
        print(f"  {chain}: {result['address']}")
    
    # Example: Send a transaction (on testnet!)
    print("\n📤 Sending test transaction...")
    result = await wallet.execute({
        "action": "send",
        "chain": "solana",
        "to": " recipient_address_here",
        "amount": 0.001
    })
    print(f"  Transaction result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
