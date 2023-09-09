from flask import Flask, request, jsonify
from LoginCtrl import LoginCtrl
from Todo_List import Todo_List

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

@app.route("/get-user")
def get_user():
    login_obj = LoginCtrl("202210274", "Thegtplayer277353", "https://gordoncollegeccs.edu.ph/ccs/students/lamp/#/login")
    res = login_obj.login_user()

    if res:
        resource = Todo_List()
        resource.get_driver(login_obj.return_driver())
        user_data = resource.make_json()

        return user_data, 200
    

@app.route("/create-user", methods=["POST"])

def create_user():
    data = request.get_json()
    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)