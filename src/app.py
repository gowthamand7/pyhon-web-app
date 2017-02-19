from flask import Flask, render_template, request, session, jsonify, make_response

from src.common.database import Database
from src.models.blogs import Blog
from src.models.posts import Post
from src.models.users import User


app = Flask(__name__)
app.secret_key = 'gowthaman'


@app.route('/')
def helloworld():
    return render_template('login.html')


@app.before_first_request
def initDB():
    Database.initialize()


#display the login template to user
@app.route('/login')
def login():
    return render_template('login.html')


#display the register template to user
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/logout',methods=['GET','POST'])
def logout():
    session['email'] = None
    return render_template('login.html')

#check the login is valid
@app.route('/auth/login',methods=['POST'])
def loginValidate():
    email = request.form['email']
    password = request.form['password']

    if User.loginValid(email,password):
        User.login(email)
    else:
        return jsonify(error='Invalid user name or password, Please try to login again')

    return render_template('profile.html',email=session['email'])


#register the user in the DB and logging in
@app.route('/auth/register',methods=['POST'])
def registerNewUser():
    email = request.form['email']
    password = request.form['password']
    if User.register(email,password) is not False:
        return render_template('profile.html', email=session['email'])
    else:
        return 'User already present in the App, Please login'


#get the list of post for a user
@app.route('/blogs/<string:userId>')
@app.route('/blogs')
def getBlogs(userId = None):
    if userId is not None:
        user = User.getById(userId)
    else:
        user = User.getByEmail(session['email'])

    blogs = user.getBlogs()
    return render_template('userBlogs.html',blogs=blogs,email=user.email)


#get the posts associated with the given blogId
@app.route('/posts/<string:blogId>')
def getPostsForBlog(blogId):
    blog = Blog.getFromMongo(blogId)
    posts = blog.getPosts()

    return render_template('posts.html',posts = posts,blogTitle=blog.title,blogId=blog._id)


#create a new blog
@app.route('/blog/new',methods=['POST','GET'])
def createNewBlog():
    if request.method == 'GET':
        return render_template('newBlog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        author = User.getByEmail(session['email'])
        blog = Blog(author.email,title,description,author._id)
        blog.saveToMongo()
        return make_response(getBlogs(author._id))


#create a new post under a given blog
@app.route('/post/new/<string:blogId>',methods=['POST','GET'])
def createNewPost(blogId):
    if request.method == 'GET':
        return render_template('newPost.html',blogId=blogId)
    else:
        title = request.form['title']
        content = request.form['content']
        author = User.getByEmail(session['email'])
        blog = Blog.getFromMongo(blogId)
        blog.newPost(title,content)
        return make_response(getPostsForBlog(blogId))


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)