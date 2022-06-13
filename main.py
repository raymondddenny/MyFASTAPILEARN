from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()


class Post(BaseModel):  # schema for the post request
    title: str
    content: str
    published: bool = True  # optional field
    rating: Optional[int] = None  # optional field


my_posts = [{"id": 1, "title": "Healthy Food",
             "description": "This is a healthy food yoo"},
            {"id": 2, "title": "Bakso Ayam",
             "description": "Bakso ayam is good", }]  # list of posts


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {'data': my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {'data': post_dict}


def find_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return post


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id = {id} was not found"}
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {id} was not found",)
    return {'data': post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    deleted_post = find_post(id)
    print(deleted_post)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"Post with id = {id} was not found"})
    my_posts.remove(deleted_post)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
