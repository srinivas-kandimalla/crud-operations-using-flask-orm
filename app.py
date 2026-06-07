from flask import Flask, render_template, request, redirect
from models import db, Person

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///people.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    people = Person.query.all()
    return render_template("index.html", people=people)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]

    person = Person(
        name=name,
        age=age
    )

    db.session.add(person)
    db.session.commit()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    person = Person.query.get_or_404(id)

    db.session.delete(person)
    db.session.commit()

    return redirect("/")
@app.route("/edit/<int:id>")
def edit(id):
    person = Person.query.get_or_404(id)
    return render_template("edit.html", person=person)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    person = Person.query.get_or_404(id)

    person.name = request.form["name"]
    person.age = request.form["age"]

    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)