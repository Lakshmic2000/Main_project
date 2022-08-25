from flask import*
from flask_mail import Mail

app=Flask(__name__)
app.secret_key="aaa"
import datetime
from  src.dbconnection import *
import smtplib
from email.mime.text import MIMEText

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'lakshmicmails4@gmail.com'
app.config['MAIL_PASSWORD'] = 'fauyrbstwrktailj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

from web3 import Web3, HTTPProvider
blockchain_address = 'HTTP://127.0.0.1:7545'
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = r'E:\Main_project\fund transfer\src\node_modules\.bin\build\contracts\amt.json'
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x5929582ECDb017639BEb9dadF1187726f60765D9'
import functools
def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return redirect ("/")
        return func()
    return secure_function



@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")

@app.route('/lg')
def lg():
    return render_template("login.html")




@app.route('/')
def main():
    return render_template("index.html")

@app.route('/login',methods=['post'])
def login():
    uname=request.form['uname']
    pswd=request.form['password']
    qry="select*from login where username=%s and password=%s"
    val=(uname,pswd)
    res=selectone(qry,val)
    if res is None:
        return'''<script>alert("invalid");window.location='/'</script>'''
    elif res[3]=='admin':
        session['lid']=res[0]
        return'''<script>alert("welcome admin");window.location='/admin_home'</script>'''
    elif res[3]=='agency':
        session['lid']=res[0]

        return'''<script>alert("welcome agency");window.location='/agency_home'</script>'''
    elif res[3] == 'officer':
        session['lid'] = res[0]

        return '''<script>alert("welcome officer");window.location='/officerhome'</script>'''


    else:
        return'''<script>alert("invalid");window.location='/'</script>'''



@app.route('/admin_home')
@login_required
def admin_home():

    return render_template("admin/adminhome.html")


@app.route('/agency_home')
@login_required
def agency_home():
    return render_template("agency/agency home.html")



@app.route('/officerhome')
@login_required
def officerhome():
    return render_template("ofiicer/officerhome.html")



@app.route('/addstaff',methods=['post'])
@login_required
def addstaff():
    type=request.form['button']
    if type=="ADD NEW":

        return render_template("admin/add staff.html")
    else:
        dis=request.form['select']
        q="SELECT `officer`.*,`officers`.* FROM `officers` JOIN `officer` ON `officer`.`lid`=`officers`.`lid` WHERE `officers`.`district`=%s"
        res=selectall(q,dis)
        return render_template("admin/managestaff.html",val=res)


@app.route('/viewstaff',methods=['get'])
@login_required
def viewstaff():
    q = "SELECT `officer`.*,`officers`.* FROM `officers` JOIN `officer` ON `officer`.`lid`=`officers`.`lid`"
    res=select(q)
    print(res)
    return render_template("admin/managestaff.html",val=res)


@app.route('/approveagency',methods=['get'])
@login_required
def approveagency():
    q="SELECT `agency`.* FROM `agency` JOIN `login` ON `login`.`id`=`agency`.`lid` WHERE `login`.`utype`='pending'"
    res=select(q)
    return render_template("admin/approve agency.html",val=res)

@app.route('/approvepackage',methods=['get'])
@login_required
def approvepackage():
    q="SELECT * FROM `officer`"
    res=select(q)

    return render_template("admin/approve package.html",val=res)




@app.route('/searchpakge',methods=['post'])
@login_required
def searchpakge():
    ofid=request.form['select']
    q="SELECT * FROM `officer`"
    res=select(q)
    q1="select * from package where officer_id=%s and status='pending'"
    rr=selectall(q1,ofid)
    return render_template("admin/approve package.html",val=res,val1=rr,ofid=int(ofid))


@app.route('/searchpakges',methods=['post'])
@login_required
def searchpakges():
    ofid=request.form['select']
    q="SELECT * FROM `officer`"
    res=select(q)
    q1="select * from package where officer_id=%s"
    rr=selectall(q1,ofid)
    return render_template("admin/trackpackage.html",val=res,val1=rr,ofid=int(ofid))


