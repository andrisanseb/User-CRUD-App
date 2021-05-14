from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time
import ast

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['InfoSys']

# Choose collections
students = db['Students']
users = db['Users']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid

def is_session_valid(user_uuid):
    return user_uuid in users_sessions


# ΕΡΩΤΗΜΑ 1: Δημιουργία χρήστη
@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None
    try:
        data=json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
    Το συγκεκριμένο endpoint θα δέχεται στο body του request του χρήστη ένα json της μορφής: 

    {
        "username": "some username", 
        "password": "a very secure password"
    }

    * Θα πρέπει να εισαχθεί ένας νέος χρήστης στο σύστημα, ο οποίος θα εισάγεται στο collection Users (μέσω της μεταβλητής users). 
    * Η εισαγωγή του νέου χρήστη, θα γίνεται μόνο στη περίπτωση που δεν υπάρχει ήδη κάποιος χρήστης με το ίδιο username. 
    * Αν γίνει εισαγωγή του χρήστη στη ΒΔ, να επιστρέφεται μήνυμα με status code 200. 
    * Διαφορετικά, να επιστρέφεται μήνυμα λάθους, με status code 400.
    """

    # Έλεγχος δεδομένων username / password
    if(users.find_one({'username':data['username']}) == None):      #ψάνει αν το username που δώθηκε ήδη υπάρχει στο collection Users.Αν ΔΕΝ υπάρχει μπαίνει στην if
        users.insert_one({"username": str(data['username']) , "password": str(data['password'])})       #δημιουργεί τον user
        # Μήνυμα επιτυχίας
        return Response(data['username'] + " was added to the MongoDB",status=200,mimetype='application/json')
    else:
        # Μήνυμα λάθους (Υπάρχει ήδη κάποιος χρήστης με αυτό το username)
        return Response("A user with the given username already exists",status=400,mimetype='application/json')


# ΕΡΩΤΗΜΑ 2: Login στο σύστημα
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
        Να καλεστεί η συνάρτηση create_session() (!!! Η ΣΥΝΑΡΤΗΣΗ create_session() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) 
        με παράμετρο το username μόνο στη περίπτωση που τα στοιχεία που έχουν δοθεί είναι σωστά, δηλαδή:
        * το data['username] είναι ίσο με το username που είναι στη ΒΔ (να γίνει αναζήτηση στο collection Users) ΚΑΙ
        * το data['password'] είναι ίσο με το password του συγκεκριμένου χρήστη.
        * Η συνάρτηση create_session() θα επιστρέφει ένα string το οποίο θα πρέπει να αναθέσετε σε μία μεταβλητή που θα ονομάζεται user_uuid.
        
        * Αν γίνει αυθεντικοποίηση του χρήστη, να επιστρέφεται μήνυμα με status code 200. 
        * Διαφορετικά, να επιστρέφεται μήνυμα λάθους με status code 400.
    """

    if(users.find_one({'username':data['username'] , 'password':data['password']}) != None):        #μπαίνει μέσα στην if μόνο εάν υπάρχει username με το συγκεκριμένο password στην βάση ( δηλαδή ΟΧΙ None)
        user_uuid = create_session(data['username'])        #ο κωδικός που θα ζητείται κάθε φορά από το σύστημα
        res = {"uuid": user_uuid, "username": data['username']}
        return Response(json.dumps(res),status=200, mimetype='application/json')

    else:       #Αν ΔΕΝ είναι σωστά τα στοιχεία που δώθηκαν περνάει εδώ
        # Μήνυμα λάθους (Λάθος username ή password)
        return Response("Wrong username or password.",status=400, mimetype='application/json')

