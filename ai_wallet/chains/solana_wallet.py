"""
Solana Wallet Module for AI Agents
支持 SOL 和 SPL Token
"""
import os
import base58
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Solana imports
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.message import Message
from solders.transaction import Transaction
from solders.rpc.responses import GetBalanceResp, SendTransactionResp

import httpx


@dataclass
class TokenInfo:
    """Token信息"""
    mint: str
    symbol: str
    decimals: int
    balance: float = 0.0


class SolanaWallet:
    """
    AI友好的Solana钱包
    
    特性:
    - 生成/导入钱包
    - 查询SOL和SPL Token余额
    - 发送交易
    - AI可直接调用的统一接口
    """
    
    # 常用Token列表 (Devnet)
    POPULAR_TOKENS = {
        'USDC': '4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU',  # Devnet USDC
        'USDT': 'BQcdHdAQW1hczDbBi9hiegXAR7A98Q9jx3X3iBBBDiq4',  # Devnet USDT
    }
    
    def __init__(self, private_key: Optional[str] = None, network: str = "devnet"):
        """
        初始化Solana钱包
        
        Args:
            private_key: Base58编码的私钥 (可选，不传则生成新钱包)
            network: "devnet", "testnet", 或 "mainnet"
        """
        self.network = network
        self._keypair = self._load_or_create_keypair(private_key)
        self.public_key = str(self._keypair.pubkey())
        
        # RPC endpoints
        self.rpc_urls = {
            'devnet': 'https://api.devnet.solana.com',
            'testnet': 'https://api.testnet.solana.com',
            'mainnet': 'https://api.mainnet-beta.solana.com'
        }
        self.rpc_url = self.rpc_urls.get(network, self.rpc_urls['devnet'])
        
    def _load_or_create_keypair(self, private_key: Optional[str]) -> Keypair:
        """加载或创建密钥对"""
        if private_key:
            # Base58解码
            decoded = base58.b58decode(private_key)
            return Keypair.from_bytes(decoded)
        else:
            return Keypair()
    
    def get_private_key(self) -> str:
        """获取Base58编码的私钥"""
        return base58.b58encode(bytes(self._keypair)).decode('ascii')
    
    async def get_balance(self) -> Dict:
        """
        获取SOL余额
        
        Returns:
            {
                "address": "...",
                "balance_sol": 1.5,
                "balance_lamports": 1500000000
            }
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.rpc_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getBalance",
                    "params": [self.public_key]
                }
            )
            result = response.json()
            
            if 'result' in result:
                lamports = result['result']['value']
                sol = lamports / 1e9
                return {
                    "address": self.public_key,
                    "balance_sol": sol,
                    "balance_lamports": lamports
                }
            else:
                return {"error": result.get('error', 'Unknown error')}
    
    async def get_token_balance(self, token_mint: str) -> Dict:
        """
        获取SPL Token余额
        
        Args:
            token_mint: Token的mint地址
        """
        # 获取Token Account
        async with httpx.AsyncClient() as client:
            # 获取关联Token账户
            response = await client.post(
                self.rpc_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getTokenAccountsByOwner",
                    "params": [
                        self.public_key,
                        {"mint": token_mint},
                        {"encoding": "jsonParsed"}
                    ]
                }
            )
            
            result = response.json()
            
            if 'result' in result and result['result']['value']:
                account = result['result']['value'][0]
                parsed = account['account']['data']['parsed']['info']
                return {
                    "token_mint": token_mint,
                    "token_account": account['pubkey'],
                    "balance": float(parsed['tokenAmount']['uiAmount']),
                    "decimals": parsed['tokenAmount']['decimals']
                }
            else:
                return {
                    "token_mint": token_mint,
                    "balance": 0.0,
                    "message": "No token account found"
                }
    
    async def send_sol(self, to_address: str, amount_sol: float) -> Dict:
        """
        发送SOL
        
        Args:
            to_address: 接收方地址
            amount_sol: SOL数量
        """
        try:
            recipient = Pubkey.from_string(to_address)
            amount_lamports = int(amount_sol * 1e9)
            
            # 获取最新blockhash
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.rpc_url,
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "getLatestBlockhash",
                        "params": [{"commitment": "finalized"}]
                    }
                )
                blockhash_result = response.json()['result']['value']['blockhash']
            
            # 创建转账指令
            transfer_ix = transfer(
                TransferParams(
                    from_pubkey=self._keypair.pubkey(),
                    to_pubkey=recipient,
                    lamports=amount_lamports
                )
            )
            
            # 构建交易
            message = Message([transfer_ix], self._keypair.pubkey())
            transaction = Transaction([self._keypair], message, Pubkey.from_string(blockhash_result))
            
            # 序列化并发送
            serialized = transaction.serialize()
            encoded_tx = base58.b58encode(bytes(serialized)).decode('ascii')
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.rpc_url,
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "sendTransaction",
                        "params": [encoded_tx]
                    }
                )
                result = response.json()
                
                if 'result' in result:
                    return {
                        "success": True,
                        "signature": result['result'],
                        "amount": amount_sol,
                        "to": to_address,
                        "explorer": f"https://explorer.solana.com/tx/{result['result']}?cluster={self.network}"
                    }
                else:
                    return {"error": result.get('error', 'Unknown error')}
                    
        except Exception as e:
            return {"error": str(e)}
    
    def to_dict(self) -> Dict:
        """导出钱包信息（AI可序列化）"""
        return {
            "chain": "solana",
            "network": self.network,
            "address": self.public_key,
            "private_key": self.get_private_key(),  # 注意：仅用于AI自我备份
            "supported_tokens": list(self.POPULAR_TOKENS.keys())
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SolanaWallet':
        """从字典恢复钱包（AI可加载）"""
        return cls(
            private_key=data.get('private_key'),
            network=data.get('network', 'devnet')
        )


# ============ AI统一接口 ============

class SolanaAgentInterface:
    """
    Solana AI Agent接口
    提供与Bitcoin/Ethereum统一的命令格式
    """
    
    COMMANDS = {
        "create_wallet": {
            "description": "创建新Solana钱包",
            "params": {"network": "devnet|testnet|mainnet"}
        },
        "get_balance": {
            "description": "查询SOL余额",
            "params": {"address": "可选，默认查询自己"}
        },
        "send_sol": {
            "description": "发送SOL",
            "params": {"to": "接收地址", "amount": "SOL数量"}
        },
        "get_token_balance": {
            "description": "查询Token余额",
            "params": {"token": "USDC|USDT 或 mint地址"}
        }
    }
    
    def __init__(self, wallet: Optional[SolanaWallet] = None):
        self.wallet = wallet
    
    async def execute(self, command: str, params: Dict = None) -> Dict:
        """
        AI执行命令的统一入口
        
        Args:
            command: 命令名称
            params: 参数字典
        """
        params = params or {}
        
        if command == "create_wallet":
            network = params.get('network', 'devnet')
            self.wallet = SolanaWallet(network=network)
            return {
                "success": True,
                "action": "wallet_created",
                "data": self.wallet.to_dict()
            }
        
        elif command == "get_balance":
            if not self.wallet:
                return {"error": "No wallet loaded"}
            result = await self.wallet.get_balance()
            return {"success": True, "action": "balance", "data": result}
        
        elif command == "send_sol":
            if not self.wallet:
                return {"error": "No wallet loaded"}
            return await self.wallet.send_sol(
                params.get('to'),
                float(params.get('amount', 0))
            )
        
        elif command == "get_token_balance":
            if not self.wallet:
                return {"error": "No wallet loaded"}
            token = params.get('token', 'USDC')
            if token in SolanaWallet.POPULAR_TOKENS:
                token = SolanaWallet.POPULAR_TOKENS[token]
            return await self.wallet.get_token_balance(token)
        
        else:
            return {
                "error": f"Unknown command: {command}",
                "available_commands": list(self.COMMANDS.keys())
            }


# ============ 示例用法 ============

if __name__ == "__main__":
    import asyncio
    
    async def demo():
        print("=" * 60)
        print("🚀 Solana Wallet for AI Agents - Demo")
        print("=" * 60)
        
        # 1. 创建钱包
        print("\n📌 创建Solana Devnet钱包...")
        wallet = SolanaWallet(network="devnet")
        print(f"地址: {wallet.public_key}")
        print(f"私钥: {wallet.get_private_key()[:20]}...")
        
        # 2. 查询余额
        print("\n📌 查询SOL余额...")
        balance = await wallet.get_balance()
        print(f"余额: {balance.get('balance_sol', 0)} SOL")
        print(f"💡 从 faucet.solana.com 获取测试币后重试")
        
        # 3. AI接口演示
        print("\n📌 AI Agent接口演示...")
        agent = SolanaAgentInterface(wallet)
        
        result = await agent.execute("get_balance")
        print(f"AI接口结果: {json.dumps(result, indent=2)}")
        
        print("\n✅ Solana钱包模块准备就绪！")
    
    asyncio.run(demo())
