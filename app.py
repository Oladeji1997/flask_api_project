from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize Flask App
app = Flask(__name__)

# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(50), nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

    def __init__(self, first_name, last_name, dob, amount_due):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.amount_due = amount_due

# Define Schema
class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

# Create Database Tables
with app.app_context():
    db.create_all()

# Routes for CRUD Operations

# 1. Create a Student Record
@app.route("/student", methods=["POST"])
def add_student():
    data = request.json
    new_student = Student(
        first_name=data["first_name"],
        last_name=data["last_name"],
        dob=data["dob"],
        amount_due=data["amount_due"]
    )
    db.session.add(new_student)
    db.session.commit()
    return student_schema.jsonify(new_student)

# 2. Get All Students
@app.route("/students", methods=["GET"])
def get_students():
    all_students = Student.query.all()
    return students_schema.jsonify(all_students)

# 3. Get a Single Student by ID
@app.route("/student/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    return student_schema.jsonify(student)

# 4. Update a Student Record
@app.route("/student/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.json
    student.first_name = data.get("first_name", student.first_name)
    student.last_name = data.get("last_name", student.last_name)
    student.dob = data.get("dob", student.dob)
    student.amount_due = data.get("amount_due", student.amount_due)

    db.session.commit()
    return student_schema.jsonify(student)

# 5. Delete a Student Record
@app.route("/student/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})


# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)
