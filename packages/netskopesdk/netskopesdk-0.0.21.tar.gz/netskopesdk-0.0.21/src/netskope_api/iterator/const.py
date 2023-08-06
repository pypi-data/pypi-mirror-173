"""
Define the const used across all components.

Only put built-in imports in this module to make this really Const.
Use var.py for variable definitions.

"""

class Const(object):

    """
    Constant definition for iterator
    """
    
    NSKP_TOKEN = "TOKEN"
    NSKP_ITERATOR_NAME = "ITERATOR_NAME"
    NSKP_EVENT_TYPE = "EVENT_TYPE"
    NSKP_TENANT_HOSTNAME = "TENANT_HOSTNAME"
    NSKP_PROXIES = "PROXIES_DICT"
    NSKP_USER_AGENT = "USER_AGENT"


    # *************************#
    # Rate limiting constants #
    #*************************#

    # Rate limit remaining
    RATELIMIT_REMAINING = "ratelimit-remaining"
    # Rate limit RESET value is in seconds
    RATELIMIT_RESET = "ratelimit-reset"
    # Ratelimit
    RATELIMIT_LIMIT = "ratelimit-limit"


