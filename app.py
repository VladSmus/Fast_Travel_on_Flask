# Импорт необходимых модулей из библиотек Flask и Flask-WTF
from flask import Flask, render_template
from flask_wtf import FlaskForm

# Импорт классов полей из модуля wtforms
from wtforms import StringField, IntegerField, SubmitField, TelField, RadioField

# Импорт валидаторов из модуля wtforms.validators
from wtforms.validators import InputRequired

# Импорт модуля SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр Flask с названием приложения
app = Flask(__name__)

# Установка URI для подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Создаем объект базы данных
db = SQLAlchemy(app)

# Класс Пользователя для базы данных
class User(db.Model):
    #Указываем им таблицы
    __tablename__ = 'users'

    # Заводим поля
    UID = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(80))
    name = db.Column(db.String(80))
    middle_name = db.Column(db.String(80))
    pol = db.Column(db.String(20))
    age = db.Column(db.Integer)
    from_city = db.Column(db.String(80))
    to_city = db.Column(db.String(80))
    type_of_transport = db.Column(db.String(80))
    tariff = db.Column(db.String(20))
    price = db.Column(db.Integer)
    is_active = db.Column(db.Boolean)
    email = db.Column(db.String(120))
    phone = db.Column(db.Integer)

    # Инициализатор для создания объектов класса
    def __init__(self,last_name, name, middle_name, pol, age, from_city,to_city,type_of_transport,tariff,price, is_active, email, phone):
        self.last_name = last_name
        self.name = name
        self.middle_name = middle_name
        self.pol = pol
        self.age = age
        self.from_city = from_city
        self.to_city = to_city
        self.type_of_transport = type_of_transport
        self.tariff = tariff
        self.price = price
        self.is_active = is_active
        self.email = email
        self.phone = phone

    # Метод для текстового представления объекта Пользователя
    def __str__(self):
        return f'<Пользователь {self.name}, {self.from_city}, {self.age}>'

# Определение класса формы регистрации
class RegistrationForm(FlaskForm):  
    # Заводим поля
    last_name = StringField(validators=[InputRequired()])
    name = StringField(validators=[InputRequired()])
    middle_name = StringField(validators=[InputRequired()])
    pol = RadioField(label='Пол', choices=[(0 ,'Мужской' ), (1, 'Женский')]) 
    age = IntegerField()
    from_city = StringField()
    to_city = StringField()
    type_of_transport = RadioField(label='Вид транспорта', choices=[(0 ,'Самолёт' ), (1, 'Поезд'),(2, 'Теплоход')]) 
    tariff = RadioField(label='Тариф', choices=[(0 ,'Эконом' ), (1, 'Бизнес')]) 
    price = RadioField(label='Цена', choices=[(0 ,'3490' ), (1, '12690'),(2, '37800')])
    email = StringField(validators=[InputRequired()])
    phone = TelField(validators=[InputRequired()])
    
    # Поле кнопки отправки формы
    submit = SubmitField(label=('Submit'))


# Обработчик маршрута для главной страницы
@app.route('/')
def index():
    return render_template('main.html')

# Обработчик маршрута для страницы пользователей с таблицей
@app.route('/users')
def users():
    #SELECT запрос на получение всей таблицы (список записей)
    people = User.query.all() 
    # Вывод полученных Пользователей в консоль
    for user in people:
        print(user)
    # Возвращаем html c таблицей
    return render_template('users.html', users = people)

# Обработчик маршрута для страницы регистрации
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    # Создаем экземпляр формы для регистрации
    form = RegistrationForm()

    # Проверяем, была ли форма отправлена и прошла ли валидацию
    if form.validate_on_submit():
        # Если форма прошла валидацию, получаем данные из полей формы
        last_name,name, middle_name, pol, age, from_city, to_city, type_of_transport, tariff, price, email, phone =  form.last_name.data, form.name.data, form.middle_name.data, form.pol.data, form.age.data,  form.from_city.data, form.to_city.data, form.type_of_transport.data, form.tariff.data, form.price.data , form.email.data, form.phone.data         
        # Выводим данные формы в консоль для отладки
        print(last_name,name, middle_name, pol, age, from_city, to_city, type_of_transport, tariff, price, email, phone)
        # Создаем новый объект Пользователя
        new_user = User(last_name=last_name,name=name, middle_name=middle_name, pol='Мужской' if pol == 0 else 'Женский',age=age, from_city=from_city, to_city=to_city, type_of_transport= 'Самолёт' if type_of_transport == 0 else'Поезд'   , tariff= 'Эконом' if tariff == 0 else 'Бизнес', price='12690' if price == 0   else  '37800',  email=email, phone=phone, is_active=True)
        db.session.add(new_user)  # Добавляем Пользователя в базу данных
        db.session.commit()  # Фиксация изменений в базе данных
        # Возвращаем приветственное сообщение (html) с использованием имени пользователя
        return render_template('success_reg.html', name=name)
    
    # Если форма не была отправлена или не прошла валидацию,
    # отображаем HTML-шаблон с формой регистрации,
    # передавая объект формы для отображения введенных пользователем данных
    return render_template('reg_form_wtf.html', form=form)


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False  # Отключаем проверку CSRF для WTForms
    app.run(debug=True)  # Запускаем приложение в режиме отладки
