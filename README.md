# About BookLoaner_API
This API provides the resources for a single page application used by a 5th grade teacher. The app helps the teacher manage book loans in her classroom.

Front-end built with **VueJS**. See [Github](https://github.com/bjfikky/BookLoaner_Vue)

## Tools

 - Python 
 - Flask
 - Flask_restful
 - Peewee
 - MySQL

## Use Cases
#### Teacher
 1. Login with email and password
 2. Add student name and 4 digit passcode
 3. Edit student name and passcode
 4. Delete a student
 5. View list of students
 6. Add a book 
 7. Edit a book
 8. Delete a book
 9. View all books 
 10. See student's loan history
 11. See which student loaned a book
 12. See unavailable books 
 13. See available books
 14. Make a book available *(perform a student's return operation)*
 15.  Logout 

#### Student
1. Loan a book using pass-code
2. Return a book using pass-code
3. View list of all books
4. View list of available books
5. View list of unavailable books

## Database Models

1. User
    - username
    - email
    - password
2. Student
    - fullname
    - passcode
3. Book
    - title
    - author
    - edition
    - genre
4. Loan
    - student
    - book
    - loan_date
    - return_date
    
## Sample Response

![Sample Response](https://github.com/bjfikky/BookLoaner_API/blob/master/sample_request.png)