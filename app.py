from logging import exception
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
    """
    This class represents a user in the system.

    Attributes:
        id (str): The unique ID of the user.
        userName (str): The username of the user.
        password (str): The password of the user.

    Methods:
        delete(self, id): This method deletes a user from the system.
        to_json(self): This method returns a JSON representation of the object.
        getID(self): This method returns the ID of the user.
    """

    # id = db.StringField(primary_key=True, required=False)
    userName = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

    def delete(self, id):
        """
        This method deletes a user from the system.

        Args:
            id (str): The ID of the user to be deleted.

        Returns:
            list: A list containing the deleted user.
        """
        userList = []
        userList = list(filter(lambda x: x["id"] != id, userList))
        return userList + "deleted"

    def to_json(self):
        """
        This method returns a JSON representation of the object.

        Returns:
            dict: A JSON representation of the object.
        """
        return {
            "id": self.id,
            "userName": self.userName,
        }

    def getID(self):
        """
        This method returns the ID of the user.

        Returns:
            str: The ID of the user.
        """
        return self.id


"""
DB Model for Personal Details
"""


class PersonalDetailsModel(db.Document):
    """
    This class represents the personal details of a user.

    Attributes:
        id (str): The unique ID of the user.
        userID (ObjectId): The ID of the user.
        firstName (str): The first name of the user.
        lastName (str): The last name of the user.
        email (str): The email ID of the user.
        mobile (str): The mobile number of the user.
        address (str): The address of the user.
        gender (str): The gender of the user.

    Methods:
        delete(self, id): This method deletes a personal details from the system.
        to_json(self): This method returns a JSON representation of the object.
    """

    # id = db.StringField(primary_key=True)
    userID = db.ObjectIdField(required=True)
    firstName = db.StringField(default="N/A")
    lastName = db.StringField(default="N/A")
    email = db.StringField(default="N/A")
    mobile = db.StringField(default="N/A")
    address = db.StringField(default="N/A")
    gender = db.StringField(default="N/A")

    def delete(self, id):
        """
        This method deletes a personal details from the system.

        Args:
            id (str): The ID of the personal details to be deleted.

        Returns:
            list: A list containing the deleted personal details.
        """
        PersonalDetailsList = []
        PersonalDetailsList = list(
            filter(lambda x: x["id"] != id, PersonalDetailsList)
        )
        return PersonalDetailsList + "deleted"

    def to_json(self):
        """
        This method returns a JSON representation of the object.

        Returns:
            dict: A JSON representation of the object.
        """
        return {
            "id": self.id,
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
    """
    This class represents the employees details of a user.

    Attributes:
        id (str): The unique ID of the user.
        userID (ObjectId): The ID of the user.
        employeeName (str): The name of the employee.
        workEmail (str): The work email of the employee.
        workPhone (str): The work phone of the employee.
        companyName (str): The company name of the employee.
        designation (str): The designation of the employee.
        department (str): The department of the employee.

    Methods:
        delete(self, id): This method deletes an employees details from the system.
        to_json(self): This method returns a JSON representation of the object.
    """

    # id = db.StringField(primary_key=True)
    userID = db.ObjectIdField(required=True)
    employeeName = db.StringField(default="N/A")
    workEmail = db.StringField(default="N/A")
    workPhone = db.StringField(default="N/A")
    companyName = db.StringField(default="N/A")
    designation = db.StringField(default="N/A")
    department = db.StringField(default="N/A")

    def delete(self, id):
        """
        This method deletes an employees details from the system.

        Args:
            id (str): The ID of the employees details to be deleted.

        Returns:
            list: A list containing the deleted employees details.
        """
        EmployeesList = []
        EmployeesList = list(filter(lambda x: x["id"] != id, EmployeesList))
        return EmployeesList + "deleted"

    def to_json(self):
        """
        This method returns a JSON representation of the object.

        Returns:
            dict: A JSON representation of the object.
        """
        return {
            "id": self.id,
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
    """
    This class represents the role based access control details of a user.

    Attributes:
        id (str): The unique ID of the user.
        userID (ObjectId): The ID of the user.
        role (str): The role of the user.

    Methods:
        delete(self): This method deletes an RBAC details from the system.
        to_json(self): This method returns a JSON representation of the object.
    """

    # id = db.StringField(primary_key=True)
    userID = db.ObjectIdField(required=True)
    role = db.StringField(default="N/A")

    def delete(self):
        """
        This method deletes an RBAC details from the system.

        Returns:
            list: A list containing the deleted RBAC details.
        """
        RBACList = []
        RBACList = list(filter(lambda x: x["id"] != self.id, RBACList))
        return RBACList + "deleted"

    def to_json(self):
        """
        This method returns a JSON representation of the object.

        Returns:
            dict: A JSON representation of the object.
        """
        return {
            "id": self.id,
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
                    ],
                },
            ],
        }
    )


