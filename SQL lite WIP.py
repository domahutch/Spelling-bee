from tkinter import *
from parse_rest.connection import register, SessionToken
from parse_rest.user import User
from parse_rest.datatypes import Object
from random import randint
import time
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()


##A fun comment

register('pTTzpgrZvewsfdyceO8uGvTLoS4oD3TU0aeoY6En', 'wezDsrAFbbuu7nHbwvFUXDNeJdzLLGdBZJS4dK74', master_key=None)

print('Beginning')
print(time.asctime( time.localtime(time.time()) ))

def getWordDetails():
    global IDsandDefinitions
    wordIDs = []
    words = []
    testIDs = []
    definitions = []
    wordAndIDs = {}
    IDsandTest = {}
    IDsandDefinitions = {}
    sql = 'SELECT * FROM words'
    for k in c.execute(sql):
        wordIDs.append(k[0])
        words.append(k[1])
        definitions.append(k[2])
        testIDs.append(k[3])
    length = len(words)
    for k in range (0, length):
        wordAndIDs[wordIDs[k]] = words[k]
        IDsandTest[wordIDs[k]] = testIDs[k]
        IDsandDefinitions[wordIDs[k]] = definitions[k]
    return(wordIDs, words, testIDs, definitions, wordAndIDs, IDsandTest, IDsandDefinitions)