@app.route('/blockagency',methods=['get'])
@login_required
def blockagency():
    q = "SELECT `agency`.*,login.utype  FROM `agency` JOIN `login` ON `login`.`id`=`agency`.`lid` WHERE `login`.`utype`!='pending'   "
    res = select(q)
    print(res)
    return render_template("admin/blockunblockagency.html",val=res)



@app.route('/viewcomplaint',methods=['get'])
@login_required
def viewcomplaint():
    q="SELECT `agency`.`name`,`complaint`.* FROM `complaint` JOIN `agency` ON `agency`.`lid`=`complaint`.`agid` WHERE `complaint`.`reply`='pending'"
    res=select(q)
    return render_template("admin/viewcomplaint.html",val=res)


@app.route('/reply',methods=['get'])
@login_required
def reply():
    id=request.args.get('id')
    session['cmpid']=id
    return render_template("admin/reply.html")

@app.route('/trackpackage',methods=['get'])
@login_required
def trackpackage():
    q = "SELECT * FROM `officer`"
    res = select(q)

    return render_template("admin/trackpackage.html",val=res)

@app.route('/officerreg',methods=['post'])

def officerreg():
    try:
        office=request.form['textfields']
        fname=request.form['textfield01']
        lname=request.form['textfield02']
        gender=request.form['radio']
        dob=request.form['textfield']
        place=request.form['textfield2']
        post=request.form['textfield3']
        pin=request.form['textfield4']
        email=request.form['textfield6']
        phone=request.form['textfield5']
        qualification=request.form['textfield7']
        uname=request.form['textfield8']
        passd=request.form['textfield9']
        desi=request.form['textfields2']
        addr=request.form['textfields1']
        dis=request.form['select']
        id=0
        q="insert into login values(null,%s,%s,'officer')"
        v=uname,passd
        id=iud(q,v)
        print(id)
        q1="insert into officer values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        v1=str(id),fname,lname,qualification,gender,dob,place,post,pin,phone,email
        iud(q1,v1)
        q="insert into officers values(null,%s,%s,%s,%s,%s)"
        v=str(id),office,dis,desi,addr
        iud(q,v)
        return '''<script>alert("success...");window.location='/viewstaff'</script>'''
    except Exception as e:
        print(e)
        if id!=0:
            q="delete from login where id=%s"
            iud(q,id)

        return '''<script>alert("duplicate entry of username or phone or email...");window.location='/admin_home'</script>'''

@app.route('/editstaff',methods=['get'])
@login_required
def editstaff():
    id=request.args.get('id')
    session['sid']=id
    q="SELECT `officer`.*,`officers`.* FROM `officers` JOIN `officer` ON `officer`.`lid`=`officers`.`lid` WHERE officer.lid=%s"
    res=selectone(q,id)
    return render_template("admin/edit staff.html",val=res)





@app.route('/officerupdate',methods=['post'])
@login_required
def officerupdate():
    try:
        office=request.form['textfields']

        fname=request.form['textfield01']
        lname=request.form['textfield02']
        gender=request.form['radio']
        dob=request.form['textfield']


        place=request.form['textfield2']
        post=request.form['textfield3']
        pin=request.form['textfield4']
        email=request.form['textfield6']
        phone=request.form['textfield5']
        qualification=request.form['textfield7']
        desi = request.form['textfields2']
        addr = request.form['textfields1']
        q1="update officer set fname=%s,lname=%s,qualification=%s,gender=%s,dob=%s,place=%s,post=%s,pin=%s,phone=%s,email=%s where lid=%s"
        v1=fname,lname,qualification,gender,dob,place,post,pin,phone,email,str(session['sid'])
        iud(q1,v1)
        q="update officers set officename=%s,designation=%s,officeaddress=%s where lid=%s"
        v=office,desi,addr,str(session['sid'])
        iud(q,v)
        return '''<script>alert("updated...");window.location='/viewstaff#about'</script>'''
    except Exception as e:
        print(e)

        return '''<script>alert("duplicate entry...");window.location='/admin_home'</script>'''






@app.route('/deltestaff',methods=['get'])
@login_required
def deltestaff():
    id=request.args.get('id')
    q="delete from officer where lid=%s "
    iud(q,id)
    q1="delete from login where id=%s"
    iud(q1,id)
    return '''<script>alert("deleted...");window.location='/viewstaff#about'</script>'''

