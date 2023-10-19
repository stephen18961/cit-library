from flask import Blueprint, render_template, abort, redirect, request, session, url_for, flash
from jinja2 import TemplateNotFound
from models import *
import base64
from sqlalchemy.exc import IntegrityError
from datetime import timedelta, date


user_page = Blueprint('user', __name__, template_folder='templates')

@user_page.route('/', methods=["GET", "POST"])
def default():
    return redirect(url_for('user.index'))

@user_page.route('/index', methods=["GET", "POST"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for('user.login'))
    
    category = request.args.get('category')  # Get the category from the query string
    if category:
        books = Book.query.filter_by(category=category).all()
    else:
        books = Book.query.all()
    
    return render_template('user/index.html', books=books)

@user_page.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user_id = request.form['nim']
        password = request.form['psw']
    elif request.method == 'GET':
        return render_template('user/login.html')

    user = User.query.filter_by(nim=user_id).first()

    if (user) and (user.password == password):
        session['logged_in'] = True
        session['id'] = user.nim
    else:
        flash("Wrong username or password. Please try again.", "danger")
        return render_template('user/login.html')
    
    return redirect(url_for('user.index'))

@user_page.route('/logout')
def logout_admin():
    if session.get('logged_in'):
        session.pop('logged_in', None)
        session.pop('id', None)
    return redirect(url_for('user.login'))

@user_page.route('/peminjaman', methods=["GET", "POST"])
def peminjaman():
    if not session.get("logged_in"):
        return redirect(url_for('user.login'))
    
    nim = session.get('nim')

    borrowed_books_with_date = db.session.query(Book, Transactions.tanggal_peminjaman).\
    join(Transactions, Transactions.book_id == Book.book_id).\
    filter(Transactions.nim == nim).\
    all()

    print(borrowed_books_with_date)

    # Calculate the deadline date for each book (7 days after the transaction date)
    today = date.today()
    borrowed_books_with_deadline = [(book, transaction_date, transaction_date + timedelta(days=7)) for book, transaction_date in borrowed_books_with_date]

    # Calculate the remaining days for each book's return
    remaining_days = [(deadline - today).days for _, _, deadline in borrowed_books_with_deadline]

    return render_template('user/peminjaman.html', borrowed_books=borrowed_books_with_deadline, remaining_days=remaining_days)
    

@user_page.route('/pustakawan')
def pustakawan():
    if not session.get("logged_in"):
        return redirect(url_for('user.login'))
    
    return render_template('user/pustakawan.html')

@user_page.route('/lokasi')
def lokasi():
    if not session.get("logged_in"):
        return redirect(url_for('user.login'))
    
    return render_template('user/lokasi.html')