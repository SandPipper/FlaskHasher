import os
from app import create_app
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate
from app.models import User, Vocabulary, UserInfo
import psycopg2

app = create_app("default")
manager = Manager(app)

from app import db
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Vocabulary=Vocabulary,
                UserInfo=UserInfo)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    test = unittest.TestLoader().discover("test")
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def get_info():
    fileName   = 'users.xml'
    message    = '<users>\n'
    tableNames = ['users', 'userinfo', 'vocabulary']


    conn = psycopg2.connect("dbname='flaskhasher_dev' user='postgres' host='localhost' password='your_password'")


    with open(fileName, 'w+') as outfile:
        cursor  = conn.cursor()
        outfile.write('<?xml version="1.0" ?>\n')
        outfile.write(message)
        for tableName in tableNames:
            columnList = []
            cursor.execute("SELECT column_name from information_schema.columns where table_name = '%s'" % tableName)
            columns = cursor.fetchall()

            for column in columns:
                columnList.append(column[0])

            cursor.execute("select * from  %s" % tableName)
            rows = cursor.fetchall()


            for row in rows:
                outfile.write('  <row>\n')
                for i in range(len(columnList)):
                    outfile.write('    <%s>%s</%s>\n' % (columnList[i], row[i],
                                                                columnList[i]))
                outfile.write('  </row>\n')
        outfile.write(message)


if __name__ == "__main__":
    manager.run()
