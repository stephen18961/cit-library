from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    nim = db.Column(db.String(9), primary_key = True)
    nama = db.Column(db.String(128), nullable = False)
    password = db.Column(db.String(128), nullable = False)

    def __repr__(self):
        return f'<User nomor_induk={self.nomor_induk}>'
    

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.String(32), primary_key = True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return f'<ADMIN id={self.admin}>'

class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.String(5), primary_key = True)
    category = db.Column(db.String(32), nullable = False)
    title = db.Column(db.String(128), nullable = False)
    author = db.Column(db.String(128), nullable = False)
    isbn = db.Column(db.String(128), nullable = True)
    status = db.Column(db.Boolean, nullable = False)
    description = db.Column(db.String(720), nullable = True)
    image = db.Column(db.LargeBinary, nullable=False)

class Transactions(db.Model):
    tablename = 'transactions'

    id_transaksi = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(9), db.ForeignKey('users.nim'), nullable=False)
    book_id = db.Column(db.String(5), db.ForeignKey('books.book_id'), nullable=False)
    tanggal_peminjaman = db.Column(db.Date, nullable=False)

    def hitung_denda(self):
            tanggal_sekarang = date.today()
            selisih_hari = (tanggal_sekarang - self.tanggal_peminjaman).days
            if selisih_hari > 7:
                denda = (selisih_hari - 7) * 1000
            else:
                denda = 0

            return denda