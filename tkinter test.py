from tkinter import *
from parse_rest.connection import register, SessionToken
from parse_rest.user import User
from parse_rest.datatypes import Object
from random import randint
import time

##A fun comment

register('pTTzpgrZvewsfdyceO8uGvTLoS4oD3TU0aeoY6En', 'wezDsrAFbbuu7nHbwvFUXDNeJdzLLGdBZJS4dK74', master_key=None)

print('Beginning')
print(time.asctime( time.localtime(time.time()) ))

def getWordDetails():
    global IDsandDefinitions
    wordIDs = []
    words = []
    nameIDs = {}
    IDsandTest = {}
    IDsandDefinitions = {}
    myClassName = 'Words'
    myClass = Object.factory(myClassName)
    word = myClass.Query.all()
    splitword = str(word).split(':')
    length = len(splitword)
    for k in range (1,length-1):
        line = splitword[k]
        splitword[k] = line[:-9]
        wordIDs.append(splitword[k])
    print('wordIDs FOUND')
    print(time.asctime( time.localtime(time.time()) ))
    wordIDs.append(splitword[length-1][:-2])
    length = len(wordIDs)
    for k in range(0, length):
        word = myClass.Query.get(objectId = wordIDs[k])
        words.append(word.text)
    print('words FOUND')
    print(time.asctime( time.localtime(time.time()) ))
    for k in range(0, length - 1):
        nameIDs[wordIDs[k]] = words[k]
    print('words and wordIDs ASSIGNED')
    print(time.asctime( time.localtime(time.time()) ))
    nameIDs[wordIDs[length-1]] = words[length-1]
    for k in range(0, length - 1):
        testID = myClass.Query.get(objectId = wordIDs[k])
        testID = testID.testID
        IDsandTest[wordIDs[k]] = testID
    print('testID and wordIDs ASSIGNED')
    print(time.asctime( time.localtime(time.time()) ))
    testID = myClass.Query.get(objectId = wordIDs[length-1])
    testID = testID.testID
    IDsandTest[wordIDs[length-1]] = testID[:-2]
    for k in range(0, length - 1):
        definition = myClass.Query.get(objectId = wordIDs[k])
        definition = definition.definition
        IDsandDefinitions[wordIDs[k]] = definition
    print('wordIDs and Definitions ASSIGNED')
    print(time.asctime( time.localtime(time.time()) ))
    definition = myClass.Query.get(objectId = wordIDs[length-1])
    definition = definition.definition
    IDsandDefinitions[wordIDs[length-1]] = definition[:-2]
    print('FUNCTION: getWordDetails COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))
    return wordIDs, words, nameIDs, IDsandTest, IDsandDefinitions

def userLogin():
    global username
    username = usernameEntry.get()
    password = passwordEntry.get()
    print(username, password)
    myClassName = 'User'
    myClass = Object.factory(myClassName)
    userDetails = str(myClass.Query.all())
    username = username.lower()
    if username in userDetails:
        try:
            print('Logging in')
            User.login(username, password)
            print('Logged in')
            currentUserLabel.config(text = 'Logged in as '+username)
            quizSelectButton.config(state = NORMAL)
            outputUserResults()
        except:
            errorLabel.config(text = 'That is an invalid password')
            print('That is an invalid password')
##If teacher or not
        outputUserResults()
    else:
        errorLabel.config(text = 'That is an invalid username')
        print('That is an invalid username')
    print('FUNCTION: userLogin COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))
    
def signUp(names):
    global username
    username = usernameEntry.get()
    password = passwordEntry.get()
    username = username.lower()
    if username in str(names):
        errorLabel.config(text = 'That username is already taken')
        print('That username is already taken')
##Add teacher option
    else:
        teacher = teacherVar.get()
        if teacher == 0:
            u = User.signup(username, password, teacher = False)
            currentUserLabel.config(text = 'Logged in as '+username)
            addUsertoResults()
            quizSelectButton.config(state = NORMAL)
            print('Account created')
        else:
            u = User.signup(username, password, teacher = True)
            currentUserLabel.config(text = 'Logged in as '+username)
            newWordButton.config(state = NORMAL)
            print('Account created')
    print('FUNCTION: signUp COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

def userIDsAndNames():
    names = []
    userIDs = []
    userDetails = {}
    myClassName = 'User'
    myClass = Object.factory(myClassName)
    details = myClass.Query.all()
    splitword = str(details).split(':')
    length = len(splitword)
    for k in range (1,length-1):
        line = splitword[k]
        names.append(line[:-24])
    lastLine = str(splitword[length-1])[:-18]
    names.append(lastLine)
    splitword = str(details).split('Id ')
    length = len(splitword)
    for k in range (1,length-1):
        line = splitword[k].split(')>,')
        userIDs.append(line[0])
    lastLine = str(splitword[length-1])[:-3]
    userIDs.append(lastLine)
    length = len(userIDs)
    for k in range(0,length):
        userDetails[names[k]] = userIDs[k]
    print('FUNCTION: userIDsAndNames COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))
    return userDetails, names, userIDs

def findTest():
    global testIDs, testIDsNames
    testNames = []
    testIDs = []
    testNameIDs = {}
    testIDsNames = {}
    myClassName = 'Tests'
    myClass = Object.factory(myClassName)
    word= myClass.Query.all()
    splitword = str(word).split(':')
    length = len(splitword)
    for k in range (1,length-1):
        line = splitword[k]
        splitword[k] = line[:-9]
        testIDs.append(splitword[k])
    testIDs.append(splitword[length-1][:-2])
    length = len(testIDs)
    for k in range (0, length - 1):
        name = myClass.Query.get(objectId = testIDs[k])
        testNames.append(name.name)
    name = myClass.Query.get(objectId = testIDs[length-1])
    testNames.append(name.name)
    for k in range (0, length):
        testNameIDs[testNames[k]] = testIDs[k]
    for k in range (0, length):
        testIDsNames[testIDs[k]] = testNames[k]
    print(testIDsNames)
    print('FUNCTION: findTest COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))
    return testIDs, testNames

def chooseQuiz(testIDs, testNames):
    global testID, testName
    value = quizList.curselection()
    strip = str(value).strip(',')
    value = int(strip[1])
    testID = testIDs[value]
    testName = testNames[value]
    quizGenerateButton.config(state = NORMAL)
    print('FUNCTION: chooseQuiz COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))
    
def findWordsForTest(testID, IDsandTest, wordIDs, nameIDs, IDsandDefinitions):
    global wordsForTest, wordIDsforTest, score, question
    score = int(0)
    question = int(0)
    IDsandDefinitons = IDsandDefinitions
    length = len(wordIDs)
    wordIDsforTest = []
    wordsForTest = []
    for k in range(0, length):
        wordID = wordIDs[k]
        if IDsandTest[wordID] == testID:
            wordIDsforTest.append(wordIDs[k])
        else:
            bob = 'ross'
    wordID = wordIDs[length-1]
    if IDsandTest[wordID] == testID:
        wordIDsforTest.append(wordIDs[length - 1])
    else:
        bob = 'ross'
    length = len(wordIDsforTest)
    for k in range(0, length ):
        word = nameIDs[wordIDsforTest[k]]
        wordsForTest.append(word)
    word = nameIDs[wordIDsforTest[length-1]]
    wordsForTest.append(word)
    test(wordsForTest, IDsandDefinitons, wordIDsforTest)
    submitButton.config(state = NORMAL)
    print('FUNCTION: findWordsForTest COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

def test(wordsForTest, IDsandDefinitons, wordIDsforTest):
    global word, question
    length = len(wordIDsforTest)
    random = randint(0, length - 1)
    definition = IDsandDefinitions[wordIDsforTest[random]]
    definitionLabel.config(text = definition)
    word = wordsForTest[random]
    wordIDsforTest.remove(wordIDsforTest[random])
    wordsForTest.remove(word)
    question = question + 1
    print('Question: '+str(question))
    print('FUNCTION: test COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

def answer(word, IDsandDefinitons):
    global score, question
    answer = answerEntry.get()
    if answer == word:
        feedbackLabel.config(text = 'That is correct')
        score = score + 2
        print('Score: '+str(score))
        text = 'Score: '+str(score)
        scoreLabel.config(text = text)
    else:
        feedbackLabel.config(text = 'That is wrong, the correct answer was '+word)
    if question <10:
        test(wordsForTest, IDsandDefinitons, wordIDsforTest)
    else:
        feedbackLabel.config(text = 'Test complete. You scored '+word)
        print('Test Finished')
        submitButton.config(state = DISABLED)
        saveHistory()
        updateResults()
        outputUserResults()
    print('FUNCTION: answer COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

def saveHistory():
    global score, username, testID
    result = History(userName = username, testID = testID, score = score)
    result.save()
    print('FUNCTION saveReult COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))
    
def addUsertoResults():
    global username, testIDs
    length = len(testIDs)
    for k in range (0, length - 1):
        testID = testIDs[k]
        newobject = Results(userName = username, testID = testID, attempts = int(0), average = int(0))
        newobject.save()
    testID = testIDs[length - 1]
    newobject = Results(userName = username, testID = testID, attempts = int(0), average = int(0))
    print('FUNCTION addUSertoRestults COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

def getResultIDs():
    global resultIDs
    resultIDs =[]
    myClassName = 'Results'
    myClass = Object.factory(myClassName)
    returned = str(myClass.Query.all())
    splited = returned.split('Results:')
    length = len(splited)
    for k in range(0, length-1):
        resultIDs.append(splited[k][:-4])
    resultIDs.append(splited[length - 1][:-2])
    print('FUNCTION getRestultIDs COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

def updateResults():
     global resultIDs, username, score, testID
     length = len(resultIDs)
     run = 1
     myClassName = 'Results'
     myClass = Object.factory(myClassName)
     while run == 1:
         for k in range(1,length):
            obj = myClass.Query.get(objectId = resultIDs[k])
            user = obj.userName
            test = obj.testID
            if user == username and test == testID:
                attempts = obj.attempts
                average = obj.average
                total = attempts*average
                attempts = attempts + 1
                average = (total + score)/attempts
                print('Attempts:'+str(attempts),'Average:'+str(average))
                obj.average = average
                obj.attempts = attempts
                obj.save()
                print('Saved')
                run = 0

def outputUserResults():
    global username, resultIDs, testIDsNames
    myClassName = 'Results'
    myClass = Object.factory(myClassName)
    results = []
    length = len(resultIDs)
    for k in range(1, length):
        obj = myClass.Query.get(objectId = resultIDs[k])
        user = obj.userName
        if user == username:
            testID = obj.testID
            average = obj.average
            attempts = obj.attempts
            testName = testIDsNames[testID]
            string = (str(testName)+': Average = '+str(average)+'; Attempts = '+str(attempts))
            results.append(string)
    print('Results collected')
    resultsList.delete(0, END)
    length = len(results)
    for k in range(0, length):
        resultsList.insert(k+1, results[k])
    print('FUNCTION outputUserResults COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))


def funButton():
    global teacherVar
    print(teacherVar.get())
    print('FUNCTION: funButton COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

wordIDs, words, nameIDs, IDsandTest, IDsandDefinitions = getWordDetails()
testIDs, testNames = findTest()
userDetails, names, userIDs = userIDsAndNames()
getResultIDs()

class Results(Object):
    pass

class History(Object):
    pass

class Words(Object):
    pass

base = Tk()
base.geometry('600x600+0+0')
base.title('Spelling bee')

print('Base DECLARED')

global teacherVar
teacherVar = IntVar()

titleLabel = Label(text='Welcome to the Speeling Bee')
buttonLogin = Button(text='Login', fg = 'blue', command = userLogin)
buttonSignUp = Button(text='Sign up', command = lambda: signUp(names))
usernameLabel = Label(text = 'Username:')
passwordLabel = Label(text = 'Password:')
usernameEntry = Entry()
passwordEntry = Entry(show = '*')
errorLabel = Label()
teacherCheckBox = Checkbutton(text = 'Teacher', variable = teacherVar, onvalue = 1, offvalue = 0)
currentUserLabel = Label()

print('Membership modules DECLARED')

titleLabel.grid(row = 0, column = 3)
usernameLabel.grid(row = 1, column = 0)
usernameEntry.grid(row = 1, column = 1)
passwordLabel.grid(row = 2, column = 0)
passwordEntry.grid(row = 2, column = 1)
buttonLogin.grid(row = 1, column = 2)
buttonSignUp.grid(row = 2, column = 2)
errorLabel.grid(row = 4, column = 0)
teacherCheckBox.grid(row = 3, column = 0)
currentUserLabel.grid(row = 0, column = 1)

print('Membership modules POSITIONED')

quizList = Listbox(selectmode = SINGLE)
quizSelectButton = Button(text = 'Choose Quiz', state = DISABLED, command = lambda: chooseQuiz(testIDs, testNames))
quizGenerateButton = Button(text = 'Generate Quiz',state = DISABLED, command = lambda: findWordsForTest(testID, IDsandTest, wordIDs, nameIDs, IDsandDefinitions))
definitionLabel =Label(width = 50)
answerEntry = Entry()
submitButton = Button(text = 'Submit',state = DISABLED, command = lambda: answer(word, IDsandDefinitions))
scoreLabel = Label(text = 'Score: 0')
feedbackLabel = Label()
resultsList = Listbox(selectmode = SINGLE, width = 40)

print('Quiz modules DECLARED')

length = len(testNames)
for k in range(0, length):
    quizList.insert(k+1, testNames[k])

quizGenerateButton.grid(row = 6, column = 1)
quizList.grid(row = 5, column = 0)
quizSelectButton.grid(row = 6, column = 0)
definitionLabel.grid(row = 7, column = 3)
feedbackLabel.grid(row = 7, column = 4)
answerEntry.grid(row = 8, column = 3)
submitButton.grid(row = 9, column = 3)
scoreLabel.grid(row = 8, column = 4)
resultsList.grid(row = 1, column = 4)

print('Quiz modules POSITIONED')

newWordEntry = Entry()
newWordDefinitionEntry = Entry()
newWordQuizEntry = Entry()
newWordLabel1 = Label(text = 'Add a new word:')
newWordLabel2 = Label(text = 'Word:')
newWordLabel3 = Label(text = 'Definition:')
newWordLabel4 = Label(text = 'Quiz:')
newWordButton = Button(text = 'Add Word', command = addWord(), state = DISABLED)

print('Teacher modules DECLARED')

newWordEntry.grid(row = 3, column = 5)
newWordDefinitionEntry.grid(row = 4, column = 5)
newWordQuizEntry.grid(row = 5, column = 5)
newWordLabel1.grid(row = 2, column = 5)
newWordLabel2.grid(row = 3, column = 4)
newWordLabel3.grid(row = 4, column = 4)
newWordLabel4.grid(row = 5, column = 4)
newWordButton.grid(row = 6, column = 5)

print('Teacher modules POSITIONED')

funButton = Button(text = 'Test', command = funButton)
funButton.grid(row=10, column = 0)

print('fun button DECLARED and POSITIONED')

print('base window LOADED')
print(time.asctime( time.localtime(time.time()) ))
base.mainloop()
