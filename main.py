from datetime import datetime

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(100), nullable=False)
  completed = db.Column(db.Boolean, default=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<User %r>' % self.id


with app.app_context():
  db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    note_content = request.form['content']
    new_note = Note(content=note_content)

    try:
      db.session.add(new_note)
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue adding your task'

  else:
    notes = Note.query.order_by(Note.date_created).all()
    return render_template('index.html', notes=notes)


@app.route('/delete/<int:id>')
def delete(id):
  note_to_delete = Note.query.get_or_404(id)

  try:
    db.session.delete(note_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was an issue deleting that task'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
  note = Note.query.get_or_404(id)
  if request.method== 'POST':
    note.content=request.form['content']
    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'There was an issue updating that task'
  
  else:
    return render_template('update.html',note=note)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
