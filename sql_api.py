from flask import *
import sqlite3 

app= Flask(__name__)
app.secret_key = "Any key"


@app.route('/')
def home():
	return render_template("addnew_api.html")


@app.route('/addnew',methods=['POST','GET'])
def addrecord():
	if request.method == 'POST':
		msg = None
		try:
			name = request.form["name"]
			contact = request.form["contact"]
			email = request.form["email"]

			if int(contact[0])<7 or len(contact)!=10:
				msg="Wrong Contact No. Entered"
			elif email.find('@gmail.com')==-1 and email.find('@ymail.com')==-1 and email.find('@hotmail.com')==-1:
				msg="Wrong Email Id Entered"
			else:				
				con =sqlite3.connect("api_data.db",timeout=10)
				with con:
					
					cur = con.cursor()
					cur.execute("CREATE table if not exists student(ID INTEGER PRIMARY KEY AUTOINCREMENT,Name text,Contact text,Email text)")
					cur.execute("INSERT into student(Name,Contact,Email) values (?,?,?)",(name,contact,email))
					
					

					con.commit()
				msg="Successfully Added information"

		except sqlite3.Error,e:
			con.rollback()
			msg=e.args[0]
		finally:
			return render_template("result.html",msg=msg)
			con.close()




@app.route('/del',methods=['POST','GET'])
def del_data():
	if request.method=='POST':
		return render_template("del_api.html")



@app.route('/delete',methods=['POST','GET'])
def delete_data():
	if request.method=='POST':
		result=None
		try:

			con=sqlite3.connect('api_data.db',timeout=10)
			cur=con.cursor()
			id_no=request.form["id"]
			val= check_val(int(id_no))
			
			if val==True:
				cur.execute("DELETE from student Where ID=?",(id_no,))
				result="Successfully Deleted"
			else:
				result="Id not Exist"
			con.commit()

		except sqlite3.Error,e:
			con.rollback()
			result=e.args[0]
		finally:
			return render_template("result.html",msg=result)
			con.close()
		



@app.route('/update',methods=['POST','GET'])
def update_data():
	if request.method=='POST':
		result=None
		try:
			con=sqlite3.connect('api_data.db',timeout=10)
			cur=con.cursor()
			id_no=request.form["id"]
			email=request.form["email"]
			if len(id_no)==0 or len(email)==0:
				result="Please make proper entry"
			else:
				cur.execute("UPDATE student set Email=? where ID=?",(email,id_no))
				result="Updated Successfully"
			con.commit()
		except sqlite3.Error,e:
			con.rollback()
			result=e.args[0]
		finally:
			return render_template("result.html",msg=result)
			con.close()




@app.route('/addid',methods=['POST','GET'])
def add_id():
		if request.method=='POST':
			
			con=sqlite3.connect('api_data.db',timeout=10)
			con.row_factory=sqlite3.Row
			cur=con.cursor()
			cur.execute("Select * from student")
			rows=cur.fetchall()
			return render_template('update_api.html',rows=rows)





@app.route('/update_d',methods=['POST','GET'])
def red_update():
	if request.method=='POST':
		return render_template("update_api.html")





def check_val(id_no):         ########Check Value in Row
	val = None
	con=sqlite3.connect('api_data.db',timeout=10)
	cur=con.cursor()
	cur.execute("SELECT * from student")
	for row in cur.fetchall():
		val=int(row[0])
		if val==id_no:
			val=True
			break
	con.commit()
	return val



@app.route('/list',methods=['POST'])
def list():
	if request.method=='POST':
		con=sqlite3.connect('api_data.db',timeout=10)
		con.row_factory=sqlite3.Row
		cur=con.cursor()
		cur.execute("Select * from student")
		rows=cur.fetchall()
		return render_template('list_api.html',rows=rows)



def check_table():              # CHeck Table Exist
	con = sqlite3.connect('api_data.db',timeout=50)
	cur = con.cursor()
	result= cur.execute("SELECT count(*) from sqlite_master where type='table' and name='student'")
	return result

if __name__=='__main__':
	app.run(debug = True,port=5000,host="0.0.0.0")
