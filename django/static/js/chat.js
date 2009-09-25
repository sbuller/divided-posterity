//Global variables
var username = "";
var roomname = "";
var public_key = "";
var numlines_inchatbox = 0;
var last_chatlineid;
var shift=false;
var chatRoomRefreshTimeout = 100;
var currentScrollHeight = 0;
var elapsedTimeFromLastResponse = 0;

//ArrayOfPending
var AOPtext = [];
AOPtext[100] = "";
var startAOP = 0;
var endAOP = 0;
var StopRefreshing = false;


//////////////////////////
//	Login Functions
//////////////////////////

function chat_show_login()
{
	userinput = document.getElementById("chat_username_input");
	userinput.disabled=false;
	$("#chat_username_input").val('Type in your username...');
	passinput = document.getElementById("chat_password_input");
	passinput.disabled=false;
	$("#chat_password_input").val('*****');

	document.getElementById("chat_button_userpass").disabled = false;
	document.getElementById("chat_button_createuserpass").disabled = false;

	userinput.style.color = "#D3D3D3";
	passinput.style.color = "#D3D3D3";

	chat_passwordtyping = false;
	chat_usernametyping = false;

	$("#chat_userprofile").show(400);
}

function CreateUserRequest()
{
	var ausername = document.getElementById("chat_username").value;
	var apassword = document.getElementById("chat_password").value;
	$.get("/ChatCommand.CreateUser",{username:ausername, password:apassword}, ReceiveCreateUserRequest)
}

function ReceiveCreateUserRequest(response)
{
	alert(response);
}

function chat_Login()
{
	if (chat_checkUserPass())
	{
		var ausername = document.getElementById("chat_username_input").value;
		var apassword = document.getElementById("chat_password_input").value;

		document.getElementById("chat_username_input").disabled=true;
		document.getElementById("chat_password_input").disabled=true;
		document.getElementById("chat_button_userpass").disabled=true;
		document.getElementById("chat_button_createuserpass").disabled=true;

		$.post("/ChatCommand.Login",{username:ausername,password:apassword},chat_login_callback);
	}
	return false;
}

function chat_login_callback(response)
{
	if (response == "ack")
	{
		username = document.getElementById("chat_username_input").value;
		$("#chat_userprofile").hide(300,chat_showjoinroom);
	}
	else
	{
		document.getElementById("chat_username_input").disabled=false;
		document.getElementById("chat_password_input").disabled=false;
		document.getElementById("chat_button_userpass").disabled=false;
		document.getElementById("chat_button_createuserpass").disabled=false;
		alert(response);
	}
}

function chat_CreateUser()
{
	if (chat_checkUserPass())
	{
		var ausername = document.getElementById("chat_username_input").value;
		var apassword = document.getElementById("chat_password_input").value;

		document.getElementById("chat_username_input").disabled=true;
		document.getElementById("chat_password_input").disabled=true;
		document.getElementById("chat_button_userpass").disabled=true;
		document.getElementById("chat_button_createuserpass").disabled=true;

		$.post("/ChatCommand.CreateUser",{username:ausername,password:apassword},chat_createuser_callback);
	}
	return false;
}

function chat_createuser_callback(response)
{
	if (response == "ack")
		alert("acknowledged");
	else
	{
		alert(response);
	}
	document.getElementById("chat_username_input").disabled=false;
	document.getElementById("chat_password_input").disabled=false;
	document.getElementById("chat_button_userpass").disabled=false;
	document.getElementById("chat_button_createuserpass").disabled=false;
}

var chat_usernametyping = false;
function chat_username_focused(o)
{
	if (!chat_usernametyping)
	{
		chat_usernametyping = true;
		o.value = "";
		o.style.color = "black";
	}
}

var chat_passwordtyping;
function chat_password_focused(o)
{
	if (!chat_passwordtyping)
	{
		chat_passwordtyping = true;
		o.value = "";
		o.style.color = "black";
	}
}

function chat_checkUserPass()
{
	if (!chat_usernametyping)
	{
		$("#chat_username_input").fadeTo(200,0.1,function () { $("#chat_username_input").fadeTo(300,1.0);} );
	}
	else if (!chat_passwordtyping)
	{
		$("#chat_password_input").fadeTo(200,0.1,function () { $("#chat_password_input").fadeTo(300,1.0);} );
	}
	return chat_usernametyping && chat_passwordtyping;
}

//////////////////////////
//	Join ChatRoom Functions
//////////////////////////

