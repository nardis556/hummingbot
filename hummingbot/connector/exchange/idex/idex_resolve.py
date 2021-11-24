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
    """Save values corresponding to selected domain at module level"""
    global _IDEX_BLOCKCHAIN, _IS_IDEX_SANDBOX

    if domain == "matic":  # prod matic
        _IDEX_BLOCKCHAIN = 'MATIC'
        _IS_IDEX_SANDBOX = False
    elif domain == "sandbox_matic":
        _IDEX_BLOCKCHAIN = 'MATIC'
        _IS_IDEX_SANDBOX = True
    else:
        raise Exception(f'Bad configuration of domain "{domain}"')


def get_idex_blockchain(domain=None) -> str:
    """Late loading of user selected blockchain from configuration"""
    if domain in ("matic", "sandbox_matic"):
        return 'MATIC'
    return _IDEX_BLOCKCHAIN or 'MATIC'


def is_idex_sandbox(domain=None) -> bool:
    """Late loading of user selection of using sandbox from configuration"""
    if domain == "matic":
        return False
    elif domain == "sandbox_matic":
        return True
    return bool(_IS_IDEX_SANDBOX)


def get_idex_rest_url(domain=None):
    """Late resolution of idex rest url to give time for configuration to load"""
    if domain == "matic":  # production uses polygon mainnet (matic)
        return _IDEX_REST_URL_PROD_MATIC
    elif domain == "sandbox_matic":
        return _IDEX_REST_URL_SANDBOX_MATIC
    elif domain is None:  # no domain, use module level memory
        blockchain = get_idex_blockchain()
        platform = 'SANDBOX' if is_idex_sandbox() else 'PROD'
        return globals()[f'_IDEX_REST_URL_{platform}_{blockchain}']
    else:
        raise Exception(f'Bad configuration of domain "{domain}"')


def get_idex_ws_feed(domain=None):
    """Late resolution of idex WS url to give time for configuration to load"""
    if domain == "matic":  # production uses polygon mainnet (matic)
        return _IDEX_WS_FEED_PROD_MATIC
    elif domain == "sandbox_matic":
        return _IDEX_WS_FEED_SANDBOX_MATIC
    elif domain is None:  # no domain, use module level memory
        blockchain = get_idex_blockchain()
        platform = 'SANDBOX' if is_idex_sandbox() else 'PROD'
        return globals()[f'_IDEX_WS_FEED_{platform}_{blockchain}']
    else:
        raise Exception(f'Bad configuration of domain "{domain}"')


_throttler = None


def get_throttler() -> Throttler:  # todo alf: check limits for v3
    global _throttler
    if _throttler is None:
        _throttler = Throttler(rate_limit=(4, 1.0))  # rate_limit=(weight, t_period)
    return _throttler
