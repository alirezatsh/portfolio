from flask import Flask , render_template , redirect , request , url_for , flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase2.sqlite"
app.config["SECRET_KEY"] =   "mysecretkey"
db = SQLAlchemy(app)

class Projects(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30) , nullable=False)


class ContactForm(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30) , nullable=False)
    email = db.Column(db.String(30) , nullable=False)
    title = db.Column(db.String(30) , nullable=False)
    text = db.Column(db.String(120) , nullable=False)



with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    project = Projects.query.all()
    return render_template('home.html' , project = project)


@app.route('/panel' , methods = ['GET' , 'POST'])
def panel():
    if request.method == 'GET':
        contacts = ContactForm.query.all()
        return render_template('panel.html' , contacts = contacts)
    elif request.method == 'POST':
        input_name = request.form.get('i_name')
        new_project = Projects(name = input_name)
        db.session.add(new_project)
        db.session.commit()
        flash('پروژه با موفقیت ایجاد شد!', 'success')
        return redirect(url_for('index'))
    
    
@app.route('/delete/<int:project_id>')
def delete(project_id):
    project_d = db.get_or_404(Projects , project_id)
    db.session.delete(project_d)
    db.session.commit()
    flash('پروژه با موفقیت حذف شد!', 'success')
    return redirect(url_for('index'))


@app.route('/delete2/<int:contact_id>')
def delete2(contact_id):
    contact_d = db.get_or_404(ContactForm , contact_id)
    db.session.delete(contact_d)
    db.session.commit()
    flash('پیام با موفقیت حذف شد!', 'success')
    return redirect(url_for('index'))


@app.route('/' , methods = ['GET' , 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        i_name = request.form.get('form_name')
        i_email = request.form.get('form_email')
        i_title = request.form.get('form_title')
        i_text = request.form.get('form_text')
        new_contact = ContactForm(name = i_name , email = i_email , title = i_title , text = i_text)
        db.session.add(new_contact)
        db.session.commit()
        flash('پیام شما با موفقیت ارسال شد' , 'success')
        return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')




if __name__ == '__main__':
    app.run(debug=False)