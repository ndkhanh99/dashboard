from flask import Flask , redirect , url_for, jsonify, render_template, request, Response, flash

import pymysql

import random

import os

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin , login_required , LoginManager , login_user, logout_user, current_user


app = Flask(__name__ , static_folder='static' , template_folder='templates')

app.config['SECRET_KEY'] = os.urandom(1000) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:duykhanh12345@localhost/dashboard'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#TAO BANG CHO USER DANG NHAP

class User(UserMixin , db.Model):
    
    id = db.Column(db.Integer , primary_key = True)
    
    email = db.Column(db.String(50) , nullable = False)
    
    hovaten = db.Column(db.String(50) , nullable = False)
    
    chucvu = db.Column(db.String(50) , nullable = False)
    
    username = db.Column(db.String(50) , nullable = False)
    
    password = db.Column(db.String(50) , nullable = False)
    
    
    def __init__ ( self, email, hovaten, chucvu, username, password ):
        
        self.email = email
        
        self.hovaten = hovaten
        
        self.chucvu = chucvu 
        
        self.username = username
        
        self.password = password 
        

#TAO BANG CHO MENU THUC DON

class Item (db.Model):
    
    id = db.Column(db.Integer , primary_key = True) 
    
    title = db.Column(db.String(200) , nullable = False)
    
    price = db.Column(db.String(200) , nullable = False)
    
    text = db.Column(db.String(200) , nullable = False)
    
    img1 = db.Column(db.String(200) , nullable = False)

    
    def __init__ (self , title , price , text , img1 ):
        
        self.title = title
        
        self.price = price 
        
        self.text = text
        
        self.img1 = img1
        

#tao table cho viec order thuc an

class Banso1 (db.Model):
    
    id = db.Column(db.Integer , primary_key = True) 
    
    tablenumber = db.Column(db.String(200) , nullable = False)
    
    table_name = db.Column(db.String(200) , nullable = False)
    
    product_id = db.Column(db.String(200) , nullable = False)
    
    product_title = db.Column(db.String(200) , nullable = False)
    
    product_price = db.Column(db.String(200) , nullable = False)

    
    def __init__ ( self , tablenumber , table_name , product_id , product_title , product_price ):
        
        
        self.tablenumber = tablenumber
        
        self.table_name = table_name
        
        self.product_id = product_id
        
        self.product_title = product_title
        
        self.product_price = product_price 

#Table cho toan bo ban trong nha hang
        
class Alltable (db.Model):
    
    id = db.Column(db.Integer , primary_key = True)
    
    table_number = db.Column(db.Integer , nullable = False)
    
    def __init__( self , table_number ):
        
        self.table_number = table_number

#dssdsda 

class Chosen_table (db.Model):
    
    id = db.Column(db.Integer , primary_key =  True)
    
    table_id = db.Column(db.String(200) , nullable = False)
    
    table_chosen = db.Column(db.String(200) , nullable = False)
    
    user_email = db.Column(db.String(50) , nullable = False)
    
    def __init__(self , table_id , table_chosen , user_email ):
        
        self.table_id = table_id
        
        self.table_chosen = table_chosen
        
        self.user_email = user_email 


login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler

def error():
    
    return redirect(url_for('Login'))


#BACKEND LOGIN DANG NHAP TAI KHOAN
@app.route('/Login' , methods = [ 'GET','POST'])
def Login(): 
    if request.method == 'POST':
        
        username = request.form['username']
            
        password = request.form['password']
            
        user = User.query.filter_by( username = username , password = password ).first()
        
        if not user:
                
            return jsonify({'message':'User Not Found - Please check again your account or create a new account!'})
            
        elif user:
            
            login_user(user)
                 
            return redirect(url_for('Home'))
        
        else:
                
            return "Password not Match"
      
        
    if request.method == 'GET' :
        
        return render_template('login.html')

#Logout

@app.route('/Logout')
def Logout():
    
    Chosen_table.query.filter_by( user_email = current_user.email ).delete()
    
    db.session.commit()
    
    logout_user()
    
    return redirect(url_for('Login'))

    
