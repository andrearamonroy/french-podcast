from flask import Flask, jsonify
#import os 
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields





app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://xrbncjawkgbyyk:cd7cf74f97fd80a43cc5422fceaa88f3b1618374cfad73d771930a34e6f65017@ec2-44-199-22-207.compute-1.amazonaws.com:5432/dfp3agm8fn43e7' 
#+ os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    

db = SQLAlchemy()
#ma = Marshmallow()


    
class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    french_level = db.Column(db.String(100), unique=True)
    units = db.relationship('Unit', backref='level')

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(250), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))


#unit schema
class UnitSchema(Schema):
    class Meta:
        fields = ('id', 'unit', 'level_id')  

#level
class LevelSchema(Schema):
    class Meta:
        fields = ('id', 'french_level', 'units')
    units = fields.Nested(UnitSchema, many=True)




#init level schema
level_schema = LevelSchema()
levels_schema = LevelSchema(many=True)

#init unit schema
unit_schema = UnitSchema()
unit_schema = UnitSchema(many=True)

# level1 = Level(french_level='Débutant')
# level2 = Level(french_level='Intermédiaire')
# level3 = Level(french_level='Avancé')

# unit1 = Unit(unit='Unit 1', level= level1)
# unit2 = Unit(unit='Unit 1', level= level2)
# unit3 = Unit(unit='Unit 1', level= level3)

db.init_app(app)
with app.app_context(): 
    #db.drop_all()
    db.create_all()
    # db.session.add_all([level1,level2,level3])
    # db.session.add_all([unit1,unit2,unit3])
    db.session.commit()

@app.route('/api/levels', methods=['GET'])
def get_levels():
    all_levels = Level.query.all()
    output = levels_schema.dump(all_levels)
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)

