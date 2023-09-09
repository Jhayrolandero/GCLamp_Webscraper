from LoginCtrl import LoginCtrl
from Todo_List import Todo_List

login_obj = LoginCtrl("username", "password", "https://gordoncollegeccs.edu.ph/ccs/students/lamp/#/main/todolist")
res = login_obj.login_user()

if res:
    resource = Todo_List()
    resource.get_driver(login_obj.return_driver())
    resource.make_csv()
