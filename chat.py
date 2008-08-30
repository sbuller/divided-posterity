import cgi
import wsgiref.handlers
import thread, time
from google.appengine.ext import db

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import memcache

#Model
  
class Room(db.Model):
	roomname = db.StringProperty()
	name_of_creator = db.StringProperty()
	line_index = db.IntegerProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class User(db.Model):
	username = db.StringProperty()
	password = db.StringProperty()
	public_key = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	
class UserInstance(db.Model):
	last_chatline_id = db.IntegerProperty()
	username = db.StringProperty()
	roomname = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class Chatline(db.Model):
	id = db.IntegerProperty()
	text = db.StringProperty()
	username = db.StringProperty()
	roomname = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

#Viewer/Controller

def IsValidString(aString):
	return 1
		
def RefreshRoom(self, username, roomname, firstId, room):

	chatlinequery = db.GqlQuery("SELECT * FROM Chatline WHERE roomname =:1 AND id >=:2 AND ANCESTOR IS:3 ORDER BY id ASC",roomname,firstId,room)
	
	messages = ("ack\n%d\n"%(chatlinequery.count()))
	for message in chatlinequery:
		if message.username == username:
			messages += ("%s\n%d\n%s\n"%(message.username,message.id," "))
		else:
			messages += ("%s\n%d\n%s\n"%(message.username,message.id,message.text))
			
	self.response.out.write(messages)

def JoinRoom(self,username,roomname):
	#check to see if the username is in the datastore
	userquery = db.GqlQuery("SELECT * FROM User WHERE username = :1 LIMIT 1", username)
	if userquery.count() == 0:
		self.response.out.write("Error: User %s doesn't exist"%(username))
		return

	#the user exists, now check to see if the room has been created
	roomquery = db.GqlQuery("SELECT * FROM Room WHERE roomname = :1 LIMIT 1",roomname)
	room = roomquery.get()

	#if room has not been created, now create room. So yes, you need to join the room to create the room
	if roomquery.count() == 0: 
		room = Room()
		room.roomname = roomname
		room.name_of_creator = username
		room.line_index = 0
		room.put()
		#now join the room
		user_instance = UserInstance()
		user_instance.last_chatline_id = room.line_index
		user_instance.username = username
		user_instance.roomname = roomname
		user_instance.put()
	#else simply check to see if the user is already inside of the room
	else:
		user_instance_query = db.GqlQuery("SELECT * FROM UserInstance WHERE username = :1 AND roomname = :2 LIMIT 1", username, roomname)
		user_instance = user_instance_query.get()
		#if user_instance_query doesn't exist, then create one
		if user_instance_query.count() == 0:
			user_instance = UserInstance()
			user_instance.last_chatline_id = room.line_index
			user_instance.username = username
			user_instance.roomname = roomname
			user_instance.put()
		#else if user does exist in room, then update the last_chatline_id
		else:
			#self.response.out.write("ack");#Error: User %s is already inside Room %s"%(username,roomname))
			user_instance.last_chatline_id = room.line_index
			user_instance.put()
	self.response.out.write("ack")

class RefreshRoomRequest(webapp.RequestHandler):
	def post(self):

		username = self.request.get('username')
		roomname = self.request.get('roomname')
		first_id = int(self.request.get('requested_line'))
		
		roomquery = db.GqlQuery("SELECT * FROM Room WHERE roomname = :1 LIMIT 1",roomname)
		user_instance_query = db.GqlQuery("SELECT * From UserInstance WHERE username = :1 AND roomname = :2 LIMIT 1",username, roomname)
		
		
		
		#if no room exists, then error
		if roomquery.count() == 0:
			self.response.out.write("Error: Room %s doesn't exist.",roomname);
			return
		#else if room exists but user is not part of it, return error
		if user_instance_query.count() == 0:
			self.response.out.write("Error: User %s is not part of the room %s.",username,roomname);
			return
			
		#room exists and user is part of it, 
		room = roomquery.get()
		user_instance = user_instance_query.get()
		
		if first_id < user_instance.last_chatline_id:
			first_id = user_instance.last_chatline_id
		
		RefreshRoom(self, user_instance.username, room.roomname, first_id, room)
		
