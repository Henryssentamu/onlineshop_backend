from flask import Flask, redirect,request,render_template, redirect,url_for,flash, jsonify
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField,EmailField,PasswordField
from wtforms.validators import ValidationError,DataRequired, EqualTo
import sqlite3

from product_details import product_details_and_orderDetails_databases
import uuid

# function call which creates product and orderDetails details database
product_details_and_orderDetails_databases()



app = Flask("__name__")


app.config["SECRET_KEY"] = "LKFIR/']UIUT458kjiuyt5838484789ekrueyYUY4dy4IUJMLKO858"







def create_database():
    with sqlite3.connect("CUSTOMER_DETAILS.db") as database:
        cursor = database.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientCredentails(
                    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ClientId VARCHAR(5) PRIMARY KEY,
                    FirstName VARCHAR(50),
                    SirName VARCHAR(50),
                    UserName VARCHAR(50) 
            )
        """)



    with sqlite3.connect("CUSTOMER_DETAILS.db") as database:
        cursor = database.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientPhoneNumber(
                    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PhoneId INTEGER PRIMARY KEY AUTOINCREMENT,
                    ClientId INTEGER,
                    
                    Number VARCHAR(50),
                    FOREIGN KEY (ClientId) REFERENCES clientCredentails(ClientId)
            )
        """)
        
    with sqlite3.connect("CUSTOMER_DETAILS.db") as database:
        cursor = database.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientEmails(
                    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    EmailId INTEGER PRIMARY KEY AUTOINCREMENT,
                    ClientId INTEGER,
                    
                    Email VARCHAR(50),
                    FOREIGN KEY (ClientId) REFERENCES clientCredentails(ClientId)
            )
        """)


    with sqlite3.connect("CUSTOMER_DETAILS.db") as database:
        cursor = database.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords(
                    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PasswordId INTEGER PRIMARY KEY AUTOINCREMENT,
                    ClientId INTEGER,
                    
                    Password VARCHAR(50),
                    FOREIGN KEY (ClientId) REFERENCES clientCredentails(ClientId)
            )
        """)
    

    # with sqlite3.connect("product_details.db") as database:
    #     cursor = database.cursor()

    #     cursor.execute("""
    #         CREATE TABLE IF NOT EXIST order_details(
    #                    Date TIMESTAMP DEFUALT CURRENT_TIMESTAMP,
    #                    OrderId INTEGER PRIMARY KEY AUTOINCREMENT,
    #                    ProductId VARCHAR(2),
    #                    OrderQantity VARCHAR(10),
    #                    DeliveryPoint VARCHAR(50),
    #                    FOREIGN KEY(ProductId) REFERENCES product_details(ProductId)
                    

    #         )
    #     """)


class creatAccountForm(FlaskForm):
    first_name = StringField("First Name ",validators=[DataRequired()])
    sir_name = StringField("Sir Name", validators=[DataRequired()])
    email = EmailField(label="Youre Email ", validators=[DataRequired()])
    phone_number = StringField("Phone Number",validators=[DataRequired("start with cuntry code: Eg +256782866055 for Uganda,")])
    user_name = StringField(label="Set User Name", validators=[DataRequired()])

    password = PasswordField(label="Password",validators=[DataRequired(message="set a strong password with  8 or more characters ")])
    confirm_password = PasswordField(label="Confirm Your Password", validators=[DataRequired(), EqualTo('password',message="password didnt match, try again ! ")])
    submit = SubmitField(label="Submit")