# ΕΡΩΤΗΜΑ 3: Επιστροφή φοιτητή βάσει email 
@app.route('/getStudent', methods=['GET'])
def get_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή και θα επιστρέφει τα δεδομένα του. 
        Να περάσετε τα δεδομένα του φοιτητή σε ένα dictionary που θα ονομάζεται student.
        
        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα.
    """

    uuid = request.headers.get('authorization')
    valid=is_session_valid(uuid)

    if valid==False:
        return Response("Unauthorized",status=401)
    else:
        if(students.find_one({"email":data['email']}) != None):     #ελέγχεται αν το email αντιστοιχεί σε κάποιον student
            s = json.dumps(students.find_one({"email":data['email']},{"_id":0}))        #αποθηκεύονται τα δεδομένα του student που του αντιστοιχεί το email ( χωρίς το id αφού δεν χρειάζεται)
            student = ast.literal_eval(s)       #Το s είναι string. Μέσω της εντολής αυτής το κάνω dict και το αποθηκεύω στο student.
            # Η παρακάτω εντολή χρησιμοποιείται μόνο στη περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχει φοιτητής με αυτό το email).
            return Response(json.dumps(student), status=200, mimetype='application/json')
        else:
            return Response("This email does not belong to any Student")


# ΕΡΩΤΗΜΑ 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών
@app.route('/getStudents/thirties', methods=['GET'])
def get_students_thirty():
    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα.
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid.
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401.
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί.

        Το συγκεκριμένο endpoint θα πρέπει να επιστρέφει τη λίστα των φοιτητών οι οποίοι είναι 30 ετών.
        Να περάσετε τα δεδομένα των φοιτητών σε μία λίστα που θα ονομάζεται students.

        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα και όχι κενή λίστα.
    """
    uuid = request.headers.get('authorization')
    valid = is_session_valid(uuid)

    if valid == False:
        return Response("Unauthorized", status=401)
    else:
        lst30 = []
        for x in students.find({},{"_id":0,"address":0}):
            if(2021-x["yearOfBirth"] == 30):
                lst30.append(x)

        if not lst30:   #checks if lst30 is empty
            return Response("No student is 30 year old")
        else:
            # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχουν φοιτητές που είναι 30 ετών).
            return Response(json.dumps(lst30), status=200, mimetype='application/json')

# ΕΡΩΤΗΜΑ 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών
@app.route('/getStudents/oldies', methods=['GET'])
def get_students_oldies():   #Changed the name
    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα.
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid.
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401.
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί.

        Το συγκεκριμένο endpoint θα πρέπει να επιστρέφει τη λίστα των φοιτητών οι οποίοι είναι 30 ετών και άνω.
        Να περάσετε τα δεδομένα των φοιτητών σε μία λίστα που θα ονομάζεται students.

        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα και όχι κενή λίστα.
    """
    uuid = request.headers.get('authorization')
    valid = is_session_valid(uuid)

    if valid == False:
        return Response("Unauthorized", status=401)
    else:
        lst = []
        for x in students.find({}, {"_id": 0, "email": 0, "address": 0}):
            if (2021 - x["yearOfBirth"] >= 30):
                lst.append(x)

        if not lst:  # checks if lst is empty
            return Response("No student is 30 year old")
        else:
            # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχουν φοιτητές που είναι 30 ετών).
            return Response(json.dumps(lst), status=200, mimetype='application/json')


# ΕΡΩΤΗΜΑ 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email
@app.route('/getStudentAddress', methods=['GET'])
def get_studentAddress():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

     OK   Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή. 
        * Στη περίπτωση που ο φοιτητής έχει δηλωμένη τη κατοικία του, θα πρέπει να επιστρέφεται το όνομα του φοιτητή η διεύθυνσή του(street) και ο Ταχυδρομικός Κωδικός (postcode) της διεύθυνσης αυτής.
        * Στη περίπτωη που είτε ο φοιτητής δεν έχει δηλωμένη κατοικία, είτε δεν υπάρχει φοιτητής με αυτό το email στο σύστημα, να επιστρέφεται μήνυμα λάθους. 

        Αν υπάρχει όντως ο φοιτητής με δηλωμένη κατοικία, να περάσετε τα δεδομένα του σε ένα dictionary που θα ονομάζεται student.
        Το student{} να είναι της μορφής: 
        student = {"name": "Student's name", "street": "The street where the student lives", "postcode": 11111}
    """
    uuid = request.headers.get('authorization')
    valid = is_session_valid(uuid)

    if valid == False:
        return Response("Unauthorized", status=401)
    else:
        if (students.find_one({"email": data['email']}) != None):       #ψάχνω εάν υπάρχει φοιτητης με αυτο το μειλ στην βάση
            s1 = json.dumps(students.find_one({"email": data['email']}, {"_id": 0,"yearOfBirth":0}))        #περνάω τα δεδομένα του συγκεκριμένου φοιτητη στο s1 που ειναι ομως STRING
            #το s1 είναι string με την δομη ενος dict. Για να εχω τα δεδομενα μου σε μεταβλητη με type = dict  εχω κανει import ast και χρησιμοποιω την μεθοδο πιο κατω
            s2 = ast.literal_eval(s1)       # from string dict to dict!!!
            address_in_dict = "address" in s2       #True εαν υπάρχει το key "address" στο s2 , μεταβλητή που περιέχει τα δεδομένα του φοιτητή
            if(address_in_dict):
                student = { "name": s2["name"] , "street": s2["address"][0]["street"],"postcode":s2["address"][0]["postcode"]}      #δημιουργια student και καταχωρηση ονοματος-διευθυνσης-ΤΚ
                # Η παρακάτω εντολή χρησιμοποιείται μόνο στη περίπτωση επιτυχούς αναζήτησης φοιτητών (δηλ. υπάρχει φοιτητής με αυτό το email).
                return Response(json.dumps(student), status=200, mimetype='application/json')
            else:
                return Response("This Student has no address")
        else:
            return Response("This email does not belong to any Student")


