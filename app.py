######################################
# author ben lawson <balawson@bu.edu> 
# Edited by: Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from 
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask.ext.login as flask_login

#for image uploading
from werkzeug import secure_filename
import os, base64

# Add by Ang Li
import time

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'PhotoShare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users") 
users = cursor.fetchall()

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users") 
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd 
	return user

'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
	return new_page_html
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return render_template('login.html')
	#The request method is POST (page is recieving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
		data = cursor.fetchall()
		pwd = str(data[0][0] )
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
			return flask.redirect(flask.url_for('protected')) #protected is a function defined in this file

	#information did not match
	return render_template('login.html', message='Username and password not match, try again')

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return render_template('hello.html', message='Logged out') 

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html') 

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register", methods=['GET'])
def register():
	return render_template('register.html', supress='True')  

@app.route("/register", methods=['POST'])
def register_user():
	try:
		email=request.form.get('email')
		password=request.form.get('password')
		firstName=request.form.get('firstName')
		lastName=request.form.get('lastName')
		dob=request.form.get('birthday')
		gender=request.form.get('gender')
		hometown=request.form.get('hometown')
	except:
		print "couldn't find all tokens" #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
		print cursor.execute("INSERT INTO Users (email, password, first_name, last_name, date_of_birth, gender, hometown) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(email, password, firstName, lastName, dob, gender, hometown))
		conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('hello.html', name=email, message='Account Created!')
	else:
		print "couldn't find all tokens"
		return flask.redirect(flask.url_for('register'))

def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT user_id FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]

def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email FROM Users WHERE email = '{0}'".format(email)): 
		#this means there are greater than zero entries with that email
		return False
	else:
		return True
#end login code

@app.route('/profile', methods=['GET', 'POST'])
@flask_login.login_required
def protected():
	userInfo = getUserInfo()
	if request.method == 'POST':
		firstName=request.form.get('firstName')
		if len(firstName) == 0:
			firstName = userInfo[1]
		print firstName
		lastName=request.form.get('lastName')
		if len(lastName) == 0:
			lastName = userInfo[2]
		print lastName
		email=request.form.get('email')
		print email
		password=request.form.get('password')
		if len(password) == 0:
			password = userInfo[4]
		print password
		dob=request.form.get('birthday')
		if len(dob) == 0:
			dob = userInfo[5]
		print dob
		gender=request.form.get('gender')
		if gender is None:
			gender = ''
		print gender
		hometown=request.form.get('hometown')
		if len(hometown) == 0:
			hometown = userInfo[7]
		print hometown
		cursor = conn.cursor()
		try:
			# cursor.execute("UPDATE Users SET first_name = '{0}' WHERE email = '{1}'".format(firstName, email))
			cursor.execute("UPDATE Users SET first_name ='{0}',last_name='{1}',password='{2}',date_of_birth='{3}',gender='{4}',hometown='{5}' WHERE email='{6}'".format(firstName, lastName, password, dob, gender, hometown, email))
			conn.commit()
		except:
			return render_template('profile.html', message="Error in updating profile. Please try again", userInfo=userInfo)
		userInfo = getUserInfo()
		return render_template('profile.html', message="Profile Updated", userInfo=userInfo)
	else:
		return render_template('profile.html', userInfo=userInfo)

#begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#edit code by Ang Li
@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	album_id = request.form.get('album_id')
	albumdata = getAlbumInfo(album_id)
	if request.method == 'POST':
		imgfile = request.files['photo']
		photo_data = base64.standard_b64encode(imgfile.read())
		caption = request.form.get('caption')
		print caption
		print album_id
		cursor = conn.cursor()
		try: 
			cursor.execute("INSERT INTO Photo (imgdata, caption, album_id) VALUES ('{0}', '{1}', '{2}' )".format(photo_data, caption, album_id))
			conn.commit()
		except:
			return render_template('albumPhotos.html', message='Error in upload sql!', photos=getAlbumPhotos(album_id), albumdata=albumdata)
		return render_template('albumPhotos.html', message='Photo uploaded!', photos=getAlbumPhotos(album_id), albumdata=albumdata)
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		return render_template('albumPhotos.html', albumdata=albumdata)
#end photo uploading code 

