from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
)
from .models import User


class RegisterForm(FlaskForm):
    username = StringField(
        "Ім'я користувача",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired(), Length(min=6, max=64)],
    )
    confirm = PasswordField(
        "Підтвердити пароль",
        validators=[DataRequired(), EqualTo("password", message="Паролі не збігаються.")],
    )
    submit = SubmitField("Зареєструватися")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Користувач з таким ім'ям вже існує.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Користувач з таким email вже існує.")


class LoginForm(FlaskForm):
    username = StringField("Ім'я користувача", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Увійти")


class BookForm(FlaskForm):
    title = StringField("Назва", validators=[DataRequired(), Length(max=200)])
    author = StringField("Автор", validators=[DataRequired(), Length(max=120)])
    genre = SelectField("Жанр", coerce=int, validators=[DataRequired()])
    cover_url = StringField("URL обкладинки", validators=[Length(max=255)])
    description = TextAreaField(
        "Короткий опис",
        validators=[DataRequired(), Length(max=1000)],
    )
    submit = SubmitField("Зберегти")