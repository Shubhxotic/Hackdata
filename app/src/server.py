from flask import Flask,jsonify, request,redirect,url_for,render_template,flash, session, logging
import requests
import json
from wtforms import *
from passlib.hash import sha256_crypt
from functools import wraps	
from bs4 import BeautifulSoup
import random,os,sys
import config
import gspread, pprint, random
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key="7dehi7h3di6teyliws8oud3ehd"
data_url = None
auth_url= None
headers = {
    'Content-Type': 'application/json'
}
data_url = "https://data.boon34.hasura-app.io/"
auth_url = 'https://auth.boon34.hasura-app.io/'

# data_url="http://data.hasura"

query_url = data_url + '/v1/query'
print("Config.Development=====",config.DEVELOPMENT)
print("config.PROJECT_NAME=====",config.PROJECT_NAME)

class RegistrationForm(Form):
    name=StringField('Name',[validators.Length(min=1 ,max=50)])
    username=StringField('Username',[validators.Length(min=4,max=25)])
    email=StringField('email',[validators.Length(min=6,max=50)])
    #mobile=StringField('Mobile',[validators.Length(min=6, max=15)])
    password=PasswordField('Password',[
            validators.DataRequired(),
            validators.Length(min=8,max=15),
            validators.EqualTo('confirm',message="Password should match Confirm Password")
        ])
    confirm=PasswordField('Confirm',[validators.Length(min=8,max=15)])

class ForgotForm(Form):
    email=StringField('Email',[validators.Length(min=4)])


class LoginForm(Form):
    username=StringField('Username',[validators.Length(min=4,max=25)])
    password=PasswordField('Password',[
            validators.DataRequired(),
            validators.Length(min=8,max=15),
        ])


def ripOff(s):
    while not s[0].isalnum():
        s=s[1:]
    while not s[-1].isalnum():
        s=s[:-2]
    return s.strip().lower()


