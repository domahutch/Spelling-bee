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
    definition = myClass.Query.get(objectId = wordIDs[length-1])
    definition = definition.definition
    print('wordIDs and Definitions ASSIGNED')
    print(time.asctime( time.localtime(time.time()) ))
    IDsandDefinitions[wordIDs[length-1]] = definition[:-2]
    print('FUNCTION: getWordDetails COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))
    return wordIDs, words, nameIDs, IDsandTest, IDsandDefinitions

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
        errorLabel.config(text = 'That is an invalid username')
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
        errorLabel.config(text = 'That username is already taken')
        print('That username is already taken')
    else:
        teacher = teacherVar.get()
        if teacher == 0:
            u = User.signup(username, password, teacher = False, group = group)
            currentUserLabel.config(text = 'Logged in as '+username)
            addUsertoResults()
            outputUserResults()
            newWordButton.config(state = DISABLED)
            quizSelectButton.config(state = NORMAL)
            print('Account created')
        else:
            u = User.signup(username, password, teacher = True, group = group)
            currentUserLabel.config(text = 'Logged in as '+username)
            newWordButton.config(state = NORMAL)
            quizSelectButton.config(state = DISABLED)
            resultsList.delete(0, END)
            print('Account created')
    print('FUNCTION: signUp COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))

def userIDsAndNames():
    global userIDtoName, userIDs, userDetails
    names = []
    userIDs = []
    userDetails = {}
    userIDtoName = {}
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
        userIDtoName[userIDs[k]] = names[k]
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
    print('FUNCTION: findTest COMPLETE')
    print(time.asctime( time.localtime(time.time()) ))
    return testIDs, testNames, testNameIDs

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
        feedbackLabel.config(text = 'Test complete. You scored '+score)
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
        errorLabel.config(text = 'That quiz does not exist')
    else:
        quizID = testNameIDs[quiz]
        if word in words:
            errorLabel.config(text = 'That word is already in the list')
        else:
            newobject = Words(text = word, definition = definition, testID = quizID)
            newobject.save()
            errorLabel.config(text = 'Word has been added to database')
            print('Word Added')
    print('FUNCTION addWord COMPLETE')

def classDetails(userIDs):
    global userIDClass
    classNames = []
    userIDClass = {}
    ClassUserId = {}
    length = len(userIDs)
    myClassName = 'User'
    myClass = Object.factory(myClassName)
    for k in range(0, length):
        Id = userIDs[k]
        data = myClass.Query.get(objectId = Id)
        group = data.group
        userIDClass[Id] = group
        if group in classNames:
            pass
        else:
            classNames.append(group)
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

wordIDs, words, nameIDs, IDsandTest, IDsandDefinitions = getWordDetails()
testIDs, testNames, testNameIDs = findTest()
userDetails, names, userIDs = userIDsAndNames()
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

print('Base DECLARED')

global teacherVar
teacherVar = IntVar()

classLength = len(classNames)

titleLabel = Label(text='Welcome to the Speeling Bee')
buttonLogin = Button(text='Login', fg = 'blue', command = lambda: userLogin(userIDClass))
buttonSignUp = Button(text='Sign up', command = lambda: signUp(names, classNames))
usernameLabel = Label(text = 'Username:')
passwordLabel = Label(text = 'Password:')
usernameEntry = Entry()
passwordEntry = Entry(show = '*')
errorLabel = Label()
teacherCheckBox = Checkbutton(text = 'Teacher', variable = teacherVar, onvalue = 1, offvalue = 0)
currentUserLabel = Label()
classBox = Listbox(selectmode = SINGLE, height = classLength)

length = len(classNames)
for k in range(0, length):
    classBox.insert(k+1, classNames[k])

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
classBox.grid(row = 1, column = 3)

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
resultTitleLabel = Label(text = 'Results')

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
resultTitleLabel.grid(row = 0, column = 4)

print('Quiz modules POSITIONED')

newWordEntry = Entry()
newWordDefinitionEntry = Entry()
newWordQuizEntry = Entry()
newWordLabel1 = Label(text = 'Add a new word:')
newWordLabel2 = Label(text = 'Word:')
newWordLabel3 = Label(text = 'Definition:')
newWordLabel4 = Label(text = 'Quiz:')
newWordButton = Button(text = 'Add Word',state = DISABLED, command = lambda: addWord(words, testNames, testNameIDs))
classPupilsList = Listbox(selectmode = SINGLE)
pupilSelectButton = Button(text = 'Choose a pupil.', command = lambda: pupilResultsToTeacher(sameGroupID))
pupilResultsList = Listbox(selectmode = SINGLE)
resultSelectButton = Button(text = 'Choose a result.', command = lambda: historyToTeacher())
historyList = Listbox(selectmode = SINGLE)

print('Teacher modules DECLARED')

newWordEntry.grid(row = 3, column = 5)
newWordDefinitionEntry.grid(row = 4, column = 5)
newWordQuizEntry.grid(row = 5, column = 5)
newWordLabel1.grid(row = 2, column = 5)
newWordLabel2.grid(row = 3, column = 4)
newWordLabel3.grid(row = 4, column = 4)
newWordLabel4.grid(row = 5, column = 4)
newWordButton.grid(row = 6, column = 5)
classPupilsList.grid(row = 5, column = 6)
pupilSelectButton.grid(row = 5, column = 7)
pupilResultsList.grid(row = 6, column = 6)
resultSelectButton.grid(row = 6, column = 7)
historyList.grid(row = 7, column =6)


print('Teacher modules POSITIONED')

funButton = Button(text = 'Test', command = funButton)
funButton.grid(row=10, column = 0)

print('fun button DECLARED and POSITIONED')

print('base window LOADED')
print(time.asctime( time.localtime(time.time()) ))
base.mainloop()