function chat_showjoinroom()
{
	roomname_input = document.getElementById("chat_roomname_input");
	roomname_input.disabled=false;
	roomname_input.style.color = "#D3D3D3";
	document.getElementById("chat_joinroom_button").disabled=false;
	chat_roomnametyping = false;

	$("#chat_roomname_input").val('Type in the roomname...');

	document.getElementById("chat_username_label").innerHTML = "Welcome, " + username + ". Please join a room. You can create a room by merely joining it.";
	$("#chat_joinroom_div").show(400);
}

var chat_roomnametyping = false;
function chat_roomname_focused(o)
{
	if (!chat_roomnametyping)
	{
		o.value = "";
		o.style.color = "black";
		chat_roomnametyping = true;
	}
}

function chat_checkRoomname()
{
	return true;
}

function chat_JoinRoom()
{
	document.getElementById("chat_roomname_input").disabled=true;
	document.getElementById("chat_joinroom_button").disabled=true;

	if (chat_checkRoomname())
	{
		$.post("/ChatCommand.JoinRoom",{username:username,roomname:document.getElementById("chat_roomname_input").value},chat_JoinRoom_callback);
	}
	else
	{
		document.getElementById("chat_roomname_input").disabled=false;
		document.getElementById("chat_joinroom_button").disabled=false;
	}
	return false;
}

function chat_JoinRoom_callback(response)
{

	response_tokens = response.split("\n");

	ack = response_tokens[0];

	if (ack == "ack")
	{
		roomname = document.getElementById("chat_roomname_input").value;
		StopRefreshing = false;
		$("#chat_joinroom_div").hide(300,chat_main_function);

		newP = document.createElement("p");
		newP.style.margin = "5px";
		newP.innerHTML += TextEdit("b","Joined Room " + roomname + ".");
		newP.style.fontSize = "8pt";
		last_chatlineid = -1;

		chatmessages_body = document.getElementById("chat_messages_div");
		chatmessages_body.appendChild(newP);
	}
	else
	{
		document.getElementById("chat_roomname_input").disabled=false;
		document.getElementById("chat_joinroom_button").disabled=false;
		alert(response);
	}
}

//////////////////////////
//	ChatRoom Functions
//////////////////////////

function chat_main_function()
{
	document.getElementById("chat_message_textarea").onkeyup = chat_message_textarea_keyUpEvent;
	document.getElementById("chat_message_textarea").onkeydown = chat_message_textarea_keyDownEvent;
	document.getElementById("chat_message_textarea").value='';

	startAOP = 0;
	endAOP = 0;

	currentScrollHeight = 0;
	chatRoomRefreshTimeout = 50;
	document.getElementById("chat_roomname_label").innerHTML = "Room: " + roomname;
	chat_RefreshRoom();
	$("#chat_main").show(400);
}

function chat_message_textarea_keyDownEvent (e)
{
	var KeyID = (window.event) ? event.keyCode : e.keyCode;
	if (KeyID == 16) //16 = shift
	{
		shift = true;
	}
}

function chat_message_textarea_keyUpEvent (e)
{
	var KeyID = (window.event) ? event.keyCode : e.keyCode;
	if (KeyID == 13 && !shift) //13 = enter
	{
		chat_SendMessageRequest();
	}
	else if (KeyID == 16)
	{
		shift = false;
	}
}

function chat_SendMessageRequest ()
{
	var unformattedMessage = document.getElementById("chat_message_textarea").value;
	var messageArray = unformattedMessage.split("\n");
	var message = "";
	var start, end;
	for (start = 0; start < messageArray.length && messageArray[start] == ""; start++);
	for (end = messageArray.length-1; end >= 0 && messageArray[end] == ""; end--);
	for (i = start; i <= end; i++)
		message += messageArray[i] + "<br>";
	$("#chat_message_textarea").val("");
	if (message != "")
	{
		$.post("/ChatCommand.SendMessage", {username:username, roomname:roomname, message:message}, chat_ReceiveSendMessage);

		pendingLabel = document.getElementById("chat_pendingmessage_label");

		if (endAOP != startAOP)
		{

			ourlength = (endAOP + 1)%AOPtext.length-startAOP;
			if (ourlength < 0)
			{
				ourlength = (endAOP + 1)%AOPtext.length + AOPtext.length-startAOP;
			}
			pendingLabel.innerHTML = "Pending " + ourlength + " messages";
			$(pendingLabel).fadeIn(200);
			AOPtext[endAOP] = message;

		}
		else
		{
			pendingLabel.innerHTML = "Pending: " + message;
			$(pendingLabel).fadeIn(200);
			AOPtext[endAOP] = message;
		}

		endAOP = (endAOP + 1)%AOPtext.length;
	}
	//chat_RefreshRoom();
}

