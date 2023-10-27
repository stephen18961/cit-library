from flask import Blueprint, render_template, abort, redirect, request, session, url_for, flash
from jinja2 import TemplateNotFound
from models import *
import base64
from sqlalchemy.exc import IntegrityError
from datetime import date


admin_page = Blueprint('admin', __name__, template_folder='templates')

@admin_page.route('/login-admin', methods=['POST', 'GET'])
def login_admin():
    if request.method == 'POST':
        admin_id = request.form['uname']
        password = request.form['psw']
    elif request.method == 'GET':
        return render_template('admin/login.html')

    admin = Admin.query.filter_by(id=admin_id).first()

    if (admin) and (admin.password == password):
        session['login'] = True
        session['id'] = admin.id
    else:
        flash("Passwords do not match. Please try again.", "danger")
        return render_template('admin/login.html')
    
    return redirect(url_for('admin.dashboard'))

@admin_page.route('/dashboard')
def dashboard():
    if not session.get('login'):
        return redirect(url_for('admin.login_admin'))
    else:
        return render_template('admin/borrow.html')
    
@admin_page.route('/logout-admin')
def logout_admin():
    if session.get('login'):
        session.pop('login', None)
        session.pop('id', None)
    return redirect(url_for('admin.login_admin'))
    
@admin_page.route('/bibliography')
def bibliography():
    if not session.get('login'):
        return redirect(url_for('admin.login_admin'))
    else:
        books = Book.query.all()
        for book in books:
            if book.image:
                # Mengonversi blob gambar menjadi data URL
                book.image = "data:image/jpeg;base64," + base64.b64encode(book.image).decode('utf-8')
        return render_template('admin/bibliography.html', books=books)

# CRUD BOOKS ------------------------------------------
@admin_page.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if not session.get('login'):
        return redirect(url_for('admin.login_admin'))
    
    if request.method == 'POST':
        book_id = request.form['book_id']
        existing_book = Book.query.filter_by(book_id=book_id).first()

        if existing_book:
            flash('ID buku sudah ada dalam database', 'danger')
        else:
            category = request.form['category']
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            description = request.form['description']
            status = bool(request.form.get('status'))

            # Mengambil file gambar yang diunggah oleh pengguna
            image = request.files['image']

            # Membaca file gambar sebagai blob
            image_blob = image.read()

            book = Book(book_id=book_id, category=category, title=title, author=author, isbn=isbn, status=status, image=image_blob, description=description)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('admin.bibliography'))

    return render_template('admin/add_book.html')


@admin_page.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get(book_id)
    if request.method == 'POST':
        book.category = request.form['category']
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.description = request.form['description']
        book.status = bool(request.form.get('status'))
        
        new_image = request.files['new_image']
        if new_image:
            book.image = new_image.read()  # Menyimpan gambar baru jika diunggah

        db.session.commit()
        return redirect(url_for('admin.bibliography'))

    if book.image:
        # Mengonversi blob gambar menjadi data URL
        book.image = "data:image/jpeg;base64," + base64.b64encode(book.image).decode('utf-8')

    return render_template('admin/edit_book.html', book=book)


