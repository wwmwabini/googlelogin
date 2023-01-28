import os
import requests

from flask import render_template, redirect, url_for, request, json, flash
from flask_login import login_user, current_user, logout_user, login_required
from googlelogin import app, oauth,db

from googlelogin.models import Users
from googlelogin.forms import LoginForm


def get_google_provider_cfg():
    return requests.get(os.environ.get('GOOGLE_OAUTH2_DISCOVERY_ENDPOINT')).json()


@app.route("/", methods=["GET", "POST"])
def login():

	form = LoginForm()

	if request.method == 'POST':
	   google_provider_cfg = get_google_provider_cfg()

	   authorization_endpoint = google_provider_cfg["authorization_endpoint"]

	   request_uri = oauth.prepare_request_uri(
		   authorization_endpoint,
		   redirect_uri=request.base_url+"login/callback",
		   scope=["openid", "email", "profile"],
		   )

	   return redirect(request_uri)
	return render_template('login.html', form=form)



@app.route("/login/callback")
def callback():

	code = request.args.get("code")

	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]

	token_url, headers, body = oauth.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code

	)

	token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(os.environ.get('GOOGLE_OAUTH2_CLIENT_ID'), os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')),

	)

	oauth.parse_request_body_response(json.dumps(token_response.json()))


	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]

	uri, headers, body = oauth.add_token(userinfo_endpoint)

	userinfo_response = requests.get(uri, headers=headers, data=body)

	print(userinfo_response)

	if userinfo_response.json().get("email_verified"):
		unique_id = userinfo_response.json()["sub"]
		user_email = userinfo_response.json()["email"]
		user_name = userinfo_response.json()["given_name"]
	else:
		return "User email not available or not verified by Google.", 400


	user = Users.query.filter_by(email=user_email).first()
	

	if not user:
		newuser = Users(unique_id=unique_id, name=user_name, email=user_email)
		db.session.add(newuser)
		db.session.commit()
		flash("User does not exist but has now been created. Please login again", 'info')
		return redirect(url_for('login'))
	else:
	    login_user(user)
	    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():

	users = Users.query.all()
	return render_template("dashboard.html", users=users)


@app.route("/logout")
@login_required
def logout():
	logout_user()
	return render_template('logout.html')