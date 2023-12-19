from flask_mongoengine import MongoEngine
from flask import request, session, redirect, url_for
from flask import Flask, jsonify
from bson.objectid import ObjectId

GET_POST = ["GET", "POST"]


# APPLICATION CONFIGURATION
app = Flask(__name__)
app.secret_key = "ZesstaSoftwareServicesPvtLtdHyderabadSainathSapaIntern"
app.config["MONGODB_SETTINGS"] = {"db": "zessta", "host": "localhost", "port": 27017}

db = MongoEngine()
db.init_app(app)


"""
UserModel for interacting with applications
"""


class UserModel(db.Document):
    _id = db.StringField()
    userName = db.StringField()
    password = db.StringField()

    def delete(self, _id):
        userList = []
        userList = list(filter(lambda x: x["_id"] != _id, userList))
        return userList + "deleted"

    def to_json(self):
        return {
            "_id": self._id,
            "userName": self.userName,
        }

    def getID(self):
        return self._id


"""
DB Model for Personal Details
"""


class PersonalDetailsModel(db.Document):
    _id = db.StringField()
    userID = db.ObjectIdField()
    firstName = db.StringField(default="N/A")
    lastName = db.StringField(default="N/A")
    email = db.StringField(default="N/A")
    mobile = db.StringField(default="N/A")
    address = db.StringField(default="N/A")
    gender = db.StringField(default="N/A")

    def delete(self, _id):
        PersonalDetailsList = []
        PersonalDetailsList = list(
            filter(lambda x: x["_id"] != _id, PersonalDetailsList)
        )
        return PersonalDetailsList + "deleted"

    def to_json(self):
        return {
            "_id": self._id,
            "userID": self.userID,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "mobile": self.mobile,
            "address": self.address,
            "gender": self.gender,
        }


"""
Employees Model
"""


class EmployeesModel(db.Document):
    _id = db.StringField()
    userID = db.ObjectIdField()
    employeeName = db.StringField(default="N/A")
    workEmail = db.StringField(default="N/A")
    workPhone = db.StringField(default="N/A")
    companyName = db.StringField(default="N/A")
    designation = db.StringField(default="N/A")
    department = db.StringField(default="N/A")

    def delete(self, _id):
        EmployeesList = []
        EmployeesList = list(filter(lambda x: x["_id"] != _id, EmployeesList))
        return EmployeesList + "deleted"

    def to_json(self):
        return {
            "_id": self._id,
            "userID": self.userID,
            "employeeName": self.employeeName,
            "workEmail": self.workEmail,
            "workPhone": self.workPhone,
            "companyName": self.companyName,
            "designation": self.designation,
            "department": self.department,
        }


"""
Model for RBAC
"""


class RBACModel(db.Document):
    _id = db.StringField()
    userID = db.ObjectIdField()
    role = db.StringField(default="N/A")

    def delete(self):
        RBACList = []
        RBACList = list(filter(lambda x: x["_id"] != self._id, RBACList))
        return RBACList + "deleted"

    def to_json(self):
        return {
            "_id": self._id,
            "userID": self.userID,
            "role": self.role,
        }


@app.route("/", methods=["GET"])
def index():
    return jsonify(
        {
            "message": "Welcome to Zessta Software Services",
            "routes": [
                {"method": "GET", "route": "/", "description": "Home Page"},
                {
                    "method": "POST",
                    "route": "/login",
                    "description": "Login Page",
                    "parameters": {
                        "userName": {
                            "type": "string",
                            "required": True,
                            "description": "User Name",
                        },
                        "password": {
                            "type": "string",
                            "required": True,
                            "description": "Password",
                        },
                    },
                },
                {
                    "method": "POST",
                    "route": "/register",
                    "description": "Register Page",
                    "parameters": [
                        "userName",
                        "password",
                        "firstName",
                        "lastName",
                        "email",
                        "mobile",
                        "address",
                        "gender",
                        "workEmail",
                        "workPhone",
                        "companyName",
                        "designation",
                        "department",
                        "role",
                    ],
                },
                {"method": "GET", "route": "/logout", "description": "Logout Page"},
            ],
        }
    )