@app.route('/approvepkg',methods=['get'])
@login_required
def approvepkg():
    id=request.args.get('id')
    q="update package set status='approve' where pid=%s"
    iud(q,id)

    return '''<script>alert("approve package...");window.location='/approvepackage#about'</script>'''
@app.route('/rejectpkge',methods=['get'])
@login_required
def rejectpkge():
    id=request.args.get('id')
    q="update package set status='reject' where pid=%s"
    iud(q,id)

    return '''<script>alert("reject package...");window.location='/approvepackage#about'</script>'''



@app.route('/managepackage',methods=['get'])
@login_required
def managepackage():
    q1="select * from package where officer_id=%s"
    rr=selectall(q1,session['lid'])
    return render_template("ofiicer/managepackage.html",val=rr)


@app.route('/searchpackage',methods=['post'])
@login_required
def searchpackage():
    type=request.form['select']
    q1="SELECT `package`.* FROM package JOIN `pkgtype` ON `pkgtype`.`pkid`=`package`.`pid` WHERE officer_id=%s AND `pkgtype`.`type`=%s"
    v=session['lid'],type
    rr=selectall(q1,v)
    return render_template("ofiicer/managepackage.html",val=rr)



@app.route('/dltpkg',methods=['get'])
@login_required
def dltpkg():
    id=request.args.get('id')
    q="delete from package where pid=%s"
    iud(q,id)
    q = "delete from pkgtype where pkid=%s"
    iud(q, id)
    return '''<script>alert(" package removed...");window.location='/managepackage#about'</script>'''

@app.route('/viewpkstatus',methods=['get'])
@login_required
def viewpkstatus():
    q1="select * from package where officer_id=%s"
    rr=selectall(q1,session['lid'])
    return render_template("ofiicer/viewpackagestatus.html",val=rr)








@app.route('/pkgrequest',methods=['get'])
@login_required
def pkgrequest():

    return render_template("ofiicer/viewpackagerequestupdatestatus.html")


@app.route('/pkgrequests',methods=['post'])
@login_required
def pkgrequests():
    type=request.form['select']
    q1="SELECT `agency`.`name`,`package`.*,`package_request`.* FROM `package_request` JOIN `package` ON `package`.`pid`=`package_request`.`pkg_id` JOIN `agency` ON `agency`.`lid`=`package_request`.`agid` JOIN `pkgtype` ON `pkgtype`.`pkid`=`package`.`pid` WHERE `package`.`officer_id`=%s AND `package_request`.`status`='pending' AND `pkgtype`.`type`=%s"
    v=session['lid'],type
    rr=selectall(q1,v)
    print(rr)
    return render_template("ofiicer/viewpackagerequestupdatestatus.html",val=rr)

@app.route('/acceptreq',methods=['get'])
@login_required
def acceptreq():
    id=request.args.get('id')
    q="update package_request set status='accept' where rid=%s"
    iud(q,id)

    return '''<script>alert("acccept package request...");window.location='/pkgrequest'</script>'''


@app.route('/rejectreq',methods=['get'])
@login_required
def rejectreq():
    id=request.args.get('id')
    q="update package_request set status='reject' where rid=%s"
    iud(q,id)

    return '''<script>alert("reject package request...");window.location='/pkgrequest'</script>'''

@app.route('/aviewpkg',methods=['get'])
@login_required
def aviewpkg():


    return render_template("agency/viewpackageandsentrequest.html")

@app.route('/aviewpkgs',methods=['post'])
@login_required
def aviewpkgs():
    type=request.form['select']
    q1="SELECT `package`.* FROM package JOIN `pkgtype` ON `pkgtype`.`pkid`=`package`.`pid` WHERE STATUS='approve' AND `pkgtype`.`type`=%s"
    rr=selectall(q1,type)
    return render_template("agency/viewpackageandsentrequest.html",val=rr,type=type)