#add code by Ang Li
@app.route('/getAllFriends', methods=['GET', 'POST'])
@flask_login.login_required
def get_all_friends():
	frienddatas = getFriendList()
	unfrienddatas = getUnFriendList()
	from_user_id = getUserIdFromEmail(flask_login.current_user.id)
	if len(frienddatas) == 0:
		message="You don't have friends now."	
	if request.method == 'POST':
		if request.form['submit'] == 'Add':
			print from_user_id
			to_user_id = request.form.get('to_friend_id')
			print to_user_id
			cursor = conn.cursor()
			try:
				cursor.execute("INSERT INTO Friendship (from_user_id, to_user_id) VALUES ('{0}', '{1}')".format(from_user_id, to_user_id))
				conn.commit()
			except:
				return render_template('friends.html', frienddatas=frienddatas, error="There is an error in the SQL for adding friends",  unfrienddatas=unfrienddatas)
		elif request.form['submit'] == 'Delete':
			print "Delete friend"
			print from_user_id
			to_user_id = request.form.get('delete_to_friend_id')
			print to_user_id
			cursor = conn.cursor()
			try:
				cursor.execute("DELETE FROM Friendship WHERE from_user_id='{0}' AND to_user_id='{1}'".format(from_user_id, to_user_id))
				conn.commit()
			except:
				return render_template('friends.html', frienddatas=frienddatas, error="There is an error in the SQL for deleting friends",  unfrienddatas=unfrienddatas)
		frienddatas = getFriendList()
		unfrienddatas = getUnFriendList()
		return render_template('friends.html', frienddatas=frienddatas, unfrienddatas=unfrienddatas)
	else:
		return render_template('friends.html', frienddatas=frienddatas, unfrienddatas=unfrienddatas)

@app.route('/getAlbums', methods=['GET', 'POST'])
@flask_login.login_required
def create_delete_albums():
	owner_id = getUserIdFromEmail(flask_login.current_user.id)
	data = getMyAlbumList(owner_id)
	if request.method == 'POST':
		if request.form['submit'] == 'Browse':
			print 'Browse album'
			album_id = request.form.get('album_select')
			imgdata = getAlbumPhotos(album_id)
			albumdata = getAlbumInfo(album_id)
			return render_template('albumPhotos.html', photos=imgdata, albumdata=albumdata)
		elif request.form['submit'] == 'Delete':
			print 'Delete album'
			album_id = request.form.get('album_select')
			cursor = conn.cursor()
			try:
				cursor.execute("DELETE FROM Album WHERE album_id='{0}'".format(album_id));
				conn.commit()
			except:
				return render_template('album.html', data=data, message="There is an error in the SQL for adding album")
		elif request.form['submit'] == 'Create':
			print 'Add album'
			album_name = request.form.get('album_name')
			todaysdate = time.strftime('%Y-%m-%d')
			if not album_name:
				return render_template('album.html', data=data, message="Please input album name")
			print album_name
			print owner_id
			print todaysdate
			cursor = conn.cursor()
			try:
				cursor.execute("INSERT INTO Album (album_name, owner_id, date_created) VALUES ('{0}', '{1}', '{2}')".format(album_name, owner_id, todaysdate))
				conn.commit()
			except:
				return render_template('album.html', data=data, message="There is an error in the SQL for adding album")
		data = getMyAlbumList(owner_id)
		return render_template('album.html', data=data)
	else:
		return render_template('album.html', data=data)

@app.route('/getPhotoInfo', methods=['POST'])
def get_photo_by_id():
	if request.method == 'POST':
		photo_id = request.form.get('photo_id')
		print 'Browse photo id: %s' % photo_id
		if request.form['submit'] == 'Delete':
			print 'Delete photo id: %s' % photo_id
			album_id = getAlbumIdByPhoto(photo_id)
			cursor = conn.cursor()
			cursor.execute("DELETE FROM Photo WHERE photo_id='{0}'".format(photo_id))
			conn.commit()
			imgdata = getAlbumPhotos(album_id)
			print "after delete photo", len(imgdata)
			albumdata = getAlbumInfo(album_id)
			return render_template('albumPhotos.html', photos=imgdata, albumdata=albumdata)
		photos = getPhotoById(photo_id)
		tags = getTagsByPhotoId(photo_id)
		comments = getCommentsByPhotoId(photo_id)
		photo_owner_id = photos[0][4]
		print 'owner id: %s' %  photo_owner_id
		ownPhoto = isYourOwnPhoto(photo_owner_id)
		if ownPhoto:
			print "your self's photo"
		else:
			print "other's photo"
		likeCount = likeCounts(photo_id)
		likes = getLikedUserList(photo_id)
		return render_template('photo.html', photos=photos, tags=tags, comments=comments, ownPhoto=ownPhoto, likeCount=likeCount, likes=likes)

