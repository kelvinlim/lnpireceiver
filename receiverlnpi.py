'''
Code from https://rahmanfadhil.com/flask-rest-api/

'''
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource


### todo add info on cors to support flutter web
# https://flask-cors.readthedocs.io/en/latest/

### TODO deploy with apache wsgi and mysql
# https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps

app = Flask(__name__)

# adding cors extension
CORS(app)

### TODO move mysql  https://docs.sqlalchemy.org/en/14/dialects/mysql.html
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# change this to use use a file
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://restreceiver:NOTREALPASSWORD@lnpiapp.med.umn.edu/lnpi_restreceiver'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


'''
To create the database execute the following code in the python interpreter
This only works for mysql > 5.5
> python
import receiverlnpi
receiverlnpi.db.create_all()
exit()
'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studycode = db.Column(db.String(50))
    data_version = db.Column(db.String(50))
    guid = db.Column(db.Text())
    data = db.Column(db.Text())
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    
    def __repr__(self):
        return '<Post %s>' % self.studycode


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "studycode", "data_version",
                  "guid", "data", "created_on")
        #fields = ("id", "studycode", "guid")


post_schema = PostSchema()
posts_schema = PostSchema(many=True, exclude = ['data'])


class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    def post(self):
        new_post = Post(
            studycode=request.json['studycode'],
            data_version=request.json['data_version'],
            guid=request.json['guid'],
            data=request.json['data']
        )
        print(new_post)
        print('hello')
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)


class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)

        if 'studycode' in request.json:
            post.studycode = request.json['studycode']
        if 'data_version' in request.json:
            post.data_version = request.json['data_version']
        if 'guid' in request.json:
            post.guid = request.json['guid']
        if 'data' in request.json:
            post.data = request.json['data']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204


api.add_resource(PostListResource, '/posts')
# api.add_resource(PostResource, '/posts/<int:post_id>')

'''
To post data

curl http://160.94.0.29:5001/posts \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"studycode":"driving", "guid": "ab1235-x25", "data_version":"0.1", "data":"[[1,2,3], [4,5,6]]"}'
    
To check on all data
curl http://160.94.0.29:5000/posts

To check on single entry
curl http://160.94.0.29:5000/posts/1

'''
if __name__ == '__main__':
    # app.run(host='0.0.0.0')  # to make visible outside of machine
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5001)

