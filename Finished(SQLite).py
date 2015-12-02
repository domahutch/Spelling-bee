#I had to use global a lot because it is impossible to return data from a function activated by a TKinter Button :(

from tkinter import * #TKInter for GUI
from random import randint #Randint for randomising test
import sqlite3 #For database

conn = sqlite3.connect('test.db')#Connects to database
c = conn.cursor()

print('Beginning')

def getWordDetails(): #Collects the details for the test words from the database (i.e. Words, Definitions, IDs, testIDs)
    global IDsandDefinitions
    wordIDs = []
    words = []
    nameIDs = {}
    testIDs = []
    definitions = []
    wordAndIDs = {}
    IDsandTest = {}
    IDsandDefinitions = {}
    sql = 'SELECT * FROM words' #Queries the database for all information for the 'words' table
    for k in c.execute(sql):#Searches database for WordIDs, words, definitions and testIDs
        wordIDs.append(k[0])
        words.append(k[1])
        definitions.append(k[2])
        testIDs.append(k[3])
    length = len(words)
    for k in range (0, length):#Associates words with their ID, test and definition
        wordAndIDs[wordIDs[k]] = words[k]
        IDsandTest[wordIDs[k]] = testIDs[k]
        IDsandDefinitions[wordIDs[k]] = definitions[k]
    print('FUNCTION getWordDetails COMPLETE')
    return(wordIDs, words, testIDs, definitions, wordAndIDs, IDsandTest, IDsandDefinitions)#Returns all details

def userIDsAndNames(): #Collects userDetails at the start from the database
    global userIDtoName, userIDs, userDetails #Sends data to other functions
    names = []
    userIDs = []
    userDetails = {}
    userIDtoName = {}
    sql = 'SELECT * FROM users' #Queries the database for all data from 'users' table
    for k in c.execute(sql):
        names.append(k[1]) #Collects the names of all users
        userIDs.append(k[0]) #Collects the userIDs of all users
    length = len(names)
    for k in range(0, length):
        userDetails[names[k]] = userIDs[k] #Assigns the each name to their ID
        userIDtoName[userIDs[k]] = names[k]#Inverse of above
    return(names, userIDs, userDetails, userIDtoName)#Returns data

def findTest(): #Collects all the data on tests from the database
    global testID, testName #Shares data to other functions
    testNames =[]
    testIDs = []
    testNameIDs = {}
    testIDsNames = {}
    sql = 'SELECT * FROM tests' #Queries database for all data from the 'tests' table
    for k in c.execute(sql):
        testNames.append(k[1])#Collects the names of all the tests
        testIDs.append(k[0])#Collects the IDs of all the tests
    length = len(testNames)
    for k in range(0, length):
        testNameIDs[testNames[k]] = testIDs[k]#Assigns each ID to the name of their test
        testIDsNames[testIDs[k]] = testNames[k]#Inverse of above
    return(testNames, testIDs, testNameIDs, testIDsNames) #Returns all data

def userLogin(userIDClass): #Logs the user in, activated when the Login button is taken
    global username, userDetails #Sends username, recieves userDetails
    username = usernameEntry.get() #Assigns text entered in the username Entrybox to the username variable
    password = passwordEntry.get() #Finds text entered in the password entrybox
    actualPassword = 'This is never going to be the real password'
    sql = 'SELECT * FROM users Where username = ?' #Queries database for all details of entries in 'users' table with the chosen username
    for k in c.execute(sql, [(username)]):
        actualPassword = k[2] #Password in databse
        group = k[3] #Class of user
        Id = k[0] #User ID
    if actualPassword == 'This is never going to be the real password': #If the password hasn't changed it means the username is not associate to an entry in the table
        currentUserLabel.config(text = 'That is an invalid username') #Outputs to user
    elif actualPassword == password: #If the entered password and username are correect
        print('Logged In') #Output to Log
        teacher = str(k[4]) #Teacher status of user from database
        currentUserLabel.config(text = 'Logged in as '+username+'. Class: '+group)
        if teacher == 'False': #If they are not a teacher, only test buttons are avalible to them
            outputUserResults() #Outputs users previous results 
            newWordButton.config(state = DISABLED) #Allows acess to appropriate buttons
            quizSelectButton.config(state = NORMAL)
            pupilSelectButton.config(state = DISABLED)
            resultSelectButton.config(state = DISABLED)
        else: #If they are a teacher the buttons related to adding words or seeing pupil results are avalible to them
            newWordButton.config(state = NORMAL)#Allows acess to appropriate buttons
            quizSelectButton.config(state = DISABLED)
            pupilSelectButton.config(state = NORMAL)
            resultSelectButton.config(state = DISABLED)
            resultsList.delete(0, END)
            findTeachersPupils(Id)
    else: #If the user exists in the table, but the entered password doesn't match that in the table
        currentUserLabel.config(text = 'Incorrect Password')#Output to user
        print('That is an invalid password')#Output to Log
    print('FUNCTION: userLogin COMPLETE')
    