@app.route('/UpdatePhotoInfo', methods=['POST'])
def update_photo():
	if request.method == 'POST':
		photo_id = request.form.get('photo_id')
		photos = getPhotoById(photo_id)
		tags = getTagsByPhotoId(photo_id)
		comments = getCommentsByPhotoId(photo_id)
		likeCount = likeCounts(photo_id)
		likes = getLikedUserList(photo_id)
		photo_owner_id = photos[0][4]
		ownPhoto = isYourOwnPhoto(photo_owner_id)
		print ownPhoto
		if request.form['submit'] == 'Get Recommend List':
			text = request.form.get('tags_word')
			if len(text) == 0:
				return render_template('photo.html', photos=photos, tags=tags, message="Please input some tags.", comments=comments, ownPhoto=ownPhoto, likeCount=likeCount, likes=likes)
			inputwords = text.split()
			inputlist = [s.encode('ascii', 'ignore') for s in inputwords]
			wordList = listToStr(inputlist)
			print "wordList: ", wordList
			# return render_template('hello.html', message='Welecome to Photoshare')
			cursor = conn.cursor()
			for word in inputlist:
				print 'update photo %s' % word
				test = isTagNotExist(word)
				if test:
					print "is not exist: ", word
					cursor.execute("INSERT INTO Tag (word) VALUES ('{0}')".format(word))
					conn.commit()
			recommendTags = getRecommendTags(wordList)
			if len(recommendTags) == 0:
				return render_template('photo.html', photos=photos, tags=tags, message="Do not have recommend tags.", comments=comments, ownPhoto=ownPhoto, recommendTags=recommendTags, likeCount=likeCount, likes=likes)
			else:
				return render_template('photo.html', photos=photos, tags=tags, comments=comments, ownPhoto=ownPhoto, recommendTags=recommendTags, likeCount=likeCount, likes=likes)
		elif request.form['submit'] == 'Add':
			text = request.form.get('tagToAdd')
			inputwords = text.split()
			inputwordsAsList = [s.encode('ascii', 'ignore') for s in inputwords]
			cursor = conn.cursor()
			for word in inputwordsAsList:
				test = isTagNotExist(word)
				if test:
					cursor.execute("INSERT INTO Tag (word) VALUES ('{0}')".format(word))
					conn.commit()
				cursor.execute("SELECT tag_id FROM Tag WHERE word = '{0}'".format(word))
				tag_id = cursor.fetchone()[0]
				try:
					cursor.execute("INSERT INTO Photo_Tag (photo_id, tag_id) VALUES ('{0}', '{1}')".format(photo_id, tag_id))
					conn.commit()
				except:
					return render_template('photo.html', photos=photos, tags=tags, message="Error in inserting tag to the photo", comments=comments, ownPhoto=ownPhoto, likeCount=likeCount, likes=likes)
		elif request.form['submit'] == 'Post':
			comment = request.form.get('comment')
			if flask_login.current_user.is_authenticated:
				owner_id = getUserIdFromEmail(flask_login.current_user.id)
			else:
				owner_id = getUserIdFromEmail('0000@Photoshare.com')
			print 'owner_id is: %s' % owner_id
			todaysdate = time.strftime('%Y-%m-%d')
			cursor = conn.cursor()
			try:
				cursor.execute("INSERT INTO Comments (texts, owner_id, date_created, photo_id) VALUES ('{0}', '{1}', '{2}', '{3}')".format(comment, owner_id, todaysdate, photo_id))
				conn.commit()
			except:
				return render_template('photo.html', photos=photos, tags=tags, message="There is an error in the SQL for posting comment", comments=comments, ownPhoto=ownPhoto, likeCount=likeCount, likes=likes)
		elif request.form['submit'] == 'Like':
			if not flask_login.current_user.is_authenticated:
				# only logged in user can like photos
				return render_template('unauth.html')
			user_id = getUserIdFromEmail(flask_login.current_user.id)
			cursor = conn.cursor()
			try:
				cursor.execute("INSERT INTO Likes (photo_id, user_id) VALUES ('{0}', '{1}')".format(photo_id, user_id))
				conn.commit()
			except:
				return render_template('photo.html', photos=photos, tags=tags, message="You have already liked this photo", comments=comments, ownPhoto=ownPhoto, likeCount=likeCount, likes=likes)
		tags = getTagsByPhotoId(photo_id)
		comments = getCommentsByPhotoId(photo_id)
		likeCount = likeCounts(photo_id)
		likes = getLikedUserList(photo_id)
		return render_template('photo.html', photos=photos, tags=tags, comments=comments, ownPhoto=ownPhoto, likeCount=likeCount, likes=likes)