@app.route('/sentreqst',methods=['get'])
@login_required
def sentreqst():
    id=request.args.get('id')
    q="select *  from  package_request where pkg_id=%s and agid=%s and date=curdate()"
    v=id,session['lid']
    res=selectone(q,v)
    if res is None:

        q="insert into package_request values(null,%s,%s,curdate(),'pending')"
        v=id,session['lid']
        iud(q,v)

        return '''<script>alert("request sent ...");window.location='/aviewpkg'</script>'''
    else:
        return '''<script>alert("already sent ...");window.location='/aviewreqstatus'</script>'''




@app.route('/aviewreqstatus',methods=['get'])
@login_required
def aviewreqstatus():

    q1="SELECT `agency`.`name`,`package`.*,`package_request`.* FROM `package_request` JOIN `package` ON `package`.`pid`=`package_request`.`pkg_id` JOIN `agency` ON `agency`.`lid`=`package_request`.`agid` WHERE `package_request`.`agid`=%s"
    rr=selectall(q1,session['lid'])
    print(rr)
    return render_template("agency/view request status.html",val=rr)



@app.route('/sentamt',methods=['get'])
@login_required
def sentamt():
    q="SELECT `agency`.`name`,`package`.*,`package_request`.* FROM `package_request` JOIN `package` ON `package`.`pid`=`package_request`.`pkg_id` JOIN `agency` ON `agency`.`lid`=`package_request`.`agid` WHERE `package_request`.`agid`=%s and  `package_request`.status='accept' and`package_request`.rid not in (select req_id from transfer_amount) "
    res=selectall(q,session['lid'])
    print(res)
    return render_template("agency/sentamounttransfer.html",val=res)



@app.route('/transfer',methods=['get'])
@login_required
def transfer():
    ofcid=request.form['select']
    amt=request.form['textfield']
    q="insert into transfer_amount values(null,%s,%s,%s,curdate(),'pending')"
    v=session['lid'],ofcid,amt
    iud(q,v)
    return '''<script>alert("amount sent ...");window.location='/sentamt'</script>'''





@app.route('/viewtransferstatus',methods=['get'])
@login_required
def viewtransferstatus():
    q1="SELECT `package`.`package`,`package`.`description`,`officer`.`fname`,`officer`.`lname`,`transfer_amount`.`amount`,`transfer_amount`.`date`,`transfer_amount`.`status` FROM `transfer_amount` JOIN `package_request` ON `package_request`.`rid`=`transfer_amount`.`req_id` JOIN `package` ON `package`.`pid`=`package_request`.`pkg_id` JOIN `officer` ON `officer`.`lid`=`package`.`officer_id` WHERE `transfer_amount`.`agid`=%s"
    rr=selectall(q1,session['lid'])
    return render_template("agency/view transfer status.html",val=rr)




@app.route('/complaint',methods=['get'])
@login_required
def complaint():


    return render_template("agency/sent complaint.html")

@app.route('/complaints',methods=['post'])
@login_required
def complaints():
    cmp=request.form['textarea']

    q="insert into complaint values(null,%s,curdate(),%s,'pending')"
    v=session['lid'],cmp
    iud(q,v)
    return '''<script>alert(" sent ...");window.location='/viewerply'</script>'''







@app.route('/reply1',methods=['post'])
@login_required
def reply1():
    reply=request.form['textarea']

    q="update complaint set reply=%s where cid=%s "
    v=reply,session['cmpid']
    iud(q,v)
    return '''<script>alert("reply sent ...");window.location='/viewcomplaint#about'</script>'''





@app.route('/viewerply',methods=['get'])
@login_required
def viewerply():
    q="select * from complaint where agid=%s "
    res=selectall(q,str(session['lid']))
    return render_template("agency/viewreply.html",val=res)

@app.route('/agency',methods=['get'])
def agency():
    return render_template("agencyreg.html")



@app.route('/agencyreg',methods=['post'])
def agencyreg():
    try:
        fname=request.form['textfield01']
        place=request.form['textfield2']
        post=request.form['textfield3']
        pin=request.form['textfield4']
        email=request.form['textfield6']
        phone=request.form['textfield5']
        uname=request.form['textfield8']
        passd=request.form['textfield9']
        q="insert into login values(null,%s,%s,'pending')"
        v=uname,passd
        id=iud(q,v)
        q1="insert into agency values(null,%s,%s,%s,%s,%s,%s,%s)"
        v1=str(id),fname,place,post,pin,phone,email
        iud(q1,v1)
        return '''<script>alert("success...");window.location='/'</script>'''
    except Exception as e:
        print(e)
        return '''<script>alert("duplicate entry of username,email,password...");window.location='/'</script>'''