def signUp(names, classNames): #Activated when the sign up button is pressed, adds users to the database
    global username #Shares the username to other functions
    username = usernameEntry.get() #Assigns text entered in the username Entrybox to the username variable
    password = passwordEntry.get()#Finds text entered in the password entrybox
    username = username.lower()#Sets the username to be in lowercase for the database
    try: #If a class has been selected
        value = classBox.curselection() #The position of the chosen class in the list box
        strip = str(value).strip(',') #Removes the comma which is for some reason returned with the value from the listBox
        value = int(strip[1])
        group = classNames[value] #The name of the class chosen by the user
        if username in str(names): #If username already exists in the table
            currentUserLabel.config(text = 'That username is already taken')#Output to user
            print('That username is already taken')#Output to log
        else: #If username isn't already included in the table
            teacher = teacherVar.get() #Checks whether the new user has chosen to be a teacher or not
            if teacher == 0: #If not a taecher
                c.execute('INSERT INTO users(username, password, class, teacher) VALUES (?,?,?,?)',(username, password, group, 'False')) #Adds data to 'users' table
                addUsertoResults(username) #Runs function that adds the user to the results table
                outputUserResults() #Outputs the users previous results
                newWordButton.config(state = DISABLED) #Allows acess to appropriate buttons
                quizSelectButton.config(state = NORMAL)
                pupilSelectButton.config(state = DISABLED)
                resultSelectButton.config(state = DISABLED)
                print('Account Created')#Output to log
            else: #If they are a teacher
                c.execute('INSERT INTO users(username, password, class, teacher) VALUES (?,?,?,?)',(username, password, group, 'True'))#Adds data to 'users' table
                currentUserLabel.config(text = 'Logged in as '+username)
                newWordButton.config(state = NORMAL) #Allows acess to appropriate buttons
                quizSelectButton.config(state = DISABLED)
                pupilSelectButton.config(state = NORMAL)
                resultSelectButton.config(state = DISABLED)
                resultsList.delete(0, END)
                print('Account Created')
            conn.commit()#Saves data to table
            currentUserLabel.config(text = 'Logged in as '+username)#Outputs to user
    except: #If a class hasn't be selected
        print('No class selected') #Output to log
        currentUserLabel.config(text = 'Please select a class') #Output to user

def chooseQuiz(testIDs, testNames): #Runs when the quizSelectButton is pressed, finds the test the user wishes to use
    value = quizList.curselection()
    strip = str(value).strip(',')
    value = int(strip[1])
    testID = testIDs[value] #Finds the ID of selected test
    testName = testNames[value] #Finds the name of selected test
    quizGenerateButton.config(state = NORMAL) #Allows the user to generate a quiz
    print('FUNCTION: chooseQuiz COMPLETE')
    
def findWordsForTest(testID, IDsandTest, wordIDs, wordAndIDs, IDsandDefinitions): #Run when Generate Quiz button is pressed
    global wordsForTest, wordIDsforTest, score, question #Shares data to other functions
    score = int(0) #Resets score to 0
    question = int(0) #Resets question count to 0
    length = len(wordIDs)
    wordIDsforTest = []
    wordsForTest = []
    for k in range(0, length):
        wordID = wordIDs[k]  #Takes a word from the list of all wordIDs
        if IDsandTest[wordID] == testID: #If the testID associated to the word is the same as the chosen testID
            wordIDsforTest.append(wordIDs[k]) #Adds the wordID to list of words for this test
        else: #If not
            pass #Do nothing
    wordID = wordIDs[length-1]
    if IDsandTest[wordID] == testID: #Checks last wordID in the list, for some reason this doesn't work in the for loop
        wordIDsforTest.append(wordIDs[length - 1])
    else:
        pass
    length = len(wordIDsforTest)
    for k in range(0, length ): #Gets the word for the test from the wordIDs
        word = wordAndIDs[wordIDsforTest[k]]
        wordsForTest.append(word)
    word = wordAndIDs[wordIDsforTest[length-1]]
    wordsForTest.append(word)
    test(wordsForTest, IDsandDefinitons, wordIDsforTest) #Runs test function
    submitButton.config(state = NORMAL) #Enables submit button
    print('FUNCTION: findWordsForTest COMPLETE')