def userLogin(userIDClass):
    global username, userDetails
    username = usernameEntry.get()
    password = passwordEntry.get()
    myClassName = 'User'
    myClass = Object.factory(myClassName)
    username = str(username.lower())
    Id = userDetails[username]
    print(Id)
    data = myClass.Query.get(objectId = Id)
    teacher = data.teacher
    print(teacher)
    if username in userDetails:
        print('Logging in')
        try:
            User.login(username, password)
            print('Logged in')
            currentUserLabel.config(text = 'Logged in as '+username+'. Class: '+userIDClass[Id])
            if teacher == False:
                outputUserResults()
                newWordButton.config(state = DISABLED)
                quizSelectButton.config(state = NORMAL)
            else:
                newWordButton.config(state = NORMAL)
                quizSelectButton.config(state = DISABLED)
                resultsList.delete(0, END)
                findTeachersPupils(Id)
        except:
            print('Incorrect password')
            currentUserLabel.config(text = 'Incorrect password')
    else:
        currentUserLabel.config(text = 'That is an invalid username')
        print('That is an invalid username')
    print('FUNCTION: userLogin COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))
    
def signUp(names, classNames):
    global username
    username = usernameEntry.get()
    password = passwordEntry.get()
    username = username.lower()
    value = classBox.curselection()
    strip = str(value).strip(',')
    value = int(strip[1])
    group = classNames[value]
    if username in str(names):
        currentUserLabel.config(text = 'That username is already taken')
        print('That username is already taken')
    else:
        teacher = teacherVar.get()
        if teacher == 0:
            c.execute('INSERT INTO users(username, password, class, teacher) VALUES (?,?,?,?)',(username, password, group, False))
            currentUserLabel.config(text = 'Logged in as '+username)
##            addUsertoResults()
##            outputUserResults()
            newWordButton.config(state = DISABLED)
            quizSelectButton.config(state = NORMAL)
            print('Account Created')
            conn.commit()
        else:
            c.execute('INSERT INTO users(username, password, class, teacher) VALUES (?,?,?,?)',(username, password, group, True))
            currentUserLabel.config(text = 'Logged in as '+username)
            newWordButton.config(state = NORMAL)
            quizSelectButton.config(state = DISABLED)
            resultsList.delete(0, END)
            print('Account Created')
            conn.commit()

def userIDsAndNames():
    global userIDtoName, userIDs, userDetails
    names = []
    userIDs = []
    userDetails = {}
    userIDtoName = {}
    sql = 'SELECT * FROM users'
    for k in c.execute(sql):
        names.append(k[1])
        userIDs.append(k[0])
    length = len(names)
    for k in range(0, length):
        userDetails[names[k]] = userIDs[k]
        userIDtoName[userIDs[k]] = names[k]
    return(names, userIDs, userDetails, userIDtoName)

def findTest():
    testNames =[]
    testIDs = []
    testNameIDs = {}
    testIDsNames = {}
    sql = 'SELECT * FROM tests'
    for k in c.execute(sql):
        testNames.append(k[1])
        testIDs.append(k[0])
    length = len(testNames)
    for k in range(0, length):
        testNameIDs[testNames[k]] = testIDs[k]
        testIDsNames[testIDs[k]] = testNames[k]
    return(testNames, testIDs, testNameIDs, testIDsNames)

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

def spellCheck(word, correct):
    lengthWord = len(word)
    lengthCorrect = len(correct)
    difference = lengthWord - lengthCorrect
    if difference == 0:
        length = lengthWord
    elif difference > 0:
        length = lengthAnswer
        difference = lengthWord - lengthCorrect
    else:
        length = lengthWord
        difference = lengthCorrect - lengthWord
    incorrect = difference
    for k in range(0, length):
        if word[k] == correct[k]:
            pass
        else:
            incorrect = incorrect + 1
    if incorrect > 1:
        returning = 'WRONG'
    elif incorrect == 1:
        returning = 'ALMOST'
    else:
        returning = 'CORRECT'
    return returning
    print('FUNCTION spellCheck COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

def answer(word, IDsandDefinitons):
    global score, question
    answer = answerEntry.get()
    state = spellCheck(answer, word)
    if state == 'CORRECT':
        feedbackLabel.config(text = 'That is correct')
        score = score + 2
        print('Score: '+str(score))
        text = 'Score: '+str(score)
        scoreLabel.config(text = text)
    elif state == 'ALMOST':
        feedbackLabel.config(text = 'That is almost correct, the correct answer was '+word)
        score = score + 1
        print('Score: '+ str(score))
        text = 'Score: '+str(score)
        scoreLabel.config(text = text)
    else:
        feedbackLabel.config(text = 'That is wrong, the correct answer was '+word)
    if question <10:
        test(wordsForTest, IDsandDefinitons, wordIDsforTest)
    else:
        feedbackLabel.config(text = 'Test complete. You scored '+str(score))
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
            average = '%.1f' % average
            attempts = obj.attempts
            testName = testIDsNames[testID]
            string = (str(testName)+': Average = '+str(average)+'; Attempts = '+str(attempts))
            results.append(string)
    print('Results collected')
    resultsList.delete(0, END)
    length = len(results)
    for k in range(0, length):
        resultsList.insert(k+1, results[k])
    length = len(results)
    resultsList.config(height = length)
    print('FUNCTION outputUserResults COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

def addWord(words, testNames, testNameIDs):
    word = newWordEntry.get()
    definition = newWordDefinitionEntry.get()
    quiz = newWordQuizEntry.get()
    if quiz not in testNames:
        currentUserLabel.config(text = 'That quiz does not exist')
    else:
        quizID = testNameIDs[quiz]
        if word in words:
            currentUserLabel.config(text = 'That word is already in the list')
        else:
            newobject = Words(text = word, definition = definition, testID = quizID)
            newobject.save()
            currentUserLabel.config(text = 'Word has been added to database')
            print('Word Added')
    print('FUNCTION addWord COMPLETE')

def classDetails(userIDs):
    global userIDClass
    classNames = []
    group = []
    userIDClass = {}
    ClassUserID = {}
    length = len(userIDs)
    sql = 'SELECT * FROM users'
    for k in c.execute(sql):
        group.append(k[3])
    print(group)
    for k in range(0, length):
        Id = userIDs[k]
        userIDClass[Id] = group[k]
        if group[k] in classNames:
            pass
        else:
            classNames.append(group[k])
    return classNames, userIDClass

def findTeachersPupils(Id):
    global userIDtoName, userIDs, sameGroupID
    sameGroupID = []
    group = userIDClass[Id]
    length = len(userIDClass)
    teacherGroup = userIDClass[Id]
    for k in range (0, length):
        userID = userIDs[k]
        if userID == Id:
            pass
        else:
            pupilGroup = userIDClass[userID]
            if pupilGroup == teacherGroup:
                sameGroupID.append(userID)
    classPupilsList.delete(0, END)
    length = len(sameGroupID)
    for k in range(0, length):
        classPupilsList.insert(k+1, userIDtoName[sameGroupID[k]])

def pupilResultsToTeacher(sameGroupID):
    global resultIDs, testIDsNames, userDetails, userIDtoName, results, pupilUserName
    results = []
    value = str(classPupilsList.curselection())
    strip = value.strip(',')
    value = int(strip[1])
    pupilID = sameGroupID[value]
    pupilName = userIDtoName[pupilID]
    pupilUserName = pupilName
    myClassName = 'Results'
    myClass = Object.factory(myClassName)
    length = len(resultIDs)
    for k in range(1, length):
        obj = myClass.Query.get(objectId = resultIDs[k])
        user = obj.userName
        if user == pupilName:
            testID = obj.testID
            average = obj.average
            average = '%.1f' % average
            attempts = obj.attempts
            testName = testIDsNames[testID]
            string = (str(testName)+': Average = '+str(average)+'; Attempts = '+str(attempts))
            results.append(string)
    print('Results collected')
    print(results)
    pupilResultsList.delete(0, END)
    length = len(results)
    for k in range(0, length):
        pupilResultsList.insert(k+1, results[k])

def historyToTeacher():
    global results, testNameIDs, pupilUserName

    user = pupilUserName
    historyIDs = []
    outputList = []

    value = str(pupilResultsList.curselection())
    strip = value.strip(',')
    value = int(strip[1])
    line = results[value]
    strip = line.split(': Average')
    testname = strip[0]
    testID = testNameIDs[testname]

    myClassName = 'History'
    myClass = Object.factory(myClassName)
    output = myClass.Query.all()
    print(output)
    length = len(output)
    print(length)

    for k in range(0, length):
        strip = str(output[k]).strip('<>')
        split = strip.split(':')
        historyIDs.append(split[1])
        print(split[1])

    for k in range(0, length):
        result = myClass.Query.get(objectId = historyIDs[k])
        historyUsername = result.userName
        historyTestID = result.testID
        if historyUsername == pupilUserName and historyTestID == testID:
            date = result.createdAt
            date = str(date)[:10]
            score = result.score
            string = (str(date)+': scored '+str(score))
            outputList.append(string)
        else:
            pass

    historyList.delete(0, END)
    length = len(outputList)
    for k in range(0, length):
        historyList.insert(k+1, outputList[k])

def funButton():
    global teacherVar
    print(teacherVar.get())
    print('FUNCTION: funButton COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

wordIDs, words, testIDs, definitions, wordAndIDs, IDsandTest, IDsandDefinitions = getWordDetails()
testNames, testIDs, testNameIDs, testIDsNames = findTest()
names, userIDs, userDetails, userIDtoName = userIDsAndNames()
classNames, userIDClass= classDetails(userIDs)
getResultIDs()

class Results(Object):
    pass

class History(Object):
    pass

class Words(Object):
    pass

base = Tk()
base.title('Spelling bee')
base.geometry("650x600")

print('Base DECLARED')

global teacherVar
teacherVar = IntVar()

classLength = len(classNames)

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
for k in range(0, length):
    classBox.insert(k+1, classNames[k])

print('Membership modules DECLARED')

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

quizBorder = Label(heigh = 9, width = 52, relief = SUNKEN)
quizList = Listbox(selectmode = SINGLE, heigh = 5, width = 15)
quizSelectButton = Button(text = 'Choose Quiz', state = DISABLED, command = lambda: chooseQuiz(testIDs, testNames),width = 12)
quizGenerateButton = Button(text = 'Generate Quiz',state = DISABLED, command = lambda: findWordsForTest(testID, IDsandTest, wordIDs, nameIDs, IDsandDefinitions),width = 12)
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
for k in range(0, length):
    quizList.insert(k+1, testNames[k])

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

teacherBorder = Label(height = 22, width = 55, relief = SUNKEN)
newWordEntry = Entry()
newWordDefinitionEntry = Entry()
newWordQuizEntry = Entry()
newWordLabel1 = Label(text = 'Add a new word:')
newWordLabel2 = Label(text = 'Word:')
newWordLabel3 = Label(text = 'Definition:')
newWordLabel4 = Label(text = 'Quiz:')
newWordButton = Button(text = 'Add Word',state = DISABLED, command = lambda: addWord(words, testNames, testNameIDs),width = 15)
classPupilsList = Listbox(selectmode = SINGLE)
pupilSelectButton = Button(text = 'Choose a pupil.', command = lambda: pupilResultsToTeacher(sameGroupID))
pupilResultsList = Listbox(selectmode = SINGLE)
resultSelectButton = Button(text = 'Choose a result.', command = lambda: historyToTeacher())
historyList = Listbox(selectmode = SINGLE)
pupilLabel = Label(text = 'Pupils')
pupilResultsLabel = Label(text = 'Results')
historyLabel = Label(text = 'History')

print('Teacher modules DECLARED')

teacherBorder.place(x=0, y =262)
newWordEntry.place(x=50, y = 287)
newWordDefinitionEntry.place(x=50, y = 310)
newWordQuizEntry.place(x=50, y = 333)
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
print(time.asctime( time.localtime(time.time()) ))
base.mainloop()
