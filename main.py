from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


class MovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    ranking = StringField('Ranking', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    img = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MovieToDelete(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie))
    all_movies = result.scalars()
    return render_template("index.html", all=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieForm()
    if request.method == "POST":
        new_movie = Movie(
            title=request.form["title"],
            year=request.form["year"],
            description=request.form["description"],
            rating=request.form["rating"],
            ranking=request.form["ranking"],
            review=request.form["review"],
            img_url=request.form["img"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html", form=form)

# new_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the
#     Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to
#     keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down
#     by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation
#     with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()



@app.route("/edit")
def edit():
    return render_template("edit.html")


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = MovieToDelete()
    if form.validate_on_submit():
        # Gets data from the form
        movie_name = form.title.data

        del_movie = Movie.query.filter_by(title=movie_name).first()
        if del_movie:
            db.session.delete(del_movie)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('select.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
