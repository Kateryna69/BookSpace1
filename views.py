from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegisterForm, LoginForm, BookForm
from .models import User, Book, Genre
from . import db, csrf

main_bp = Blueprint("main", __name__)
books_bp = Blueprint("books", __name__)
auth_bp = Blueprint("auth", __name__)


@main_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    genre_id = request.args.get("genre", type=int)
    books_query = Book.query

    if q:
        books_query = books_query.filter(
            db.or_(Book.title.ilike(f"%{q}%"), Book.author.ilike(f"%{q}%"))
        )
    if genre_id:
        books_query = books_query.filter_by(genre_id=genre_id)

    books = books_query.order_by(Book.created_at.desc()).all()
    genres = Genre.query.order_by(Genre.name).all()
    return render_template(
        "index.html",
        books=books,
        genres=genres,
        active_genre=genre_id,
        q=q,
    )


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        flash("Реєстрація успішна. Тепер увійдіть.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not check_password_hash(user.password_hash, form.password.data):
            flash("Невірні логін або пароль.", "danger")
            return render_template("login.html", form=form)
        login_user(user)
        flash("Ви успішно увійшли!", "success")
        return redirect(url_for("main.index"))
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з акаунту.", "info")
    return redirect(url_for("main.index"))


@books_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_book():
    form = BookForm()
    form.genre.choices = [(g.id, g.name) for g in Genre.query.order_by(Genre.name).all()]
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            genre_id=form.genre.data,
            cover_url=form.cover_url.data or None,
            description=form.description.data,
        )
        db.session.add(book)
        db.session.commit()
        flash("Книга додана.", "success")
        return redirect(url_for("main.index"))
    return render_template("book_form.html", form=form)


@books_bp.route("/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book_detail.html", book=book)


@books_bp.route("/<int:book_id>/favorite")
@login_required
def toggle_favorite(book_id):
    book = Book.query.get_or_404(book_id)
    if book in current_user.favorites:
        current_user.favorites.remove(book)
        flash("Книга видалена з обраного.", "info")
    else:
        current_user.favorites.append(book)
        flash("Книга додана до обраного.", "success")
    db.session.commit()
    return redirect(request.referrer or url_for("main.index"))


@books_bp.route("/<int:book_id>/read")
@login_required
def toggle_read(book_id):
    book = Book.query.get_or_404(book_id)
    if book in current_user.read:
        current_user.read.remove(book)
        flash("Книга прибрана зі списку прочитаних.", "info")
    else:
        current_user.read.append(book)
        flash("Книга позначена як прочитана.", "success")
    db.session.commit()
    return redirect(request.referrer or url_for("main.index"))


@books_bp.route("/<int:book_id>/delete", methods=["POST"])
@login_required
@csrf.exempt
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Книга видалена.", "info")
    return redirect(url_for("main.index"))


@books_bp.route("/favorites")
@login_required
def favorites():
    return render_template(
        "favorites.html",
        favorites=current_user.favorites,
        read=current_user.read,
    )