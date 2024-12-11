'''
Webbshop.py: Ett lager med tio olkia prudukter från n elektronik lagger, där du kan ta bort, lägga till och visa produkter.  

__author__  = "Gustav.Waldenfeldt Uppenberg"
__version__ = "1.0.1"
__email__   = "gustav.waldenfeldtuppenberg@elev.ga.ntig.se"
'''

import csv
import os
import locale
from time import sleep
import uuid  # För att generera unika ID:n för nya produkter

# Skapa en mappning mellan UUID och numeriska ID
id_map = {}

# Läs in produkter från en CSV-fil och returnera en lista.
def load_data(filename):
    products = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader, 1):
                id_map[str(index)] = row['id']  # Skapa mappning
                products.append({
                    "id": row['id'],
                    "name": row['name'],
                    "desc": row['desc'],
                    "price": float(row['price']),
                    "quantity": int(row['quantity']),
                })
    except FileNotFoundError:
        print(f"Filen {filename} hittades inte.")
    return products

# Sparar det nya producter i csv-filen
def save_data(filename, products):
    with open(filename, 'w', newline='') as file:
        fieldnames = ["id", "name", "desc", "price", "quantity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    print("\nÄndringar har sparats.")

# visar det produckter du har som en listan
def view_products(products):
    product_list = []
    for index, product in enumerate(products, 1):
        product_info = (
            f"{index}) (#{index}) {product['name']} "
            f"– {locale.currency(product['price'], grouping=True)} "
            f"({product['quantity']} i lager)"
        )
        product_list.append(product_info)
    return "\n".join(product_list)

# Visa detaljer om en produkt baserat på dess kortare ID.
def view_product(products, id):
    uuid_id = id_map.get(id)
    if not uuid_id:
        return "Produkten hittas inte."
    for product in products:
        if product["id"] == uuid_id:
            return (
                f"Produkt: {product['name']}\n"
                f"Beskrivning: {product['desc']}\n"
                f"Pris: {locale.currency(product['price'], grouping=True)}\n"
                f"Lager: {product['quantity']}"
            )
    return "Produkten hittas inte."

# Lägg till en ny produkt.
def add_product(products):
    try:
        name = input("Ange produktens namn: ").strip()
        desc = input("Ange produktbeskrivning: ").strip()
        price = float(input("Ange produktens pris: ").strip())
        quantity = int(input("Ange antal i lager: ").strip())
        new_id = str(uuid.uuid4())  # Skapa ett unikt ID
        new_short_id = str(len(id_map) + 1)
        id_map[new_short_id] = new_id
        products.append({
            "id": new_id,
            "name": name,
            "desc": desc,
            "price": price,
            "quantity": quantity,
        })
        print(f"Produkten '{name}' har lagts till.")
    except ValueError:
        print("Felaktig inmatning. Försök igen.")

# Ta bort en produkt baserat på dess kortare ID.
def remove_product(products, id):
    uuid_id = id_map.get(id)
    if not uuid_id:
        return "Produkten hittades inte."
    for product in products:
        if product["id"] == uuid_id:
            products.remove(product)
            del id_map[id]
            return f"Produkten '{product['name']}' har tagits bort."
    return "Produkten hittades inte."

# Huvudprogram
def main():
    locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')
    filename = 'db_products.csv'
    products = load_data(filename)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Webbshop Lagerhantering")
        print(view_products(products))
        print("\nAlternativ: (V)isa, (T)a bort, (L)ägga till, (S)para & Avsluta")
        choice = input("Vad vill du göra? ").strip().upper()

        if choice == "V":
            try:
                product_id = input("Ange produktens ID: ").strip()
                print("\n" + view_product(products, product_id))
            except ValueError:
                print("Ogiltig inmatning.")
        elif choice == "T":
            try:
                product_id = input("Ange produktens ID att ta bort: ").strip()
                print("\n" + remove_product(products, product_id))
            except ValueError:
                print("Ogiltig inmatning.")
        elif choice == "L":
            add_product(products)
        elif choice == "S":
            save_data(filename, products)
            print("Programmet avslutas.")
            break
        else:
            print("Ogiltigt val, försök igen.")

        input("\nTryck Enter för att fortsätta")

if __name__ == "__main__":
    main()