@app.route("/register", methods=["POST"])
# This function registers a new user in the system.
# It takes in the following parameters:
#   userName (str): The username of the user.
#   password (str): The password of the user.
#   firstName (str): The first name of the user.
#   lastName (str): The last name of the user.
#   email (str): The email ID of the user.
#   mobile (str): The mobile number of the user.
#   address (str): The address of the user.
#   gender (str): The gender of the user.
#   workEmail (str): The work email of the employee.
#   workPhone (str): The work phone of the employee.
#   companyName (str): The company name of the employee.
#   designation (str): The designation of the employee.
#   department (str): The department of the employee.
#   role (str): The role of the user.
# It saves the user information to the database and creates a session for the user.
# If the user already exists, it returns an error.
# If there is an error saving the user information, it returns an error.
# Otherwise, it returns a success message.
def register():
    """
    This function registers a new user in the system.

    Returns:
        dict: A JSON object containing the message and status code.
    """
    # Parse the request parameters
    parseRequestParameters = request.values
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
    # Check if the user already exists
    if UserModel.objects(userName=userName).count() > 0:
        # If the user exists, return an error
        return jsonify({"message": "User Already Exists"})
    else:
        # If the user does not exist, create a new user
        # Save the user information to the database
        try:
            addNewUsertoUserTable = UserModel(userName=userName, password=password)
            addNewUsertoUserTable.save()

            # Get the object ID of the new user
            objectID = ObjectId(addNewUsertoUserTable.pk)

            # Save the personal details of the user
            addNewUsertoPersonalDetailsTable = PersonalDetailsModel(
                userID=objectID,
                firstName=firstName,
                lastName=lastName,
                email=email,
                mobile=mobile,
                address=address,
                gender=gender,
            )
            addNewUsertoPersonalDetailsTable.save()

            # Save the employee details of the user
            addNewUsertoEmployeesTable = EmployeesModel(
                userID=objectID,
                employeeName=firstName,
                workEmail=workEmail,
                workPhone=workPhone,
                companyName=companyName,
                designation=designation,
                department=department,
            )
            addNewUsertoEmployeesTable.save()

            # Save the RBAC details of the user
            addNewUsertoRBACTable = RBACModel(userID=objectID, role=role)
            addNewUsertoRBACTable.save()

            # Create a session for the user
            session["userID"] = objectID
            session["role"] = role

            # Return a success message
            return jsonify(
                {"message": "User Created and Session Started", "id": objectID}
            )
        except Exception as e:
            # If there is an error, return an error message
            print(e)
            return jsonify({"message": "Something went wrong", "status": 500})


@app.route("/login", methods=["POST"])
# This function handles user login requests.
# It checks if the user is already logged in, and if not, it authenticates the user using the provided credentials.
# If the credentials are valid, it creates a session for the user and returns a success message.
# If the credentials are invalid, it returns an error message.
def login():
    """
    Login Route

    Args:
        userName (str): The username of the user.
        password (str): The password of the user.

    Returns:
        dict: A JSON object containing the message and status code.
    """
    try:
        if session["userID"] != None:
            return jsonify({"ERROR": {"message": "Already Logged In"}})
    except:
        pass
    # Parse the request parameters
    parseRequestParameters = request.values
    userName = parseRequestParameters.get("userName")
    password = parseRequestParameters.get("password")
    # Check if the user exists in the database
    tempUserObjFetch = UserModel.objects(userName=userName, password=password)

    if tempUserObjFetch.count() > 0:
        # Create a session for the user
        session["userID"] = userName
        return jsonify(
            {"message": "Logged In Successfully", "id": tempUserObjFetch.first().id}
        )
    else:
        return jsonify({"message": "Invalid Credentials"})


