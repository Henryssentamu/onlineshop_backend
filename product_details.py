import sqlite3
Data = [
    {
    "id":1,
    "name":"Reveal Cap Toe",
    "image":"static/product-images/51JurNzG3kL._AC_SY575_.jpg",
    "price":6995,
    "availabelSize":[40, 42, 44,45,],
    "availableColors":["Gray","white","black"],
    "CountryofOrigin":"China"}
]



def product_details_and_orderDetails_databases():

    with sqlite3.connect("product_details.db") as database:
        cursor = database.cursor()
        cursor.execute( """CREATE TABLE IF NOT EXISTS productDetails(
                    Date TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
                    ProductId INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name VARCHAR(50),
                    Image VARCHAR(200),
                    Price INTEGER)
                """)




    with sqlite3.connect("product_details.db") as database:
        cursor = database.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orderDetails(
                    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    OrderId INTEGER PRIMARY KEY AUTOINCREMENT ,
                    ProductId INTEGER,
                    OrderQantity INTEGER,
                    DeliveryPoint VARCHAR(50),
                    FOREIGN KEY(ProductId) references productDetails(ProductId)

            )

        """)



    global Data
    Data = Data

    for product in Data:
        name = product["name"]
        Image = product["image"]
        price = product["price"]
        with sqlite3.connect("product_details.db") as database:
            cursor = database.cursor()

            cursor.execute("""
                INSERT INTO productDetails(Name, Image, Price) VALUES(?,?,?)

            """, (name,Image,price))
            database.commit()


