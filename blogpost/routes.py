from crypt import methods
from email.quoprimime import quote
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from blogpost import app, db, bcrypt
from blogpost.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm
from blogpost.models import Quote, User, Post, Comments
from flask_login import login_user, current_user, logout_user, login_required
import requests
import json



def get_quote():
    quote_url = 'http://quotes.stormconsultancy.co.uk/random.json'
    req = requests.get(quote_url)
    data = json.loads(req.content)
    quote = Quote(data["quote"],data["author"])
    return quote


@app.route('/')
    
@app.route("/home")
@login_required
def home():
    quote = get_quote()
    page = request.args.get('page', 1, type=int)
   
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    return render_template("home.html", posts=posts, quote=quote)



@app.route("/register", methods=['GET', 'POST'] )
def register():
   
    
    if current_user.is_authenticated:
        
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        
        
        flash('Your account has been created you can now Login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
           
        # if form.email.data == 'wayne@qq.com' and form.password.data == '12345':
        #     flash('You have been logged in!', 'success')
        #     return redirect(url_for('home'))
        else:
            flash('Invalid Credentials! Check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# Custom Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('fourOwfour.html'),404



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


 
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    quote = get_quote()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data , category=form.category.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form,legend='New Post',quote=quote)


# @app.route("/post/<int:post_id>", methods=['GET', 'POST'])
# def post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated', 'alert alert-primary')
#         return redirect(url_for('post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


# @app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
        
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title= form.title.data
#         post.content= form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

# @app.route("/post/<int:post_id>/delete", methods=['POST', 'GET'])
# @login_required
# def delete_post(post_id): 
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted!', 'alert alert-success')
#     return redirect(url_for('home'))

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comments.query.order_by(Comments.date_posted.desc()).filter_by(post_id=post_id)
    form = CommentForm()
    if form.validate_on_submit():
      if form.upvote.data:
        recent = post.likes
        new = recent + 1
        post.likes = new
        db.session.commit()

      if form.downvote.data:
        recent = post.dislikes
        new = recent + 1
        post.dislikes = new
        db.session.commit()

      comment = Comments(content=form.content.data, user_comments= current_user, post_id=post_id)
      db.session.add(comment)
      db.session.commit()
      flash('Your comment has been updated', 'primary')
      return redirect(url_for('post', post_id=post_id))
    return render_template('post.html', post=post, form=form, comments=comments)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title= form.title.data
        post.content= form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
    
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id): 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    flash('Your post has been deleted!', 'alert alert-success')
    return redirect(url_for('home'))