@app.route('/approvea',methods=['get'])
@login_required
def approvea():
    id=request.args.get('id')
    q="update login set utype='agency' where id=%s"
    iud(q,id)
    return '''<script>alert("approved...");window.location='/approveagency'</script>'''


@app.route('/rejecta',methods=['get'])
@login_required
def rejecta():
    id=request.args.get('id')
    q="update login set utype='reject' where id=%s"
    iud(q,id)
    return '''<script>alert("rejected...");window.location='/approveagency'</script>'''




@app.route('/blockagencys',methods=['get'])
@login_required
def blockagencys():
    id=request.args.get('id')
    q="update login set utype='block' where id=%s"
    iud(q,id)
    return '''<script>alert("blocked...");window.location='/blockagency#about'</script>'''


@app.route('/unblockagency',methods=['get'])
@login_required
def unblockagency():
    id=request.args.get('id')
    q="update login set utype='agency' where id=%s"
    iud(q,id)
    return '''<script>alert("unblocked...");window.location='/blockagency#about'</script>'''



@app.route('/addpackage',methods=['post'])
@login_required
def addpackage():
    return render_template("ofiicer/addpackage.html")






@app.route('/addpackages',methods=['post'])
@login_required
def addpackages():
    type=request.form['radio']
    pkg=request.form['textfield']
    desp=request.form['textarea']
    q="insert into package values(null,%s,%s,%s,'pending')"
    v=session['lid'],pkg,desp
    id=iud(q,v)
    q="insert into pkgtype values(null,%s,%s)"
    v=id,type
    iud(q,v)

    return '''<script>alert("added...");window.location='/managepackage#about'</script>'''


@app.route('/reqamt',methods=['get'])
@login_required
def reqamt():
    id=request.args.get('id')
    session['rid']=id
    return render_template("agency/amount.html")


@app.route('/amounts',methods=['post'])
@login_required
def amounts():
    amt=request.form['text']
    q="insert into transfer_amount values(null,%s,%s,%s,curdate(),'pending')"
    v=session['lid'],session['rid'],amt
    iud(q,v)
    return '''<script>alert("added...");window.location='/viewtransferstatus#about'</script>'''







@app.route('/updatetransferinfo',methods=['get'])
@login_required
def updatetransferinfo():
    q1="SELECT `agency`.`name`,`package`.`package`,`package`.`description`,`transfer_amount`.* FROM `transfer_amount` JOIN `agency` ON `agency`.`lid`=`transfer_amount`.`agid` JOIN `package_request` ON `package_request`.`rid`=`transfer_amount`.`req_id` JOIN `package` ON `package`.`pid`=`package_request`.`pkg_id` WHERE `package`.`officer_id`=%s and `transfer_amount`.`status`='pending'"
    rr=selectall(q1,session['lid'])
    print(rr)
    return render_template("ofiicer/update transfer info.html",val=rr)



@app.route('/acceptt',methods=['get'])
@login_required
def acceptt():
    id=request.args.get('id')
    qry="SELECT `amount` FROM `transfer_amount` WHERE `tid`=%s"
    res=selectone(qry,id)
    amt=res[0]
    q="update transfer_amount set status='accept' where tid=%s "
    iud(q,id)
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()

        d = datetime.datetime.now().strftime("%Y-%m-%d")
        message2 = contract.functions.add_transferrequest(blocknumber + 1, int(id),amt,d).transact()
        print (message2)
    return '''<script>alert("accepted...");window.location='/updatetransferinfo#about'</script>'''


@app.route('/rejectt',methods=['get'])
@login_required
def rejectt():
    id=request.args.get('id')
    q="update transfer_amount set status='reject' where tid=%s "
    iud(q,id)
    return '''<script>alert("rejected...");window.location='/updatetransferinfo#about'</script>'''


