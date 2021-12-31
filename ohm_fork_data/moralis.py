import requests
import datetime


class MoralisPy:
    def __init__(self, url='https://deep-index.moralis.io/api/v2/', key=None):
        self.url_base = url
        self.api_key = key

    def set_api_key(self, api_key):
        self.api_key = api_key

    def api_request(self, endpoint, method="GET"):
        headers = {
            "x-api-key": self.api_key
        }
        response = requests.request(url=self.url_base + endpoint, method=method, headers=headers)
        if response.status_code == 200:
            response_object = response.json()
            return response_object
        else:
            return False

    def get_native_balance(self, wallet_address, chain, block=None):
        endpoint = wallet_address + "/balance?chain=" + chain
        if block:
            endpoint += f"&to_block={block}"

        return float(self.api_request(endpoint)['balance'])

    def get_tokens_for_wallet(self, wallet_address, chain, block=None):
        endpoint = wallet_address + "/erc20?chain=" + chain
        if block:
            endpoint += f"&to_block={block}"
    
        return self.api_request(endpoint)

    def get_token_price(self, token_address, chain, block=None):
        endpoint = 'erc20/' + token_address + "/price?chain=" + chain
        if block:
            endpoint += f"&to_block={block}"

        return self.api_request(endpoint)

    def convert_native_amount_to_token_amount(self, token_address, chain, native_price_amount):
        price_api_response = self.get_token_price(token_address, chain)
        native_price = float(price_api_response['nativePrice']['value']) * (
                    10 ** float(-price_api_response['nativePrice']['decimals']))
        native_amount = (1 / native_price) * native_price_amount
        return native_amount

    def convert_token_amount_to_native_amount(self, token_address, chain, token_amount):
        price_api_response = self.get_token_price(token_address, chain)
        native_price = float(price_api_response['nativePrice']['value']) * (
                    10 ** float(-price_api_response['nativePrice']['decimals']))
        token_amount = (native_price) * token_amount
        return token_amount

    def get_token_metadata(self, token_address, chain):
        metadata = self.api_request("/erc20/metadata?chain="+chain+"&addresses="+token_address)[0]
        return metadata

    def get_total_token_assets(self, wallet_address, chains, tokens_to_exclude=None, block=None):
        erc20_token_assets_detail_list = []

        for chain in chains:

            tokens = self.get_tokens_for_wallet(wallet_address, chain=chain, block=block)
            for token in tokens:
                token_price_object = self.get_token_price(token['token_address'], chain=chain, block=block)
                if not token_price_object:
                    pass
                else:
                    token_quantity = float(token['balance'])*(10**-float(token['decimals']))
                    holdings_value = token_quantity*float(token_price_object['usdPrice'])
                    erc20_token_assets_detail_list.append({
                          "symbol": token['symbol']
                        , "quantity": token_quantity
                        , "holdings_value_usd": holdings_value
                    })


        return erc20_token_assets_detail_list
