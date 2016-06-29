from flask import Flask
from flask import render_template
from flask import request
from TurkeyCon import getAllbyName, sqlExec, getAllbyLast_F, getAllbyFirst_F, getAllbyLast, getAllbyFirst

# def getAllbyName(firstName, lastName, fuzzyQuery, pageNum):
#     listTemp = [1, 0]
#     return listTemp

app = Flask(__name__)

@app.route('/')
@app.route('/search/')
def search():
    return render_template('search.html', pageNum=0, )

@app.route('/test/')
def test():
    return render_template("test.html")

@app.route('/result/', methods=['POST', 'GET'])
def doForm():
    firstName = ""
    lastName = ""
    sqlStr = ""
    fuzzyQuery = False
    pageNum = 0
    # count = 0
    # turkeyList = []
    if request.method == 'POST':
        pageNum = int(request.form['PageNum'])
        try:
            sqlStr = str(request.form['SqlStr'])
        except Exception:
            sqlStr = ""
        if request.form['FuzzyQuery'] == "True":
            fuzzyQuery = True
            # sqlStr = str(request.form['SqlStr'])
            if sqlStr == "":
                errorStr = "Please input the Sql sentence."
                return render_template('error.html', errorStr=errorStr)
        else:
            fuzzyQuery = False
            print fuzzyQuery
            # if request.form['FirstName'] != "":
            firstName = str(request.form['FirstName']).strip().upper()
            print firstName
            # if request.form['LastName'] != "":
            lastName = str(request.form['LastName']).strip().upper()
            print lastName
    if firstName is "" and lastName is "" and sqlStr is not "":
        fuzzyQuery = True
    if fuzzyQuery is True:
        turkeyList = doFuzzy(sqlStr, pageNum, fuzzyQuery)
        if type(turkeyList) is list:
            count = len(turkeyList)
            if count == 0:
                errorStr = "We have no idea about this person."
                return render_template('error.html', errorStr=errorStr)
            else:
                return render_template('result_sql.html',
                                       turkeyList=turkeyList,
                                       sqlStr=sqlStr,
                                       pageNum=pageNum,
                                       count=count,
                                       fuzzyQuery=fuzzyQuery)
        # elif turkeyList is None:
        #     errorStr = "We have no idea about this person1."
        #     return render_template('error.html', errorStr=errorStr)
        # elif turkeyList is Exception:
        elif type(turkeyList) is not list:
            errorStr = str(turkeyList)
            return render_template('error.html', errorStr=errorStr)
    else:
        if firstName == "" and lastName == "":
            errorStr = "Please input FirstName or LastName."
            return render_template('error.html', errorStr=errorStr)
        turkeyList = doExact(firstName, lastName, fuzzyQuery, pageNum)
        count = turkeyList.pop()
        if count == 0:
            errorStr = "We have no idea about this person."
            return render_template('error.html', errorStr=errorStr)
        else:
            return render_template('result.html',
                                   firstName=firstName,
                                   lastName=lastName,
                                   fuzzyQuery=fuzzyQuery,
                                   pageNum=pageNum,
                                   count=count,
                                   turkeyList=turkeyList)


def doFuzzy(sqlStr="", pageNum=0, fuzzyQuery=True):
    sqlStr += " limit 50 OFFSET %s" % (pageNum * 50)
    turkeyList = sqlExec(sqlStr)
    return turkeyList
    # if turkeyList is list:
    #     return render_template('result_sql.html', sqlStr=sqlStr, pageNum=pageNum, fuzzyQuery=fuzzyQuery)
    # else:
    #     errorStr = str(turkeyList)
    #     return render_template('error.html', errorStr=errorStr)


def doExact(firstName="", lastName="", fuzzyQuery=False, pageNum=0):
    if firstName != "" and lastName == "":
        turkeyList = getAllbyFirst(firstName, pageNum)
    elif firstName == "" and lastName != "":
        turkeyList = getAllbyLast(lastName, pageNum)
    elif firstName != "" and lastName != "":
        turkeyList = getAllbyName(firstName, lastName, fuzzyQuery, pageNum)
    return turkeyList
    # count = turkeyList.pop()
    # if count == 0:
    #     errorStr = "We have no idea about this person."
    #     return render_template('error.html', errorStr=errorStr)
    # else:
    #     turkeyList = getAllbyName(firstName, lastName, fuzzyQuery, pageNum)
    #     return render_template('result.html',
    #                            firstName=firstName,
    #                            lastName=lastName,
    #                            fuzzyQuery=fuzzyQuery,
    #                            pageNum=pageNum,
    #                            count=count,
    #                            turkeyList=turkeyList)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
