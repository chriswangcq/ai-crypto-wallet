"""
AI Crypto Wallet - AutoGPT Plugin
=================================

Plugin for AutoGPT to enable crypto capabilities.
"""

from auto_gpt_plugin_template import AutoGPTPluginTemplate
from ai_wallet import AICryptoWallet

class AICryptoWalletPlugin(AutoGPTPluginTemplate):
    """Give AutoGPT the ability to hold and transfer crypto."""
    
    def __init__(self):
        super().__init__()
        self._name = "AI-Crypto-Wallet"
        self._version = "0.1.0"
        self._description = "Enable crypto payments for your AI agent"
        self.wallet = AICryptoWallet()
    
    def post_prompt(self, prompt):
        """Add crypto commands to the prompt."""
        prompt.add_command(
            "crypto_balance",
            "Check crypto balance",
            {"chain": "<blockchain name>"},
            self.check_balance
        )
        prompt.add_command(
            "crypto_send", 
            "Send cryptocurrency",
            {"chain": "<blockchain>", "to": "<address>", "amount": "<amount>"},
            self.send_crypto
        )
        prompt.add_command(
            "crypto_address",
            "Get receiving address",
            {"chain": "<blockchain>"},
            self.get_address
        )
        return prompt
    
    async def check_balance(self, chain: str):
        return await self.wallet.execute({
            "action": "get_balance",
            "chain": chain
        })
    
    async def send_crypto(self, chain: str, to: str, amount: float):
        return await self.wallet.execute({
            "action": "send",
            "chain": chain,
            "to": to,
            "amount": amount
        })
    
    async def get_address(self, chain: str):
        return await self.wallet.execute({
            "action": "get_address",
            "chain": chain
        })
