# 載入flask套件
from flask import Flask,render_template,request,redirect,session

# 載入 pymongo 套件
import pymongo

# mongodb連線(要先pip安裝) root是使用者名稱 root123是當初設定的密碼
client = pymongo.MongoClient("mongodb://root:root123@ac-nxhavl3-shard-00-00.kecqc4f.mongodb.net:27017,ac-nxhavl3-shard-00-01.kecqc4f.mongodb.net:27017,ac-nxhavl3-shard-00-02.kecqc4f.mongodb.net:27017/?ssl=true&replicaSet=atlas-10enrt-shard-0&authSource=admin&retryWrites=true&w=majority")

app = Flask(__name__)
app.secret_key="secret"

# 操作 madetect 資料庫
db = client.madetect   

#首頁頁面
@app.route('/')
def home():
    return render_template('homepage.html')

#登入頁面
@app.route('/login')
def login_page():
    return render_template('userLogin.html')

#登入功能
@app.route('/login_function', methods=['POST'])
def login_function():

	# 接收前端資料
	user_email=request.values.get("user_email")
	user_password=request.values.get("user_password")

	# 根據接受到的資料跟資料庫互動，操作 madetect資料庫 的 user集合
	collection = db.user

	# 檢查帳號密碼是否正確
	result=collection.find_one({
		"$and":[
			{"user_email":user_email},
			{"user_password":user_password}
		]
	})
	#登入失敗
	if result==None:
		return redirect('/login')
	
	#登入成功，在session紀錄會員資訊，導向到內部主頁
	session["user_name"] = result["user_name"]
	session['_id'] = result['_id']
	return redirect("/inner_homepage")

#內部主頁頁面
@app.route('/inner_homepage')
def inner_homepage():
	# 確認session裡是否已有資料(在/login_function中或登入失敗就不會將資料傳入session)

	if "user_name" in session:
		return render_template("inner_homepage.html")	
	else:
		return redirect("/")
		

#註冊頁面
@app.route('/signup')
def signup_page():

	return render_template('userSignup.html')

#註冊功能
@app.route('/signup_function', methods=['POST'])
def signup_function():

	# 接收前端資料
	user_name=request.values.get("user_name")
	user_email=request.values.get("user_email")
	user_password=request.values.get("user_password")

	# 根據接受到的資料跟資料庫互動，操作 madetect資料庫 的 user集合
	collection = db.user

	#檢查是否有重複帳號
	#---------------還沒做QQ

	#檢查再次確認密碼
	#---------------還沒做QQ

	if len(user_name)==0:
		return redirect('/signup')
	
	elif len(user_email)==0:
		return redirect('/signup')
	
	elif len(user_password)==0:
		return redirect('/signup')
	
	#插入資料進資料庫
	else:
		collection.insert_one({
			"user_name":user_name,
			"user_email":user_email,
			"user_password":user_password
		})
		return user_name+user_email+user_password

#忘記密碼頁面
@app.route('/forgetpsw')
def forgetpsw():
	return render_template('userForget.html')

#忘記密碼功能
@app.route('/forgetpsw_function', methods=['POST'])
def forgetpsw_function():

	# 接收前端資料
	user_name=request.values.get("user_name")
	user_email=request.values.get("user_email")

	# 根據接受到的資料跟資料庫互動，操作 madetect資料庫 的 user集合
	collection = db.user

	#檢查是否有user名字及郵件
	result=collection.find_one({
		"$and":[
			{"user_name":user_name},
			{"user_email":user_email}	
		]
	})
	if result==None:
		return "帳號不存在"
	else:
		session["user_email"]=result["user_email"]
		return redirect("/reset")

#重設密碼頁面
@app.route('/reset')
def resetpsw():
	return render_template('resetPassword.html')

#重設密碼功能
@app.route('/reset_function', methods=['POST'])
def reset_function():

	# 接收前端資料
	user_password=request.values.get("user_password")

	# 根據接受到的資料跟資料庫互動，操作 madetect資料庫 的 user集合
	collection = db.user

	#確認密碼還沒做QQ

	#更新user_password
	collection.update_one({
    	"user_email":session["user_email"]
	},{
    "$set":{
        "user_password":user_password
    	}
	})
	return render_template('userLogin.html')

#管理員登入
@app.route('/adminlogin')
def adminlogin_page():
	return render_template('adminLogin.html')

#管理員忘記密碼
@app.route('/adminforgetpsw')
def adminforgetpsw_page():
	return render_template('adminForget.html')

#管理員重設密碼
@app.route('/adminresetpsw')
def adminresetpsw_pages():
	return render_template('adminReset.html')

#後端flask設定s
if __name__ == '__main__':
	app.run(host='0.0.0.0',port='5000',debug=True)