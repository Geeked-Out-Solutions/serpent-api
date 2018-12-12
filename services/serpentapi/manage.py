# services/serpentapi/manage.py


import coverage
import unittest

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models.user import User
from project.api.models.snake import Snake


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.xml_report()
        COV.erase()
        return 0
    return 1


@cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(User(
        username='monty',
        email='monty@python.org',
        password='holygrail'
    ))
    db.session.add(User(
        username='vader',
        email='vader@starwarz.org',
        password='lukesfather'
    ))
    db.session.commit()

    snake_1 = {
        "owner_id": 1,
        "name": 'sir hiss',
        "description": 'test description',
        "snake_genus": 'ball python',
        "alive": True,
        "added_date": '2018-04-20T04:20:00.00+00:00',
        "modified_at": '2018-04-20T04:20:00.00+00:00'
    }

    snake_2 = {
        "owner_id": 2,
        "name": 'hedwig',
        "description": 'test description',
        "snake_genus": 'ball python',
        "alive": True,
        "added_date": '2018-04-20T04:20:00.00+00:00',
        "modified_at": '2018-04-20T04:20:00.00+00:00'
    }

    monty_snake = Snake(snake_1)
    vader_snake = Snake(snake_2)
    monty_snake.save()
    vader_snake.save()
    


if __name__ == '__main__':
    cli()