def ripOff2(s):
    while not s[0].isalnum():
        s=s[1:]
    while not s[-1].isalnum():
        s=s[:-1]
    return s.strip()

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and auth_token in session and 'Authorization' in headers:
            return f(*args, **kwargs)
        else:
            flash("Unauthorised, Please Login", 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route("/")
def hello():
    # scope = ['https://spreadsheets.google.com/feeds']
    # creds = ServiceAccountCredentials.from_json_keyfile_name('/home/shubham/Downloads/client_secret.json', scope)
    # client = gspread.authorize(creds)
    # # print(client.open('Final Allocation list.xlsx').worksheets())
    # sheet = client.open('Final Allocation list.xlsx').worksheet('Sheet2')
    #
    # pp = pprint.PrettyPrinter()
    # res=sheet.get_all_records()
    # # res=sheet.col_values(6)
    # # # res=sheet.row_values(16)
    # # res=sheet.cell(16,1).value
    # # # res=sheet.cell(1197,2).value
    # print("res==\n",res)
    # l=102
    # for i in res.split(','):
    #     x=[]
    #     x.append(i)
    #     print(x)
    #     sheet.insert_row(x,l)
    #     l+=1
    #     print(l)
    # x=0
    # for i in res:
    #     query_url = data_url + '/v1/query'
    #     query = {
    #         "type": "insert",
    #         "args": {
    #             "table": "QandA",
    #             "objects": [{
    #                 "Disease": i['Disease'],
    #                 "Cause": i['Cause'],
    #                 "Question": i['Question'],
    #             }]
    #         }
    #     }
    #     print(query_url, query)
    #     r = requests.post(query_url, data=json.dumps(query), headers=headers)
    #     if r.status_code == 200:
    #         print("r=======", r.json())
    #         # return redirect(url_for('login'))
    #     else:
    #         return json.dumps(r.json(), indent=2)

        # x+=1
        # print("Row ",x,"=> ",res[i])
        # print("The symptoms for ",res[i]['Disease']," are:- ")
        # for j in res[i]['Symptom'].split(','):
        #     print(j)
    # res = sheet.row_values(1)
    # print(res)


    # query = {"type": "select",
    #          "args": {
    #              "table": "Disease",
    #              "columns": ["*"],
    #             }
    #          }
    # print(query)
    # print(query_url)
    # print(headers)
    # r = requests.post(query_url, data=json.dumps(query), headers=headers).json()
    # print("r=====", r)
    query_url = data_url + '/v1/query'
    symp = []
    query = {"type": "select",
             "args": {
                 "table": "Symptoms",
                 "columns": ["symptom"],
             }}
    print(query)
    r = requests.post(query_url, data=json.dumps(query), headers=headers)
    print("r=======", r, "\n", r.json())
    if r.status_code == 200 and len(r.json()) > 0:
        # print("successfully retrieved some questions")
        for i in r.json():
            symp.append(i['symptom'].lower())
        # questions = list(questions)
        symp.sort()
        print(symp)
    else:
        return "<h1>Match not found</h1>"

    # symptom = x['Search'][0]
    query = {"type": "select",
             "args": {
                 "table": "Disease",
                 "columns": ["*"],
             }
             }
    print(query)
    r = requests.post(query_url, data=json.dumps(query), headers=headers)
    print("r=======", r, "\n", r.json())
    # ProbableDiseases = []
    # for i in r.json():
    #     if (symptom.lower() in str(i['symptom']).lower()):
    #         ProbableDiseases.append(i['disease'])
    #
    # print("Probable disease are:- ", ProbableDiseases)
    #
    # ques = []
    # dis = []
    # for i in ProbableDiseases:
    #     query = {"type": "select",
    #              "args": {
    #                  "table": "QandA",
    #                  "columns": ["*"],
    #              }
    #              }
    #     print(query)
    #     questions = requests.post(query_url, data=json.dumps(query), headers=headers)
    #     print("r=======", r, "\n", r.json())
    #     ques.append(questions['Question'])
    #     dis.append(questions['Disease'])
    return render_template('index.html',  len=len )
    # return render_template("index.html")
    # return json.dumps({"message":"Hello World!"})


@app.route("/login", methods=['GET', 'POST'])
def login():
    print("Config.Development=====", config.DEVELOPMENT)
    print("This is login endpoint")
    print(headers)
    try:
        if ('Authorization') in headers.keys():
            headers.pop('Authorization')
        session.clear()
    except Exception as e:
        print("error=", e)

    form = LoginForm(request.form)
    if request.method == 'POST':
        query_url = auth_url + '/login'
        username = request.form['username']
        password = request.form['password']
        ps = form.password.data
        print(ps)
        query = {'username': username, "password": password}
        try:
            print(query)
            print(query_url)
            print(headers)
            # Set the headers to correct  values
            r = requests.post(query_url, data=json.dumps(query), headers=headers).json()
            print("r inside try=====", r)
            if (r['auth_token']):
                session['logged_in'] = True
                session['auth_token'] = r['auth_token']
                session['hasura_id'] = r['hasura_id']
                session['username'] = username
                headers['Authorization'] = 'Bearer ' + session['auth_token']
                query = {
                    "type": "update", "args": {
                        "table": "profile",
                        "$set": {"id": session['hasura_id']},
                        "where": {"username": username},
                        "returning": ["id"]
                    }
                }
                query_url = data_url + '/v1/query'
                print(query)
                print(headers)
                print(query_url)
                r = requests.post(query_url, data=json.dumps(query), headers=headers)
                print("r=======", r)
                if r.status_code != 200:
                    print("Not Found PP")
                else:
                    r = r.json()
            else:
                return jsonify(r)
            print("Redirecting...")
        except Exception as e:
            print(e)
            incor = True
            flash("Invalid Credentials", "warning")
            return redirect(url_for('login', incor="True"))
        print("Sessions====", session)
        return redirect(url_for('home'))
    # render_template('home.html')
    print("FORM FOR LOGIN ENDPOINT IS ", form)
    return render_template('login.html', form=form, endpoint="login")


# return "You have logged in successfully"

# @app.route('/predDis', methods=["POST"])
# def PredDis():
#


@app.route('/search', methods=["POST"])
def search():
    print(request.form)
    print(type(request.form))
    x = dict(request.form)
    print("\n\n\nx=======",x)
    query_url = data_url + '/v1/query'
    symp = []
    query = {"type": "select",
             "args": {
        "table": "Symptoms",
        "columns": ["symptom"],
    }}
    print(query)
    r = requests.post(query_url, data=json.dumps(query), headers=headers)
    print("r=======", r, "\n", r.json())
    if r.status_code == 200 and len(r.json()) > 0:
        # print("successfully retrieved some questions")
        for i in r.json():
            symp.append(i['symptom'].lower())
        # questions = list(questions)
        symp.sort()
        print(symp)
    else:
        return "<h1>Match not found</h1>"

    symptom=x['Search'][0]
    query = {"type": "select",
             "args": {
                 "table": "Disease",
                 "columns": ["*"],
             }
            }
    print(query)
    r = requests.post(query_url, data=json.dumps(query), headers=headers)
    print("r=======", r, "\n", r.json())
    ProbableDiseases=[]
    for i in r.json():
        if(symptom.lower() in str(i['symptom']).lower()):
            ProbableDiseases.append(i['disease'])

    print("Probable disease are:- ",ProbableDiseases)

    ques=[]
    dis=[]
    for i in ProbableDiseases:
        query = {"type": "select",
                 "args": {
                     "table": "QandA",
                     "columns": ["*"],
                     "where": {"Disease": i }
                 }
                }
        print(query)
        questions = requests.post(query_url, data=json.dumps(query), headers=headers).json()
        print("r=======", r, "\n", r.json())
        ques.append(questions[0]['Question'])
        dis.append(questions[0]['Disease'])
    return render_template('index.html', symptoms=symp, pd=ProbableDiseases, len=len, questions=ques, dis=dis)

    # if 'logged_in' in session:
    #     headers['Authorization'] = 'Bearer ' + session['auth_token']
    #     query = {"type": "select",
    #              "args": {"table": "profile", "columns": ["profilepic"], "where": {"username": session['username']}}}
    #     print(query)
    #     PP = requests.post(query_url, data=json.dumps(query), headers=headers).json()
    #     print(PP, "\n\n\n\n")
    #     print(session['logged_in'], session['auth_token'], headers['Authorization'])
    # else:
    #     print("User is not logged in")
    #     session.clear()
    #     if ('Authorization') in headers.keys():
    #         headers.pop('Authorization')

    # query = {"type": "select", "args": {"table": "categories", "columns": ["*"]}}
    # r = requests.post(query_url, data=json.dumps(query), headers=headers).json()
    # print("r=", r)
    #
    # # selecting sample answers for home page
    # query = {"type": "select", "args": {"table": "answers", "columns": ["*"], }}
    # SampleAns = requests.post(query_url, data=json.dumps(query), headers=headers).json()
    # random.shuffle(SampleAns)
    # # print("Sample answers=",SampleAns)
    # SampQues = []
    # for i in SampleAns:
    #     q = i['question']
    #     query = {
    #         "args": {
    #
    #             "columns": [
    #                 "title"
    #             ], "where": {"id": q},
    #             "table": "questions"
    #         },
    #         "type": "select"
    #     }
    #     temp = requests.post(query_url, json.dumps(query, indent=2), headers=headers).json()
    #     SampQues.append(temp[0]['title'])
    # print("SampQues", SampQues)
    # x = SampleAns[0]['answer'];
    # print(x)
    # # print(PP[0]['profilepic'])

@app.route('/selectedQuery', methods=["POST"])
def selectedQuery():
    print(request.form)
    print(type(request.form))
    x = dict(request.form)
    print("\n\n\nx=======",x)



if __name__ == '__main__':
    app.secret_key="37dehi7h3di6teyliws8oud3ehd7eyd)dof"
    app.run(debug=True)

