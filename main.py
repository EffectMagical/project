from flask import Flask, render_template, request
from data import db_session
from data.text import Text
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, validators, SelectField

from cryptogrs_decrs import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main(text_):
    db_session.global_init("db/blogs.db")
    user = Text()
    user.text = text_
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def last_entry():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(Text).all()
    last = user[-1].text
    db_sess.query(Text).filter(Text.text == user[-1].text).delete()
    db_sess.commit()
    return last


class EncryptionForm(FlaskForm):
    ciphers_list = SelectField('Шифры', choices=[(0, 'Цезарь'), (1, 'Замена'), (2, 'Перестановка'),
                                                 (3, 'Транскрипция-кирилици'), (4, 'Транскрипция-латиници'),
                                                 (5, 'Геошифр')])
    keys_encryption = TextAreaField("Введите переменную", [validators.InputRequired(),
                                                           validators.Length(max=100)])
    text_input = TextAreaField("Введите текст (макс символов: 1000)", [validators.InputRequired(),
                                                                       validators.Length(max=1000,
                                                                                         message=
                                                                                         'Макс. символов: 1000')],
                               render_kw={'rows': 15, 'cols': 60})
    cipher_btn = SubmitField('Зашифровать')


class DecryptionForm(FlaskForm):
    ciphers_list2 = SelectField('Шифры', choices=[(0, 'Цезарь'), (1, 'Замена'), (2, 'Перестановка'),
                                                  (3, 'Транскрипция-кирилици'), (4, 'Транскрипция-латиници'),
                                                  (5, 'Геошифр')],
                                default=0)
    keys_encryption2 = TextAreaField("Введите переменную", [validators.InputRequired(),
                                                            validators.Length(max=100)])
    text_input2 = TextAreaField("Введите текст (макс символов: 1000)", [validators.InputRequired(),
                                                                        validators.Length(max=1000,
                                                                                          message=
                                                                                          'Макс. символов: 1000')],
                                render_kw={'rows': 15, 'cols': 60})
    decipher_btn = SubmitField('Расшифровать')


@app.route('/', methods=['GET', 'POST'])
def encryption():
    en_form = EncryptionForm()
    if en_form.validate_on_submit():
        if request.method == 'POST':
            if en_form.ciphers_list.data == '1':
                en_form.text_input.data = encrypt(en_form.text_input.data)
                main(en_form.text_input.data)
            elif en_form.ciphers_list.data == '2':
                en_form.text_input.data = encode(en_form.keys_encryption.data, en_form.text_input.data)
                main(en_form.text_input.data)
            elif en_form.ciphers_list.data == '3':
                en_form.text_input.data = transcription1(en_form.text_input.data)
                main(en_form.text_input.data)
            elif en_form.ciphers_list.data == '4':
                en_form.text_input.data = transcription2(en_form.text_input.data)
                main(en_form.text_input.data)
            elif en_form.ciphers_list.data == '5':
                en_form.text_input.data = geoshifr(en_form.text_input.data, en_form.keys_encryption.data)
                main(en_form.text_input.data)
            else:  # Цезарь
                en_form.text_input.data = caesar_cipher(en_form.text_input.data, en_form.keys_encryption.data)
                main(en_form.text_input.data)
    return render_template('encrypt.html', title='Шифрование', form=en_form)


