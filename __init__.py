from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
import config

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .views import main_bp, books_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from . import models

    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    
    from .models import Genre, Book

    if Genre.query.first():
        return

    detective = Genre(name="Детектив")
    romance = Genre(name="Роман")
    fantasy = Genre(name="Фентезі")

    db.session.add_all([detective, romance, fantasy])
    db.session.flush()  

    books = [
        Book(
            title="Виживуть п'ятеро",
            author="Голі Джексон",
            genre=detective,
            cover_url="/static/image/five_survive.jpg",
            description="Компанія підлітків вирушає в подорож, яка перетворюється на смертельну гру, де вижити зможуть не всі.",
        ),
        Book(
            title="Посібник з убивства для хороших дівчат",
            author="Голі Джексон",
            genre=detective,
            cover_url="/static/image/good_girls_guide_murder.jpg",
            description="Старшокласниця розслідує давнє вбивство у своєму містечку та знаходить докази, що суперечать офіційній версії.",
        ),
        Book(
            title="Хірург",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/the_surgeon.jpg",
            description="Бостон шокують жорстокі вбивства, а слідчі розуміють, що копіюються методи маніяка з минулого.",
        ),
        Book(
            title="Асистент",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/the_apprentice.jpg",
            description="Нові злочини натякають, що в хірурга-вбивці з’явився послідовник, і полювання йде одразу на двох.",
        ),
        Book(
            title="Грішна",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/the_sinner.jpg",
            description="У монастирі знаходять мертву черницю, і розслідування відкриває моторошні таємниці за стінами обителі.",
        ),
        Book(
            title="Двійник",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/body_double.jpg",
            description="Судово-медична експертка знаходить жінку, схожу на неї як дві краплі води, і починає шукати правду про себе.",
        ),
        Book(
            title="Смертниці",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/vanish.jpg",
            description="У морзі «оживає» невідома жінка, а лікарня стає сценою небезпечної заручницької драми.",
        ),
        Book(
            title="Клуб «Мефісто»",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/mephisto_club.jpg",
            description="Таємний клуб вивчає природу зла, а серія ритуальних убивств змушує повірити в його реальність.",
        ),
        Book(
            title="Хранителі смерті",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/keepers_of_death.jpg",
            description="Старе вбивство пов’язує групу друзів, які багато років приховують спільну страшну таємницю.",
        ),
        Book(
            title="Убивчий холод",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/ice_cold.jpg",
            description="Подорож у засніжені гори закінчується тим, що героїня опиняється в покинутому поселенні без людей.",
        ),
        Book(
            title="Дівчина, яка мовчить",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/the_silent_girl.jpg",
            description="На даху китайського кварталу знаходять обезголовлене тіло, і слід веде до давньої легенди.",
        ),
        Book(
            title="Останній, хто помре",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/last_to_die.jpg",
            description="Троє підлітків, які пережили сімейні трагедії, опиняються в елітній школі, де минуле наздоганяє їх знову.",
        ),
        Book(
            title="Послухай мене",
            author="Тесс Ґеррітсен",
            genre=detective,
            cover_url="/static/image/listen_to_me.jpg",
            description="Мати, якій ніхто не вірить, підозрює щось страшне у поведінці сусідів і починає власне розслідування.",
        ),
        Book(
            title="Панк 57",
            author="Пенелопа Дуглас",
            genre=romance,
            cover_url="/static/image/punk_57.jpg",
            description="Двоє підлітків роками листуються і домовляються ніколи не зустрічатися, аж поки доля не зіштовхує їх у реальному житті.",
        ),
        Book(
            title="Вбивство у «Східному експресі»",
            author="Аґата Крісті",
            genre=detective,
            cover_url="/static/image/murder_on_orient_express.jpg",
            description="У знаменитому поїзді вбивають пасажира, і Еркюль Пуаро шукає убивцю серед замкненої групи людей.",
        ),
        Book(
            title="Гаррі Поттер і філософський камінь",
            author="Дж. К. Ролінґ",
            genre=fantasy,
            cover_url="/static/image/harry_potter1.jpg",
            description="Хлопчик-сирота дізнається, що він чарівник, і вирушає до школи магії Гоґвартс.",
        ),
    ]

    db.session.add_all(books)
    db.session.commit()