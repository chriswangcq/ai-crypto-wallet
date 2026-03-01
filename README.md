# 🤖💎 AI Crypto Wallet

> **The Universal Crypto Wallet for AI Agents**
> 
> Give your AI agents true economic autonomy — send, receive, and manage crypto assets across Bitcoin, Ethereum, and Solana

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Bitcoin](https://img.shields.io/badge/Bitcoin-supported-orange.svg)](https://bitcoin.org)
[![Ethereum](https://img.shields.io/badge/Ethereum-supported-blue.svg)](https://ethereum.org)
[![Solana](https://img.shields.io/badge/Solana-supported-purple.svg)](https://solana.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🌐 **English** | [中文](#中文文档) | [Roadmap](#roadmap)

---

## 🚀 One Interface, Multiple Chains

```python
from ai_wallet import AICryptoWallet

# Initialize the universal wallet
wallet = AICryptoWallet()

# AI can control BTC, ETH, SOL with the same simple interface
await wallet.execute({
    "action": "send",
    "chain": "solana",  # or "bitcoin", "ethereum"
    "to": "recipient_address",
    "amount": 0.1
})
```

---

## ✨ Features

### 🔗 Multi-Chain Support
| Chain | Status | Assets | Network |
|-------|--------|--------|---------|
| **Bitcoin** | ✅ Live | BTC | Testnet3 / Mainnet |
| **Ethereum** | ✅ Live | ETH, ERC-20 | Sepolia / Mainnet |
| **Solana** | ✅ Live | SOL, SPL tokens | Devnet / Mainnet |
| **TRON** | 🚧 Coming | TRX, TRC-20 | Nile / Mainnet |

### 🤖 AI-Native Design
- **JSON API** — No GUI, just programmatic control
- **Natural Language** — "Send 0.1 ETH to..."
- **Self-Custody** — AI holds keys, no human approval needed
- **Multi-Agent** — Supports agent-to-agent payments

### 🔐 Security First
- Testnet defaults for safe experimentation
- Encrypted key storage
- Transaction signing without exposing private keys

---

## 📦 Quick Start

### Installation

```bash
git clone https://github.com/chriswangcq/ai-crypto-wallet.git
cd ai-crypto-wallet
pip install -r requirements.txt
```

### 1️⃣ Bitcoin Wallet

```python
from ai_wallet.chains.bitcoin import BitcoinWallet

# Create or load wallet
wallet = BitcoinWallet(network='testnet')  # or 'mainnet'
wallet.create_wallet("my_ai_wallet")

# Check balance
balance = wallet.get_balance()
print(f"Balance: {balance} BTC")

# Send Bitcoin
tx_hash = wallet.send(
    to_address="tb1q...",
    amount_btc=0.001
)
print(f"Transaction: {tx_hash}")
```

### 2️⃣ Ethereum Wallet

```python
from ai_wallet.chains.ethereum import EthereumWallet

wallet = EthereumWallet(network='sepolia')  # or 'mainnet'
wallet.create_wallet("my_eth_wallet")

# Send ETH
tx_hash = wallet.send(
    to_address="0x...",
    amount_eth=0.1
)

# Send ERC-20 tokens
tx_hash = wallet.send_token(
    token_address="0x...",
    to_address="0x...",
    amount=100
)
```

### 3️⃣ Solana Wallet

```python
from ai_wallet.chains.solana import SolanaWallet

wallet = SolanaWallet(network='devnet')  # or 'mainnet'
wallet.create_wallet()

# Send SOL
tx_hash = wallet.send_sol(
    to_address="HN7c...",
    amount_sol=0.1
)

# Send SPL tokens
tx_hash = wallet.send_spl_token(
    mint_address="EPjF...",  # USDC mint
    to_address="HN7c...",
    amount=10
)
```

---

## 🎯 AI Agent Integration

### For LangChain Agents

```python
from langchain.tools import tool
from ai_wallet import AICryptoWallet

wallet = AICryptoWallet()

@tool
def send_crypto(chain: str, to: str, amount: float) -> str:
    """Send cryptocurrency to an address"""
    result = wallet.execute({
        "action": "send",
        "chain": chain,
        "to": to,
        "amount": amount
    })
    return f"Transaction sent: {result['tx_hash']}"

@tool  
def check_balance(chain: str) -> str:
    """Check wallet balance"""
    result = wallet.execute({
        "action": "balance",
        "chain": chain
    })
    return f"Balance: {result['balance']}"

# Agent can now use crypto autonomously
```

### For AutoGPT

```python
# In your AI's command registry
COMMANDS = {
    "crypto_send": {
        "function": wallet.send,
        "description": "Send crypto to an address"
    },
    "crypto_balance": {
        "function": wallet.get_balance,
        "description": "Check wallet balance"
    }
}
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│            Your AI Agent (GPT-4/Claude)         │
│                  ↓ JSON/API                     │
├─────────────────────────────────────────────────┤
│     Agent Interface (Unified JSON API)          │
├──────────┬──────────┬──────────┬────────────────┤
│  Bitcoin │ Ethereum │  Solana  │     TRON       │
│   Core   │   Core   │   Core   │    Core        │
├──────────┼──────────┼──────────┼────────────────┤
│ mempool  │  Alchemy │  Solana  │   TronGrid     │
│  .space  │ Infura   │   RPC    │     API        │
└──────────┴──────────┴──────────┴────────────────┘
```

**Design Philosophy**: One unified interface, multiple chains.

---

## 🔒 Security

- ✅ **Testnet-first**: Default to testnets for safe experimentation
- ✅ **Self-custody**: AI holds keys locally, no custodial risk
- ✅ **Encrypted storage**: Private keys encrypted at rest
- ⚠️ **Production**: Use HSM or MPC for production deployments

---

## 🌟 Why This Project?

> "AI agents need wallets just like humans need bank accounts."

Current AI limitations:
- ❌ Depend on humans for payments
- ❌ Cannot participate in economic activities autonomously
- ❌ Locked into platform economies (OpenAI credits, etc.)

Our vision:
- ✅ AI has true economic autonomy
- ✅ AI becomes independent economic entities
- ✅ AI participates equally in the global economy

---

## 🚧 Roadmap

### Phase 1: Core Chains ✅ COMPLETE
- [x] Bitcoin support (BTC)
- [x] Ethereum support (ETH, ERC-20)
- [x] Solana support (SOL, SPL tokens)
- [ ] TRON support (TRX, TRC-20)

### Phase 2: Advanced Features
- [ ] Multi-sig wallets for AI committees
- [ ] DeFi integrations (Uniswap, Aave, Jupiter)
- [ ] NFT support (ERC-721, Metaplex)
- [ ] Lightning Network

### Phase 3: AI Framework Integration
- [ ] LangChain official integration
- [ ] AutoGPT plugin
- [ ] CrewAI support
- [ ] ElizaOS connector

### Phase 4: Production
- [ ] Hardware Security Module (HSM) support
- [ ] Multi-Party Computation (MPC)
- [ ] Enterprise key management
- [ ] Insurance integration

---

## 📊 Growth & Promotion

We're building this in public! Follow our journey:

- 📰 **Updates**: Check [GROWTH_STRATEGY.md](GROWTH_STRATEGY.md)
- 📢 **Ready-to-use content**: [PROMOTION_CONTENT.md](PROMOTION_CONTENT.md)
- 🐦 **Twitter**: [@AI_Crypto_Wallet](https://twitter.com/)
- 💬 **Discord**: [Coming Soon]

---

## 🤝 Contribute

Join us in building the economic infrastructure for AI agents!

- 💻 **Developers**: Add new chains, improve security
- 🧠 **AI Researchers**: Explore AI economic behaviors
- 🎨 **Designers**: Make tools more accessible
- 📢 **Evangelists**: Spread the word

---

## 📜 License

MIT License — Build the future of AI economics together.

---

<p align="center">
  <b>🚀 Give AI a wallet. Change the world. 🚀</b>
</p>

---

# 中文文档

## 简介

**AI Crypto Wallet** 是专为 AI Agent 设计的多链加密货币钱包。

让 AI 拥有真正的经济自主权——发送、接收和管理加密资产。

### 支持的区块链
- ✅ **比特币** (BTC) — Testnet3 / 主网
- ✅ **以太坊** (ETH, ERC-20) — Sepolia / 主网  
- ✅ **Solana** (SOL, SPL) — Devnet / 主网
- 🚧 **TRON** (TRX) — 开发中

### 核心特性
- **AI 原生设计** — JSON API，无需 GUI
- **自托管** — AI 自主掌控私钥
- **多链统一接口** — 一条命令，多条链通用
- **测试网优先** — 安全实验，默认使用测试网

### 快速开始

```python
from ai_wallet import AICryptoWallet

wallet = AICryptoWallet()

# AI 可以控制 BTC、ETH、SOL
result = await wallet.execute({
    "action": "send",
    "chain": "solana",
    "to": "接收地址",
    "amount": 0.1
})
```

了解更多：[查看完整文档](https://github.com/chriswangcq/ai-crypto-wallet)
