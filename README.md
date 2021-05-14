# Ergasia_1_E18008_Andrisan_Sebastian


Ερώτημα 1: Δημιουργία χρήστη

Κώδικας:


![cruser1](https://user-images.githubusercontent.com/52543423/118262747-02482300-b4be-11eb-9f3f-660e9ae7716d.PNG)


Μια if ελέγχει εάν το username που δώθηκε υπάρχει ήδη στην users μέσω της find_one().
Εάν ΔΕΝ βρεθεί ίδιο username στην βάση τότε δημιουργείται νέος χρήστης μέσω της insert_one() και επιστρέφει ανάλογο μήνυμα με status code 200.
Αν βρέθηκε ίδιο username στην βάση με αυτό που δώθηκε τότε επιστρέφει πως υπάρχει ήδη χρήστης με αυτό το username με status code 400.



Αποτέλεσμα POSTMAN 1ης φοράς:


![createUser1](https://user-images.githubusercontent.com/52543423/118262110-17708200-b4bd-11eb-8c13-975bdea057c6.PNG)

Αποτέλεσμα POSTMAN 2η φορά(ίδιο username):


![createUser1pali](https://user-images.githubusercontent.com/52543423/118262190-32db8d00-b4bd-11eb-8234-7f2b3a460452.PNG)



Ερώτημα 2: Login στο σύστημα

Κώδικας:

![logincode1](https://user-images.githubusercontent.com/52543423/118262648-db89ec80-b4bd-11eb-97a6-0e02959261fd.PNG)




Η εντολή find_one() ψάχνει εάν υπάρχει username με password στην collection Users που να είναι ίδια με τα αντίστοιχα data['username'] και data['password'] που δώθηκαν.
Εφόσον υπάρχει , καλείται η create_session με παράμετρο το username και επιστρέφεται ένας κωδικός που αποθηκεύεται στο user_uuid.
Στην συνέχεια επιστρέφεται απάντηση που περιλαμβάνει τον κωδικό user_uuid και το username που έκανε login , με status code 200.
Στην περίπτωση που δεν βρέθηκε user στην βάση με το ίδιο username και password με αυτά που δώθηκαν , επιστρέφεται απάντηση πως τα δεδομένα που δώθηκαν είναι λάθος , με status code 400 .

POSTMAN:

![login1](https://user-images.githubusercontent.com/52543423/118262961-4f2bf980-b4be-11eb-8930-8b4a7e020c25.PNG)




Ερώτημα 3: Επιστροφή φοιτητή βάσει email

Κώδικας:

![3rdcode](https://user-images.githubusercontent.com/52543423/118263451-fa3cb300-b4be-11eb-8291-7d9b5dbdaced.PNG)



Ελέγχεται αν ο χρήστης έχει αυθεντικοποιηθεί, η απάντηση αποθηκεύεται στην μεταβλητή valid.
Αν δεν έχει γίνει αυθεντικοποίηση ( valid == False ) τότε επιστρέφεται Unauthorized με status 401
Αν έχει γίνει αυθεντικοποίηση τότε η εφαρμογή ψάχνει αν υπάρχει student που να του ανήκει το email που δώθηκε χρησιμοποιόντας την find_one().
Αν το email ανήκει σε student τότε περνάμε τα όλα τα δεδομένα(χωρίς το _id ) του student σε μια μεταβλητή s χρησιμοποιόντας την json.dumps() .
Το s όμως είναι string που έχει ίδια δομή με ένα dictionary. Έκανα import ast και με χρήση της ast.literal.eval(s) το s γίνεται dict.Αποθηκεύεται το dict αποτέλεσμα στην μεταβλητή student και επιστρέφεται με status code 200.
Σε περίπτωση που το email δεν άνηκε σε κάποιον student επιστρέφεται ανάλογο μήνυμα.

POSTMAN(με έγκυρο email):

![apotel3](https://user-images.githubusercontent.com/52543423/118263518-0f194680-b4bf-11eb-8e45-42a5238fd583.PNG)




Ερώτημα 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών

Κώδικας:

![4code](https://user-images.githubusercontent.com/52543423/118264184-ff4e3200-b4bf-11eb-868c-57d0f37f442f.PNG)


Εξετάζεται αν ο χρήστης έχει authorization.
Αν ναι (περνάει στο else), δημιουργείτε η λίστα lst30.
Στην συνέχεια ψάχνουμε έναν-έναν τους students της βάσης μέσω της find ποιοι είναι 30 χρονών ,2021-x["yearOfBirth"] == 30 όπου κρατάει τα δεδομένα του τρέχων student από το loop.Αν η συνθήκη ισχύει τότε προσθέτουμε τα δεδομένα του συγκεκριμένου student στην lst30 (μέσω του append(x) ).
Αφού έχει ελέγξει όλους τους student , αν η lst30 είναι άδεια επιστρέφει πως κανείς δεν είναι 30 χρονών. Διαφορετικά επιστρέφει την lst30 / τα δεδομένα των student.   


POSTMAN:

![4pstman](https://user-images.githubusercontent.com/52543423/118265309-a8e1f300-b4c1-11eb-88c4-1759c9e4a6ab.PNG)



Ερώτημα 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών

Ο κώδικας είναι ο ίδιος με αυτόν του 4ου ερωτήματος.
Μόνη αλλαγή είναι η συνθήκη που τώρα διαλέγει μόνο όσους είναι τουλάχιστον 30 ετών.
Επίσης χρησιμοποιώ άλλη λίστα για την αποφυγή τυχών error.
Δηλαδή  2021-x["yearOfBirth"] >= 30


Ερώτημα 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email

Κώδικας:

![6coddd](https://user-images.githubusercontent.com/52543423/118276880-d4200e80-b4d0-11eb-8ebc-46149d26b45b.PNG)


Αρχικά,επαναλαμβάνεται η διαδικασία ελέγχου authorization.
Εφόσον έχει authorization ψάχνουμε αν υπάρχει φοιτητής στην βάση με το email που δώθηκε.
Αν δεν υπάρχει επιστρέφει ανάλογο μήνυμα.
Αν υπάρχει, τότε τα δεδομένα του φοιτητή περνάνε στην μεταβλητή s1. Το s1 όμως είναι τύπου string αν και έχει ακριβώς την δομή ενός dict.Για να έχω τα δεδομένα μου σε μεταβλητή τύπου dict κάνω import ast και μέσω της μεθόδου ast.literal_eval(s1) περνάω τα δεδομένα στην μεταβλητή s2 που είναι dict.
Στην συνέχεια  χρησιμοποιώ το "address" in s2 που ελέγχει εάν υπάρχει το key "address" στο s2(εάν ο φοιτητής έχει καταχωρημένη διεύθυνση δηλαδή) και το αποτέλεσμα True ή False αποθηκεύεται στο address_in_dict .Εφόσον έχει διεύθυνση δημιουργείται το student{} όπου προσθέτω name-street-postcode.Τέλος, επιστρέφεται το student στην μορφή που ζητείται με status 200.


POSTMAN(δίνεται email φοιτητή που να έχει address):

![6legit](https://user-images.githubusercontent.com/52543423/118274491-df256f80-b4cd-11eb-999b-56f84fedd5d0.PNG)


POSTMAN(δίνεται φοιτητής που δεν έχει address):

![6notlegit](https://user-images.githubusercontent.com/52543423/118276755-a89d2400-b4d0-11eb-9928-f8c457ca64b6.PNG)



Ερώτημα 7: Διαγραφή φοιτητή βάσει email

Κώδικας:

![7codd](https://user-images.githubusercontent.com/52543423/118277712-bd2dec00-b4d1-11eb-8e15-ed967677f9ad.PNG)


Ελέγχεται αν η πρόσβαση έχει authorization.
Αν ναι γίνεται αρχικοποίηση του msg με μήνυμα αποτυχίας.
Αν βρεθεί φοιτητής με το email που δώθηκε τότε γίνεται η διαδικασία όπου φέρνουμε τα δεδομένα του φοιτητή στο s2 dict από όπου χρησιμοποιούμε μόνο το όνομα ώστε να το περάσουμε στο msg .
Τέλος επιστρέφεται το msg με status 200.

POSTMAN(διαγραφή ενός φοιτητή):

![7deleted](https://user-images.githubusercontent.com/52543423/118279573-f6fff200-b4d3-11eb-9915-f8b3a4194c6e.PNG)


POSTMAN(δίνω το email του φοιτητή που σβήστηκε πιο πάνω):

![7alrdlted](https://user-images.githubusercontent.com/52543423/118279690-1860de00-b4d4-11eb-98b1-60752578e6b7.PNG)



Ερώτημα 8: Εισαγωγή μαθημάτων σε φοιτητή βάσει email

ΠΡΟΣΟΧΗ:
Για την υλοποίηση αυτού του ερωτήματος θεώρησα πως το courses ακολουθεί την ίδια δομή με το address.
Συγκεκριμένα τα δεδομένα θα δίνονται όπως παρακάτω! :

{
    "email":"lavonneleon@ontagene.com",
    "courses":[
        {"course1":10,
        "course2":3,
        "course3":8}
    ]
}

Στην βάση θα έχει την ίδια δομή με το address:
MongoDB Compass:

![8compass](https://user-images.githubusercontent.com/52543423/118282416-eb61fa80-b4d6-11eb-90dd-79e570c4e1af.PNG)


Κώδικας:

![8dcode](https://user-images.githubusercontent.com/52543423/118282603-206e4d00-b4d7-11eb-8cc2-33ef525a3e91.PNG)


Γίνεται έλεγχος authorization και του email όπως και στα υπόλοιπα ερωτήματα.
Εφόσον αντιστοιχεί το email σε φοιτητή , του προσθέτουμε τα courses μέσω της update_one .
Το msg ενημερώνεται στην περίπτωση επιτυχούς πρόσθεσης των courses.
Επιστρέφεται msg


POSTMAN:

![8SWSTO](https://user-images.githubusercontent.com/52543423/118288846-6dedb880-b4dd-11eb-85cc-5fc90167cb76.PNG)



Ερώτημα 9: 

Κώδικας:

![9code](https://user-images.githubusercontent.com/52543423/118285637-59f48780-b4da-11eb-876d-2b42cc015ef8.PNG)



Γίνεται έλεγχος authorization και του email όπως και στα υπόλοιπα ερωτήματα.
Περνάμε τα δεδομένα του φοιτητή στο s2 με την γνωστή διαδικασία.
Δημιουργία του student τύπου dict και αρχικοποίηση με τον όνομα του φοιτητή.
Αρχικοποίηση μεταβλητής atLeastOne ως False η οποία θα αλλάξει μόνο εάν ο φοιτητής έχει περασμένο μάθημα (Χρησιμεύει ώστε να εμφανίσουμε σωστό μήνυμα στο τέλος).
Στην συνέχεια με την βοήθεια του courses_in_dict = "courses" in s2 ελέγχουμε αν ο φοιτητής έχει τουλάχιστον ένα καταχωρημένο μάθημα.Αν ναι,μέσω for περνάμε έναν-έναν τους βαθμούς και όσους είναι τουλάχιστον 5 τους περνάμε στο student dict.Αν συμβεί τουλάχιστον μια φορά το παραπάνω σενάριο ενημερώνεται και η atLeastOne αναλόγως.
Τέλος, επιστρέφουμε το όνομα του φοιτητή με όλα τα περασμένα μαθήματα (student) αλλιώς αναφέρουμε πως δεν έχει περάσει κανένα μάθημα.

 
POSTMAN:

![9SWSTO](https://user-images.githubusercontent.com/52543423/118289146-b4dbae00-b4dd-11eb-9f9a-fc0c2536dad5.PNG)



Στον κώδικα υπάρχουν comments για την καλύτερη κατανόηση του κώδικα


Andrisan Sebastian E18008
















