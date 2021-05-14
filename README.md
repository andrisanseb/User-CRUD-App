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




Ερώτηση 3: Επιστροφή φοιτητή βάσει email

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




Ερώτηση 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών

Κώδικας:

![4code](https://user-images.githubusercontent.com/52543423/118264184-ff4e3200-b4bf-11eb-868c-57d0f37f442f.PNG)


Εξετάζεται αν ο χρήστης έχει authorization.
Αν ναι (περνάει στο else), δημιουργείτε η λίστα lst30.
Στην συνέχεια ψάχνουμε έναν-έναν τους students της βάσης μέσω της find ποιοι είναι 30 χρονών ,2021-x["yearOfBirth"] == 30 όπου κρατάει τα δεδομένα του τρέχων student από το loop.Αν η συνθήκη ισχύει τότε προσθέτουμε τα δεδομένα του συγκεκριμένου student στην lst30 (μέσω του append(x) ).
Αφού έχει ελέγξει όλους τους student , αν η lst30 είναι άδεια επιστρέφει πως κανείς δεν είναι 30 χρονών. Διαφορετικά επιστρέφει την lst30 / τα δεδομένα των student.   


POSTMAN:

![4pstman](https://user-images.githubusercontent.com/52543423/118265309-a8e1f300-b4c1-11eb-88c4-1759c9e4a6ab.PNG)



Ερώτηση 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών

Ο κώδικας είναι ο ίδιος με αυτόν του 4ου ερωτήματος.
Μόνη αλλαγή είναι η συνθήκη που τώρα διαλέγει μόνο όσους είναι τουλάχιστον 30 ετών.
Επίσης χρησιμοποιώ άλλη λίστα για την αποφυγή τυχών error.
Δηλαδή  2021-x["yearOfBirth"] >= 30


Ερώτηση 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email

Κώδικας:



Αρχικά,επαναλαμβάνεται η διαδικασία ελέγχου authorization.
Εφόσον έχει authorization ψάχνουμε αν υπάρχει φοιτητής στην βάση με το email που δώθηκε.
Αν δεν υπάρχει επιστρέφει ανάλογο μήνυμα.
Αν υπάρχει, τότε τα δεδομένα του φοιτητή περνάνε στην μεταβλητή s1. Το s1 όμως είναι τύπου string αν και έχει ακριβώς την δομή ενός dict.Για να έχω τα δεδομένα μου σε μεταβλητή τύπου dict κάνω import ast και μέσω της μεθόδου ast.literal_eval(s1) περνάω τα δεδομένα στην μεταβλητή s2 που είναι dict.
Στην συνέχεια  γίνεται ο εξής έλεγχος if(isinstance(s2["address"][0]["street"],str)) . Αν ο φοιτητής έχει καταχωρημένη διεύθυνση τότε το s2["address"][0]["street"] είναι τύπου string και επιστρέφεται True (οπότε περνάει τον έλεγχο). Εφόσον έχει διεύθυνση δημιουργείται το student{} όπου προσθέτω name-street-postcode.Τέλος, επιστρέφεται το student με status 200.


POSTMAN(δίνεται email φοιτητή που να έχει address):

![6legit](https://user-images.githubusercontent.com/52543423/118274491-df256f80-b4cd-11eb-999b-56f84fedd5d0.PNG)







