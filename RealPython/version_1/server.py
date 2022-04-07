from flask import Flask, render_template

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL to route in our application for "/"
@app.route("/")
def home():
    return render_template("home.html")

if __name__=='__main__':
    app.run(debug=True)