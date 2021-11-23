#!/usr/bin/env python

from hummingbot.core.utils.asyncio_throttle import Throttler


# IDEX v3 REST API url for production and sandbox (users may need to modify this someday)
_IDEX_REST_URL_PROD_MATIC = "https://api-matic.idex.io"
_IDEX_REST_URL_SANDBOX_MATIC = "https://api-sandbox-matic.idex.io"

# IDEX v3 WebSocket urls for production and sandbox (users may need to modify this someday)
_IDEX_WS_FEED_PROD_MATIC = "wss://websocket-matic.idex.io/v1"
_IDEX_WS_FEED_SANDBOX_MATIC = "wss://websocket-sandbox-matic.idex.io/v1"


# --- users should not modify anything beyond this point ---

_IDEX_BLOCKCHAIN = None
_IS_IDEX_SANDBOX = None


def set_domain(domain: str):
    """Save user selected domain so we don't have to pass around domain to every method"""
    global _IDEX_BLOCKCHAIN, _IS_IDEX_SANDBOX

    if domain == "matic":  # prod matic
        _IDEX_BLOCKCHAIN = 'MATIC'
        _IS_IDEX_SANDBOX = False
    elif domain == "sandbox_matic":
        _IDEX_BLOCKCHAIN = 'MATIC'
        _IS_IDEX_SANDBOX = True
    else:
        raise Exception(f'Bad configuration of domain "{domain}"')


def get_rest_url_for_domain(domain: str) -> str:
    if domain == "matic":  # production uses polygon mainnet (matic)
        return _IDEX_REST_URL_PROD_MATIC
    elif domain == "sandbox_matic":
        return _IDEX_REST_URL_SANDBOX_MATIC
    else:
        raise Exception(f'Bad configuration of domain "{domain}"')


def get_ws_url_for_domain(domain: str) -> str:
    if domain == "matic":  # production uses polygon mainnet (matic)
        return _IDEX_WS_FEED_PROD_MATIC
    elif domain == "sandbox_matic":
        return _IDEX_WS_FEED_SANDBOX_MATIC
    else:
        raise Exception(f'Bad configuration of domain "{domain}"')


def get_idex_blockchain() -> str:
    """Late loading of user selected blockchain from configuration"""
    return _IDEX_BLOCKCHAIN or 'MATIC'


def is_idex_sandbox() -> bool:
    """Late loading of user selection of using sandbox from configuration"""
    return bool(_IS_IDEX_SANDBOX)


def get_idex_rest_url(domain=None):
    """Late resolution of idex rest url to give time for configuration to load"""
    if domain is not None:
        # we need to pass the domain only if the method is called before the market is instantiated
        return get_rest_url_for_domain(domain)
    blockchain = get_idex_blockchain()
    platform = 'SANDBOX' if is_idex_sandbox() else 'PROD'
    return globals()[f'_IDEX_REST_URL_{platform}_{blockchain}']


def get_idex_ws_feed(domain=None):
    """Late resolution of idex WS url to give time for configuration to load"""
    if domain is not None:
        # we need to pass the domain only if the method is called before the market is instantiated
        return get_ws_url_for_domain(domain)
    blockchain = get_idex_blockchain()
    platform = 'SANDBOX' if is_idex_sandbox() else 'PROD'
    return globals()[f'_IDEX_WS_FEED_{platform}_{blockchain}']


_throttler = None


def get_throttler() -> Throttler:  # todo alf: check limits for v3
    global _throttler
    if _throttler is None:
        _throttler = Throttler(rate_limit=(4, 1.0))  # rate_limit=(weight, t_period)
    return _throttler
