from dexscreener import DexscreenerClient
import asyncio

token_ca = []
token_details = []

class GetTokens():
    async def main():
        client = DexscreenerClient()

        token_profiles = client.get_latest_token_profiles()

        for token in token_profiles:
            # tokens.append(format_token_info(token))
            if token.chain_id == "solana":
                token_ca.append(token.token_address)
                pair = client.search_pairs(token.token_address)
                if pair: token_details.append(pair)
    
        return token_ca, token_details
        
                
    
    