def test(wordsForTest, IDsandDefinitons, wordIDsforTest):
    global word, question
    length = len(wordIDsforTest)
    random = randint(0, length - 1) #Picks a random word
    definition = IDsandDefinitions[wordIDsforTest[random]] #Finds defintion for word
    definitionLabel.config(text = definition) #Updates label to show definition
    word = wordsForTest[random]
    wordIDsforTest.remove(wordIDsforTest[random]) #Removes the wordID from list so it can't be chosen again
    wordsForTest.remove(word)#Removes word so the positioning is correct
    question = question + 1 #Increases the question count by one
    print('Question: '+str(question))
    print('FUNCTION: test COMPLETE')

def spellCheck(word, correct): #Spell checks the word
    lengthWord = len(word)
    lengthCorrect = len(correct)
    difference = lengthWord - lengthCorrect
    if difference == 0: #If entered word is the same length an the correct word
        length = lengthWord
    elif difference > 0: #If entered word is longer than correct word
        length = lengthCorrect
        difference = lengthWord - lengthCorrect
    else: #If correct word is longer than entered word
        length = lengthWord
        difference = lengthCorrect - lengthWord
    incorrect = difference #Every letter in length they missed out is considered wrong
    for k in range(0, length):
        if word[k] == correct[k]: #If letter in correct word is identical to the letter in the same position of the correct word
            pass
        else: #If not, increase incorrect count by one
            incorrect = incorrect + 1
    if incorrect > 1: #If more than one letter is wrong, or word is more than one letter out in length
        returning = 'WRONG'
    elif incorrect == 1: #If only one letter is wrong, or word is only one letter out in length
        returning = 'ALMOST'
    else: #If word is completly correct
        returning = 'CORRECT'
    return returning
    print('FUNCTION spellCheck COMPLETE')

def answer(word, IDsandDefinitons): #Activated when user presses submit button
    global score, question
    answer = answerEntry.get() #Assigns text in answer entry box to the answer variable
    state = spellCheck(answer, word) #Spell checks the answer
    if state == 'CORRECT': #If answer is completly correct
        feedbackLabel.config(text = 'That is correct') #Outputs to user
        score = score + 2 #Increases score
        print('Score: '+str(score))#Output to log
        text = 'Score: '+str(score)
        scoreLabel.config(text = text)#Output to user
    elif state == 'ALMOST': #If answer is partially correct
        feedbackLabel.config(text = 'That is almost correct, the correct answer was '+word)#Output to user
        score = score + 1 #Increases score
        print('Score: '+ str(score))#Output to log
        text = 'Score: '+str(score)
        scoreLabel.config(text = text)#Output to user
    else: #If answer is wrong
        feedbackLabel.config(text = 'That is wrong, the correct answer was '+word) #Output to user
    answerEntry.delete(0, END)#Enters answer entrybox
    if question <10: #If 10 questions have not been completed
        test(wordsForTest, IDsandDefinitons, wordIDsforTest) #Run test
    else: #If 10 questions have been completed
        feedbackLabel.config(text = 'Test complete. You scored '+str(score)) #Output ot user
        print('Test Finished')#Output to log
        submitButton.config(state = DISABLED) #Disables submit button
        saveHistory()#Saves test to 'history' table
        updateResults()#Updates user results in database
        outputUserResults()#Output results to user (Updates the resultbox on the GUI)
    print('FUNCTION: answer COMPLETE')
    
def saveHistory(): #Saves test details to 'history' table
    global score, username, testID, userDetails
    userID = userDetails[username]
    c.execute('INSERT INTO history(userID, testID, score) VALUES (?,?,?)', (userID, testID, score)) #Saves the user who took the test, the test they took and the score they got
    conn.commit()#Saves result
    print('FUNCTION saveReult COMPLETE')
    
def addUsertoResults(username): #Adds new users to 'results' table
    global testIDs, userDetails
    length = len(testIDs)
    sql = 'SELECT * FROM users WHERE username = ?' #Queries 'users' table for all data from entries with the username of the new user
    for k in c.execute(sql, ([username])):
        userID = k[0]#UserID of the current user
        for k in range(0, length): #Adds a seperate entry for each test
            testID = testIDs[k]
            c.execute('INSERT INTO results(userID, testID, attempts, average) VALUES (?,?,?,?)',(userID, testID, 0, 0))
            conn.commit()#Saves data to table