@app.route('/viewmore',methods=['get'])
@login_required
def viewmore():
    id=request.args.get('id')
    session['pkid']=id
    q="SELECT `agency`.`name`,`agency`.`phone`,`transfer_amount`.`date`,`transfer_amount`.`amount`,`transfer_amount`.`status` FROM `transfer_amount` JOIN `agency` ON `agency`.`lid`=`transfer_amount`.`agid` JOIN `package_request` ON `package_request`.`rid`=`transfer_amount`.`req_id` WHERE `package_request`.`pkg_id`=%s"
    res=selectall(q,id)
    return render_template("admin/trackpackages.html",val=res)



@app.route('/viewmore1',methods=['get'])
@login_required
def viewmore1():
    id = request.args.get('id')
    q = "SELECT `agency`.`name`,`agency`.`phone`,`transfer_amount`.`date`,`transfer_amount`.`amount`,`transfer_amount`.`status` FROM `transfer_amount` JOIN `agency` ON `agency`.`lid`=`transfer_amount`.`agid` JOIN `package_request` ON `package_request`.`rid`=`transfer_amount`.`req_id` WHERE `package_request`.`pkg_id`=%s"
    res = selectall(q, id)
    print(res)
    return render_template("ofiicer/tracktranferinfo.html",val=res)

@app.route('/searchpakges1',methods=['get'])
@login_required
def searchpakges1():
    q1="select * from package where officer_id=%s and status='approve'"
    rr=selectall(q1,session['lid'])
    return render_template("ofiicer/trackpackage.html",val1=rr)











@app.route('/forpassword', methods=['POST','GET'])
def forpassword():
    emails=request.form['textfield']
    if '@gmail.com' in emails:

        q="SELECT `lid` FROM `agency` WHERE `email`=%s"
        v=emails
        res=selectone(q,v)
        if res is None:
            if '@gmail.com' in emails:
                q = "SELECT `lid` FROM `officer` WHERE `email`=%s"
                v = emails
                res = selectone(q, v)
                if res is None:
                    return "<script>alert('Email not valid');window.location='/forgot';</script>"
                else:
                    lid = res[0]
                    print("lid" + str(lid))
                    qq = "SELECT `password` FROM `login` WHERE `id`=%s"
                    res = selectone(qq, lid)
                    print(res)
                    try:
                        gmail = smtplib.SMTP('smtp.gmail.com', 587)
                        gmail.ehlo()
                        gmail.starttls()
                        gmail.login('lakshmicmails4@gmail.com','fauyrbstwrktailj')
                    except Exception as e:
                        print("Couldn't setup email!!" + str(e))
                    msg = MIMEText("your restored password from govt education fund site")
                    print(msg)
                    msg['Subject'] = 'your password is ' + str(res[0])
                    msg['To'] = emails
                    msg['From'] = 'lakshmicmails4@gmail.com'
                    try:
                        gmail.send_message(msg)
                        return "<script>alert('you can check your password in your email....');window.location='/forgot';</script>"

                    except Exception as e:
                        print("COULDN'T SEND EMAIL", str(e))
                        return "<script>alert('Error');window.location='/forgot';</script>"





        else:
            lid=res[0]
            print("lid"+str(lid))
            qq="SELECT `password` FROM `login` WHERE `id`=%s"
            res=selectone(qq,lid)
            print(res)
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                gmail.ehlo()
                gmail.starttls()
                gmail.login('lakshmicmails4@gmail.com','fauyrbstwrktailj')
            except Exception as e:
                print("Couldn't setup email!!" + str(e))
            msg = MIMEText("your restored password from govt education fund site")
            print(msg)
            msg['Subject'] = 'your password is '+str(res[0])
            msg['To'] = emails
            msg['From'] = 'lakshmicmails4@gmail.com'
            try:
                gmail.send_message(msg)
                return "<script>alert('you can check your password in your email....');window.location='/forgot';</script>"

            except Exception as e:
                print("COULDN'T SEND EMAIL", str(e))
                return "<script>alert('Error');window.location='/forgot';</script>"
    else:
        uname = request.form['textfield']
        q = "select * from login where username=%s"
        v = uname
        ee = selectone(q, v)
        pa = ee[2]
        print()
        return render_template("forgotpassword.html", val="your password is " + pa)



