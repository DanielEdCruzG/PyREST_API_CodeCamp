from flask import Flask, request
from validationRules import PostSchema

app = Flask(__name__)

myPosts = [{'title': 'Post 1', 'content': 'This is the content of the post 1', 'rating': 5, 'publish': True, 'id': 1}, {'title': 'Post 2', 'content': 'This is the content of the post 2', 'rating': 4, 'publish': False, 'id': 2}]

# This is a Decorator: Basically gets the 
# function and do all the stuff to make 
# it work. But the decorator keep in mind 
# the methods HTTP. Ex: get, post, put ...

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

@app.get('/posts')
def getPosts():
    return myPosts

@app.get('/posts/<int:id>/') # This is a path parameter.
def getPost(id):
    if ( (id <= 0) or (not(id)) ):
        return {'message': 'Invalid ID'}, 400

    for post in myPosts:
        if post.get('id') == id:
            return {'data': post}, 200
    return {'message': 'Post not found'}, 404

@app.get('/posts/<path:id>')
def handle_invalid_param(id):
    return {"error": "Invalid path parameter", "message": f"'{id}' is not a valid integer for post ID."}, 422 

@app.post('/posts/') 
def createPost():
    payload = request.get_json()
    postSchema = PostSchema()
    try:
        postSchema.load(payload)
        postSchema.validate_title(payload.get('title'))
        postSchema.validate_content(payload.get('content'))
        postSchema.validate_rating(payload.get('rating'))
        dumpData = postSchema.dump(payload)

        
        if not(dumpData.get('publish')):
            return {'data': dumpData, 'message': 'Post eraser created successfully'}, 202
            
        dumpData['id'] = len(myPosts) + 1
        myPosts.append(dumpData)    
        return {'data': dumpData, 'message': 'Post Created Successfully!. '}, 201
    
    except Exception as e:
        return {'error': str(e)}, 500

# What's the difference between PUT and PATCH?... 
# Well when you use the PUT method you must pass all the information
# And when you use PATCH method you only pass the specific info.

 