function chat_ReceiveSendMessage (response)
{
	if (response == "ack")
	{
		chatRoomRefreshTimeout = 0;
	}
	else alert(response);
}


function chat_RefreshRoom ()
{
	if (StopRefreshing)
		return;
	if (elapsedTimeFromLastResponse > chatRoomRefreshTimeout)
	{
		$.post("/ChatCommand.RefreshRoom", {username:username, roomname:roomname, requested_line:last_chatlineid+1}, chat_ReceiveRefreshRoom);
	}
	else
	{
		timeout = 50;
		elapsedTimeFromLastResponse += timeout;
		setTimeout(chat_RefreshRoom,timeout);
	}
}

function chat_ReceiveRefreshRoom (response)
{
	response_tokens = response.split("\n");

	ack = response_tokens[0];

	if (ack == "ack")
	{
		numchatlines = parseInt(response_tokens[1]);

		if (numchatlines > 0)
		{

			index = 2;

			chatmessages_body = document.getElementById("chat_messages_div");

			innerHTML = document.getElementById("chat_messages_p").innerHTML;

			pendingLabel = document.getElementById("chat_pendingmessage_label");

			for (i = 0; i < numchatlines; i++)
			{
				chatline_username = response_tokens[index++];
				chatline_id = response_tokens[index++];
				chatline_text = response_tokens[index++];
				last_chatlineid = parseInt(chatline_id);

				if (chatline_username == username)
				{
					chatline_text = AOPtext[startAOP];
					startAOP = (startAOP+1)%AOPtext.length;

					if (endAOP == startAOP)
					{
						$(pendingLabel).fadeOut(300);
					}
					else
					{
						ourlength = endAOP - startAOP;
						if (ourlength < 0)
							ourlength = endAOP + AOPtext.length-startAOP;

						if (ourlength == 1)
							pendingLabel.innerHTML = "Pending: " + AOPtext[startAOP];
						else
							pendingLabel.innerHTML = "Pending " + ourlength + " messages.";
					}
				}

				newP = document.createElement("p");
				newP.style.margin = "0px";
				newP.innerHTML += TextEdit("b",chatline_username);
				newP.innerHTML += ": " + chatline_text;

				chatmessages_body.appendChild(newP);

				numlines_inchatbox++;
			}

			document.getElementById("chat_messages_p").innerHTML = innerHTML;

			if (true)
			{
				chatmessages_body.scrollTop = chatmessages_body.scrollHeight;
				currentScrollHeight = chatmessages_body.scrollTop;
			}
			chatRoomRefreshTimeout = 300;
		}
		else
		{
			if (chatRoomRefreshTimeout < 5000)
			chatRoomRefreshTimeout = chatRoomRefreshTimeout*2;
		}
		elapsedTimeFromLastResponse = 0;
		chat_RefreshRoom();
	}
}

function TextEdit(effect, text)
{
	p = "";
	p += "<"+effect+">";
	p += text;
	p += "</" +effect+ ">";
	return p;
}

function chat_ExitRoom()
{
	StopRefreshing = true;

	newP = document.createElement("p");
	newP.style.margin = "5px";
	newP.innerHTML += TextEdit("b","Exited Room " + roomname + ".");
	newP.style.fontSize = "8pt";
	chatmessages_body = document.getElementById("chat_messages_div");
	chatmessages_body.appendChild(newP);

	$("#chat_main").hide(400)

	$.post("/ChatCommand.ExitRoom", {username:username, roomname:roomname}, chat_ReceiveExitRoom);
}

function chat_ReceiveExitRoom(response)
{
	response_tokens = response.split("\n");

	ack = (response_tokens[0] == "ack");

	if (ack)
	{
		chat_showjoinroom();
	}
}

function chat_Logout()
{
	document.getElementById("chat_messages_div").innerHTML = "<p id=\"chat_messages_p\"></p>"
	$("#chat_joinroom_div").hide(400);
	$.post("/ChatCommand.ExitRoom", {username:username, public_key:""}, chat_show_login);
}
//////////////////////////
//	End Of Functions
//////////////////////////

$(document).ready(function(){
	$("#chat_username_input").removeAttr("disabled");
	$("#chat_username_input").val('Type in your username...');

	$("#chat_password_input").removeAttr("disabled");
	$("#chat_password_input").val('*****');


	$("#chat_roomname_input").css("width","100%");

	$("#chat_pendingmessage_label").hide(0);
})