@app.route("/forgot")
def forgot():

    return render_template("forgotpassword.html")

@app.route("/c1")
def c1():

    return render_template("admin/change password.html")


@app.route("/c2")
def c2():

    return render_template("agency/change password.html")


@app.route("/c3")
def c3():

    return render_template("ofiicer/change password.html")


@app.route('/passwordchange',methods=['get','post'])
def passwordchange():
    if 'lid' in session:
            offid=session['lid']

            currentpassword=request.form['textfield']

            newpassword = request.form['textfield2']

            confirmpassword = request.form['textfield3']

            q=("SELECT * FROM `login` WHERE `login`.`id`=%s and password=%s")
            v=session['lid'],currentpassword
            s=selectone(q,v)

            if s is None:
               return  '''<script>alert("incorrect password");window.location='/admin_home'</script>'''
            elif newpassword==confirmpassword:
               q=("update login set password=%s where id=%s")
               v=newpassword,session['lid']
               iud(q,v)
               return '''<script>alert("password changed");window.location='/admin_home'</script>'''
            else:
               return '''<script>alert("password missmatch");window.location='/admin_home'</script>'''
    else:
       return '''<script>alert("please login");window.location='/' </script>'''


@app.route('/passwordchange1',methods=['get','post'])
def passwordchange1():
    if 'lid' in session:
            offid=session['lid']

            currentpassword=request.form['textfield']

            newpassword = request.form['textfield2']

            confirmpassword = request.form['textfield3']

            q=("SELECT * FROM `login` WHERE `login`.`id`=%s and password=%s")
            v=session['lid'],currentpassword
            s=selectone(q,v)

            if s is None:
               return  '''<script>alert("incorrect password");window.location='/agency_home'</script>'''
            elif newpassword==confirmpassword:
               q=("update login set password=%s where id=%s")
               v=newpassword,session['lid']
               iud(q,v)
               return '''<script>alert("password changed");window.location='/agency_home'</script>'''
            else:
               return '''<script>alert("password missmatch");window.location='/agency_home'</script>'''
    else:
       return '''<script>alert("please login");window.location='/' </script>'''


@app.route('/passwordchange2',methods=['get','post'])
def passwordchange2():
    if 'lid' in session:
            offid=session['lid']

            currentpassword=request.form['textfield']

            newpassword = request.form['textfield2']

            confirmpassword = request.form['textfield3']

            q=("SELECT * FROM `login` WHERE `login`.`id`=%s and password=%s")
            v=session['lid'],currentpassword
            s=selectone(q,v)

            if s is None:
               return  '''<script>alert("incorrect password");window.location='/officerhome'</script>'''
            elif newpassword==confirmpassword:
               q=("update login set password=%s where id=%s")
               v=newpassword,session['lid']
               iud(q,v)
               return '''<script>alert("password changed");window.location='/officerhome'</script>'''
            else:
               return '''<script>alert("password missmatch");window.location='/officerhome'</script>'''
    else:
       return '''<script>alert("please login");window.location='/' </script>'''


@app.route('/viewhistory',methods=['get'])
@login_required
def viewhistory():
    return render_template("admin/history.html")



@app.route('/history',methods=['post'])
@login_required
def history():
    year=request.form['select']
    q="SELECT `agency`.`name`,`transfer_amount`.* FROM `transfer_amount` JOIN `agency` ON `agency`.`lid`=`transfer_amount`.`agid` WHERE YEAR(`date`)=%s and status='accept'"
    res=selectall(q,year)
    return render_template("admin/history.html",val=res)





@app.route('/searchpackage1',methods=['post'])
@login_required
def searchpackage1():
    type=request.form['select']
    q1="SELECT `package`.* FROM package JOIN `pkgtype` ON `pkgtype`.`pkid`=`package`.`pid` WHERE officer_id=%s AND `pkgtype`.`type`=%s"
    v=session['lid'],type
    rr=selectall(q1,v)
    return render_template("ofiicer/viewpackagestatus.html",val=rr)




app.run(debug=True)