class SendMessageRequest(webapp.RequestHandler):
	def post(self):
	
		roomname = self.request.get('roomname')
		username = self.request.get('username')
		message = self.request.get('message')
		
		if not IsValidString(message):
			self.response.out.write("Error: Message \"%s\" is invalid"%(username))
			return

		userquery = db.GqlQuery("SELECT * FROM User WHERE username = :1 LIMIT 1",username)
		roomquery = db.GqlQuery("SELECT * FROM Room WHERE roomname = :1 LIMIT 1",roomname)
		user_instance_query = db.GqlQuery("SELECT * FROM UserInstance WHERE username = :1 AND roomname = :2",username,roomname)
		
		#if user doesn't exist, then simply abort
		if userquery.count() == 0:
			self.response.out.write("Error: User %s doesn't exist"%(username))
			return
		
		#if room doesn't exist, then simply abort
		if roomquery.count() == 0:
			self.response.out.write("Error: Room %s doesn't exist"%(roomname))
			return
		
		#if user is not part of room, then join the room
		if user_instance_query.count() == 0:
			JoinRoom(self,username,roomname)
		
		
		#user exists, room exists, the user has an instance with the room, now just create the message
		user = userquery.get()
		room = roomquery.get()
		id = room.line_index
		room.line_index += 1
		room.put()
		user_instance = user_instance_query.get()
		
		newchatline = Chatline(parent=room)
		newchatline.id = id
		newchatline.username = username
		newchatline.roomname = roomname
		newchatline.text = message
		newchatline.put()
		self.response.out.write("ack")

class CreateUserRequest(webapp.RequestHandler):
	def post(self):
		
		username = self.request.get('username')
		password = self.request.get("password")
		
		if not IsValidString(username) or not IsValidString(password):
			self.response.out.write("Error: username or password contained illegal characters")
		else:
			userquery = db.GqlQuery("SELECT * FROM User WHERE username = :1 LIMIT 1",username)
			if userquery.count() == 0: #User doesn't exist, please create a new user
				user = User()
				user.username = username
				user.password = password
				user.public_key = ""
				user.put()
				self.response.out.write("ack")
			else:
				self.response.out.write("Error: User \"%s\" already exists. User is not being created."%(username))

class LogoutRequest(webapp.RequestHandler):
	def post(self):
		username = self.request.get('username')
		public_key = self.request.get("public_key") #this key will be encrypted via its own key (ie when decrypted, this key will match the current key)
		
		userquery = db.GqlQuery("SELECT * FROM User WHERE username = :1 LIMIT 1",username)
		if userquery.count() == 0: #User doesn't exist, respond with User DNE
			self.response.out.write("Error: Username doesn't exist")
		else: #User exists, just ack now (once security bumps in, we ack and update the RSA public key)
			user = userquery.get()
			user.public_key = "";
			user.put();
			
			userinstance_query = db.GqlQuery("SELECT * FROM UserInstance WHERE username = :1 LIMIT 1",username)
			db.delete(userinstance_query.fetch())
			
			self.response.out.write("ack")

class LoginRequest(webapp.RequestHandler):
	def post(self):
		
		username = self.request.get('username')
		password = self.request.get("password")
		
		userquery = db.GqlQuery("SELECT * FROM User WHERE username = :1 AND password =:2 LIMIT 1",username,password)
		if userquery.count() == 0: #User doesn't exist, respond with User DNE
			self.response.out.write("Error: Username/Password doesn't exist")
		else: #User exists, just ack now (once security bumps in, we ack and update the RSA public key)
			self.response.out.write("ack")

class JoinRoomRequest(webapp.RequestHandler):
	def post(self):
		
		roomname = self.request.get('roomname')
		username = self.request.get('username')
		
		#if the username or roomname cannot be cleaned, they will be empty strings
		if not IsValidString(roomname):
			self.response.out.write("Error: username or roomname contained illegal characters")
			return
			
		JoinRoom(self,username,roomname)
		
def ExitRoom(self,username,roomname):
	#check to see if the username is in the datastore
	userquery = db.GqlQuery("SELECT * FROM User WHERE username = :1 LIMIT 1", username)
	if userquery.count() == 0:
		self.response.out.write("Error: User %s doesn't exist"%(username))
		return
	
	#now check to see if the user is in the particular room by checking its instance with the room
	user_instance_query = db.GqlQuery("SELECT * FROM UserInstance WHERE username = :1 AND roomname = :2 LIMIT 1", username, roomname)
	user_instance = user_instance_query.get()
	#if user_instance_query doesn't exist, then error
	if user_instance_query.count() == 0:
		self.response.out.write("Error: user doesn't exist")
		return
	#else if user does exist in room, then erase user
	else:
		db.delete(user_instance)
	self.response.out.write("ack")

class ExitRoomRequest(webapp.RequestHandler):
	def post(self):
		
		roomname = self.request.get('roomname')
		username = self.request.get('username')
		
		#if the username or roomname cannot be cleaned, they will be empty strings
		if not IsValidString(roomname):
			self.response.out.write("Error: username or roomname contained illegal characters")
			return
			
		ExitRoom(self,username,roomname)
			
    
def main():
	application = webapp.WSGIApplication(
									   [
										('/ChatCommand.JoinRoom', JoinRoomRequest),
										('/ChatCommand.ExitRoom', ExitRoomRequest),
										('/ChatCommand.RefreshRoom', RefreshRoomRequest),
										('/ChatCommand.SendMessage', SendMessageRequest),
										('/ChatCommand.CreateUser', CreateUserRequest),
										('/ChatCommand.Logout', LogoutRequest),
										('/ChatCommand.Login', LoginRequest)
									   ],
									   debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
  
