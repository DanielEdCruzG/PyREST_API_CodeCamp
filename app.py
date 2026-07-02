from flask import Flask, request
from validationRules import PostSchema

app = Flask(__name__)

def findPost(id):
    for post in myPosts:
        if post.get('id') == id:
            return post
    return None

def updatePost(dict, oldDict):
    for key, value in dict.items():
        if key in oldDict:  # solo si el campo existe
            oldDict[key] = value

# This is a list of dictionaries.
myPosts = [
    {
        'title': 'Post 1', 'content': 'This is the content of the post 1', 'rating': 5, 'publish': True, 'id': 1
    }, 
    {
        'title': 'Post 2', 'content': 'This is the content of the post 2', 'rating': 4, 'publish': False, 'id': 2
    },
    {
        'title': 'Post 3', 'content': 'This is the content of the post 3', 'rating': 3, 'publish': True, 'id': 3
    }
    ]

# This is a Decorator: Basically gets the 
# function and do all the stuff to make 
# it work. But the decorator keep in mind 
# the methods 8HTTP. Ex: get, post, put ...

@app.get('/') 
def root():
    return {'message': 'Hello there!. '}


# The previos block of code is also call 
# Route in frameworks like: 
# Flask(In this case)
# Or Path Operation in cases like:
# FastAPI
 

# An standar convetion is to name the path file in plural for example:
# /posts or /users or /products

# The idea is to create a crud to manage the posts...

@app.get('/posts/')
def getPosts():
    auxList = []
    for post in myPosts:
        if post.get('publish') == True:
            auxList.append(post)
    return auxList, 200

@app.get('/posts/<int:id>/') # This is a path parameter.
def getPost(id):    
    if (not id):
        return {'message': 'Invalid ID'}, 400

    findedPost = findPost(id)
    if findedPost:
        return {'data': findedPost}, 200
    
    return {'message': 'Post not found'}, 404

@app.get('/posts/<path:id>')
def handle_invalid_param(id):
    return {"error": "Invalid path parameter", "message": f"'{id}' is not a valid integer for post ID."}, 422 

@app.post('/posts/') 
def createPost():
    infoFrontend = request.get_json()
    postSchema = PostSchema()

    postSchema.load(infoFrontend)
    postSchema.validate_title(infoFrontend.get('title'))
    postSchema.validate_content(infoFrontend.get('content'))
    postSchema.validate_rating(infoFrontend.get('rating'))

    infoFrontend['id'] = len(myPosts) + 1
    myPosts.append(infoFrontend)
       
    if not(infoFrontend.get('publish')):
        return {'data': infoFrontend, 'message': 'Post eraser created successfully. '}, 202

    return {'data': infoFrontend, 'message': 'Post Created Successfully!. '}, 201

# What's the difference between PUT and PATCH?... 
# Well when you use the PUT method you must pass all the information
# And when you use PATCH method you only pass the specific info.

@app.post('/posts/<path:AdditionalParam>')
def handleInvalidParamToPost(AdditionalParam):
    return {"error": "Invalid path parameter", "message": f"'{AdditionalParam}' There's not allowed to add params to the path. "}, 422 

@app.put('/posts/<int:id>/')
def updateFullPost(id):
    infoFrontend = request.get_json()
    postSchema = PostSchema()

    postSchema.load(infoFrontend)
    postSchema.validate_title(infoFrontend.get('title'))
    postSchema.validate_content(infoFrontend.get('content'))
    postSchema.validate_rating(infoFrontend.get('rating'))

    if not(infoFrontend.get('publish')):
        return {'data': infoFrontend, 'message': 'Post eraser created. '}, 202

    postToUpdate = findPost(id)

    if postToUpdate:        
        updatePost(infoFrontend, postToUpdate)
        return {'data': infoFrontend, 'message': 'Post Updated Successfully!. '}, 200

    return {'message': 'Post not found'}, 404
    
@app.put('/posts/<path:id>')
def handleInvalidParamToUpdate(id):
    return {"error": "Invalid path parameter", "message": f"'{id}' is not a valid integer for post ID."}, 422 

@app.delete('/posts/<int:id>/')
def deletePost(id):
    if (not id):
        return {'message': 'Invalid ID'}, 400

    findedPost = findPost(id)
    if findedPost:
        # Remember that .remove is used to remove an element but by their value
        # and .pop is used to remove an element by index.
        # So in this case we are using .remove to remove the post by their value.
        # Because we know that the ID is unique.
        # But we can also use .pop to remove the post by index.
        # To do it we need to find the index of the post first.
        myPosts.remove(findedPost)

        return '', 204
       
    return {'message': 'The post that is trying to delete was not found'}, 404

@app.delete('/posts/<path:id>')
def handleInvalidParamToDelete(id):
    return {"error": "Invalid path parameter", "message": f"'{id}' is not a valid integer for post ID."}, 422