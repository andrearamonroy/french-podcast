from fileinput import filename
from flask import Flask, jsonify, request, redirect, url_for
import os 
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import click
from flask.cli import with_appcontext
from werkzeug.utils import secure_filename




app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xrbncjawkgbyyk:cd7cf74f97fd80a43cc5422fceaa88f3b1618374cfad73d771930a34e6f65017@ec2-44-199-22-207.compute-1.amazonaws.com:5432/dfp3agm8fn43e7' 
#+ os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
 
 
#ma = Marshmallow()

#bind_key = none problem, need bidings in all tables
#Solution: Override SQLAlchemy get_tables_for_bind() to support '__all__'.
class MySQLAlchemy(SQLAlchemy):
    def get_tables_for_bind(self, bind=None):
        result = []
        for table in self.Model.metadata.tables.values():
            # if table.info.get('bind_key') == bind:
            if table.info.get('bind_key') == bind or (bind is not None and table.info.get('bind_key') == '__all__'):
                result.append(table)
        return result

db = MySQLAlchemy(app)
db.init_app(app)
    
class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(100), unique=True)
    units = db.relationship('Unit', backref='level')

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(250), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    podcasts = db.relationship('Podcast', backref='unit')

class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    podcast_name = db.Column(db.String(250), nullable=False)
    podcast = db.Column(db.Text)
    image = db.Column(db.Text)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))

#podcast schema
class PodcastSchema(Schema):
    class Meta:
        fields = ('id', 'podcast_name', 'podcast', 'image' ,'unit_id')  

#unit schema
class UnitSchema(Schema):
    class Meta:
        fields = ('id', 'unit_name', 'level_id', 'podcasts') 
    podcasts = fields.Nested(PodcastSchema, many=True)

#level
class LevelSchema(Schema):
    class Meta:
        fields = ('id', 'level_name', 'units')
    units = fields.Nested(UnitSchema, many=True)

#init level schema
level_schema = LevelSchema()
levels_schema = LevelSchema(many=True)

#init unit schema
unit_schema = UnitSchema()
unit_schema = UnitSchema(many=True)

#init podcast schema
podcast_schema = PodcastSchema()
podcast_schema= PodcastSchema(many=True)

#save podcast
# podcasts_folder = '/Users/andreamonroy/Documents/postgres/static/podcasts'
# app.config['podcasts_folder'] = podcasts_folder

# def save_file(filename, data):
#     path = os.path.join(app.config['podcasts_folder'], filename)
#     fp = open(path, 'wb')
#     fp.write(data)
#     fp.close()

#save_file('dialogue1.mp3', 'mp3')


#save image
# images_folder = '/Users/andreamonroy/Documents/postgres/static/images'
# app.config['images_folder'] = images_folder

# def save_image(filename, data):
#     path = os.path.join(app.config['images_folder'], filename)
#     fp = open(path, 'wb')
#     fp.write(data)
#     fp.close()

#save_image('dig1.png', 'png')


#binary data 
# def load_file(filename):
#     path = os.path.join(app.config['podcasts_folder'], filename)
#     fp = open(path, 'rb')
#     data = fp.read()
#     fp.close()
#     return data

# load_file('dialogue1.mp3')

# level1 = Level(level_name='Débutant')
# level2 = Level(level_name='Intermédiaire')
# level3 = Level(level_name='Avancé')

# unit1 = Unit(unit_name='Unit 1', level= level1)
# unit2 = Unit(unit_name='Unit 1', level= level2)
# unit3 = Unit(unit_name='Unit 1', level= level3)

podcast1 = Podcast(podcast_name = 'vous êtes', podcast = 'https://french-podcast-bucket.s3.us-east-2.amazonaws.com/dialogue1.mp3', image = 'https://french-podcast-bucket.s3.us-east-2.amazonaws.com/dig1.png', unit = unit1 )

# db.drop_all()

@app.cli.command(name='create_tables')
@with_appcontext
def create_tables():
    #db.drop_all()
    db.create_all()
    #db.session.add_all([level1,level2,level3])
    #db.session.add_all([unit1,unit2,unit3])
    db.session.add_all([podcast1])
    db.session.commit()


@app.route('/api/levels', methods=['GET'])
def get_levels():
    all_levels = Level.query.all()
    output = levels_schema.dump(all_levels)
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)