# ΕΡΩΤΗΜΑ 7: Διαγραφή φοιτητή βάσει email
@app.route('/deleteStudent', methods=['DELETE'])
def delete_student():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή. 
        * Στη περίπτωση που υπάρχει φοιτητής με αυτό το email, να διαγράφεται από τη ΒΔ. Να επιστρέφεται μήνυμα επιτυχούς διαγραφής του φοιτητή.
        * Διαφορετικά, να επιστρέφεται μήνυμα λάθους. 

        Και στις δύο περιπτώσεις, να δημιουργήσετε μία μεταβλήτη msg (String), η οποία θα περιλαμβάνει το αντίστοιχο μήνυμα.
        Αν βρεθεί ο φοιτητής και διαγραφεί, στο μήνυμα θα πρέπει να δηλώνεται και το όνομά του (πχ: msg = "Morton Fitzgerald was deleted.").
    """
    uuid = request.headers.get('authorization')
    valid = is_session_valid(uuid)

    if valid == False:
        return Response("Unauthorized", status=401)
    else:
        msg="This email does not belong to any Student"     #το μηνυμα που θα εμφανιστει στο τελος εαν ΔΕΝ γινει διαγραφη καποιου student
        if (students.find_one({"email": data['email']}) != None):
            #ακολουθειται η ιδια διαδικασια οπου το string s1 γινεται s2 που ειναι dict (περιεχει τα δεδομενα του φοιτητη)
            s1 = json.dumps(students.find_one({"email": data['email']}, {"_id": 0,"yearOfBirth":0}))
            s2 = ast.literal_eval(s1)
            nm = s2["name"]
            msg= nm+" was deleted."     #αλλαγη του μηνυματος που θα επιστραφει στο τελος
            students.delete_one({"name": nm})       #διαγραφη του φοιτητη

    return Response(msg, status=200, mimetype='application/json')


# ΕΡΩΤΗΜΑ 8: Εισαγωγή μαθημάτων σε φοιτητή βάσει email
@app.route('/addCourses', methods=['PATCH'])
def add_courses():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data or not "courses" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή. Στο body του request θα πρέπει δίνεται ένα json της παρακάτω μορφής:

        {
            email: "an email",
            courses: [
                {'course 1': 10, 
                {'course 2': 3 }, 
                {'course 3': 8},
                ...
            ]
        } 

        Η λίστα courses έχει μία σειρά από dictionary για τα οποία τα key αντιστοιχούν σε τίτλο μαθημάτων και το value στο βαθμό που έχει λάβει ο φοιτητής σε αυτό το μάθημα.
        * Στη περίπτωση που υπάρχει φοιτητής με αυτό το email, θα πρέπει να γίνει εισαγωγή των μαθημάτων και των βαθμών τους, σε ένα νέο key του document του φοιτητή που θα ονομάζεται courses. 
        * Το νέο αυτό key θα πρέπει να είναι μία λίστα από dictionary.
        * Αν δε βρεθεί φοιτητής με αυτό το email να επιστρέφεται μήνυμα λάθους. 
    """

    uuid = request.headers.get('authorization')
    valid = is_session_valid(uuid)

    if valid == False:
        return Response("Unauthorized", status=401)
    else:
        msg = "This email does not belong to any Student"
        if (students.find_one({"email": data['email']}) != None):
            students.update_one({"email": data['email']}, {"$set" : {"courses":data["courses"] }})
            msg="Courses Added"

        return Response(msg, status=200, mimetype='application/json')


