import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from mvt import app, db, bcrypt, mail, s
from mvt.forms import RegistrationForm, LoginForm, EventForm, UpdateAccountForm
from mvt.models import User, Events
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature


@app.route("/")
@app.route("/home")
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'heroimage.jpg')
    return render_template('home.html', title='Home', userimage=full_filename)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm Email', sender='', recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = "Hello from Nagpur Startup community! Click on the link to verify your account! Your link is {}".format(link)
        mail.send(msg)
        flash('We have sent you an email for verification!','success')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', title='Register', form=form)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    form = RegistrationForm()
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        flash('The token has expired, try again','danger')
        return render_template('register.html', title='Register', form=form)   
    except BadTimeSignature:
        flash('The token is broken! Wow that rhymes:p !Try again','danger')
        return render_template('register.html', title='Register', form=form)    
    flash('Account created!','success')
    return redirect(url_for('login'))
    





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
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/event", methods=['GET', 'POST'])
@login_required
def eventpage():
    form = EventForm()
    if form.validate_on_submit():
        event = Events(eventname=form.eventname.data, 
                            eventlocation=form.eventlocation.data, eventdate=form.eventdate.data, user_id=current_user.id)
        db.session.add(event)
        db.session.commit()        
        flash('Event has been created!', 'success')
        return redirect(url_for('home'))
    image_file = url_for('static', filename='eventpics/default.jpg')
    #page = request.args.get('page', 1, type=int)
    events = Events.query.order_by(Events.eventdate.desc())#.paginate(page=page, per_page=5)
    return render_template('event.html', title='Event', form=form, eventshow = events, eventpic=image_file)

@app.route("/memberlisting")
@login_required
def members():
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    users = User.query.all()
    return render_template('memberlisting.html', title='Members', users=users, userimage=image_file)


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


@app.route("/profile", methods=['GET', 'POST'])
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
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Account',
                           userimage=image_file, form=form)

