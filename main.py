from flask import Flask, render_template
import requests
from post import Post

app = Flask(__name__)
blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
posts = requests.get(blog_url).json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)


@app.route('/')
def home():
    return render_template("index.html", all_posts=post_objects)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<int:blog_id>')
def get_blog(blog_id):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == blog_id:
            requested_post = blog_post
    return render_template("single-post.html", post=requested_post)


if __name__ == '__main__':
    app.run(debug=True)
