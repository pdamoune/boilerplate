import os
import click

from app import create_app

app = create_app(os.getenv('FLASK_ENV') or 'default')


# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Role=Role)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""  # TODO single unittest don't work
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