#BACKEND DANG KI REGISTER
@app.route('/Register' , methods = ['GET' , 'POST'])
def Register():
    
    if request.method == 'POST':
        
        email = request.form['email']
        
        hovaten = request.form['hovaten']
        
        chucvu = request.form['chucvu']
        
        username = request.form['username']
        
        password = request.form['password']
        
        password_check = request.form['password_check']
        
        user_check = User.query.filter_by(email = email).first()
        
        user_name = User.query.filter_by(username = username).first()
        
        if password != password_check:
            
            return jsonify({'message':'Password Does Not Match'})
        
        elif user_check:
            
            return jsonify({'message':'User Already Created' })
        
        elif user_name:
                
            return jsonify({'message':'User Already Created' })
    
        else:
        
            user = User( email, hovaten, chucvu, username , password ) 
            
            db.session.add(user)
                
            db.session.commit()
            
            return jsonify({'message':'TRUE'})
           
    
    if request.method == 'GET':
    
        return render_template('register.html')
    

@app.route('/' , methods = ['GET'])
def Home():
    
        items = Alltable.query.filter().all()  
                    
        return render_template('home.html' , items = items )


#BACKEND THEM MON AN CHO MENU 

@app.route('/add_product' , methods = [ 'GET', 'POST'])
def add_product():
    
    if request.method == 'POST':
    
        title = request.form['title']
        
        price = request.form['price']
        
        text = request.form['text']
        
        img1 = request.files['img1']
        
        item = Item( title , price , text , img1.read() )
        
        db.session.add(item)
        
        db.session.commit()
        
        flash(f"Add Successful")
        
        return redirect(request.referrer)
    
    else:
    
        return render_template('/add_product.html')
    
#BACKEND THEM SO BAN TABLE TRONG NHA HANG

@app.route('/add_table' , methods = [ 'GET', 'POST'])
def add_table():
    
    if request.method == 'POST':
    
        table_number = request.form['table_number']
        
        itemss = Alltable( table_number )
        
        db.session.add(itemss)
        
        db.session.commit()
        
        flash(f"Add Successful")
        
        return redirect(request.referrer)
    
    else:
    
        return render_template('/add_table.html')

#BACKEND CHO TRANG HIEN THI THUC DON 

@app.route('/item_img_1/<int:id>')
def get_img_1(id):
    
    img = Item.query.filter_by(id = id).first()

    return Response(img.img1 , mimetype='jpeg')  
    
@app.route('/menu')
def menu():
    
    item = Item.query.filter().all()
    
    return render_template('/menu.html' , item = item )


#BACKEND CHON BAN


@app.route('/checkbn/<int:id>' , methods = ['GET'])
def checktable(id):
    
    list_do_an = []
    
    list_price = []
    
    list_number = []
    
    table_order = Banso1.query.filter_by(tablenumber = id).all()
    
    for i in table_order:
        
        list_do_an.append(i.product_title)
        list_price.append(i.product_price)
    
    return jsonify(table_order = list_do_an , table_price = list_price) 
        
          
    
@app.route('/chon-ban-1/<int:id>' , methods = ['GET'])
@login_required 
def chonban(id):
    
    user_email = current_user.email
    
    print(user_email)
    
    table_order = Alltable.query.filter_by( id = id ).first()
    
    items = Item.query.filter().all()
    
    table_id = id 
    
    table_chosen = table_order.table_number
    
    chosen_table = Chosen_table( table_id , table_chosen , user_email )
    
    db.session.add(chosen_table)
    
    db.session.commit()
    
    return jsonify({'ok':'sdasdad'})


#backend chon mon an 
@app.route('/add-to-ban-1/<int:id>' , methods = ['GET'])
def add(id):
    
    items = Item.query.filter_by( id = id ).first()
    
    tableorder = Chosen_table.query.filter().all()
    
    
    for i in tableorder:
    
        tablenumber  = i.table_id
        
        table_name = i.table_chosen
    
    
    product_id = id
        
    product_title = items.title
        
    product_price = items.price
    
    monanbanso1 = Banso1(tablenumber , table_name , product_id , product_title , product_price )
    
    db.session.add(monanbanso1)
    
    db.session.commit()
    
    return jsonify({'oke':'dada'})


@app.route('/ban-ordering')
@login_required
def ordering():

    items = Item.query.filter().all()
    
    return render_template('ban1.html' , items = items )

@app.route('/hosonhanvien')
def quanli():
    
    itm = User.query.filter().all()
    
    return render_template('nhanvien.html' , itm = itm )



if __name__ == '__main__':
        
    app.run(debug = True , port = 5050)
