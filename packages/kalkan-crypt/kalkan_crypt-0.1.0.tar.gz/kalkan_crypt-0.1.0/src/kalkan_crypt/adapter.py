import ctypes as ct
import typing as t
from pathlib import Path

from . import exceptions as exc
from .enums import StorageType, SignatureFlag


class KalkanAdapter:
    """
    Адаптер для работы криптографической библиотекой Kalkan Crypt.
    """

    def __init__(self, cert_path: str, cert_password: str):
        """
        :param cert_path: Путь к сертификату
        :param cert_password: Пароль от сертификата
        """
        self._alias = ct.create_string_buffer(''.encode())
        self._dll = self._init_dll()
        self._init_argtypes()
        self._load_keystore(cert_path, cert_password)
        self._public_cert = self._get_public_cert()

    @property
    def public_cert(self):
        return self._public_cert

    def _init_dll(self):
        """
        Инициализация библиотеки Kalkan Crypt.
        """
        try:
            dll_path = Path(__file__).parent.joinpath('dll')
            dll_file = 'libkalkancryptwr-64.so.2.0.2'
            _dll = ct.CDLL(str(dll_path.joinpath(dll_file)), mode=1)
            if status_code := _dll.Init() != 0:
                raise exc.DllInitError(status_code)
            return _dll
        except Exception as err:
            raise exc.DllInitError(str(err))

    def _load_keystore(self, cert_path: str, cert_password: str):
        """
        Загрузка сертификата в хранилище.

        :param cert_path: Путь к сертификату
        :param cert_password: Пароль от сертификата
        """
        storage_type = ct.c_int(StorageType.KCST_PKCS12.value)
        cert_password = ct.create_string_buffer(cert_password.encode())
        cert_file = ct.create_string_buffer(cert_path.encode())
        status_code = self._dll.KC_LoadKeyStore(
            storage_type,
            cert_password,
            len(cert_password),
            cert_file,
            len(cert_file),
            self._alias,
        )
        if status_code != 0:
            self._raise_exception(exc.LoadKeyStoreError)

    def sign_data(self, data: bytes, flags: t.Iterable[SignatureFlag] = (
            SignatureFlag.KC_SIGN_DRAFT, SignatureFlag.KC_IN_BASE64, SignatureFlag.KC_OUT_BASE64)) -> bytes:
        """
        Создание подписи на основе переданных данных.

        :param data: Данные
        :param flags: Список флагов
        :return: Подпись
        """
        flags = ct.c_int(sum([flag.value for flag in flags]))
        data_to_sign = ct.create_string_buffer(data)
        signed_data = ct.create_string_buffer(len(data_to_sign) * 2 + 50000)
        status_code = self._dll.SignData(
            self._alias,
            flags,
            data_to_sign,
            len(data_to_sign),
            ct.create_string_buffer(''.encode()),
            len(data_to_sign) * 2 + 50000,
            signed_data,
            ct.pointer(ct.c_int(len(data_to_sign) * 2 + 50000))
        )
        if status_code != 0:
            self._raise_exception(exc.SignDataError)
        return signed_data.value

    def _get_public_cert(self) -> str:
        """
        Получение публичного сертификата из хранилища.
        """
        flags = ct.c_int(1)
        cert_len = ct.pointer(ct.c_int(32768))
        public_cert = ct.create_string_buffer(32768)
        status_code = self._dll.X509ExportCertificateFromStore(
            self._alias,
            flags,
            public_cert,
            cert_len,
        )
        if status_code != 0:
            self._raise_exception(exc.GetPublicCertError)
        public_cert = public_cert.value.decode().replace('-----BEGIN CERTIFICATE-----', '')
        public_cert = public_cert.replace('-----END CERTIFICATE-----', '')
        public_cert = public_cert.replace('\n', '')
        return public_cert

    def finalize(self):
        """
        Освобождает ресурсы криптопровайдера KalkanCryptCOM
        и завершает работу библиотеки.
        """
        self._dll.KC_Finalize()

    def _init_argtypes(self):
        """
        Инициализация типов аргументов вызываемых функий.
        """
        self._dll.KC_LoadKeyStore.argtypes = [
            ct.c_int, ct.c_char_p, ct.c_int,
            ct.c_char_p, ct.c_int, ct.c_char_p
        ]
        self._dll.SignData.argtypes = [
            ct.c_char_p, ct.c_int, ct.c_char_p,
            ct.c_int, ct.c_char_p, ct.c_int,
            ct.c_char_p, ct.POINTER(ct.c_int)
        ]
        self._dll.X509ExportCertificateFromStore.argtypes = [
            ct.c_char_p, ct.c_int, ct.c_char_p, ct.POINTER(ct.c_int)
        ]
        self._dll.KC_GetLastErrorString.argtypes = [ct.c_char_p, ct.POINTER(ct.c_int)]

    def _raise_exception(self, exception: t.Type[exc.KalkanCryptError]):
        error_message = self._get_error_message()
        raise exception(error_message)

    def _get_error_message(self) -> str:
        """
        Получение информации о последней ошибке.

        :return: Информация об ошибке
        """
        error_message = ct.create_string_buffer(32768)
        error_code = ct.c_int(65534)
        self._dll.KC_GetLastErrorString(
            error_message,
            ct.byref(error_code)
        )
        return error_message.value
