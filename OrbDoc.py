from flask import Flask, request, render_template, url_for, redirect
import mysql.connector as mc
app = Flask(__name__,template_folder = "templates") 

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/assessment', methods=['GET','POST'])
def assessment():
    if request.method == 'GET':
        return render_template("index.html") # to display form
    elif request.method == 'POST': # after submit
        email = request.form.get("email") # to get email from form
        like = request.form.get('like') # to get boolean value from form
        if like == "yes":
            like = 1
        else:
            like = 0
        fav_num = request.form.get("fav") # to get favourite number from form
        con = mc.connect(host='localhost', user='root', passwd='''put your mysql password''')
        cur = con.cursor()
        cur.execute('create database if not exists OrbDoc')
        cur.execute('use OrbDoc')
        cur.execute('create table if not exists Customer_Discovery(Email varchar(100) not null, Boolean_Value tinyint(1) not null, Favourite_Number int not null, primary key(email))')
        data =(email,like,fav_num)
        query ='insert into Customer_Discovery values (%s,%s,%s)'
        try: # execution of the query will pose in error, if email already exists
            cur.execute(query,data) # as email is the primary key
            con.commit()
            return render_template("result.html",alert_msg="Thank You, Your preference has been stored successfully!")
        except:
            return render_template("result.html",alert_msg="Thank You, we already have your preference stored!")
                
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5555, debug = False) #debug = True while developing