# ΕΡΩΤΗΜΑ 9: Επιστροφή περασμένων μαθημάτων φοιτητή βάσει email
@app.route('/getPassedCourses', methods=['GET'])
def get_courses():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή.
        * Στη περίπτωση που ο φοιτητής έχει βαθμολογία σε κάποια μαθήματα, θα πρέπει να επιστρέφεται το όνομά του (name) καθώς και τα μαθήματα που έχει πέρασει.
        * Στη περίπτωη που είτε ο φοιτητής δεν περάσει κάποιο μάθημα, είτε δεν υπάρχει φοιτητής με αυτό το email στο σύστημα, να επιστρέφεται μήνυμα λάθους.

        Αν υπάρχει όντως ο φοιτητής με βαθμολογίες σε κάποια μαθήματα, να περάσετε τα δεδομένα του σε ένα dictionary που θα ονομάζεται student.
        Το dictionary student θα πρέπει να είναι της μορφής: student = {"course name 1": X1, "course name 2": X2, ...}, όπου X1, X2, ... οι βαθμολογίες (integer) των μαθημάτων στα αντίστοιχα μαθήματα.
    """


    uuid = request.headers.get('authorization')
    valid = is_session_valid(uuid)

    if valid == False:
        return Response("Unauthorized", status=401)
    else:
        msg = "This email does not belong to any Student"
        if (students.find_one({"email": data['email']}) != None):
            s1 = json.dumps(students.find_one({"email": data['email']}, {"_id": 0, "yearOfBirth": 0}))
            s2 = ast.literal_eval(s1)
            student = {"name":s2["name"]}
            atLeastOne=False        #μεταβλητη που βοηθαει να ελεγξουμε αν εχει τουλαχιστον ενα περασμενο μαθημα.
            courses_in_dict = "courses" in s2       #true εαν ο φοιτητης εχει τουλαχιστον ενα ΚΑΤΑΧΩΡΗΜΕΝΟ μαθημα
            if(courses_in_dict):
                for x in s2["courses"][0]:      #loop ώστε να ψάξουμε ένα-ένα τους βαθμούς
                    if(s2["courses"][0][x]>=5):     #ελεγχος αν το συγκεκριμενο course εχει περαστει (δηλαδη ο βαθμος του ειναι >=5)
                        student[x]=s2["courses"][0][x]      #προσθεση του περασμενου μαθηματος στο student dict που θα επιστραφει στο τελος
                        atLeastOne=True
        else:
            return Response(msg)

    if(atLeastOne==False):
        return Response("This student has 0 courses passed.")

    else:
        # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητή (υπάρχει ο φοιτητής και έχει βαθμολογίες στο όνομά του).
        return Response(json.dumps(student), status=200, mimetype='application/json')

# Εκτέλεση flask service σε debug mode, στην port 5000. 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)