@app.route('/browseByTag', methods=['GET', 'POST'])
@flask_login.login_required
def get_photo_by_tag():
	cursor = conn.cursor()
	if request.method == 'POST':
		owner_id = getUserIdFromEmail(flask_login.current_user.id)
		tag_id = request.form.get('tag_id')
		if request.form['category'] == 'my':
			print 'my photos'
			cursor.execute("SELECT p.photo_id, p.imgdata, p.caption, a.album_name, u.first_name, u.last_name FROM Photo_Tag pt, Photo p, Album a, Users u WHERE a.owner_id = u.user_id AND pt.photo_id = p.photo_id AND p.album_id = a.album_id AND pt.tag_id = '{0}' AND a.owner_id = '{1}'".format(tag_id, owner_id))
			photos = cursor.fetchall()
		else:
			print 'all photos'
			cursor.execute("SELECT p.photo_id, p.imgdata, p.caption, a.album_name, u.first_name, u.last_name FROM Photo_Tag pt, Photo p, Album a, Users u WHERE a.owner_id = u.user_id AND pt.photo_id = p.photo_id AND p.album_id = a.album_id AND pt.tag_id = '{0}'".format(tag_id))
			photos = cursor.fetchall()
		return render_template('tagPhotos.html', photos=photos)
	else:
		cursor.execute("SELECT t.tag_id, t.word FROM PhotoShare.Tag t, Photo_Tag pt where t.tag_id = pt.tag_id group by pt.tag_id")
		allTags = cursor.fetchall()
		popularTags = getPopularTags()
		return render_template('tagPhotos.html', allTags=allTags, popularTags=popularTags)

@app.route('/browseByPopularTag/<popularTagId>', methods=['GET', 'POST'])
@flask_login.login_required
def get_photo_by_popular_tag(popularTagId):
	cursor = conn.cursor()
	print "in browseByPopularTag get"
	cursor.execute("SELECT t.tag_id, t.word FROM PhotoShare.Tag t, Photo_Tag pt where t.tag_id = pt.tag_id group by pt.tag_id")
	allTags = cursor.fetchall()
	popularTags = getPopularTags()
	tag_id = popularTagId
	cursor.execute("SELECT p.photo_id, p.imgdata, p.caption, a.album_name, u.first_name, u.last_name FROM Photo_Tag pt, Photo p, Album a, Users u WHERE a.owner_id = u.user_id AND pt.photo_id = p.photo_id AND p.album_id = a.album_id AND pt.tag_id = '{0}'".format(tag_id))
	photos = cursor.fetchall()
	return render_template('tagPhotos.html', allTags=allTags, popularTags=popularTags, photos=photos)

@app.route('/photoSearch', methods=['POST'])
def search_photo_by_tag():
	cursor = conn.cursor()
	if request.method == 'POST':
		text = request.form.get('tags')
		print "search tags: %s" % text
		tags = text.split()
		pidquery = []
		tempTableName = ['a', 'b', 'c', 'd', 'e']
		query = 'SELECT DISTINCT a.photo_id FROM '
		if len(tags) == 0:
			return render_template('hello.html', message='Please input some tags')
		if len(tags) > 5:
			return render_template('hello.html', message='Please input no more than 5 tags')
		for index in range(len(tags)):
			if index == 0:
				pidquery.append("(SELECT pt.photo_id FROM Photo_Tag pt, Tag t WHERE pt.tag_id = t.tag_id AND t.word='" + tags[index] + "') AS " + tempTableName[index])
			else:
				pidquery.append(" INNER JOIN (SELECT pt.photo_id FROM Photo_Tag pt, Tag t WHERE pt.tag_id = t.tag_id AND t.word='" + tags[index] + "') AS " + tempTableName[index] + " ON " + tempTableName[index - 1] + ".photo_id = " + tempTableName[index] + ".photo_id")
			query += pidquery[index]
		print "query: %s" % query	
		cursor.execute(query)
		records = cursor.fetchall()
		pidsWithAllTags = [record[0] for record in records]
		# flatten pidsWithAllTags into a string
		ids = listToStr(pidsWithAllTags)
		print "id are: %s" %ids
		cursor.execute("SELECT p.photo_id, p.imgdata, p.caption FROM Photo p WHERE p.photo_id IN ({0})".format(ids))
		photos = cursor.fetchall()
		if len(photos) == 0:
			return render_template('hello.html', message='No photo contain all those tags', photos=photos)	
		return render_template('hello.html', message='Here are photos contain all the tags', photos=photos)

