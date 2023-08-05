class KalkanCryptError(Exception):
    ...


class DllInitError(KalkanCryptError):
    ...


class LoadKeyStoreError(KalkanCryptError):
    ...


class SignDataError(KalkanCryptError):
    ...


class GetPublicCertError(KalkanCryptError):
    ...