@app.route("/register", methods=["POST"])
def register():
    parseRequestParameters = request.values
    # return jsonify(parseRequestParameters)
    userName = parseRequestParameters.get("userName")
    password = parseRequestParameters.get("password")
    firstName = parseRequestParameters.get("firstName")
    lastName = parseRequestParameters.get("lastName")
    email = parseRequestParameters.get("email")
    mobile = parseRequestParameters.get("mobile")
    address = parseRequestParameters.get("address")
    gender = parseRequestParameters.get("gender")
    workEmail = parseRequestParameters.get("workEmail")
    workPhone = parseRequestParameters.get("workPhone")
    companyName = parseRequestParameters.get("companyName")
    designation = parseRequestParameters.get("designation")
    department = parseRequestParameters.get("department")
    role = parseRequestParameters.get("role")

    # USERCREATIONLOGIC
    addNewUsertoUserTable = UserModel(userName=userName, password=password)

    if UserModel.objects(userName=userName).count() > 0:
        return jsonify({"message": "User Already Exists"})
    else:
        # IF NOT SAVING USERNAME to DATABASE
        try:
            addNewUsertoUserTable.save()

            objectID = ObjectId(addNewUsertoUserTable.pk)

            # SAVING PASSED PARSONAL DETAILS
            addNewUsertoPersonalDetailsTable = PersonalDetailsModel(
                userID=objectID,
                firstName=firstName,
                lastName=lastName,
                email=email,
                mobile=mobile,
                address=address,
                gender=gender,
            )

            # TRIGGER SAVE

            addNewUsertoPersonalDetailsTable.save()

            # Adding Employee Details
            addNewUsertoEmployeesTable = EmployeesModel(
                userID=objectID,
                employeeName=firstName,
                workEmail=workEmail,
                workPhone=workPhone,
                companyName=companyName,
                designation=designation,
                department=department,
            )

            # Trigger Save
            addNewUsertoEmployeesTable.save()

            # Adding RBAC Details
            addNewUsertoRBACTable = RBACModel(userID=objectID, role=role)

            # Trigger Save
            addNewUsertoRBACTable.save()
            session["userID"] = objectID
            session["role"] = role

            return jsonify({"message": "User Created and Session Started"})
        except:
            return jsonify({"message": "Something went wrong", "status": 500})


@app.route("/login", methods=["POST"])
def login():
    try:
        if session["userID"] != None:
            return jsonify({"ERROR": {"message": "Already Logged In"}})
    except:
        pass
    parseRequestParameters = request.values
    userName = parseRequestParameters.get("userName")
    password = parseRequestParameters.get("password")
    tempUserObjFetch = UserModel.objects(userName=userName, password=password).count()

    if tempUserObjFetch > 0:
        session["userID"] = userName
        return jsonify({"message": "Logged In Successfully"})
    else:
        return jsonify({"message": "Invalid Credentials"})


@app.route("/logout/", methods=GET_POST)
def logout():
    session.clear()
    return jsonify({"message": "Logged Out Successfully"})


@app.route("/user/get", methods=GET_POST)
def getUser():
    
    if session.get("userID") == None:
        return jsonify({"ERROR": {"message": "Not Logged In"}})
    else:
        parseRequestParameters = request.values
        obj = ObjectId(parseRequestParameters.get("id"))

        tempUserObjFetch = UserModel.objects.filter(_id=obj).first()

        if tempUserObjFetch == None:
            return jsonify({"message": "User Not Found"})
        tempUserPersonalObjFetch = PersonalDetailsModel.objects.filter(
            userID=obj
        ).first()
        tempUserEmployeesObjFetch = EmployeesModel.objects.filter(
            userID=obj
        ).first()
        tempRoleObjFetch = RBACModel.objects.filter(userID=obj).first()

        returnJsonFile = {
            "userDetails": {"userName": tempUserObjFetch.userName},
            "PersonalDetails": {
                "firstName": tempUserPersonalObjFetch.firstName,
                "lastName": tempUserPersonalObjFetch.lastName,
                "email": tempUserPersonalObjFetch.email,
                "mobile": tempUserPersonalObjFetch.mobile,
                "address": tempUserPersonalObjFetch.address,
                "gender": tempUserPersonalObjFetch.gender,
            },
            "CompanyDetails": {
                "companyName": tempUserEmployeesObjFetch.companyName,
                "designation": tempUserEmployeesObjFetch.designation,
                "department": tempUserEmployeesObjFetch.department,
                "workEmail": tempUserEmployeesObjFetch.workEmail,
                "workPhone": tempUserEmployeesObjFetch.workPhone,
                "role": tempRoleObjFetch.role,
            },
        }

        return returnJsonFile
   


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    session(app)
