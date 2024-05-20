#we will create an API using Flask, which will use the JSON data format
from flask import Flask, jsonify, request
# jsonify is for converting python dictionaries into JSON(Javascript Object Notation) format
#request is for sending HTTP requests to web servers using the HTTP methods(GET, PUT, DELETE, POST)
from flask_restful import Resource, Api
# flask_restful module is used for creating RESTFUL APIs in flask
#Resource is a class represents a endpoint in an API
#Api is aclass that provides a framework for building RESTFUL APIs with Flask
import pymysql
from pymysql import cursors
#cursors class enables us to execute SQL queries and retrieve results from the DB. they include: fetchall(), fetchone(), fetchmany()
import pymysql.cursors

app = Flask(__name__) #this is a common cnstruct used to create a flask application instance
my_api = Api(app) #making our app class for a particular resource

class Employee(Resource):
    #we will use HTTP(Hypertext Trasfer Protocol) methods/verbs that indicate the desired action to be performed on a given resourse, GET: it request a representation of a specified resourse, POST: it submits data to be processed by the server, PUT: it updates data in the server or it creates data to be processed by the server, DELETE: it removes data in the server
    def get(self):
        #here we will ftch data in our DB
        #step 1: connect to our DB
        connection = pymysql.connect(host = "localhost", user = "root",password = "",database="KindiApp")
        my_cursor= connection.cursor(pymysql.cursors.DictCursor)
        #DictCursor arranges our output in key and Value format(disctionary)
        #step 2: create our query
        query = "SELECT * FROM employees"
        my_cursor.execute(query)
        if my_cursor.rowcount == 0:
            return jsonify({'message': 'No Records'})
        else:
            employees = my_cursor.fetchall()
            return jsonify(employees)
    
    

    #we are converting a python dictionary to a JSON format using jsonify
    def post(self):
        data = request.json
        id_number = data["id_number"]
        username = data["username"]
        others = data["others"]
        salary = data["salary"]
        department = data["department"]

        connection = pymysql.connect(host = "localhost", user = "root",password = "",database="KindiApp")
        my_cursor= connection.cursor()

        #step 3
        query = "INSERT INTO employees (id_number,username,others, salary,department)VALUES(%s,%s,%s,%s,%s)"

        try:
            #here we execute our query
            my_cursor.execute(query, (id_number,username,others,salary,department))
            connection.commit()
            return jsonify({"message":"Post Successful"})
        except:
            #if we dont get to submit data to our DB successfully then the codes will be executed
            connection.rollback()
            #we are geting back our data
            return jsonify({"message":"Post Failed"})


    def put(self):
        #here we will update our rows in the table employees, we will use id_number to update salary and username column
        #step 1: converting our input to a json format
        data = request.json
        id_number = data["id_number"]
        salary = data["salary"]
        username = data["username"]
        #step 2: connect to the DB
        connection = pymysql.connect(host = "localhost", user = "root",password = "",database="KindiApp")
        my_cursor= connection.cursor()
        #step 3: create a query that updates the salary and username using id_number
        query = "UPDATE employees SET salary =%s , username=%s WHERE id_number =%s"
            #the codes in the try statement will update the row in employees table
        my_cursor.execute(query, (salary,username,id_number))
        connection.commit()
        return jsonify({'message':'UPDATE SUCCESSFULL'})
        


    def delete(self):
        #here we will delete certain row in thatble employees using id_number
        #step 1: convet out input(id_number) into json format
        data = request.json
        id_number = data["id_number"]
        #step 2: connsct to database
        connection = pymysql.connect(host = "localhost", user = "root",password = "",database="KindiApp")
        my_cursor= connection.cursor()
        #step 3: create a quert to delete a row using id_number
        query =  "DELETE FROM `employees` WHERE id_number = %s"
        #step 4: try and except
        try:
            my_cursor.execute(query, (id_number))
            connection.commit()
            return jsonify({'message': 'UPDATE SUCCESS'})

        except:
            connection.rollback()
            return jsonify({'message': 'UPDATE FAILED'})
    
#we need to create an endpoint. an endpoint is a URL(Uniform Resource Locator) that provides the location os a resource on a server

my_api.add_resource(Employee, '/employees')
if __name__ == '__main__':
    app.run(debug =True)