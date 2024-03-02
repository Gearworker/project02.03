from flask import render_template, redirect, request, Flask
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
from forms.user import RegisterForm
from data import db_session
from data.users import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# class RegisterForm(FlaskForm):
#     email = EmailField('Login/email', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     password_again = PasswordField('Repeat password', validators=[DataRequired()])
#     surname = StringField('Surname', validators=[DataRequired()])
#     name = StringField('Name', validators=[DataRequired()])
#     age = StringField('Age', validators=[DataRequired()])
#     position = StringField('Position', validators=[DataRequired()])
#     speciality = StringField('Speciality', validators=[DataRequired()])
#     address = StringField('Address', validators=[DataRequired()])
#     submit = SubmitField('Submit')
#
#     def __init__(self, formdata=_Auto, **kwargs):
#         super().__init__(formdata, kwargs)
#         self.hashed_password = None
#
#     def set_password(self, password):
#         self.hashed_password = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.hashed_password, password)


def main():
    db_session.global_init("mars.db")
    app.run()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