def updateResults(): #Updates the results in the database for the current user with the test they just took
     global resultIDs, username, score, testID, userDetails
     userID = userDetails[username] #Current user's ID
     sql = 'SELECT * FROM results WHERE testID = ?' #Queries 'results' table for all data from entries with specified testID
     for k in c.execute(sql, ([testID])):
         if k[1] == userID: #If the userID associated with test is the same as the current user's
             ID = k[0] 
             attempts = k[3] #Takes attempts from database
             average = k[4] #Takes average from database
             newAverage = ((average*attempts)+score)/(attempts+1) #Updates the average
             newAttempts = attempts + 1 #Upades the attempts
             c.execute('UPDATE results SET average = ? WHERE ID = ?',(newAverage, ID)) #Updates average data
             c.execute('UPDATE results SET attempts = ? WHERE ID = ?',(newAttempts, ID)) #Updates attempts data
             conn.commit() #Saves data
             print('Saved Result')#Outputs to log

def outputUserResults(): #Outputs results of current user to the listbox in the GUI
    global username, testIDsNames, userIDtoName, userDetais
    sql = 'SELECT * FROM results' #Queries the 'results' table for all data
    resultIDs = []
    results = []
    currentUserID = userDetails[username]
    for k in c.execute(sql): #Executes Query
        userID = k[1] #User ID for entry
        if userID == currentUserID: #If userID for entity is the same as the current user's
            resultIDs.append(k[0]) #Adds resultID to list
            average = k[4] #Takes the average
            attempts = k[3] #Takes the attempts
            testName = testIDsNames[k[2]] #Finds testName
            string = (str(testName)+': Average = '+str(average)+'; Attempts = '+str(attempts)) #Constructs string to be outputted to user
            results.append(string)#Saves string to list
        else:
            pass
    resultsList.delete(0, END) #Clears listbox
    length = len(results)
    for k in range(0, length): #Updates listBox
        resultsList.insert(k+1, results[k])

def addWord(words, testNames, testNameIDs): #Activated when addWord button is pressed
    word = newWordEntry.get() #Gets text from word entrybox
    definition = newWordDefinitionEntry.get() #Gets text from definition entrybox
    quiz = newWordQuizEntry.get() #Gets text from quiz entrybox
    if quiz not in testNames:#If entered quiz doesn't exist
        currentUserLabel.config(text = 'That quiz does not exist') #Output to user
    else: #If entered quiz does exist
        quizID = testNameIDs[quiz]
        if word in words: #If word is already included in word list (Doesn't check whether it is for selected test or not)
            currentUserLabel.config(text = 'That word is already in the list')
        else:
            c.execute('INSERT INTO words(word, definition, testID) VALUES (?,?,?)',(word, definition, quizID)) #Adds data to database
            conn.commit()#Saves data
            currentUserLabel.config(text = 'Word has been added to database') #Outputs to user
            print('Word Added')
    print('FUNCTION addWord COMPLETE')

def classDetails(userIDs): #Gets details for classes
    global userIDClass
    classNames = []
    group = []
    userIDClass = {}
    ClassUserID = {}
    length = len(userIDs)
    sql = 'SELECT * FROM users' #Queries 'users' table for all data
    for k in c.execute(sql): #Executes query
        group.append(k[3]) #Appends class name to list
    print(group)
    for k in range(0, length):
        Id = userIDs[k]
        userIDClass[Id] = group[k]
        if group[k] in classNames: #If class is already in list of names
            pass
        else:#If not
            classNames.append(group[k]) #Add to list
    return classNames, userIDClass

def findTeachersPupils(Id): #Finds pupils for teachers, activates when a teacher logins in /signs up
    global userIDtoName, userIDs, sameGroupID #Takes information
    sameGroupID = []
    length = len(userIDClass)
    teacherGroup = userIDClass[Id] #Finds the teacher's class
    for k in range (0, length):#Checks everyother user to see if they are in the same class as the teacher
        userID = userIDs[k]#Picks a pupil
        if userID == Id: #If the user is the teacher then ignore
            pass
        else:
            pupilGroup = userIDClass[userID] #Finds the User's class
            if pupilGroup == teacherGroup: #If pupil is in the same class as the teacher then adds them to a list
                sameGroupID.append(userID)
    classPupilsList.delete(0, END) #Clears listBox
    length = len(sameGroupID)
    for k in range(0, length): #Writes list of pupils to ListBox
        classPupilsList.insert(k+1, userIDtoName[sameGroupID[k]])

