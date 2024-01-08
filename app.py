from flask import Flask, render_template,request,flash ,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user 
from datetime import datetime 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dave.db'
app.config['SECRET_KEY']='thisissecretkeyABC'


login_manager = LoginManager()
login_manager.init_app(app)
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
app.app_context().push()

class User(UserMixin,db.Model):
    # Id : Field which stores unique id for every row in 
    # database table.
    # first_name: Used to store the first name if the user
    # last_name: Used to store last name of the user
  
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(140),unique=True,nullable=False)
    
 
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.first_name} {self.last_name}" 

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),unique=True,nullable=False)
    author = db.Column(db.String(20),unique=True,nullable=False)
    content = db.Column(db.Text(),nullable=True)
    pub_date = db.Column(db.DateTime(),nullable=False,default=datetime.utcnow)
    # pub_date = db.Column(db.DateTime(),nullable=False,default=datetime.today())
    
    
    def __repr__(self):
        # return f"Title: {self.title} {self.author}"
        return 'Blog %r>' , self.title



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def main():
    # return "<p>Hello, World!</p>"
    return render_template('main.html')

@app.route("/index")
def index():
    data = Blog.query.all()
    return render_template('index.html',data=data)

@app.route("/register",methods=['GET','POST'])
def register():
    # return "<p>This is register Page</p>"
    if request.method== "POST":
        email= request.form.get('email')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        uname=request.form.get('uname')
        password=request.form.get('password')
        
        user = User(user_name=uname,first_name=fname,last_name=lname,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        flash('Usr has been registered successfully','success')
        return redirect('/login')
        
        
    return render_template("register.html")


# @app.route("/")
# def index():
#     # return "<p>Hello, World!</p>"
#     return render_template('index.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
    # return "<p>This is login Page</p>"
        username=request.form.get('username')
        password=request.form.get('password')
        user = User.query.filter_by(user_name=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/index')
        else:
            flash('Invalid Credentials','danger')
            return redirect('/login')
        
    return render_template('login.html')

@app.route("/blog",methods=['GET','POST'])
def blogpost():
    # return "<p>Hello, World!</p>"
    if request.method== "POST":
        title= request.form.get('title')
        author=request.form.get('author')
        content=request.form.get('content')
        
        blog = Blog(title=title,author=author,content=content)
        db.session.add(blog)
        db.session.commit()
        flash('Your post has been successfully','success')
        return redirect('/index')
 
    return render_template('blog.html')

@app.route("/logout")
# @login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route("/blog_detail/<int:id>",methods=['GET','POST'])
def blog_detail(id):
    blog = Blog.query.get(id)

    return render_template('blog_detail.html',blog=blog)

@app.route("/delete/<int:id>",methods=['GET','POST'])
def delete_post(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash("Post has been deleted",'success')

    return redirect('/index')

@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit_post(id):
    blog = Blog.query.get(id)
    if request.method=="POST":
        blog.title=request.form.get('title')
        blog.author=request.form.get('author')
        blog.content=request.form.get('content')
        db.session.commit()
        flash("Post has been updated",'success')
        return redirect('/index')

    return render_template('edit.html',blog=blog)


if __name__ =="__main__":
 with app.app_context():
        db.create_all()
        app.run(debug=True,port=8000)