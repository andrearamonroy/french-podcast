import click
from flask import Blueprint
import click
from flask.cli import with_appcontext

from app import db, Level, Unit

level1 = Level(french_level='Débutant')
level2 = Level(french_level='Intermédiaire')
level3 = Level(french_level='Avancé')

unit1 = Unit(unit='Unit 1', level= level1)
unit2 = Unit(unit='Unit 1', level= level2)
unit3 = Unit(unit='Unit 1', level= level3)

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    db.session.add_all([level1,level2,level3])
    db.session.add_all([unit1,unit2,unit3])
    db.session.commit()