@app.route('/browseByAlbum', methods=['GET', 'POST'])
def search_photo_by_album():
	cursor.execute("SELECT a.album_id, a.album_name, a.owner_id, a.date_created, count(p.photo_id) FROM Album a, Photo p where a.album_id = p.album_id group by a.album_id having count(p.photo_id) > 0 ")
	albumList = cursor.fetchall()
	if request.method == 'POST':
		print "browseByAlbum POST"
		album_id = request.form.get('album_id')
		photos = getAlbumPhotos(album_id)
		cursor.execute("SELECT a.album_name, u.first_name, u.last_name FROM Album a, Users u WHERE a.owner_id = u.user_id AND a.album_id = '{0}'".format(album_id))
		albumInfo = cursor.fetchall()
		return render_template('browsePhotos.html', albumList=albumList, albumInfo=albumInfo, photos=photos)
	else:
		return render_template('browsePhotos.html', albumList=albumList)

@app.route('/recommend', methods=['GET', 'POST'])
@flask_login.login_required
def recommendations():
	user_id = getUserIdFromEmail(flask_login.current_user.id)
	mostCommonTags = getMostCommonTags(user_id)
	if len(mostCommonTags) == 0:
		return render_template('recommend.html', message='Cannot get recommendation, please add some tag to photos')
	mostCommonTagids = [record[0] for record in mostCommonTags]
	tagids = listToStr(mostCommonTagids)
	print "tagids are: %s" % tagids
	maylikes = getRecommendPhotoIds(tagids, user_id)
	if len(maylikes) == 0:
		return render_template('recommend.html', message='Cannot get recommendation, please add tag to more photos')
	maylikeids = [record[0] for record in maylikes]
	photoids = listToStr(maylikeids)
	print photoids
	photos = getRecommendPhotos(photoids)
	eachPhotoTags = []
	for pid in maylikeids:
		photoTags = getTagsByPhotoId(pid)
		photoTagWord = [record[1] for record in photoTags]
		tagwords = listToStr(photoTagWord)
		eachPhotoTags.append(tagwords)
	print "each photo tags: %s" %  eachPhotoTags
	if request.method == 'POST':
		photo_id = request.form.get('photo_id')
		cursor = conn.cursor()
		try:
			cursor.execute("INSERT INTO Likes (photo_id, user_id) VALUES ('{0}', '{1}')".format(photo_id, user_id))
			conn.commit()
		except:
			return render_template('recommend.html', photos=photos, tags=tags, message="Error in the sql for liking the photo")
		maylikes = getRecommendPhotoIds(tagids, user_id)
		maylikeids = [record[0] for record in maylikes]
		photoids = listToStr(maylikeids)
		print photoids
		photos = getRecommendPhotos(photoids)
		eachPhotoTags = []
		for pid in maylikeids:
			photoTags = getTagsByPhotoId(pid)
			photoTagWord = [record[1] for record in photoTags]
			tagwords = listToStr(photoTagWord)
			eachPhotoTags.append(tagwords)
		return render_template('recommend.html', mostCommonTags=mostCommonTags, photos=photos, eachPhotoTags=eachPhotoTags)
	else:
		return render_template('recommend.html', mostCommonTags=mostCommonTags, photos=photos, eachPhotoTags=eachPhotoTags)

