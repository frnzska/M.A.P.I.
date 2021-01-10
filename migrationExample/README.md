### commands

`flask db init`
creates migration repo by adding migration folder

`flask db migrate -m "Initial migration."`
creates first migration. Manual proof required since
Alembic does not detect  table name changes, column name changes, or anonymously named constraints.
Note: Add migration generated files to version control. 

Apply migration with:
`flask db upgrade`


####Mit flask-script:

initialize manager
```
manager = Manager(app)
manager.add_command('db', MigrateCommand)
```
and add to main
```
if __name__ == '__main__':
    manager.run()
```

Migrate with 

```
$ python manage.py db init
$ python manage.py db migrate -m 'msg'
$ python manage.py db upgrade
$ python manage.py db --help
```
