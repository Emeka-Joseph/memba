from flask import render_template, redirect, flash, session, request, url_for
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from membapp.models import Party,Topics


from membapp import app, db

@app.route('/admin/topics')
def all_topics():
    if session.get('loggedin')==None:
        return redirect('/login')
    else:
        topics = Topics.query.all()
        return render_template('admin/alltopics.html', topics=topics)



@app.route('/admin/topic/delete/<id>')
def delete_post(id):
    topicobj = Topics.query.get_or_404(id)
    db.session.delete(topicobj)
    db.session.commit()
    flash('Succesfully Deleted')
    return redirect(url_for('all_topics'))


@app.route('/admin', methods=['POST', 'GET'])
def admin_home():
    if request.method =='GET':
        return render_template('admin/adminreg.html')
    else:
        #to retrieve data from the form, use request.form.get() method
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        '''Convert the plain password to hashed balue and insert into db'''
        hashed_pwd= generate_password_hash(pwd)
        if username !='' or pwd !='':
            query = f'INSERT INTO admin SET admin_username="{username}", admin_pwd="{hashed_pwd}"'

            db.session.execute(text(query))
            db.session.commit()
            flash('Registration successful. Log in Here')
            return redirect('/admin/login')
        else:
            flash('username and password must be supplied')
            return redirect(url_for('admin_home'))

@app.route('/admin/login', methods = ['POST','GET'])
def login():
    if request.method =='GET':
        return render_template('admin/adminlogin.html')
    else:
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        #write your query
        query = f'SELECT * FROM admin WHERE admin_username="{username}"' 
        #AND admin_pwd="{pwd}"'
        result = db.session.execute(text(query))
        total = result.fetchone() #fetchone or fetchmany()
        if total:
            pwd_indb = total[2] #hashed pwd from the database #comapre this hashed with the pwd coming from the form 
            chk = check_password_hash(pwd_indb, pwd) #returns True or False
            if chk ==True: #login is successful, save his details in a session
                session['loggedin']=username 
                return redirect(url_for('admin_dashboard'))
            else:
                flash('invalid credentials')
                return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('loggedin')!=None:
        return render_template('admin/index.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin/party', methods=['POST','GET'])
def add_party():
    if session.get('loggedin')==None:
        return render_template('admin/adminlogin.html')
    else:
        
        if request.method =='GET':
            return render_template('admin/party.html')
        else:
            #to retrieve data from the form, use request.form.get() method
            partyname = request.form.get('partyname')
            shortcode = request.form.get('partycode')
            contact = request.form.get('partycontact')
            #Insert into the party table using orm method
            #crete an instance of party (ensure that party is imported from models)    #obj= classname(column1=value1, comulumn2=value2)
            p = Party(party_name=partyname, party_shortcode=shortcode, party_contact=contact)
            #step 2: add to session 
            db.session.add(p)      
            #step3:
            #commite the session 
            db.session.commit()
            flash('Party added')
            return redirect(url_for('parties'))

@app.route('/admin/parties')
def parties():
    if session.get('loggedin') !=None:
        #We will fetch from db using ORM method
        data = db.session.query(Party).all()
        return render_template('admin/all_parties.html', data=data)
    else:
        return redirect('/admin/login')



@app.route('/admin/logout')
def admin_logout():
    if session.get('loggedin') !=None:
        session.pop('loggedin',None)
    return redirect(url_for('login'))

@app.route('/admin/topic/edit/<id>')
def edit_topic(id):
    if session.get('loggedin') !=None:
        #TO DO, write a query to fetch the topic on interest (the one with id)
        #Pass it to the template

        topic_deets = db.session.query(Topics).get(id)
        if topic_deets:
            return render_template('admin/edit_topic.html', topic_deets=topic_deets)
    else:
        return ''


@app.route('/admin/update_topic', methods=['POST'])
def update_topic():
    if session.get('loggedin') !=None:
        newstatus = request.form.get('status')
        topicid = request.form.get('topicid')
        t = Topics.query.get(topicid)
        t.topic_status = newstatus
        db.session.commit()
        flash('Topic successfully updated')
        return redirect('/admin/topics')
    else:
        return redirect('/admin/login')