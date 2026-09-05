"""列表、元组、集合与切片示例。"""


def unique_recent_products(products: list[str], start: int) -> set[str]:
    """返回指定位置之后出现过的不同商品。"""
    return set(products[start:])


def main() -> None:
    products = ["Pen", "Notebook", "Pen", "Mouse"]
    order = ("Notebook", 2, 12.5)
    recent_products = unique_recent_products(products, 1)

    print("切片：", products[1:3])
    print("订单元组：", order)
    print("不同商品：", sorted(recent_products))
    print("共同客户：", sorted({"C1", "C2"} & {"C2", "C3"}))


if __name__ == "__main__":
    main()
