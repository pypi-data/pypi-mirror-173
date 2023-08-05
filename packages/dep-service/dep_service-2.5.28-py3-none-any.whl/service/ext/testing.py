"""Testing ext funcs."""

import random

from dataclasses import dataclass
from decimal import Decimal

from httpx import AsyncClient as XClient
from faker import Faker as _Faker
from fastapi.testclient import TestClient as ApiClient
from starlette.testclient import TestClient as AppClient


@dataclass(frozen=True)
class I18nFaker:
    """I18n Faker interface."""

    en: _Faker
    ru: _Faker

    def shake(self) -> None:
        """Shake fakers."""
        _Faker.seed(random.randint(0, 99999))

    def faker(self, lang: str = None) -> _Faker:
        """Faker."""
        if not lang:
            return self.en
        return {'en': self.en, 'ru': self.ru}[lang]

    # Any randoms with locales

    def any_country(self, lang: str = None) -> str:
        """Any country, like `Russia`."""
        self.shake()
        return str(self.faker(lang).country())

    def any_currency(self, lang: str = None) -> str:
        """Any currency, like `Russian Ruble`."""
        self.shake()
        return str(self.faker(lang).currency_name())

    def any_currency_code(self, lang: str = None) -> str:
        """Any currency code, like `RUB`."""
        self.shake()
        return str(self.faker(lang).currency_code())

    def any_word(self, lang: str = None) -> str:
        """Any word, like `Bubble`."""
        self.shake()
        return self.faker(lang).word()

    def any_sentence(self, lang: str = None) -> str:
        """Any sentence, like `Rocks and roll with boobs`."""
        self.shake()
        return self.faker(lang).sentence()

    def any_int(self, min_value: int = 0, max_value: int = 100) -> int:
        """Any int from range."""
        random.seed(random.randint(0, 99999))
        return random.randint(min_value, max_value)

    def any_int_pos(self) -> int:  # noqa
        """Any int positive."""
        random.seed(random.randint(0, 99999))
        return self.any_int(min_value=1, max_value=100)  # noqa

    def any_int_neg(self) -> int:
        """Any int negative."""
        return self.any_int(min_value=-100, max_value=-1)

    def any_bool(self) -> bool:  # noqa
        """Any bool."""
        random.seed(random.randint(0, 99999))
        return random.choice([True, False])

    def any_url(self) -> str:
        """Any url."""
        self.shake()
        return self.faker().url()

    def any_image_url(self) -> str:
        """Any image url."""
        self.shake()
        return self.faker().image_url()

    def any_money_amount_float(  # noqa
        self,
        min_amount: float = 0,
        max_amount: float = 99999.99,
    ) -> float:
        """Any money amount, like `1500.50` as float."""
        random.seed(random.randint(0, 99999))
        return round(random.uniform(min_amount, max_amount), ndigits=2)

    def any_money_amount_decimal(  # noqa
        self,
        min_amount: float = 0,
        max_amount: float = 99999.99,
    ) -> Decimal:
        """Any money amount, like `1500.50` as Decimal."""
        amount = round(random.uniform(min_amount, max_amount), ndigits=2)
        return Decimal(str(amount))


faker = I18nFaker(
    en=_Faker(locale='en_US'),
    ru=_Faker(locale='ru_RU'),
)


__all__ = (
    'ApiClient',
    'AppClient',
    'XClient',
    'faker',
)