@app.route("/logout/", methods=GET_POST)
# This function handles user logout requests.
# It clears the session data and returns a success message.
def logout():
    """
    This function handles user logout requests.
    It clears the session data and returns a success message.

    Returns:
        dict: A JSON object containing the message and status code.
    """
    if session.get("userID"):
        session.clear()
        return jsonify({"message": "Logged Out Successfully"})
    else:
        return jsonify({"Error": "Couldn't log out", "message": "User not logged in"})


def checkLogin():
    if session.get("userID") == None:
        return False


@app.route("/user/get", methods=["GET"])
# This function retrieves the user details based on the user ID.
# It returns a JSON object containing the user details.
def getUser():
    """
    This function retrieves the user details based on the user ID.
    It returns a JSON object containing the user details.

    Args:
        id (str): The ID of the user.

    Returns:
        dict: A JSON object containing the user details.
    """
    if checkLogin() == False:
        return jsonify({"ERROR": {"message": "Not Logged In"}})

    parseRequestParameters = request.values
    obj = ObjectId(parseRequestParameters.get("id"))

    tempUserObjFetch = UserModel.objects.filter(id=obj).first()

    if tempUserObjFetch == None:
        return jsonify({"message": "User Not Found"})
    tempUserPersonalObjFetch = PersonalDetailsModel.objects.filter(userID=obj).first()
    tempUserEmployeesObjFetch = EmployeesModel.objects.filter(userID=obj).first()
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


@app.route("/user/update", methods=["PUT"])
def updateUser():
    if checkLogin() == False:
        return jsonify({"ERROR": {"message": "Not Logged In"}})

    try:
        parseRequestParameters = request.values
        Objid = ObjectId(parseRequestParameters.get("id"))

        requestJSONData = request.get_json()

        PersonalDetails = requestJSONData.get("personalDetails")
        EmployementDetails = requestJSONData.get("employeeDetails")
        RBACModelDetails = requestJSONData.get("RBAC")

        UpdateUserPerSonalDetails = PersonalDetailsModel.objects.filter(
            userID=Objid
        ).update(**PersonalDetails)
        UpdateEmployeeDetails = EmployeesModel.objects.filter(userID=Objid).update(
            **EmployementDetails
        )

        UpdateRBACDetails = RBACModel.objects.filter(userID=Objid).update(
            **RBACModelDetails
        )

        # print(UpdateUserDetails)

        return jsonify({"SUCESS": {"message": "User Updated Successfully"}})
    except:
        return jsonify({"ERROR": {"message": "Something went wrong"}})


@app.route("/user/delete", methods=["DELETE"])
def deleteUser():
    if checkLogin() == False:
        return jsonify({"ERROR": {"message": "Not Logged In"}})

    try:
        parseRequestParameters = request.values
        if parseRequestParameters.get("id") is None:
            return jsonify({"ERROR": {"message": "Invalid Request"}})
        
        Objid = ObjectId(parseRequestParameters.get("id"))
        
        
        DeleteUserDetails = UserModel.objects.filter(id=Objid).delete()
        DeleteUserPersonalDetails =  PersonalDetailsModel.objects.filter(id=Objid).delete()
        DeleteUserEmployementDetails = EmployeesModel.objects.filter(id=Objid).delete()
        DeleteUserRABC = RBACModel.objects.filter(id=Objid).delete()
        
        logout()
        return jsonify({"message": "User Deleted Successfully", "id": Objid})
    
    except:
        return jsonify({"ERROR": {"message": "Something went wrong"}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    session(app)