@app.route('/stars', methods=['GET'])
def getStars():
	anonymous_id = getUserIdFromEmail('0000@Photoshare.com')
	cursor = conn.cursor()
	cursor.execute("SELECT u.user_id, u.first_name, u.last_name, u.email, COUNT(p.photo_id) + temp.CommentNums AS totalNums FROM (SELECT u.user_id, COUNT(c.comment_id) AS CommentNums FROM Users u LEFT JOIN Comments c ON c.owner_id = u.user_id GROUP BY u.user_id ) AS temp, Users u LEFT JOIN Album a NATURAL JOIN Photo p ON a.album_id = p.album_id AND a.owner_id = u.user_id WHERE u.user_id = temp.user_id AND u.user_id != '{0}' GROUP BY u.user_id ORDER BY totalNums DESC LIMIT 10".format(anonymous_id))
	vips = cursor.fetchall()
	return render_template('stars.html', vips=vips)

def extractData(cursor):
	data = []
	for item in cursor:
		data.append(item)
	return data

def listToStr(recordList):
	result = ''
	for index in range(len(recordList)):
		if index == len(recordList) - 1:
			result += "'" + (str)(recordList[index]) + "'"
		else:
			result +=  "'" + (str)(recordList[index]) + "'" + ', '
	return result

def getUserInfo():
	email = flask_login.current_user.id
	cursor = conn.cursor()
	cursor.execute("SELECT user_id, first_name, last_name, email, password, date_of_birth, gender, hometown FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()

def getFriendList():
	email = flask_login.current_user.id
	from_user_id = getUserIdFromEmail(email)
	cursor = conn.cursor()
	cursor.execute("SELECT U.user_id, U.first_name, U.last_name, U.email FROM Friendship F, Users U WHERE F.to_user_id = U.user_id AND F.from_user_id = '{0}'".format(from_user_id))
	return cursor.fetchall()

def getUnFriendList():
	from_user_id = getUserIdFromEmail(flask_login.current_user.id)
	cursor = conn.cursor()
	cursor.execute("SELECT u.user_id, u.first_name, u.last_name, u.email FROM Users u WHERE u.user_id NOT IN (SELECT to_user_id FROM Friendship WHERE from_user_id = '{0}') AND user_id != '{1}' AND u.email != '0000@Photoshare.com'".format(from_user_id, from_user_id))
	return cursor.fetchall()

def getMyAlbumList(owner_id):
	cursor = conn.cursor()
	cursor.execute("SELECT album_id, album_name, owner_id FROM Album WHERE owner_id = '{0}'".format(owner_id))
	return cursor.fetchall()

def getAlbumPhotos (album_id):
	cursor = conn.cursor()
	cursor.execute("SELECT imgdata, photo_id, caption FROM Photo WHERE album_id = '{0}' order by photo_id desc".format(album_id))
	return cursor.fetchall() #NOTE list of tuples, [(imgdata, pid), ...]

def getAlbumIdByPhoto(photo_id):
	cursor = conn.cursor()
	cursor.execute("SELECT album_id FROM Photo WHERE photo_id = '{0}'".format(photo_id))
	return cursor.fetchone()[0]

def getAllPhotos():
	cursor = conn.cursor()
	cursor.execute("SELECT photo_id, imgdata, caption, album_id FROM Photo order by photo_id desc")
	return cursor.fetchall()

def getAlbumInfo(album_id):
	cursor = conn.cursor()
	cursor.execute("SELECT album_id, album_name, owner_id, date_created FROM Album WHERE album_id = '{0}'".format(album_id))
	return cursor.fetchone()

def getPhotoById(photo_id):
	cursor = conn.cursor()
	cursor.execute("SELECT p.photo_id, p.imgdata, p.caption, p.album_id, a.owner_id FROM Photo p, Album a WHERE p.album_id = a.album_id AND p.photo_id = '{0}'".format(photo_id))
	return cursor.fetchall()

def getTagsByPhotoId(photo_id):
	cursor = conn.cursor()
	cursor.execute("SELECT t.tag_id, t.word FROM Photo_Tag pt, Tag t WHERE pt.tag_id = t.tag_id AND pt.photo_id = '{0}'".format(photo_id))
	return cursor.fetchall()

def isTagNotExist(word):
	cursor = conn.cursor()
	if cursor.execute("SELECT tag_id FROM Tag WHERE word = '{0}'".format(word)): 
		#this means there are greater than zero entries with that tag
		return False
	else:
		return True

def getPopularTags():
	cursor = conn.cursor()
	cursor.execute("SELECT t.tag_id, t.word, Popular.Occurance FROM Tag t INNER JOIN (SELECT tag_id, COUNT(photo_id) AS occurance FROM Photo_Tag GROUP BY tag_id ORDER BY occurance desc limit 5) As Popular ON t.tag_id = Popular.tag_id ORDER BY Popular.occurance DESC");
	return cursor.fetchall()

def getCommentsByPhotoId(photo_id):
	cursor = conn.cursor()
	cursor.execute("SELECT c.comment_id, c.texts, c.date_created, u.first_name, u.last_name FROM Comments c, Users u WHERE c.owner_id = u.user_id AND c.photo_id = '{0}' ORDER BY c.comment_id DESC".format(photo_id))
	return cursor.fetchall()

def isYourOwnPhoto(photo_owner_id):
	if not flask_login.current_user.is_authenticated:
		user_id = getUserIdFromEmail('0000@Photoshare.com')
	else:
		user_id = getUserIdFromEmail(flask_login.current_user.id)
	return user_id == photo_owner_id

def likeCounts(photo_id):
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM Likes WHERE photo_id = '{0}'".format(photo_id))
	return cursor.fetchone()[0]

def getLikedUserList(photo_id):
	cursor = conn.cursor()
	cursor.execute("SELECT u.first_name, u.last_name, u.email FROM Likes l, Users u WHERE l.user_id = u.user_id AND l.photo_id = '{0}'".format(photo_id))
	return cursor.fetchall()

def getMostCommonTags(user_id):
	cursor = conn.cursor()
	cursor.execute("SELECT pt.tag_id, t.word, COUNT(photo_id) AS occurance FROM Photo_Tag pt, Tag t WHERE pt.tag_id = t.tag_id AND pt.photo_id IN (SELECT photo_id FROM Photo p, Album a WHERE p.album_id = a.album_id AND a.owner_id = '{0}') GROUP BY pt.tag_id ORDER BY occurance DESC LIMIT 5".format(user_id))
	return extractData(cursor)

def getRecommendPhotoIds(tagids, user_id):
	cursor = conn.cursor()
	cursor.execute("SELECT pt.photo_id, COUNT(pt.tag_id) AS CommonTags, Total.TotalTags FROM Photo_Tag pt, (SELECT photo_id, COUNT(tag_id) AS TotalTags FROM Photo_Tag GROUP BY photo_id) AS Total WHERE pt.photo_id = Total.photo_id AND pt.tag_id IN ({0}) AND pt.photo_id NOT IN (SELECT l.photo_id FROM Likes l WHERE l.user_id = '{1}') GROUP BY pt.photo_id ORDER BY CommonTags DESC, TotalTags ASC".format(tagids, user_id))
	return extractData(cursor)

def getRecommendPhotos(photoids):
	cursor = conn.cursor()
	cursor.execute("SELECT p.photo_id, p.imgdata, p.caption, a.album_name, u.first_name, u.last_name FROM Photo p, Album a, Users u WHERE p.album_id = a.album_id AND a.owner_id = u.user_id AND p.photo_id IN ({0}) ORDER BY field(p.photo_id, {1})".format(photoids, photoids))
	return extractData(cursor)

def getRecommendTags(wordList):
	cursor = conn.cursor()
	cursor.execute("SELECT t1.tag_id, t1.word FROM Tag t1, (SELECT pt.tag_id, COUNT(pt.photo_id) AS occurance FROM Photo_Tag pt WHERE pt.photo_id IN (SELECT pt.photo_id FROM Photo_Tag pt, Tag t WHERE t.tag_id = pt.tag_id AND t.word IN ({0})) AND pt.tag_id NOT IN (SELECT  tag_id FROM Tag WHERE word IN ({1})) GROUP BY pt.tag_id) as temp where temp.tag_id = t1.tag_id ORDER BY temp.occurance DESC limit 5".format(wordList, wordList))
	return cursor.fetchall()
#end add code by Ang Li

#default page  
@app.route("/", methods=['GET'])
def hello():
	photos = getAllPhotos();
	return render_template('hello.html', message='Welecome to Photoshare', photos=photos)


if __name__ == "__main__":
	#this is invoked when in the shell  you run 
	#$ python app.py 
	app.run(port=5000, debug=True)