def pupilResultsToTeacher(sameGroupID):#Finds the results of the chosen pupil, activated when the 'Choose a pupil' button is pressed
    global resultIDs, testIDsNames, userDetails, userIDtoName, results, pupilUserName
    resultSelectButton.config(state = NORMAL) #Enables the 'Select a result' button
    results = []
    value = str(classPupilsList.curselection())
    strip = value.strip(',')
    value = int(strip[1])
    pupilID = sameGroupID[value]#The ID of chosen pupil
    pupilName = userIDtoName[pupilID] #Name of chosen pupil
    pupilUserName = pupilName
    sql = ('SELECT * FROM results WHERE userID = ?') #Queries the 'results' table for all results where the userID is the same as the chosen pupil's
    for k in c.execute(sql, ([pupilID])):#Executes query
        testID = k[2]
        testName = testIDsNames[testID]
        average = k[4]
        attempts = k[3]
        string = (str(testName)+': Average = '+str(average)+'; Attempts = '+str(attempts)) #Creates the string which will be outputted to the user
        results.append(string)#Adds string to the list
    print('Results collected')
    print(results)
    pupilResultsList.delete(0, END) #Clears the Pupil Results Listbox
    length = len(results)
    for k in range(0, length):#Writes the results to the listBox
        pupilResultsList.insert(k+1, results[k])

def historyToTeacher(): #Finds the history of results for the chosen user, in the chosen test
    global results, testNameIDs, pupilUserName, userDetails
    scores = []
    outputList = []

    value = str(pupilResultsList.curselection())
    strip = value.strip(',')
    value = int(strip[1])
    line = results[value] #The line chosen by the user from the results listBox
    strip = line.split(': Average') 
    testname = strip[0] #Chosen test name
    testID = testNameIDs[testname] #Chosen test ID
    pupilID = userDetails[pupilUserName] #Chosen pupilId

    sql = 'SELECT * FROM history WHERE userID = ?' #Queries 'history' for all entries with a userID is the same as the chosen user
    for k in c.execute(sql, ([pupilID])):#Executes query
        score = k[3]
        scores.append(score)
    length = len(scores)
    for k in range(0, length): #Creates strings to be outputted to user
        string = ('Attempt '+str(k)+'; Score '+str(scores[k]))
        outputList.append(string)
        
    historyList.delete(0, END)#Clears listbox
    length = len(outputList)
    for k in range(0, length):#Adds data to listbox
        historyList.insert(k+1, outputList[k])

def funButton(): #I have used this to test parts of the program, currently not in GUI
    global teacherVar
    print(teacherVar.get())
    print('FUNCTION: funButton COMPLETE')

#Collects the data from the database at the start of the program
wordIDs, words, testIDs, definitions, wordAndIDs, IDsandTest, IDsandDefinitions = getWordDetails()
testNames, testIDs, testNameIDs, testIDsNames = findTest()
names, userIDs, userDetails, userIDtoName = userIDsAndNames()
classNames, userIDClass= classDetails(userIDs)

#Creates window, gives it a title and defines dimensions
base = Tk()
base.title('Spelling bee')
base.geometry("650x600")

print('Base DECLARED')

global teacherVar #Variable of the 'teacher' tick box
teacherVar = IntVar()

#Creates the widgets used for Login/SignUp
loginBorder = Label(width = 52, height = 6, relief = SUNKEN)
titleLabel = Label(text='Welcome to the Speeling Bee', relief = RAISED)
buttonLogin = Button(height = 3, width = 7,text='Login', fg = 'blue', command = lambda: userLogin(userIDClass))
buttonSignUp = Button(width = 7, text='Sign up', command = lambda: signUp(names, classNames))
usernameLabel = Label(text = 'Username:')
passwordLabel = Label(text = 'Password:')
usernameEntry = Entry()
passwordEntry = Entry(show = '*')
labelSignIn1 = Label(text = 'Sign Up Options', width = 15)
teacherCheckBox = Checkbutton(text = 'Teacher', variable = teacherVar, onvalue = 1, offvalue = 0)
currentUserLabel = Label()
classBox = Listbox(selectmode = SINGLE, height = 3, width = 15)

length = len(classNames)
for k in range(0, length):#Adds names of classes to listbox
    classBox.insert(k+1, classNames[k])

print('Membership modules DECLARED')

