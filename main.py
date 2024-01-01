from flask import Flask, render_template, request
import requests
from post import Post
import smtplib

app = Flask(__name__)
blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
posts = requests.get(blog_url).json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)

my_email = "my_email_id"
my_password = "my_password"

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


@app.route('/contact', methods=['POST', 'GET'])
def receive_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        send_email(name=name, email=email, phone=phone, message=message)
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


def send_email(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Name:{name} \n Email: {email} \n Phone:{phone} \n Message:{message}")


if __name__ == '__main__':
    app.run(debug=True)