class loginForm(FlaskForm):
    username = StringField(label="User name", validators=[DataRequired()])
    email = EmailField(label="Your Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


@app.route("/product_details",methods=["GET"])
def send_data():
    # this function retrive data from the product details database and send it to frontend to create main page product container

    with sqlite3.connect("product_details.db") as database:
        cursor = database.cursor()
        cursor.execute("""
            SELECT ProductId, Name,Image,Price
            FROM productDetails
        """)
        product_details_list = cursor.fetchall()
        data = []
        for product in product_details_list:
            data.append(
                {"productId": product[0], "name":product[1],"image":product[2],"price":product[3]}
            )
        #print(f"editted :{data}")

    return jsonify(data)


@app.route("/",methods=["GET", "POST"])
def home():
    return render_template("general-site-html.html")




@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    create_database()
    form = creatAccountForm()
    first_name = None
    sir_name = None
    email = None
    phone_number = None
    user_name = None
    password = None
    confirm_password = None
    flash("your password didnt match with what you confirmed")

    if form.validate_on_submit():
        client_id = str(uuid.uuid4())[:5]


        first_name = form.first_name.data
        sir_name = form.sir_name.data
        email = form.email.data
        phone_number = form.phone_number.data
        user_name = form.user_name.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # submit = submit()

        # re-intialize the variables and making the feilds empty for new data fill

        form.first_name.data = ""
        form.sir_name.data= ""
        form.email.data = ""
        form.phone_number.data = ""
        form.user_name.data = ""
        form.password.data = ""
        form.confirm_password.data = ""

        if password != confirm_password:
            # this should take you back to the form
            return redirect(url_for("create_account"))
        else:

            with sqlite3.connect("CUSTOMER_DETAILS.db") as database:
                cursor = database.cursor()
                cursor.execute("""
                    INSERT INTO clientCredentails( ClientId, FirstName,SirName,UserName) VALUES(?,?,?,?)
                """,(client_id,first_name, sir_name, user_name))
                database.commit()

            with sqlite3.connect("CUSTOMER_DETAILS.db") as database:
                cursor = database.cursor()
                cursor.execute("""
                    INSERT INTO clientPhoneNumber( ClientId, Number ) VALUES(?,?)
                """,(client_id,phone_number))
                database.commit()

            with sqlite3.connect("CUSTOMER_DETAILS.db") as database:
                cursor = database.cursor()
                cursor.execute("""
                    INSERT INTO clientEmails( ClientId,Email ) VALUES(?,?)
                """,(client_id,email))
                database.commit()


            with sqlite3.connect("CUSTOMER_DETAILS.db") as database:
                cursor = database.cursor()
                cursor.execute("""
                    INSERT INTO passwords( ClientId,Password ) VALUES(?,?)
                """,(client_id, password))
                database.commit()
        return redirect(url_for('home'))

    return render_template("create_account.html", accountform = form)

            




@app.route("/login", methods=["GET","POST"])
def login():
    form = loginForm()
    username = None
    email = None
    password = None

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        form.username.data= ""
        form.email.data = ""
        form.password.data = ""
        if username and email and password:
            with sqlite3.connect("CUSTOMER_DETAILS.db") as database:
                # api for login system
                cursor  = database.cursor()
                cursor.execute("""
                    SELECT c.UserName, p.Password, e.Email FROM clientCredentails c
                    JOIN passwords p on p.ClientId == c.ClientId
                    JOIN clientEmails e on e.ClientId == c.ClientId

                """)
                clientList = cursor.fetchall()
            # print(clientList)
            for clientLoginDetails in clientList:
                if username in clientLoginDetails and email in clientLoginDetails and password in clientLoginDetails:
                    return redirect(url_for("home", name = username))
                else:
                    message = "incorrect credientials "
                    return redirect(url_for('login'))
            
                
    return render_template("login.html", loginform = form)





# api for both retriving order details  data from the frontend side which will be used to querry product database for more details and these details are sent to the frontend to generate the chart html page

@app.route("/data_api", methods=["GET", "POST"])
def handle_data():
    # this is a demo data but actual data will be quered from the product database
    
    if request.method == "GET":
        # handling get request from frontend, (ie send data to frontend )
        try:
            try:
                with sqlite3.connect("product_details.db") as database:
                    cursor = database.cursor()
                    cursor.execute("""
                        SELECT p.Name, p.Price, p.Image, o.OrderId, o.OrderQantity,o.DeliveryPoint
                        FROM productDetails as p
                        JOIN orderDetails as o ON p.ProductId == o.ProductId

                    """)
                    data = cursor.fetchall()
                    new_data = []
                    print("ready to be sent to front", data)
                    for details in data:
                        new_data.append({"name":details[0],"price":details[1], "image":details[2],"orderid":details[3], "orderqantity":details[4],"deliverypoint":details[5]})


                
            except sqlite3.Error as e:
                print(f"Database error: {str(e)}")
                return jsonify({"error","Database error"}),500
            return jsonify(new_data)
        except Exception as e:
            # print(f"error processing get request: {str(e)}")
            return jsonify({"error":"internal server error"}),500

    elif request.method == "POST":
        # handling post request from the frontend (ie retrive data from font end )
        data = request.get_json()
        for order in data:
            id = int(order["product_Id"])
            qantity = int(order["ordered_Qantity"])
            location = order["DeliveryTo"]
            with sqlite3.connect("product_details.db") as database:
                cursor = database.cursor()
                cursor.execute("""
                    INSERT INTO orderDetails(ProductId,OrderQantity,DeliveryPoint) VALUES(?,?,?)
                """,(id,qantity,location ))
                database.commit()
        else:
            print("data has been posted to the database")

        
        # print("orderdetails here",data)
        

        return jsonify({ "message":"data from frontend", "data": data})











@app.route("/orders_returns")
def orders_returns():
    pass

@app.route("/view_chart")
def view_chart():
    return render_template("view_chart.html")



if __name__ == "__main__":
    app.run(debug=True)