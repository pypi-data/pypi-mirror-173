"""intel_sgx_ra.error module."""


class SGXQuoteNotFound(Exception):
    """SGX Quote extension not found in X509 certificate."""