@app.route('/decryption', methods=['GET', 'POST'])
def decryption():
    de_form = DecryptionForm()
    if de_form.validate_on_submit():
        if request.method == 'POST':
            if de_form.ciphers_list2.data == '1':
                de_form.text_input2.data = decrypt(de_form.text_input2.data)
            elif de_form.ciphers_list2.data == '2':
                de_form.text_input2.data = deencode(de_form.keys_encryption2.data, de_form.text_input2.data)
            elif de_form.ciphers_list2.data == '3':
                de_form.text_input2.data = detranscription1(de_form.text_input2.data)
            elif de_form.ciphers_list2.data == '4':
                de_form.text_input2.data = detranscription2(de_form.text_input2.data)
            elif de_form.ciphers_list2.data == '5':
                de_form.text_input2.data = degeoshifr(de_form.text_input2.data, de_form.keys_encryption2.data)
            else:
                de_form.text_input2.data = caesar_decipher(de_form.text_input2.data, de_form.keys_encryption2.data)
    return render_template('decrypt.html', title='Расшифрование', form=de_form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

# from flask import Flask, render_template, request

# from flask_wtf import FlaskForm
# from wtforms import TextAreaField, SubmitField, validators, SelectField

# from cryptogrs_decrs import *


# class EncryptionForm(FlaskForm):
#     ciphers_list = SelectField('Шифры', choices=[(0, 'Цезарь'), (1, 'Шифр'), (2, 'Шифр2'),
#                                                  (3, 'Транскрипция1'), (4, 'Транскрипция2'), (5, 'Геошифр')])
#     text_input = TextAreaField("Введите текст (макс символов: 1000)", [validators.InputRequired(),
#                                                                        validators.Length(max=1000,
#                                                                                          message='Макс. символов: 1000')],
#                                render_kw={'rows': 15, 'cols': 60})
#     cipher_btn = SubmitField('Зашифровать')


# class DecryptionForm(FlaskForm):
#     ciphers_list2 = SelectField('Шифры', choices=[(0, 'Цезарь'), (1, 'Шифр'),
#                                                   (3, 'Транскрипция1'), (4, 'Транскрипция2'), (5, 'Геошифр')],
#                                 default=0)
#     text_input2 = TextAreaField("Введите текст (макс символов: 1000)", [validators.InputRequired(),
#                                                                         validators.Length(max=1000,
#                                                                                           message='Макс. символов: 1000')],
#                                 render_kw={'rows': 15, 'cols': 60})
#     decipher_btn = SubmitField('Расшифровать')


# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# @app.route('/', methods=['GET', 'POST'])
# def encryption():
#     en_form = EncryptionForm()
#     if en_form.validate_on_submit():
#         if request.method == 'POST':
#             if en_form.ciphers_list.data == '1':
#                 en_form.text_input.data = encrypt(en_form.text_input.data)
#             elif en_form.ciphers_list.data == '2':
#                 # en_form.text_input.data = encode(en_form.text_input.data) - key?
#                 pass
#             elif en_form.ciphers_list.data == '3':
#                 en_form.text_input.data = transcription1(en_form.text_input.data)
#             elif en_form.ciphers_list.data == '4':
#                 en_form.text_input.data = transcription2(en_form.text_input.data)
#             elif en_form.ciphers_list.data == '5':
#                 # en_form.text_input.data = geoshifr(en_form.text_input.data) - city?
#                 pass
#             else:  # Цезарь
#                 # en_form.text_input.data = caesar_cipher(en_form.text_input.data) - shift?
#                 pass
#     return render_template('encrypt.html', title='Шифрование', form=en_form)


# @app.route('/decryption', methods=['GET', 'POST'])
# def decryption():
#     de_form = DecryptionForm()
#     if de_form.validate_on_submit():
#         if request.method == 'POST':
#             if de_form.ciphers_list2.data == '1':
#                 de_form.text_input2.data = decrypt(de_form.text_input2.data)
#             elif de_form.ciphers_list2.data == '3':
#                 de_form.text_input2.data = detranscription1(de_form.text_input2.data)
#             elif de_form.ciphers_list2.data == '4':
#                 de_form.text_input2.data = detranscription2(de_form.text_input2.data)
#             elif de_form.ciphers_list2.data == '5':
#                 # de_form.text_input2.data = degeoshifr(de_form.text_input2.data) - city?
#                 pass
#             else:  # Цезарь
#                 # de_form.text_input2.data = caesar_decipher(de_form.text_input2.data) - shift?
#                 pass
#     return render_template('decrypt.html', title='Расшифрование', form=de_form)


# if __name__ == '__main__':
#     app.run(port=8080, host='127.0.0.1')