#Places Login/SignUp widgets
loginBorder.place(x=0, y=25)
usernameLabel.place(x=2, y=35)
usernameEntry.place(x=60, y=35)
passwordLabel.place(x=3, y=65)
passwordEntry.place(x=60, y=65)
buttonLogin.place(x=185, y=30)
labelSignIn1.place(x=245, y=30)
buttonSignUp.place(x=185, y=85)
teacherCheckBox.place(x=253, y=48)
currentUserLabel.place(x=4, y =0)
classBox.place(x=245, y=68)

print('Membership modules POSITIONED')

#Creates the widgest used for the test
quizBorder = Label(heigh = 9, width = 52, relief = SUNKEN)
quizList = Listbox(selectmode = SINGLE, heigh = 5, width = 15)
quizSelectButton = Button(text = 'Choose Quiz', state = DISABLED, command = lambda: chooseQuiz(testIDs, testNames),width = 12)
quizGenerateButton = Button(text = 'Generate Quiz',state = DISABLED, command = lambda: findWordsForTest(testID, IDsandTest, wordIDs, wordAndIDs, IDsandDefinitions),width = 12)
definitionLabel =Label(width = 37, relief = SUNKEN)
answerEntry = Entry()
submitButton = Button(text = 'Submit',state = DISABLED, command = lambda: answer(word, IDsandDefinitions))
scoreLabel = Label(text = 'Score: 0')
feedbackLabel = Label()
resultsList = Listbox(selectmode = SINGLE, width = 40)
resultTitleLabel = Label(text = 'Results')
testLabel1 = Label(text = 'Answer:')

print('Quiz modules DECLARED')

length = len(testNames)
for k in range(0, length):#Adds the names of Tests to listbox
    quizList.insert(k+1, testNames[k])

#Places test widgets
quizBorder.place(x=0, y =122)
quizGenerateButton.place(x=4, y=235)
quizList.place(x=4, y=125)
quizSelectButton.place(x=4, y=210)
definitionLabel.place(x=100, y=125)
feedbackLabel.place(x=100, y=170)
testLabel1.place(x=100, y=147)
answerEntry.place(x=150, y=149)
submitButton.place(x=275, y=147)
scoreLabel.place(x=275, y=170)
resultsList.place(x=400, y=25)
resultTitleLabel.place(x=400, y=5)

print('Quiz modules POSITIONED')

#Creates widgets used for teacher features
teacherBorder = Label(height = 22, width = 55, relief = SUNKEN)
newWordEntry = Entry()
newWordDefinitionEntry = Entry()
newWordQuizEntry = Entry()
newWordLabel1 = Label(text = 'Add a new word:')
newWordLabel2 = Label(text = 'Word:')
newWordLabel3 = Label(text = 'Definition:')
newWordLabel4 = Label(text = 'Quiz:')
newWordButton = Button(state = DISABLED, text = 'Add Word',command = lambda: addWord(words, testNames, testNameIDs),width = 15)
classPupilsList = Listbox(selectmode = SINGLE)
pupilSelectButton = Button(state = DISABLED, text = 'Choose a pupil.', command = lambda: pupilResultsToTeacher(sameGroupID))
pupilResultsList = Listbox(selectmode = SINGLE)
resultSelectButton = Button(state = DISABLED, text = 'Choose a result.', command = lambda: historyToTeacher())
historyList = Listbox(selectmode = SINGLE)
pupilLabel = Label(text = 'Pupils')
pupilResultsLabel = Label(text = 'Results')
historyLabel = Label(text = 'History')

print('Teacher modules DECLARED')

#Places teacher feature widgets
teacherBorder.place(x=0, y =262)
newWordEntry.place(x=70, y = 287)
newWordDefinitionEntry.place(x=70, y = 310)
newWordQuizEntry.place(x=70, y = 333)
newWordLabel1.place(x=75, y = 265)
newWordLabel2.place(x=27, y = 287)
newWordLabel3.place(x=4, y = 310)
newWordLabel4.place(x=31, y = 333)
newWordButton.place(x=62, y = 355)
pupilLabel.place(x=50, y=381)
classPupilsList.place(x=4, y = 401)
pupilSelectButton.place(x=20, y = 565)
pupilResultsLabel.place(x=170, y=381)
pupilResultsList.place(x=134, y = 401)
resultSelectButton.place(x=150, y = 565)
historyLabel.place(x=306, y=381)
historyList.place(x=264, y =401)


print('Teacher modules POSITIONED')

print('base window LOADED')
base.mainloop()
