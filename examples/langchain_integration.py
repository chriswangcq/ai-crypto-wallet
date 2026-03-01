"""
AI Crypto Wallet - LangChain Integration
========================================

Give your LangChain agent the ability to handle crypto.
"""

from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from ai_wallet import AICryptoWallet

# Initialize wallet
wallet = AICryptoWallet()

@tool
def crypto_balance(chain: str) -> str:
    """Get the balance of a specific blockchain. 
    Chains: bitcoin, ethereum, solana, tron"""
    import asyncio
    result = asyncio.run(wallet.execute({
        "action": "get_balance",
        "chain": chain
    }))
    return f"Balance on {chain}: {result}"

@tool  
def crypto_send(chain: str, to_address: str, amount: float) -> str:
    """Send cryptocurrency to an address.
    Args:
        chain: blockchain to use (bitcoin, ethereum, solana, tron)
        to_address: recipient address
        amount: amount to send"""
    import asyncio
    result = asyncio.run(wallet.execute({
        "action": "send",
        "chain": chain,
        "to": to_address,
        "amount": amount
    }))
    return f"Sent {amount} on {chain}. TX: {result.get('tx_hash', 'pending')}"

@tool
def crypto_address(chain: str) -> str:
    """Get receiving address for a blockchain."""
    import asyncio
    result = asyncio.run(wallet.execute({
        "action": "get_address",
        "chain": chain
    }))
    return f"Your {chain} address: {result['address']}"

# Setup agent with crypto tools
tools = [crypto_balance, crypto_send, crypto_address]
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Example usage
if __name__ == "__main__":
    print("🤖 Crypto-enabled AI Agent")
    print("Try asking: 'What's my Solana balance?' or 'Send 0.01 ETH to 0x123...'")
    
    # Run interactive mode
    while True:
        query = input("\nYou: ")
        if query.lower() in ['exit', 'quit']:
            break
        response = agent.run(query)
        print(f"Agent: {response}")
