from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    credentialID = db.Column(db.Integer, default=0)
    firstDay = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<employee %r>' % self.id
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        employee_name = request.form['name']
        credential_ID = request.form['credentials']
        new_employee = Employee(name = employee_name, credentialID=credential_ID)
        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR'
    else:
        employees = Employee.query.order_by(Employee.firstDay).all()        
        return render_template('index.html', employees=employees)
@app.route('/delete/<int:id>')
def delete(id):
    employee_to_delete = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR'
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        employee.name = request.form['name']
        employee.credential_ID = request.form['credentials']

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR: UPDATE ISSUE'

    else:
        return render_template('update.html', employee=employee)


if __name__ ==   "__main__":
    app.run(debug=True)