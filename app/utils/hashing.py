from passlib import context

pwd_cxt = context.CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    """
    Класс хеша
    """

    @staticmethod
    def encrypt(password: str) -> str:
        """
        Хеширует пароль.

        :param password:
        :return: хеш пароля
        """
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """
        Проверяет пароль.

        :param hashed_password:
        :param plain_password:
        :return: bool
        """
        return pwd_cxt.verify(plain_password, hashed_password)
