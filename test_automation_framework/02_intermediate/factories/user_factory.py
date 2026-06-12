"""Фабрика тестовых пользователей."""

from dto.user_dto import UserDTO


class UserFactory:
    """Генерирует предустановленных и случайных пользователей."""

    @staticmethod
    def standard_user() -> UserDTO:
        return UserDTO(
            username="standard_user",
            password="secret_sauce",
            first_name="John",
            last_name="Doe",
        )

    @staticmethod
    def locked_out_user() -> UserDTO:
        return UserDTO(
            username="locked_out_user",
            password="secret_sauce",
            first_name="Locked",
            last_name="Out",
        )

    @staticmethod
    def problem_user() -> UserDTO:
        return UserDTO(
            username="problem_user",
            password="secret_sauce",
            first_name="Problem",
            last_name="User",
        )

    @classmethod
    def all_users(cls) -> list[UserDTO]:
        return [
            cls.standard_user(),
            cls.locked_out_user(),
            cls.problem_user(),
        ]


class ProductFactory:
    """Генерирует тестовые товары."""

    @staticmethod
    def sauce_labs_backpack():
        from dto.product_dto import ProductDTO
        return ProductDTO(
            name="Sauce Labs Backpack",
            description="carry.allTheThings()",
            price=29.99,
        )

    @staticmethod
    def sauce_labs_bike_light():
        from dto.product_dto import ProductDTO
        return ProductDTO(
            name="Sauce Labs Bike Light",
            description="A red light isn't the desired state",
            price=9.99,
        )

    @classmethod
    def all_products(cls):
        return [
            cls.sauce_labs_backpack(),
            cls.sauce_labs_bike_light(),
        ]
