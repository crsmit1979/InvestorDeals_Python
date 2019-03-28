from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])
def gerroot():
    return "test"


app.run(
    host="0.0.0.0",
    port=80
)