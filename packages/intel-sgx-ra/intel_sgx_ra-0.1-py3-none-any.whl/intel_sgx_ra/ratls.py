"""intel_sgx_ra.ratls module."""

import hashlib
from typing import Union, cast

from cryptography import x509
from cryptography.hazmat.primitives.serialization import (Encoding,
                                                          PublicFormat)

from intel_sgx_ra.error import SGXQuoteNotFound
from intel_sgx_ra.quote import Quote

SGX_QUOTE_EXTENSION_OID = x509.ObjectIdentifier("1.2.840.113741.1337.6")


def quote_from_cert(ratls_cert: Union[bytes, x509.Certificate]) -> Quote:
    """Extract SGX quote from X509 certificate."""
    cert: x509.Certificate = (x509.load_pem_x509_certificate(ratls_cert)
                              if isinstance(ratls_cert, bytes) else ratls_cert)

    try:
        quote_extension: x509.UnrecognizedExtension = cast(
            x509.UnrecognizedExtension,
            cert.extensions.get_extension_for_oid(
                SGX_QUOTE_EXTENSION_OID).value)
    except x509.extensions.ExtensionNotFound as exc:
        raise SGXQuoteNotFound from exc

    return Quote.from_bytes(quote_extension.value)


def verify_user_report_data(ratls_cert: Union[bytes, x509.Certificate]):
    """Check user_report_data in SGX quote to match SHA256(cert.public_key())."""
    cert: x509.Certificate = (x509.load_pem_x509_certificate(ratls_cert)
                              if isinstance(ratls_cert, bytes) else ratls_cert)
    quote: Quote = quote_from_cert(cert)
    pk: bytes = cert.public_key().public_bytes(encoding=Encoding.Raw,
                                               format=PublicFormat.Raw)

    return hashlib.sha256(pk).digest() == quote.report_body.report_data[:32]
