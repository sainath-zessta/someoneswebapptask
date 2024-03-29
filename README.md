# Zessta Software Services

This is a sample code for Zessta Software Services. It is a web application that provides user authentication, personal details management, and role-based access control (RBAC) management. The code is written in Python and uses the Flask web framework.

## Requirements

To run this code, you need to have the following installed on your system:

- Python 3.x
- pip
- Flask
- Flask-Mongoengine

## How to run the code

1. Clone this repository using the following command:

```bash
git clone https://github.com/your-username/zessta-software-services.git
```

2. Install the required packages by running the following command in the project directory:

```bash
pip install -r requirements.txt
```

3. Run the following command to start the server:

```bash
python app.py
```

4. Open your web browser and go to http://localhost:80 to see the home page.

## Database schema

The database schema for this code is as follows:

```
UserModel:
{
    "id": "ObjectId",
    "userName": "StringField",
    "password": "StringField"
}

PersonalDetailsModel:
{
    "id": "ObjectId",
    "userID": "ObjectIdField",
    "firstName": "StringField",
    "lastName": "StringField",
    "email": "StringField",
    "mobile": "StringField",
    "address": "StringField",
    "gender": "StringField"
}

EmployeesModel:
{
    "id": "ObjectId",
    "userID": "ObjectIdField",
    "employeeName": "StringField",
    "workEmail": "StringField",
    "workPhone": "StringField",
    "companyName": "StringField",
    "designation": "StringField",
    "department": "StringField"
}

RBACModel:
{
    "id": "ObjectId",
    "userID": "ObjectIdField",
    "role": "StringField"
}
```
