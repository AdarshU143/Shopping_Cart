class Item:
    def __init__(self, name="undefined", price=10.0, stock=0, discount=0.0, taxable=True):
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__discount = discount
        self.__taxable = taxable

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_discount(self):
        return self.__discount

    def get_taxable(self):
        return self.__taxable

    def set_price(self, price):
        self.__price = price

    def set_stock(self, stock):
        self.__stock = stock

    def set_discount(self, discount):
        self.__discount = discount

    def set_taxable(self, taxable):
        self.__taxable = taxable

    def print_item(self):
        print(f"Name: {self.__name}, Price: {self.__price}, Stock: {self.__stock}, Discount: {self.__discount}%, Taxable: {self.__taxable}")


def create_items():
    all_items = []
    try:
        with open("items_info.txt", "r") as file:
            for line in file:
                name, price, stock, discount, taxable = line.strip().split(',')
                item = Item(name, float(price), int(stock), float(discount), taxable == 'y')
                all_items.append(item)
    except FileNotFoundError:
        print("Error: items_info.txt not found.")
    return all_items


def online_shopping(all_items):
    cart = {}
    while True:
        print("\nOptions: show, add, delete, cart, check out, done")
        choice = input("Enter your choice: ").lower()

        if choice == "show":
            for item in all_items:
                print_item_info(item)
        elif choice == "add":
            add_to_cart(all_items, cart)
        elif choice == "delete":
            delete_from_cart(all_items, cart)
        elif choice == "cart":
            display_cart(cart, all_items)
        elif choice == "check out":
            checkout(cart, all_items)
            break
        elif choice == "done":
            break
        else:
            print("Invalid option. Please choose again.")


def print_item_info(item):
    discounted_price = item.get_price() - item.get_price() * item.get_discount() / 100
    print(f"Name: {item.get_name()}, Price: {item.get_price()}, Discounted Price: {discounted_price}")


def add_to_cart(all_items, cart):
    item_name = input("Enter the name of the item you want to add: ")
    item = find_item_by_name(all_items, item_name)

    if item and item.get_stock() > 0:
        quantity = int(input("Enter the quantity you want to add: "))
        if quantity <= item.get_stock():
            if item_name in cart:
                cart[item_name] += quantity
            else:
                cart[item_name] = quantity
            print(f"{quantity} {item_name}(s) added to your cart.")
            item.set_stock(item.get_stock() - quantity)
        else:
            print(f"Error: Not enough stock for {item_name}.")
    else:
        print(f"Error: Item {item_name} not found or out of stock.")


def delete_from_cart(all_items, cart):
    item_name = input("Enter the name of the item you want to delete: ")
    item = find_item_by_name(all_items, item_name)

    if item_name in cart and item:
        quantity = int(input("Enter the quantity you want to delete: "))
        if quantity <= cart[item_name]:
            cart[item_name] -= quantity
            print(f"{quantity} {item_name}(s) deleted from your cart.")
            item.set_stock(item.get_stock() + quantity)
            if cart[item_name] == 0:
                del cart[item_name]
        else:
            print(f"Error: Not enough {item_name} in your cart.")
    else:
        print(f"Error: Item {item_name} not found in your cart or not available.")


def display_cart(cart, all_items):
    total_price = 0
    for item_name, quantity in cart.items():
        item = find_item_by_name(all_items, item_name)
        discounted_price = item.get_price() - item.get_price() * item.get_discount() / 100
        total_price += discounted_price * quantity
        print(f"{item_name}: {quantity} x {discounted_price} = {quantity * discounted_price}")

    sales_tax_rate = 4.225
    sales_tax = total_price * sales_tax_rate / 100
    final_amount = total_price + sales_tax

    print(f"\nTotal Price (after discount): {total_price}")
    print(f"Sales Tax: {sales_tax}")
    print(f"Final Amount: {final_amount}")


def checkout(cart, all_items):
    display_cart(cart, all_items)

    for item_name, quantity in cart.items():
        item = find_item_by_name(all_items, item_name)
        discounted_price = item.get_price() - item.get_price() * item.get_discount() / 100
        total_price = discounted_price * quantity
        item.set_stock(item.get_stock() - quantity)
        item.set_price(discounted_price)

    write_updated_items_info(all_items)


def find_item_by_name(all_items, item_name):
    for item in all_items:
        if item.get_name() == item_name:
            return item
    return None


def write_updated_items_info(all_items):
    with open("items_info_updated.txt", "w") as file:
        for item in all_items:
            file.write(f"{item.get_name()},{item.get_price()},{item.get_stock()},{item.get_discount()},{ 'y' if item.get_taxable() else 'n'}\n")


def main():
    all_items = create_items()
    online_shopping(all_items)


if __name__ == "__main__":
    main()
