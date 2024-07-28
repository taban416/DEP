from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,logout_user,login_required,UserMixin,current_user,login_user
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:taban@localhost/database1'
dtb=SQLAlchemy(app)
app.config['SECRET_KEY']='taban369#'
bcrypt=Bcrypt(app)
loginmanager=LoginManager(app)
loginmanager.login_view='login'
#///////////////////////////////////////////
#
#creating a column in database
#
#////////////////////////////////////////////
class usr(dtb.Model,UserMixin):
    id=dtb.Column(dtb.Integer,primary_key=True)
    Name=dtb.Column(dtb.String(100),nullable=False,unique=True)
    password=dtb.Column(dtb.String(100),nullable=False)
@loginmanager.user_loader
def loader_user(user_id):
    return usr.query.get(int(user_id))
with app.app_context():
    dtb.create_all()
 #///////////////////////////////////////////////////////
 # 
 # GETTING DATA FROM HTML PAGE AND ADD TO DATABASE
 #               
 # /////////////////////////////////////////////////////


#///////////////////////////
#
#THIS REGISTERATION PAGE
#
#//////////////////////////

@app.route('/',methods=['POST','GET'])
def register():
    if request.method=='POST':
        name=request.form['username']
        password=request.form['password']
        hsh_password=bcrypt.generate_password_hash(password).decode('utf_8')
        dtb_data=usr(Name=name,password=hsh_password)
        dtb.session.add(dtb_data)
        dtb.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

#////////////////////
#                   
#THIS IS LOGIN PAGE
#
#///////////////////
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        name=request.form['username']
        password=request.form['password']
        user_db_data=usr.query.filter_by(Name=name).first()
        if user_db_data and bcrypt.check_password_hash(user_db_data.password,password):
            login_user(user_db_data)
            return redirect(url_for('profile'))
        
    return render_template('login.html')
#/////////////////////
#
#USER PROFILE
#//////////////////////
@app.route('/profile')
@login_required
def profile():
    
    return redirect(url_for('getting_user'))
    
#/////////////////////
#
#USER LOGOUT
#//////////////////////
@app.route('/logout')
@login_required
def logot():
    logout_user()
    return redirect(url_for('login'))


#///////////////////////////////////
#
#CRUDE OPERATIONS
#
#/////////////////////////////////

#//////////////////////////////
#1:GETTING RECORD FROM DATABASE
#////////////////////////////////
@app.route('/get_list')
def getting():
    user_rec1=usr.query.all()
    fr=[ {'name':user.Name} for user in user_rec1]
   
    return jsonify({'list':fr})
#////////////////////////////
#2:DELETING DATABASE RECORD
#3: UPDATING DATABASE RECORD
#///////////////////////////
@app.route('/user_operation',methods=['POST','GET'])
def getting_user():

    user_rec1=usr.query.all()
    fr=[ user.Name for user in user_rec1]
    
    if request.method=='POST':
         new_name=request.form['new_name']
         name1=request.form['name']
         operation=request.form['operation']
         #/////////////////////
         #
         #HERE WE DELETE NAME
         #
         #/////////////////////
         if name1 in fr:
             if operation=='delete':
                  
                  user_rec=usr.query.filter(usr.Name==name1).delete()
                  dtb.session.commit()
                  return 'successfully deleted'
             #/////////////////////
             #
             #HERE WE UPDATE NAME
             #
             #////////////////////
             elif operation=='update':
                 user_rec=usr.query.filter(usr.Name==name1).update({'Name':new_name})
                 dtb.session.commit()
                 return 'successfully updated'
                 
                 
             
            
         else:
             return 'user not in list or empty list'
    return render_template('operation.html')
         

   




app.run(debug=True)