@admin_page.route('/delete/<book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('admin.bibliography'))

#CRUD end of line --------------------------------------------

# BORROW AND RETURN ------------------------------------------
@admin_page.route('/borrow')
def borrow():
    if not session.get('login'):
        return redirect(url_for('admin.login_admin'))
    else:
        return render_template('admin/borrow.html')
    
@admin_page.route('/check-borrow', methods=['GET', 'POST'])
def check_borrow():
    if not session.get('login'):
        return redirect(url_for('admin.login_admin'))

    NIM = request.args.get('nim')
    BOOK_ID = request.args.get('kode-buku')

    user = User.query.filter_by(nim=NIM).first()
    book = Book.query.filter_by(book_id=BOOK_ID).first()

    if not user:
        flash("NIM not found", "danger")
        return redirect(url_for('admin.borrow'))
    if not book:
        flash("Book not found", "danger")
        return redirect(url_for('admin.borrow'))

    return render_template('admin/check-borrow.html', user=user, book=book)

@admin_page.route('/check-borrow/<book_id>/<NIM>', methods=['POST'])
def borrow_book(book_id, NIM):
    book = Book.query.get(book_id)

    user = User.query.filter_by(nim=NIM).first()
    if book:
        book.status = 0
        db.session.commit()
        flash("Book status updated successfully", "success")
        
        # Create a new transaction record
        today = date.today()
        transaction = Transactions(
            nim=user.nim,
            book_id=book.book_id,
            tanggal_peminjaman=today
        )
        db.session.add(transaction)
        db.session.commit()
    else:
        flash("Book not found", "danger")
        
    return redirect(url_for('admin.dashboard'))

@admin_page.route('/return', methods=['GET', 'POST'])
def retur():
    if not session.get('login'):
        return redirect(url_for('admin.login_admin'))
    else:
        return render_template('admin/return.html')
    
    
@admin_page.route('/check-return', methods=['GET', 'POST'])
def check_return():
    if not session.get('login'):
        return redirect(url_for('admin.login_admin'))
    
    NIM = request.args.get('nim')
    BOOK_ID = request.args.get('kode-buku')

    user = User.query.filter_by(nim=NIM).first()
    book = Book.query.filter_by(book_id=BOOK_ID).first()

    if not user:
        flash("NIM not found", "danger")
        return redirect(url_for('admin.borrow'))
    if not book:
        flash("Book not found", "danger")
        return redirect(url_for('admin.borrow'))
    
    # if book.status == 1:
    #     flash("Book is not borrowed", "danger")
    #     return redirect(url_for('admin.borrow'))

    transactions = Transactions.query.filter_by(book_id = BOOK_ID).first()
    transactions.denda = transactions.hitung_denda()

    return render_template('admin/check-return.html', user=user, book=book, transaction=transactions)

@admin_page.route('/check-return/<book_id>/<NIM>', methods=['POST'])
def return_book(book_id, NIM):
    book = Book.query.get(book_id)
    user = User.query.get(NIM)

    if not user:
        flash("NIM not found", "danger")
        return redirect(url_for('admin.borrow'))
    if not book:
        flash("Book not found", "danger")
        return redirect(url_for('admin.borrow'))
    
    # if book.status == 1:
    #     flash("Book is not borrowed", "danger")
    #     return redirect(url_for('admin.borrow'))

    if book:
        book.status = 1
        db.session.commit()
        flash("Book status updated successfully", "success")

        # # Create a new history of transacion.
        # today = date.today()
        # transaction_hist = TransactionsHistory(
        #     nim=user.nim,
        #     book_id=book.book_id,
        #     tanggal_selesai=today
        # )
        # db.session.add(transaction_hist)

        transaction = Transactions.query.filter_by(book_id=book_id).first()
        transaction.tanggal_selesai = date.today()
        db.session.commit()
    else:
        flash("Book not found", "error")

    return redirect(url_for('admin.retur'))

# TRANSACTIONS ----------------------------------------------
@admin_page.route('/transactions', methods=['POST', 'GET'])
def show_transactions():
    transactions = Transactions.query.order_by(Transactions.tanggal_peminjaman).all()

    for transaction in transactions:
        transaction.denda = transaction.hitung_denda()

    return render_template('admin/transactions.html', transactions=transactions)

# REGISTER USERS ---------------------------------------------
@admin_page.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('login'):
        return redirect(url_for('admin.login_admin'))
    
    if request.method == 'POST':
        nama = request.form.get('nama')
        nim = request.form.get('nim')
        password = request.form.get('psw')
        repeat_password = request.form.get('psw-repeat')
        
        if password != repeat_password:
            flash("Passwords do not match. Please try again.", "danger")
            return render_template('admin/register.html')
        
        try:
            new_user = User(nim=nim, nama=nama, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account registered successfully!", "success")
        except IntegrityError as e:
            db.session.rollback()
            flash("User with this NIM already exists.", "danger")

        return render_template('admin/register.html')
        
    return render_template('admin/register.html')
