import flask
import flask.ext.sqlalchemy
import flask.ext.restless

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask.ext.sqlalchemy.SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer)
    username = db.Column(db.Unicode, primary_key=True)
    age = db.Column(db.Float)

class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    owner = db.relationship('Person', backref=db.backref('computers', lazy='dynamic'))

db.create_all()

apimanager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# foo.com/api/v1/people/<username>
apimanager.create_api(Person,
    methods=['GET', 'POST', 'DELETE', 'PUT'],
    url_prefix='/api/v1', #defaults to just /api
    collection_name='people') #defaults to class name - person
"""
    allow_patch_many=True,
    validation_exceptions=[ValidationError],
    allow_functions=True, #allow evaluation of sql functions
    include_columns=['name', 'age'],
    exclude_cloumns=['id'],
    results_per_page=20, #<0 to disable pagination
    max_results_per_page=50)#, #<0 to set to infinity

    preprocessors={
        'GET_SINGLE': [pre_get_single], #(instance_id=None, **kw)
        'GET_MANY': [pre_get_many], #(search_params=None, **kw)
        'POST': [pre_post], #(data=None, **kw)
        'DELETE': [pre_delete], #(instance_id=None, **kw)
        'PATCH_SINGLE': [pre_patch_single], #(instance_id=None,data=None,**kw)
        'PATCH_MANY': [pre_patch_many], #(search_params=None,data=None,**kw)
        },
    postprocessors={
        'GET_SINGLE': [post_get_single], #(result=None, **kw)
        'GET_MANY': [post_get_many], #(result=None, search_params=None, **kw)
        'POST': [post_post], #(result=None, **kw)
        'DELETE': [post_delete], #(was_deleted=None, **kw)
        'PATCH_SINGLE': [post_patch_single], #(result=None, **kw)
        'PATCH_MANY': [post_patch_many], #(query=None, data=None, search_params=None, **kw)
        }
    )
"""
apimanager.create_api(Computer, methods=['GET'])

app.run()
