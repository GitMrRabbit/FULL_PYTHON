"""DTO для товаров (Product Data Transfer Object)."""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class ProductDTO:
    """Модель товара в интернет-магазине."""

    name: str
    description: str = ""
    price: float = 0.0
    image_url: str = ""
    in_stock: bool = True

    def __post_init__(self):
        if self.price < 0:
            raise ValueError(f"Цена не может быть отрицательной: {self.price}")

    @property
    def price_formatted(self) -> str:
        return f"${self.price:.2f}"

    def __str__(self) -> str:
        return f"{self.name} — {self.price_formatted}"


@dataclass
class OrderDTO:
    """DTO заказа."""

    items: list[ProductDTO] = field(default_factory=list)
    total: float = 0.0
    tax: float = 0.0
    status: str = "pending"
    shipping_address: str = ""
    TAX_RATE: ClassVar[float] = 0.08

    def add_item(self, product: ProductDTO) -> None:
        self.items.append(product)
        self._recalculate()

    def _recalculate(self) -> None:
        subtotal = sum(item.price for item in self.items)
        self.tax = subtotal * self.TAX_RATE
        self.total = subtotal + self.tax

    @property
    def item_count(self) -> int:
        return len(self.items)

    def __str__(self) -> str:
        return (f"Order({self.item_count} items, "
                f"total=${self.total:.2f}, status={self.status})")
