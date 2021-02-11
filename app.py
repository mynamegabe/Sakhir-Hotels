from flask import Flask, Response, render_template, request, redirect, url_for, session, send_from_directory
from Forms import CreateDishForm, CreateUserForm, CreatePromoForm, CreateTempForm, CreateSignupForm, CreateLoginForm, CreateRoomSearchForm, CreateUserSearchForm, CreateChatForm, CreateDetailsForm, CreateUpdateDetailsForm, CreateSwabForm, CreateUpdateSwabForm, CreateRoomForm, UpdateBookingForm, UpdateContactForm, UpdateReviewForm, CreateStaffForm, UpdateStaffForm, UpdateRestaurantForm
import datetime, hashlib, requests, shelve, os, User, Promo, SwabLog, Chat, Room, ChatLog, TempLog, Booking, BookingLog, Contact, Review, Restaurant, OpeningHours, Dish, Staff
from werkzeug.utils import secure_filename
from authy.api import AuthyApiClient
import pytesseract
from PIL import Image
from re import search
from ast import literal_eval

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__, static_url_path='',static_folder='static')
app.secret_key = "fiegclub"
app.config.from_object('config')
api = AuthyApiClient(app.config['AUTHY_API_KEY'])

@app.route('/', methods=['GET', 'POST'])
def home(booked=""):
    dict = homepage()
    if dict['roomlist'] != None:
        roomcount = len(dict['roomlist'])
    else:
        roomcount = 0

    swab = False
    try:
        if session["Swab"] == True:
            swab = True
        session.pop("Swab",None)
    except:
        print("None")
    return render_template("home.html",promo_list=loadpromo(),restaurant_list=loadrestaurants(),form=dict["form"],chat=dict["chat"],support=dict["support"], searchform=dict["search"], rooms=dict["roomlist"], roomcount=roomcount, swab=swab,booked=booked)

@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    dict = initSupport()
    return render_template("rooms.html",promo_list=loadpromo(),restaurant_list=loadrestaurants(),form=dict["form"],chat=dict["chat"],support=dict["support"])

@app.route('/a-rooms', methods=['GET', 'POST'])
def retrieve_rooms():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        db = shelve.open('storage.db', 'r')
        room_dict = db['Rooms']
        db.close()

        studio_list = []
        regular_list = []
        suite_list = []

        room_list = []
        for key in room_dict:
            room = room_dict.get(key)
            room_list.append(room)

        for room in room_list:
            if room.get_category() == "Studio":
                studio_list.append(room)
            elif room.get_category() == "Regular":
                regular_list.append(room)
            elif room.get_category() == "Suite":
                suite_list.append(room)

        return render_template('a-rooms.html', studio_list=studio_list, regular_list=regular_list, suite_list=suite_list)
    else:
        return "Unauthorized"

@app.route('/a-deleteRoom/<int:id>', methods=['POST'])
def delete_room(id):

    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        room_dict = {}
        db = shelve.open('storage.db', 'w')
        room_dict = db['Rooms']

        room_dict.pop(id)

        db['Rooms'] = room_dict
        db.close()

        return redirect(url_for('retrieve_rooms'))
    else:
        return "Unauthorized"

@app.route('/a-createRoom', methods=['GET', 'POST'])
def create_room():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        create_room_form = CreateRoomForm(request.form)
        if request.method == 'POST' and create_room_form.validate():
            room_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                room_dict = db['Rooms']
            except:
                print("Error in retrieving Rooms from storage.db.")

            room = Room.Room(create_room_form.category.data, create_room_form.room_name.data, create_room_form.rooms.data,
                             create_room_form.avail_rooms.data, create_room_form.price.data,
                             create_room_form.capacity.data, create_room_form.details.data)
            room_dict[room.get_room_id()] = room
            db['Rooms'] = room_dict

            db.close()

            return redirect(url_for('retrieve_rooms'))
        return render_template('createRoom.html', form=create_room_form)
    else:
        return "Unauthorized"

@app.route('/a-updateRoom/<int:id>/', methods=['GET', 'POST'])
def update_room(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        update_room_form = CreateRoomForm(request.form)
        if request.method == 'POST' and update_room_form.validate():
            room_dict = {}
            db = shelve.open('storage.db', 'w')
            room_dict = db['Rooms']

            room = room_dict.get(id)
            room.set_room_name(update_room_form.room_name.data)
            room.set_rooms(update_room_form.rooms.data)
            room.set_avail_rooms(update_room_form.avail_rooms.data)
            room.set_price(update_room_form.price.data)
            room.set_capacity_list(update_room_form.capacity.data)
            room.set_details_list(update_room_form.details.data)

            db['Rooms'] = room_dict
            db.close()

            return redirect(url_for('retrieve_rooms'))
        else:
            room_dict = {}
            db = shelve.open('storage.db', 'r')
            room_dict = db['Rooms']
            db.close()

            room = room_dict.get(id)
            update_room_form.room_name.data = room.get_room_name()
            update_room_form.rooms.data = room.get_rooms()
            update_room_form.avail_rooms.data = room.get_avail_rooms()
            update_room_form.price.data = room.get_price()
            update_room_form.capacity.data = room.get_capacity_list()
            update_room_form.details.data = room.get_detail_list()

            return render_template('updateRoom.html', form=update_room_form)
    else:
        return "Unauthorized"


@app.route('/rooms/studio-rooms', methods=['GET', 'POST'])
def studio():
    dict = initSupport()
    db = shelve.open('storage.db', 'r')
    rooms_dict = db['Rooms']
    db.close()

    room_list = []
    for key in rooms_dict:
        room = rooms_dict[key]
        if room.get_category() == "Studio":
            room_list.append(room)

    return render_template('studio.html',promo_list=loadpromo(),restaurant_list=loadrestaurants(),form=dict["form"],chat=dict["chat"],support=dict["support"],rooms=room_list)

@app.route('/rooms/regular-rooms', methods=['GET', 'POST'])
def regular():
    dict = initSupport()
    db = shelve.open('storage.db', 'r')
    rooms_dict = db['Rooms']
    db.close()

    room_list = []
    for key in rooms_dict:
        room = rooms_dict[key]
        if room.get_category() == "Regular":
            room_list.append(room)

    return render_template('regular.html',promo_list=loadpromo(),restaurant_list=loadrestaurants(),form=dict["form"],chat=dict["chat"],support=dict["support"],rooms=room_list)

@app.route('/rooms/suites', methods=['GET', 'POST'])
def suites():
    dict = initSupport()
    db = shelve.open('storage.db', 'r')
    rooms_dict = db['Rooms']
    db.close()

    room_list = []
    for key in rooms_dict:
        room = rooms_dict[key]
        if room.get_category() == "Suite":
            room_list.append(room)

    return render_template('suites.html',promo_list=loadpromo(),restaurant_list=loadrestaurants(),form=dict["form"],chat=dict["chat"],support=dict["support"],rooms=room_list)

@app.route('/contactUs', methods=['GET', 'POST'])
def contact_us():
    if request.method == "POST":
        data = request.form
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        tel = data['tel']
        msg = data['msg']
        contact = Contact.Contact(firstname, lastname, email, tel, msg)
        db = shelve.open('storage.db', 'c')
        contact_dict = db['Contacts']
        contact_dict[contact.get_contact_id()] = contact
        db['Contacts'] = contact_dict
        dict = initSupport()
        return render_template('contact.html', promo_list=loadpromo(),restaurant_list=loadrestaurants(), form=dict["form"], chat=dict["chat"],support=dict["support"])
    else:
        dict = initSupport()
        return render_template('contact.html',promo_list=loadpromo(),restaurant_list=loadrestaurants(),form=dict["form"],chat=dict["chat"],support=dict["support"])

@app.route('/a-contacts', methods=['GET'])
def retrieve_contacts():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        db = shelve.open('storage.db', 'r')
        contacts_dict = db['Contacts']
        db.close()

        contacts_list = []
        for key in contacts_dict:
            contact = contacts_dict.get(key)
            contacts_list.append(contact)


        return render_template('a-contacts.html', count=len(contacts_list), contact_list=contacts_list)
    else:
        return "Unauthorized"

@app.route('/a-deleteContact/<int:id>', methods=['POST'])
def delete_contact(id):

    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        db = shelve.open('storage.db', 'w')
        contacts_dict = db['Contacts']

        contacts_dict.pop(id)

        db['Contacts'] = contacts_dict
        db.close()

        return redirect(url_for('retrieve_contacts'))
    else:
        return "Unauthorized"

@app.route('/a-updateContact/<int:id>/', methods=['GET', 'POST'])
def update_contact(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        update_contact_form = UpdateContactForm(request.form)
        if request.method == 'POST' and update_contact_form.validate():
            db = shelve.open('storage.db', 'w')
            contacts_dict = db['Contacts']

            contact = contacts_dict.get(id)
            contact.set_name(update_contact_form.name.data)
            contact.set_email(update_contact_form.email.data)
            contact.set_tel(update_contact_form.tel.data)
            contact.set_msg(update_contact_form.msg.data)


            db['Contacts'] = contacts_dict
            db.close()

            return redirect(url_for('retrieve_contacts'))
        else:
            db = shelve.open('storage.db', 'r')
            contacts_dict = db['Contacts']
            db.close()

            contact = contacts_dict.get(id)
            update_contact_form.name.data = contact.get_name()
            update_contact_form.email.data = contact.get_email()
            update_contact_form.tel.data = contact.get_tel()
            update_contact_form.msg.data = contact.get_msg()

            return render_template('updateContact.html', form=update_contact_form)
    else:
        return "Unauthorized"

@app.route('/promotions', methods=['GET', 'POST'])
def promotions():
    dict = initSupport()
    return render_template('promotions.html',promo_list=loadpromo(),restaurant_list=loadrestaurants(),form=dict["form"],chat=dict["chat"],support=dict["support"])

@app.route('/promotion/<cn>', methods=['GET', 'POST'])
def promotion(cn):
    dict = initSupport()
    db = shelve.open('storage.db', 'r')
    promo_dict = db['Promotions']
    db.close()
    for i in promo_dict:
        if promo_dict[i].get_promo_cn() == cn:
            promoid = promo_dict[i].get_promo_id()
    promoselect = promo_dict[promoid]
    return render_template('promotion.html',promo=promoselect)

@app.route('/swabtest', methods=['GET', 'POST'])
def swabtest():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        if users_dict[i].get_username() == session["login"]:
            userid = users_dict[i].get_user_id()

    user = users_dict[userid]
    swab_form = CreateSwabForm(request.form)
    if request.method == "POST" and swab_form.validate():
        log = SwabLog.SwabLog(user.get_user_id(), swab_form.ic.data, swab_form.first_name.data, swab_form.last_name.data,swab_form.swabcheck.data)
        db = shelve.open('storage.db', 'c')
        swab_dict = db["SwabLogs"]
        swab_dict[user.get_user_id()] = log
        db["SwabLogs"] = swab_dict
        db.close()
        return redirect(url_for('home'))
    else:
        swab_form.first_name.data = user.get_first_name()
        swab_form.last_name.data = user.get_last_name()
        return render_template('swabtest.html',form=swab_form)

@app.route('/profile',methods=["GET","POST"])
def profile():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    bookings_dict = db['Bookings']
    db.close()
    if request.method == "POST":
        session.pop("login",None)
        return redirect(url_for("home"))
    for i in users_dict:
        if users_dict[i].get_username() == session["login"]:
            userid = users_dict[i].get_user_id()
    user1 = users_dict[userid]

    booking_list = []
    for booking in user.get_bookings():
        booking_list.append(bookings_dict[booking])
    return render_template('profile.html',user=user1, booking_list=booking_list)

@app.route('/resetpw',methods=["POST"])
def resetpw():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        if users_dict[i].get_username() == session["login"]:
            userid = users_dict[i].get_user_id()

    user = users_dict[userid]

    oldpw = request.form['old']
    newpw = request.form['new']
    confirmpw = request.form['confirm']
    if user.get_password() == sha256(oldpw+"shho"):
        if newpw == confirmpw:
            db = shelve.open('storage.db', 'c')
            users_dict = db['Users']
            user.set_password(sha256(newpw+"shho"))
            users_dict[user.get_user_id()] = user
            db['Users'] = users_dict

            db.close()
            return "Password changed"
        else:
            return "Confirm password different from New password"
    else:
        return "Password incorrect"

@app.route('/admin')
def admin():

    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        return render_template('admin.html')
    else:
        return "Unauthorized"


@app.route('/a-createUser', methods=['GET', 'POST'])
def create_user():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        create_user_form = CreateUserForm(request.form)
        if request.method == 'POST' and create_user_form.validate():
            users_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                users_dict = db['Users']
            except:
                print("Error in retrieving Users from storage.db.")

            user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
                             create_user_form.birthdate.data, create_user_form.countrycode.data, create_user_form.phonenumber.data,
                             create_user_form.gender.data, create_user_form.membership.data,
                             create_user_form.remarks.data, create_user_form.pw.data, "Unverified")
            users_dict[user.get_user_id()] = user
            db['Users'] = users_dict

            db.close()

            return redirect(url_for('retrieve_users'))
        return render_template('createUser.html', form=create_user_form)
    else:
        return "Unauthorized"

@app.route('/a-updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        update_user_form = CreateUserForm(request.form)
        if request.method == 'POST' and update_user_form.validate():
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Users']

            user = users_dict.get(id)
            user.set_first_name(update_user_form.first_name.data)
            user.set_last_name(update_user_form.last_name.data)
            user.set_gender(update_user_form.gender.data)
            user.set_membership(update_user_form.membership.data)
            user.set_remarks(update_user_form.remarks.data)
            user.set_password(sha256(update_user_form.pw.data+"shho"))

            db['Users'] = users_dict
            db.close()

            return redirect(url_for('retrieve_users'))
        else:
            users_dict = {}
            db = shelve.open('storage.db', 'r')
            users_dict = db['Users']
            db.close()

            user = users_dict.get(id)
            update_user_form.first_name.data = user.get_first_name()
            update_user_form.last_name.data = user.get_last_name()
            update_user_form.gender.data = user.get_gender()
            update_user_form.membership.data = user.get_membership()
            update_user_form.remarks.data = user.get_remarks()

            return render_template('updateUser.html', form=update_user_form)
    else:
        return "Unauthorized"



@app.route('/a-deleteUser/<int:id>', methods=['POST'])
def delete_user(id):

    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        users_dict.pop(id)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        return "Unauthorized"


@app.route('/a-users', methods=['GET', 'POST'])
def retrieve_users():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        count = 0
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)
            count += 1
        search_user_form = CreateUserSearchForm(request.form)
        if request.method == 'POST' and search_user_form.validate():
            users_list = []
            db = shelve.open('storage.db', 'w')
            users_dict = db['Users']

            usersearch = search_user_form.username.data
            if usersearch.isnumeric():
                try:
                    users_list = [users_dict[int(usersearch)]]
                except:
                    users_list = "None"
            elif usersearch.isalnum():
                for i in users_dict:
                    if usersearch.lower() in users_dict[i].get_username().lower():
                        userid = users_dict[i].get_user_id()
                        users_list = [users_dict[userid]]
                    else:
                        users_list ="None"
            else:
                users_list = "Invalid"
        return render_template('users.html', count=count, users_list=users_list, form=search_user_form)
    else:
        return "Unauthorized"



@app.route('/a-templogs')
def retrieve_templogs():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        temp_dict = {}
        db = shelve.open('storage.db', 'r')
        temp_dict = db['TempLogs']
        db.close()

        temp_list = []
        for key in temp_dict:
            temp = temp_dict.get(key)
            temp_list.append(temp)

        return render_template('templogs.html', count=len(temp_list), temp_list=temp_list)
    else:
        return "Unauthorized"

@app.route('/a-createTempLog', methods=['GET', 'POST'])
def create_templog():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        create_templog_form = CreateTempForm(request.form)
        if request.method == 'POST' and create_templog_form.validate():
            db = shelve.open('storage.db', 'c')
            try:
                templogs_dict = db['TempLogs']
            except:
                print("Error in retrieving Temperature Logs from storage.db.")
            member_id = create_templog_form.id.data
            try:
                member = users_dict[member_id]
            except:
                return "User not found"
            temperature = create_templog_form.temperature.data
            temp_log = TempLog.TempLog(member.get_user_id(), member.get_username(), temperature, member.get_swabcheck())
            templogs_dict[temp_log.get_templog_id()] = temp_log
            db['TempLogs'] = templogs_dict

            db.close()

            return redirect(url_for('retrieve_templogs'))
        return render_template('createTempLog.html', form=create_templog_form)
    else:
        return "Unauthorized"

@app.route('/a-deleteTempLog/<int:id>', methods=['POST'])
def delete_TempLog(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        templogs_dict = {}
        db = shelve.open('storage.db', 'w')
        templogs_dict = db['TempLogs']

        templogs_dict.pop(id)

        db['TempLogs'] = templogs_dict
        db.close()

        return redirect(url_for('retrieve_templogs'))
    else:
        return "Unauthorized"

@app.route('/a-updateTempLog/<int:id>/', methods=['GET', 'POST'])
def update_templog(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        create_temp_form = CreateTempForm(request.form)
        if request.method == 'POST' and create_temp_form.validate():
            templogs_dict = {}
            db = shelve.open('storage.db', 'w')
            templogs_dict = db['TempLogs']

            templog = templogs_dict.get(id)
            member_id = create_temp_form.id.data
            try:
                member = users_dict[member_id]
            except:
                return "User not found"

            templog.set_username(member.get_username())
            templog.set_user_id(member.get_user_id())
            templog.set_swabcheck(member.get_swabcheck())
            templog.set_temperature(create_temp_form.temperature.data)


            db['TempLogs'] = templogs_dict
            db.close()

            return redirect(url_for('retrieve_templogs'))
        else:
            db = shelve.open('storage.db', 'r')
            templogs_dict = db['TempLogs']
            db.close()

            templog = templogs_dict.get(id)
            create_temp_form.id.data = templog.get_templog_id()
            create_temp_form.temperature.data = templog.get_temperature()

            return render_template('updateTempLog.html', form=create_temp_form)
    else:
        return "Unauthorized"


@app.route('/a-swablogs')
def retrieve_swablogs():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        swab_dict = {}
        db = shelve.open('storage.db', 'r')
        swab_dict = db['SwabLogs']
        db.close()

        swab_list = []
        for key in swab_dict:
            swab = swab_dict.get(key)
            swab_list.append(swab)

        return render_template('swablogs.html', count=len(swab_list), swab_list=swab_list)
    else:
        return "Unauthorized"


@app.route('/a-promotions')
def retrieve_promotions():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        promo_dict = {}
        db = shelve.open('storage.db', 'r')

        promo_dict = db['Promotions']

        db.close()

        promo_list = []
        for key in promo_dict:
            promo = promo_dict.get(key)
            promo_list.append(promo)

        return render_template('a-promotions.html', count=len(promo_list), promo_list=promo_list)
    else:
        return "Unauthorized"

@app.route('/a-createPromotion', methods=['GET', 'POST'])
def create_promo():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        create_promo_form = CreatePromoForm(request.form)
        if request.method == 'POST' and create_promo_form.validate():
            promo_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                promo_dict = db['Promotions']
            except:
                print("Error in retrieving Promotions from storage.db.")
            promo_cn = create_promo_form.promo_name.data.lower().replace(" ","-")
            #retrieve filename first
            with open("promo_filename.txt", "r+") as p:
                file_name = p.read()
                p.close()
            with open('promo_filename.txt', 'w+') as p:
                p.truncate(0)
                p.close()
            if file_name != "":
                os.rename("static/Images/" + file_name,"static/Images/" + promo_cn + file_name[-4:].lower())
                promo = Promo.Promo(create_promo_form.promo_name.data, promo_cn, create_promo_form.desc.data, create_promo_form.endDate.data, create_promo_form.remarks.data)
                promo_dict[promo.get_promo_id()] = promo
                db['Promotions'] = promo_dict
            else:
                return "No image uploaded, please upload image and press 'Submit'"

            db.close()

            return redirect(url_for('retrieve_promotions'))
        return render_template('createPromotion.html', form=create_promo_form)
    else:
        return "Unauthorized"

@app.route('/promoimgupload', methods=['GET', 'POST'])
def upload_promoimg():
    if request.method == 'POST':
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        for i in users_dict:
            try:
                if users_dict[i].get_username() == session["login"]:
                    userid = users_dict[i].get_user_id()
            except:
                return "Not logged in"
        if users_dict[userid].get_membership() == "A" and session["auth"] == True:

            f = request.files['file']
            if allowed_file(f.filename):
                f.save("static/Images/"+secure_filename(f.filename))
                with open('promo_filename.txt', 'w+') as p:
                    p.truncate(0)
                    p.write(secure_filename(f.filename))
                    p.close()
                    return "File uploaded, return to tab"
            else:
                return "File type not accepted"

@app.route('/a-updatePromo/<int:id>/', methods=['GET', 'POST'])
def update_promo(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        update_promo_form = CreatePromoForm(request.form)
        if request.method == 'POST' and update_promo_form.validate():
            promo_dict = {}
            db = shelve.open('storage.db', 'w')
            promo_dict = db['Promotions']

            promo = promo_dict.get(id)
            promo.set_promo_name(update_promo_form.promo_name.data)
            promo.set_desc(update_promo_form.desc.data)
            promo.set_endDate(update_promo_form.endDate.data)
            promo.set_remarks(update_promo_form.remarks.data)

            db['Promotions'] = promo_dict
            db.close()

            return redirect(url_for('retrieve_promotions'))
        else:
            promo_dict = {}
            db = shelve.open('storage.db', 'r')
            promo_dict = db['Promotions']
            db.close()

            promo = promo_dict.get(id)
            update_promo_form.promo_name.data = promo.get_promo_name()
            update_promo_form.desc.data = promo.get_desc()
            update_promo_form.endDate.data = promo.get_endDate()
            update_promo_form.remarks.data = promo.get_remarks()

            return render_template('updatePromo.html', form=update_promo_form)
    else:
        return "Unauthorized"

@app.route('/a-deletePromo/<int:id>', methods=['POST'])
def delete_promo(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        promo_dict = {}
        db = shelve.open('storage.db', 'w')
        promo_dict = db['Promotions']

        promo_dict.pop(id)

        db['Promotions'] = promo_dict
        db.close()

        return redirect(url_for('retrieve_promotions'))
    else:
        return "Unauthorized"

@app.route('/a-chatusers', methods=['GET', 'POST'])
def retrieve_chats():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        count = 0
        db = shelve.open('storage.db', 'r')
        chats_dict = db['Chats']
        chatlogs_dict = db['ChatLogs']
        db.close()

        chats_list = []
        for key in chats_dict:
            chat = chats_dict.get(key)
            chats_list.append(chat)
            if chat.get_status() == "Incomplete":
                count += 1

        chatlogs_list = []
        for key in chatlogs_dict:
            chatlog = chatlogs_dict.get(key)
            chatlogs_list.append(chatlog)
        return render_template('chats.html', count=count, chats_list=chats_list, chatlogs_list=chatlogs_list)
    else:
        return "Unauthorized"

@app.route('/a-deleteChat/<int:id>', methods=['GET', 'POST'])
def delete_chat(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        db = shelve.open('storage.db', 'w')
        chats_dict = db['Chats']
        chat = chats_dict[id]
        chats_dict.pop(id)
        db['Chats'] = chats_dict

        chatlogs_dict = db['ChatLogs']
        chat_log = ChatLog.ChatLog(chat.get_name(), chat.get_email(), chat.get_phone(),chat.get_query())
        chat_log.set_status("Complete")
        chatlogs_dict[chat_log.get_chatlog_id()] = chat_log
        db['ChatLogs'] = chatlogs_dict
        db.close()

        return redirect(url_for('retrieve_chats'))
    else:
        return "Unauthorized"

@app.route('/a-deleteChatLog/<int:id>', methods=['GET', 'POST'])
def delete_chatlog(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        db = shelve.open('storage.db', 'w')
        chatlogs_dict = db['ChatLogs']
        chatlogs_dict.pop(id)
        db['ChatLogs'] = chatlogs_dict

        return redirect(url_for('retrieve_chats'))
    else:
        return "Unauthorized"

@app.route('/a-updateChatLog/<int:id>/', methods=['GET', 'POST'])
def update_chatlog(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        update_details_form = CreateUpdateDetailsForm(request.form)
        if request.method == 'POST' and update_details_form.validate():
            db = shelve.open('storage.db', 'w')
            chatlogs_dict = db['ChatLogs']

            chatlog = chatlogs_dict.get(id)
            chatlog.set_name(update_details_form.name.data)
            chatlog.set_email(update_details_form.email.data)
            chatlog.set_phone(update_details_form.phone.data)
            chatlog.set_query(update_details_form.query.data)

            db['ChatLogs'] = chatlogs_dict
            db.close()

            return redirect(url_for('retrieve_chats'))
        else:
            db = shelve.open('storage.db', 'r')
            chatlogs_dict = db['ChatLogs']
            db.close()

            chatlog = chatlogs_dict.get(id)
            update_details_form.name.data = chatlog.get_name()
            update_details_form.email.data = chatlog.get_email()
            update_details_form.phone.data = chatlog.get_phone()
            update_details_form.query.data = chatlog.get_query()

            return render_template('updateChatLog.html', form=update_details_form)
    else:
        return "Unauthorized"

@app.route('/a-chatlog/<int:id>', methods=['GET', 'POST'])
def chatlog(id):
    if request.method != 'POST':
        db = shelve.open('storage.db', 'r')
        chatlogs_dict = db['ChatLogs']
        chatlog = chatlogs_dict[id]
        chatlist = chatlog.get_chat()
        db.close()
        return render_template("chatlog.html", chat=chatlist, info=chat)

@app.route('/a-chat/<int:id>', methods=['GET', 'POST'])
def chat(id):
    chat_form = CreateChatForm(request.form)
    if request.method != 'POST':
        db = shelve.open('storage.db', 'r')
        chats_dict = db['Chats']
        chat = chats_dict[id]
        chatlist = chat.get_chat()
        db.close()
        return render_template("chat.html", form=chat_form, chat=chatlist, info=chat)
    elif request.method == 'POST' and chat_form.validate():
        if chat_form.inputtext.data == "reload":
            db = shelve.open('storage.db', 'c')
            chats_dict = db['Chats']
            chat = chats_dict[id]
            chatlist = chat.get_chat()
            chat_form.inputtext.data = ""
            return render_template("chat.html", form=chat_form, chat=chatlist, info=chat)
        elif len(chat_form.inputtext.data) > 0:
            db = shelve.open('storage.db', 'c')
            chats_dict = db['Chats']
            chat = chats_dict[id]
            chatlist = chat.get_chat()
            chatlist.append("admn:" + chat_form.inputtext.data)
            chat.set_chat(chatlist)
            chats_dict[id] = chat
            db['Chats'] = chats_dict
            chat_form.inputtext.data = ""
            return render_template("chat.html", form=chat_form, chat=chatlist, info=chat)

@app.route('/a-updateChat/<int:id>/', methods=['GET', 'POST'])
def update_chat(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        update_details_form = CreateUpdateDetailsForm(request.form)
        if request.method == 'POST' and update_details_form.validate():
            chats_dict = {}
            db = shelve.open('storage.db', 'w')
            chats_dict = db['Chats']

            chat = chats_dict.get(id)
            chat.set_name(update_details_form.name.data)
            chat.set_email(update_details_form.email.data)
            chat.set_phone(update_details_form.phone.data)
            chat.set_query(update_details_form.query.data)

            db['Chats'] = chats_dict
            db.close()

            return redirect(url_for('retrieve_chats'))
        else:
            chats_dict = {}
            db = shelve.open('storage.db', 'r')
            chats_dict = db['Chats']
            db.close()

            chat = chats_dict.get(id)
            update_details_form.name.data = chat.get_name()
            update_details_form.email.data = chat.get_email()
            update_details_form.phone.data = chat.get_phone()
            update_details_form.query.data = chat.get_query()

            return render_template('updateChat.html', form=update_details_form)
    else:
        return "Unauthorized"

@app.route('/login', methods=['GET', 'POST'])
def login():
    create_login_form = CreateLoginForm(request.form)
    if request.method == 'POST' and create_login_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']

        for userid in users_dict:
            user = users_dict[userid]
            if user.get_username() == create_login_form.username.data:
                if user.get_password() == sha256(create_login_form.pw.data+"shho"):
                    session["login"] = user.get_username()
                    if user.get_membership() == "A":
                        session["auth"] = True
                    return redirect(url_for('home'))
        return "<h1>Invalid credentials</h1>"
        #return redirect(url_for('login'))
    return render_template('login.html', form=create_login_form)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    create_signup_form = CreateSignupForm(request.form)
    if request.method == 'POST' and create_signup_form.validate():
        country_code = request.form.get("country_code")
        phone_number = create_signup_form.phonenumber.data
        session['first_name'] = create_signup_form.first_name.data
        session['last_name'] = create_signup_form.last_name.data
        session['gender'] = create_signup_form.gender.data
        session['birthdate'] = create_signup_form.birthdate.data
        session['country_code'] = country_code
        session['phone_number'] = phone_number
        session['password'] = create_signup_form.pw.data
        api.phones.verification_start(phone_number, country_code, via='sms')
        return redirect(url_for("verify"))
    return render_template('signup.html', form=create_signup_form)

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        token = request.form.get("token")

        phone_number = session.get("phone_number")
        country_code = session.get("country_code")

        verification = api.phones.verification_check(phone_number,
                                                     country_code,
                                                     token)

        if verification.ok():
            db = shelve.open('storage.db', 'c')

            try:
                users_dict = db['Users']
            except:

                print("Error in retrieving Users from storage.db.")
            user = User.User(session.get("first_name"), session.get("last_name"),
                             session.get("gender"),
                             session.get("birthdate"), session.get("country_code"),
                             session.get("phone_number"), "C", "", sha256(session.get("password")),
                             "Unverified")
            users_dict[user.get_user_id()] = user
            db['Users'] = users_dict

            db.close()

            session["login"] = user.get_username()
            return redirect(url_for('home'))
        else:
            return "Nope"

    return render_template("verify.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if allowed_file(f.filename):

            db = shelve.open('storage.db', 'r')
            users_dict = db['Users']
            db.close()

            for i in users_dict:
                if users_dict[i].get_username() == session["login"]:
                        userid = users_dict[i].get_user_id()

            username = users_dict[userid].get_username()
            try:
                f.save("swabtests/"+secure_filename(f.filename))
            except:
                print("File with same name already in server")
                os.remove("swabtests/"+secure_filename(f.filename))
                f.save("swabtests/"+secure_filename(f.filename))

            try:
                os.rename("swabtests/"+secure_filename(f.filename),"swabtests/"+username+f.filename[-4:].lower())
            except:
                print("User has already submitted swab test image, overwriting old image")
                os.remove("swabtests/"+username+f.filename[-4:].lower())
                os.rename("swabtests/" + secure_filename(f.filename), "swabtests/" + username + f.filename[-4:].lower())
            pytesseract.pytesseract.tesseract_cmd = ('Tesseract-OCR/tesseract.exe')
            img = 'swabtests/' + username + f.filename[-4:].lower()
            img_text = pytesseract.image_to_string(Image.open(img))
            ic_search = search('[0-9]{3}[a-zA-Z]{1}',img_text)
            db = shelve.open('storage.db', 'c')
            users_dict = db['Users']
            if ic_search and "negative" in img_text.lower():
                users_dict[userid].set_swabcheck("Negative")
                try:
                    swab_dict = db["SwabLogs"]
                except:
                    print("Error opening dictionary")
                user = users_dict[userid]
                log = SwabLog.SwabLog(user.get_user_id(), ic_search.group(0), user.get_first_name(), user.get_last_name(), "Negative")
                swab_dict[user.get_user_id()] = log
                db["SwabLogs"] = swab_dict
                db.close()
                return "Swab test verified"
            elif ic_search and "positive" in img_text.lower():
                users_dict[userid].set_swabcheck("Positive")
                try:
                    swab_dict = db["SwabLogs"]
                except:
                    print("Error opening dictionary")
                user = users_dict[userid]
                log = SwabLog.SwabLog(user.get_user_id(), ic_search.group(0), user.get_first_name(), user.get_last_name(), "Positive")
                swab_dict[user.get_user_id()] = log
                db["SwabLogs"] = swab_dict
                db.close()
                return "Swab test positive, not verified"
            elif not ic_search:
                return "Last 4 digits IC not found"
        else:
            return "File type not accepted"

@app.route('/a-updateSwab/<int:id>/', methods=['GET', 'POST'])
def update_swab(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        update_swab_form = CreateUpdateSwabForm(request.form)
        if request.method == 'POST' and update_swab_form.validate():
            swab_dict = {}
            db = shelve.open('storage.db', 'w')
            swab_dict = db['SwabLogs']

            swab = swab_dict.get(id)
            swab.set_ic(update_swab_form.ic.data)
            swab.set_first_name(update_swab_form.first_name.data)
            swab.set_last_name(update_swab_form.last_name.data)
            swab.set_swabcheck(update_swab_form.swabcheck.data)

            db['SwabLogs'] = swab_dict
            db.close()

            return redirect(url_for('retrieve_swablogs'))
        else:
            swab_dict = {}
            db = shelve.open('storage.db', 'r')
            swab_dict = db['SwabLogs']
            db.close()

            swab = swab_dict.get(id)
            update_swab_form.ic.data = swab.get_ic()
            update_swab_form.first_name.data = swab.get_first_name()
            update_swab_form.last_name.data = swab.get_last_name()
            update_swab_form.swabcheck.data = swab.get_swabcheck()

            return render_template('updateSwab.html', form=update_swab_form)
    else:
        return "Unauthorized"

@app.route('/a-deleteSwabLog/<int:id>', methods=['POST'])
def delete_SwabLog(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        swab_dict = {}
        db = shelve.open('storage.db', 'w')
        swab_dict = db['SwabLogs']

        swab_dict.pop(id)

        db['SwabLogs'] = swab_dict
        db.close()

        return redirect(url_for('retrieve_swablogs'))
    else:
        return "Unauthorized"

@app.route('/uploads/<filename>', methods=['GET','POST'])
def uploaded_file(filename):
    return send_from_directory("swabtests/",filename=filename)

@app.route('/a-bookings', methods=['GET', 'POST'])
def retrieve_bookings():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        room_dict = {}
        db = shelve.open('storage.db', 'c')
        booking_dict = db['Bookings']
        bookinglog_dict = db['BookingLogs']

        today = datetime.date.today()
        currentdate = today.strftime("%d/%m/%Y")

        for key in booking_dict:
            booking = booking_dict.get(key)
            if booking.get_endDate() == currentdate:
                bookinglog = BookingLog.BookingLog(booking.get_customer_id(),booking.get_room_type(),booking.get_customer_name(),booking.get_startDate(),booking.get_endDate())
                bookinglog_dict[bookinglog.get_booking_id()] = bookinglog
                booking_dict.pop(key)
        db['Bookings'] = booking_dict
        db['BookingLogs'] = bookinglog_dict
        db.close()

        booking_list = []
        for key in booking_dict:
            booking = booking_dict.get(key)
            booking_list.append(booking)

        return render_template('a-bookings.html', booking_list=booking_list, count=len(booking_list))
    else:
        return "Unauthorized"

@app.route('/a-bookinglogs', methods=['GET', 'POST'])
def retrieve_bookinglogs():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        db = shelve.open('storage.db', 'c')
        booking_dict = db['Bookings']
        bookinglog_dict = db['BookingLogs']

        today = datetime.date.today()
        currentdate = today.strftime("%d/%m/%Y")

        for key in booking_dict:
            booking = booking_dict.get(key)
            if booking.get_endDate() == currentdate:
                bookinglog = BookingLog.BookingLog(booking.get_customer_id(),booking.get_room_type(),booking.get_customer_name(),booking.get_startDate(),booking.get_endDate())
                bookinglog_dict[bookinglog.get_booking_id()] = bookinglog
                booking_dict.pop(key)
        db['Bookings'] = booking_dict
        db['BookingLogs'] = bookinglog_dict
        db.close()

        bookinglog_list = []
        for key in bookinglog_dict:
            bookinglog = bookinglog_dict.get(key)
            bookinglog_list.append(bookinglog)

        return render_template('a-bookinglogs.html', bookinglog_list=bookinglog_list, count=len(bookinglog_list))
    else:
        return "Unauthorized"

@app.route('/a-deleteBooking/<int:id>', methods=['POST'])
def delete_booking(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        db = shelve.open('storage.db', 'w')
        booking_dict = db['Bookings']

        booking_dict.pop(id)

        db['Bookings'] = booking_dict
        db.close()

        return redirect(url_for('retrieve_bookings'))
    else:
        return "Unauthorized"

@app.route('/a-deleteBookingLog/<int:id>', methods=['POST'])
def delete_bookinglog(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        db = shelve.open('storage.db', 'w')
        bookinglog_dict = db['BookingLogs']

        bookinglog_dict.pop(id)

        db['BookingLogs'] = bookinglog_dict
        db.close()

        return redirect(url_for('retrieve_bookinglogs'))
    else:
        return "Unauthorized"

def sha256(hash_string):
    sha_signature = \
        hashlib.sha256((hash_string+"shho").encode()).hexdigest()
    return sha_signature

@app.route('/a-updateBooking/<int:id>/', methods=['GET', 'POST'])
def update_booking(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        update_booking_form = UpdateBookingForm(request.form)
        if request.method == 'POST' and update_booking_form.validate():
            db = shelve.open('storage.db', 'w')
            booking_dict = db['Rooms']

            booking = booking_dict.get(id)
            booking.set_customer_id(update_booking_form.customerid.data)
            booking.set_customer_name(update_booking_form.customername.data)
            booking.set_room_type(update_booking_form.room_type.data)
            booking.set_startDate(update_booking_form.startdate.data)
            booking.set_endDate(update_booking_form.enddate.data)

            db['Bookings'] = booking_dict
            db.close()

            return redirect(url_for('retrieve_bookings'))
        else:
            db = shelve.open('storage.db', 'r')
            booking_dict = db['Bookings']
            db.close()

            booking = booking_dict.get(id)
            update_booking_form.customerid.data = booking.get_customer_id()
            update_booking_form.customername.data = booking.get_customer_name()
            update_booking_form.room_type.data = booking.get_room_type()
            update_booking_form.startdate.data = booking.get_startDate()
            update_booking_form.enddate.data = booking.get_endDate()

            return render_template('updateBooking.html', form=update_booking_form)
    else:
        return "Unauthorized"

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    db = shelve.open('storage.db', 'r')
    reviews_dict = db['Reviews']
    users_dict = db['Users']
    db.close()

    reviews_list = []
    for key in reviews_dict:
        reviews_list.append(reviews_dict.get(key))

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
                user = users_dict[userid]
        except:
            user = "None"
    if request.method == "GET":
        return render_template('reviews.html', reviews_list = reviews_list, user=user)
    elif request.method == "POST":
        db = shelve.open('storage.db', 'c')
        reviews_dict = db['Reviews']
        data = request.form
        review = Review.Review(data['username'],data['email'],int(data['rating']),data['title'],data['body'])
        reviews_dict[review.get_review_id()] = review
        db['Reviews'] = reviews_dict

        reviews_list = []
        for key in reviews_dict:
            reviews_list.append(reviews_dict.get(key))
        db.close()
        return render_template('reviews.html',reviews_list = reviews_list, user=user)

@app.route('/a-reviews')
def retrieve_reviews():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        db = shelve.open('storage.db', 'r')

        reviews_dict = db['Reviews']

        db.close()

        reviews_list = []
        for key in reviews_dict:
            review = reviews_dict.get(key)
            reviews_list.append(review)

        return render_template('a-reviews.html', count=len(reviews_list), reviews_list=reviews_list)
    else:
        return "Unauthorized"

@app.route('/a-deleteReview/<int:id>', methods=['POST'])
def delete_review(id):

    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        db = shelve.open('storage.db', 'w')
        reviews_dict = db['Reviews']

        reviews_dict.pop(id)

        db['Reviews'] = reviews_dict
        db.close()

        return redirect(url_for('retrieve_reviews'))
    else:
        return "Unauthorized"

@app.route('/a-updateReview/<int:id>/', methods=['GET', 'POST'])
def update_review(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        update_review_form = UpdateReviewForm(request.form)
        if request.method == 'POST' and update_review_form.validate():
            db = shelve.open('storage.db', 'w')
            reviews_dict = db['Reviews']

            review = reviews_dict.get(id)
            review.set_name(update_review_form.name.data)
            review.set_email(update_review_form.email.data)
            review.set_rating(int(update_review_form.rating.data))
            review.set_title(update_review_form.title.data)
            review.set_review(update_review_form.review.data)
            review.set_date(update_review_form.date.data)

            db['Reviews'] = reviews_dict
            db.close()

            return redirect(url_for('retrieve_reviews'))
        else:
            db = shelve.open('storage.db', 'r')
            reviews_dict = db['Reviews']
            db.close()

            review = reviews_dict.get(id)
            update_review_form.name.data = review.get_name()
            update_review_form.email.data = review.get_email()
            update_review_form.rating.data = str(review.get_rating())
            update_review_form.title.data = review.get_title()
            update_review_form.review.data = review.get_review()
            update_review_form.date.data = review.get_date()

            return render_template('updateReview.html', form=update_review_form)
    else:
        return "Unauthorized"

@app.route('/restaurants/<name>',methods=['GET','POST'])
def restaurant(name):
    db = shelve.open('storage.db', 'r')
    restaurants_dict = db['Restaurants']
    db.close()
    restaurant = restaurants_dict[name]
    return render_template('restaurant.html',restaurant=restaurant,restaurant_list=loadrestaurants())

def loadrestaurants():
    db = shelve.open('storage.db', 'r')
    restaurant_dict = db['Restaurants']
    db.close()

    restaurant_list = []
    for key in restaurant_dict:
        restaurant = restaurant_dict.get(key)
        restaurant_list.append(restaurant)
    print(restaurant_list)
    return restaurant_list

@app.route('/a-restaurants')
@app.route('/a-restaurants/<name>')
def retrieve_restaurant(name="None"):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        db = shelve.open('storage.db', 'r')

        restaurants_dict = db['Restaurants']

        db.close()

        restaurants_list = []
        for key in restaurants_dict:
            restaurant = restaurants_dict.get(key)
            restaurants_list.append(restaurant)
        if name in list(restaurants_dict.keys()):
            restaurant = restaurants_dict.get(name)
        else:
            restaurant = restaurants_dict.get(list(restaurants_dict.keys())[0])

        staff_list = []
        for key in restaurant.get_staff_list():
            staff = restaurant.get_staff_list().get(key)
            staff_list.append(staff)
        return render_template('a-restaurants.html', restaurant=restaurant, count=len(restaurants_list), restaurants_list=restaurants_list, staff_list=staff_list)
    else:
        return "Unauthorized"

@app.route('/a-updateRestaurant/<name>/', methods=['GET', 'POST'])
def update_restaurant(name):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        update_restaurant_form = UpdateRestaurantForm(request.form)
        if request.method == 'POST' and update_restaurant_form.validate():
            db = shelve.open('storage.db', 'w')
            restaurant_dict = db['Restaurants']

            restaurant = restaurant_dict.get(name)
            restaurant.set_name(update_restaurant_form.name.data)
            restaurant.set_cuisine(update_restaurant_form.cuisine.data)
            restaurant.set_description(update_restaurant_form.description.data)
            restaurant.set_opening_hours(literal_eval(update_restaurant_form.opening_hours.data))

            db['Restaurants'] = restaurant_dict
            db.close()

            return redirect(url_for('retrieve_restaurant'))
        else:
            db = shelve.open('storage.db', 'r')
            restaurant_dict = db['Restaurants']
            db.close()

            restaurant = restaurant_dict.get(name)
            update_restaurant_form.name.data = restaurant.get_name()
            update_restaurant_form.cuisine.data = restaurant.get_cuisine()
            update_restaurant_form.description.data = restaurant.get_description()
            update_restaurant_form.opening_hours.data = restaurant.get_opening_hours()

            return render_template('updateRestaurant.html', form=update_restaurant_form)
    else:
        return "Unauthorized"


@app.route('/a-restaurants/<name>/a-createDish', methods=['GET', 'POST'])
def create_dish(name):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        create_dish_form = CreateDishForm(request.form)
        if request.method == 'POST' and create_dish_form.validate():
            db = shelve.open('storage.db', 'c')

            try:
                restaurant_dict = db['Restaurants']
            except:
                print("Error in retrieving Rooms from storage.db.")

            menu = restaurant_dict[name].get_menu()

            dish = Dish.Dish(create_dish_form.name.data, create_dish_form.description.data, create_dish_form.price.data,)
            menu[dish.get_dish_id()] = dish
            restaurant_dict[name].set_menu(menu)
            db['Restaurants'] = restaurant_dict

            db.close()

            return redirect(url_for('retrieve_restaurant'))
        return render_template('createDish.html', form=create_dish_form)
    else:
        return "Unauthorized"

@app.route('/a-restaurants/<name>/a-deleteDish/<int:id>', methods=['POST'])
def delete_dish(name,id):

    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        db = shelve.open('storage.db', 'w')
        restaurant_dict = db['Restaurants']
        menu = restaurant_dict[name].get_menu()
        menu.pop(id)
        restaurant_dict[name].set_menu(menu)
        db['Restaurants'] = restaurant_dict
        db.close()

        return redirect(url_for('retrieve_restaurant'))
    else:
        return "Unauthorized"

@app.route('/a-restaurants/<name>/a-updateDish/<int:id>/', methods=['GET', 'POST'])
def update_dish(name,id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        update_dish_form = CreateDishForm(request.form)
        if request.method == 'POST' and update_dish_form.validate():
            db = shelve.open('storage.db', 'w')
            restaurant_dict = db['Restaurants']
            menu = restaurant_dict[name].get_menu()

            dish = menu.get(id)
            dish.set_name(update_dish_form.name.data)
            dish.set_description(update_dish_form.description.data)
            dish.set_price(update_dish_form.price.data)

            menu[id] = dish
            restaurant_dict[name].set_menu(menu)
            db['Restaurants'] = restaurant_dict
            db.close()

            return redirect(url_for('retrieve_restaurant'))
        else:
            db = shelve.open('storage.db', 'r')
            restaurant_dict = db['Restaurants']
            db.close()
            menu = restaurant_dict[name].get_menu()
            dish = menu.get(id)
            update_dish_form.name.data = dish.get_name()
            update_dish_form.description.data = dish.get_description()
            update_dish_form.price.data = dish.get_price()

            return render_template('updateDish.html', form=update_dish_form)
    else:
        return "Unauthorized"


@app.route('/a-deleteRestaurant/<name>', methods=['POST'])
def delete_restaurant(name):

    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        db = shelve.open('storage.db', 'w')
        restaurant_dict = db['Restaurants']

        restaurant_dict.pop(name)

        db['Restaurants'] = restaurant_dict
        db.close()

        return redirect(url_for('retrieve_restaurant'))
    else:
        return "Unauthorized"


@app.route('/a-staff')
def retrieve_staff():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        db = shelve.open('storage.db', 'r')

        staff_dict = db['Staff']

        db.close()

        staff_list = []
        for key in staff_dict:
            staff = staff_dict.get(key)
            staff_list.append(staff)

        return render_template('a-staff.html', count=len(staff_list), staff_list=staff_list)
    else:
        return "Unauthorized"

@app.route('/a-createStaff', methods=['GET', 'POST'])
def create_staff():
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        create_staff_form = CreateStaffForm(request.form)
        if request.method == 'POST' and create_staff_form.validate():
            db = shelve.open('storage.db', 'c')
            try:
                staff_dict = db['Staff']
                restaurant_dict = db['Restaurants']
            except:
                print("Error in retrieving Temperature Logs from storage.db.")

            staff = Staff.Staff(create_staff_form.name.data, create_staff_form.restaurant.data, create_staff_form.position.data, create_staff_form.salary.data, create_staff_form.birthday.data)
            staff_dict[staff.get_staff_id()] = staff

            try:
                restaurant_dict[staff.get_restaurant()].get_staff_list()[staff.get_staff_name()] = staff
            except:
                return "Restaurant not found"

            db['Restaurants'] = restaurant_dict
            db['Staff'] = staff_dict
            db.close()

            return redirect(url_for('retrieve_staff'))
        return render_template('createStaff.html', form=create_staff_form)
    else:
        return "Unauthorized"

@app.route('/a-deleteStaff/<int:id>', methods=['POST'])
def delete_staff(id):

    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:
        db = shelve.open('storage.db', 'w')
        staff_dict = db['Staff']

        staff_dict.pop(id)

        db['Staff'] = staff_dict
        db.close()

        return redirect(url_for('retrieve_staff'))
    else:
        return "Unauthorized"

@app.route('/a-updateStaff/<int:id>/', methods=['GET', 'POST'])
def update_staff(id):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"
    if users_dict[userid].get_membership() == "A" and session["auth"] == True:

        update_staff_form = UpdateStaffForm(request.form)
        if request.method == 'POST' and update_staff_form.validate():
            db = shelve.open('storage.db', 'w')
            staff_dict = db['Staff']
            restaurant_dict = db['Restaurants']

            staff = staff_dict.get(id)
            staff.set_staff_name(update_staff_form.name.data)
            if staff.get_restaurant() != update_staff_form.restaurant.data:
                restaurant_dict[staff.get_restaurant()].get_staff_list().pop(staff.get_staff_id())
                newres = restaurant_dict[update_staff_form.restaurant.data]
                newres.get_staff_list()[staff.get_staff_id()] = staff
                restaurant_dict[update_staff_form.restaurant.data] = newres
                db['Restaurants'] = restaurant_dict
            staff.set_restaurant(update_staff_form.restaurant.data)
            staff.set_position(update_staff_form.position.data)
            staff.set_salary(update_staff_form.salary.data)
            staff.set_birthday(update_staff_form.birthday.data)

            db['Staff'] = staff_dict
            db.close()

            return redirect(url_for('retrieve_staff'))
        else:
            db = shelve.open('storage.db', 'r')
            promo_dict = db['Staff']
            db.close()

            staff = promo_dict.get(id)
            update_staff_form.name.data = staff.get_staff_name()
            update_staff_form.restaurant.data = staff.get_restaurant()
            update_staff_form.position.data = staff.get_position()
            update_staff_form.salary.data = staff.get_salary()
            update_staff_form.birthday.data = staff.get_birthday()

            return render_template('updateStaff.html', form=update_staff_form)
    else:
        return "Unauthorized"


def loadpromo():
    db = shelve.open('storage.db', 'r')

    promo_dict = db['Promotions']

    db.close()

    promo_list = []
    for key in promo_dict:
        promo = promo_dict.get(key)
        promo_list.append(promo)
    return promo_list

def initSupport():
    details_form = CreateDetailsForm(request.form)
    chat_form = CreateChatForm(request.form)
    if request.method == 'POST' and details_form.validate():
        db = shelve.open('storage.db', 'c')
        chats_dict = db['Chats']
        chat = Chat.Chat(details_form.name.data, details_form.email.data, details_form.phone.data,
                         details_form.query.data)
        chats_dict[chat.get_chat_id()] = chat
        db['Chats'] = chats_dict
        chatlist = chat.get_chat()
        db.close()
        session["Support"] = chat.get_chat_id()
        return {"form":chat_form, "chat":chatlist, "support":True}
    elif request.method == 'POST' and chat_form.validate():
        if chat_form.inputtext.data == "reload":
            db = shelve.open('storage.db', 'c')
            chats_dict = db['Chats']
            chat = chats_dict[session["Support"]]
            chatlist = chat.get_chat()
            chat_form.inputtext.data = ""
            return {"form":chat_form, "chat":chatlist, "support":True}
        elif len(chat_form.inputtext.data) > 0:
            db = shelve.open('storage.db', 'c')
            chats_dict = db['Chats']
            chat = chats_dict[session["Support"]]
            chatlist = chat.get_chat()
            chatlist.append("cust:" + chat_form.inputtext.data)
            chat.set_chat(chatlist)
            chats_dict[session["Support"]] = chat
            db['Chats'] = chats_dict
            chat_form.inputtext.data = ""
            return {"form":chat_form, "chat":chatlist, "support":True}
    else:
        session["Support"] = "None"
        return {"form":details_form, "chat":None, "support":False}

def homepage():
    details_form = CreateDetailsForm(request.form)
    chat_form = CreateChatForm(request.form)
    search_form = CreateRoomSearchForm(request.form)
    if request.method == 'POST' and search_form.validate():
        children = search_form.children.data
        adults = search_form.adults.data
        formatted_capacity = [children,adults]
        db = shelve.open('storage.db','r')
        rooms_dict = db['Rooms']
        roomlist = []
        for key in rooms_dict:
            for key2 in rooms_dict[key]:
                room = rooms_dict[key][key2]
                if formatted_capacity in room.get_capacity_list():
                    roomlist.append(room)
        return {"form": details_form, "chat": None, "support": False, 'search': search_form, 'roomlist': roomlist}
    if request.method == 'POST' and details_form.validate():
        db = shelve.open('storage.db', 'c')
        chats_dict = db['Chats']
        chat = Chat.Chat(details_form.name.data, details_form.email.data, details_form.phone.data,
                         details_form.query.data)
        chats_dict[chat.get_chat_id()] = chat
        db['Chats'] = chats_dict
        chatlist = chat.get_chat()
        db.close()
        session["Support"] = chat.get_chat_id()
        return {"form": chat_form, "chat": chatlist, "support": True, 'search': search_form, 'roomlist': None}
    elif request.method == 'POST' and chat_form.validate():
        if chat_form.inputtext.data == "reload":
            try:
                db = shelve.open('storage.db', 'c')
                chats_dict = db['Chats']
                chat = chats_dict[session["Support"]]
                chatlist = chat.get_chat()
                chat_form.inputtext.data = ""
                return {"form": chat_form, "chat": chatlist, "support": True, 'search': search_form, 'roomlist': None}
            except:
                session["Support"] = "None"
                return {"form": details_form, "chat": None, "support": False, 'search': search_form, 'roomlist': None}
        elif len(chat_form.inputtext.data) > 0:
            try:
                db = shelve.open('storage.db', 'c')
                chats_dict = db['Chats']
                chat = chats_dict[session["Support"]]
                chatlist = chat.get_chat()
                chatlist.append("cust:" + chat_form.inputtext.data)
                chat.set_chat(chatlist)
                chats_dict[session["Support"]] = chat
                db['Chats'] = chats_dict
                chat_form.inputtext.data = ""
                return {"form": chat_form, "chat": chatlist, "support": True, 'search': search_form, 'roomlist': None}
            except:
                session["Support"] = "None"
                return "Live support chat closed"
    else:
        session["Support"] = "None"
        return {"form": details_form, "chat": None, "support": False, 'search': search_form, 'roomlist': None}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/confirmdetails', methods=['POST'])
def confirmdetails():
    with open('bookingprocessing.txt','w+') as b:
        b.truncate(0)
        data = request.form
        startdate = datetime.datetime.strptime(data['startdate'], '%Y-%m-%d').strftime('%d/%m/%y')
        enddate = datetime.datetime.strptime(data['enddate'], '%Y-%m-%d').strftime('%d/%m/%y')
        days = str(datetime.datetime.strptime(enddate,'%d/%m/%y') - datetime.datetime.strptime(startdate,'%d/%m/%y'))
        days = days[0:days.index("days")-1]
        room_type = data['room_type']
        b.write(str(startdate)+","+str(enddate)+","+days+','+room_type)
        b.close()
    return "cool"

@app.route('/approve', methods=['POST'])
def approve():
    return redirect(url_for('success'))

@app.route('/success', methods=['GET'])
def success():
    db = shelve.open('storage.db', 'c')
    booking_dict = db['Bookings']
    users_dict = db['Users']

    for i in users_dict:
        try:
            if users_dict[i].get_username() == session["login"]:
                userid = users_dict[i].get_user_id()
        except:
            return "Not logged in"

    with open('bookingprocessing.txt','r') as b:
        b = b.read()
        data = b.split(',')
        startdate = data[0]
        enddate = data[1]
        days = data[2]
        room_type = data[3]

    newbooking = Booking.Booking(userid,room_type,session["login"], datetime.datetime.strptime(startdate, '%d/%m/%y'), datetime.datetime.strptime(enddate,'%d/%m/%y'))
    booking_dict[newbooking.get_booking_id()] = newbooking
    db['Bookings'] = booking_dict
    db.close()
    return redirect(url_for('home', booked=True))

if __name__ == '__main__':
    db = shelve.open('storage.db', 'c')

    try:
        users_dict = db['Users']
    except:
        print("Error in retrieving Users from storage.db.")

    #Test user and promo

    user = User.User("Admin", "1", "M", "28/09/2003", "65", "96322451", "A", "", sha256("hello"+"shho"), "Negative")
    users_dict[user.get_user_id()] = user
    user1 = User.User("Karen", "1", "F", "28/09/2003", "65", "96322451", "C", "", sha256("hello"+"shho"), "Negative")
    users_dict[user1.get_user_id()] = user1

    promo_dict = {}
    promo = Promo.Promo("Christmas Deals", "christmas-deals", "Free Christmas buffet dinner", datetime.datetime.strptime("31/12/2020","%d/%m/%Y").date(), "none")
    promo_dict[promo.get_promo_id()] = promo
    promo = Promo.Promo("DBS Card Promotion", "dbs-card-promotion", "5% rebate on hotel booking", datetime.datetime.strptime("31/12/2020","%d/%m/%Y").date(), "none")
    promo_dict[promo.get_promo_id()] = promo
    promo = Promo.Promo("Family Deals", "family-deals", "Free kids meal for families of 3 or more with children", datetime.datetime.strptime("31/12/2020","%d/%m/%Y").date(), "none")
    promo_dict[promo.get_promo_id()] = promo
    db['Users'] = users_dict
    db['Promotions'] = promo_dict

    swab_dict = {}
    log = SwabLog.SwabLog(user.get_user_id(), "123A", user.get_first_name(), user.get_last_name(), "Negative")
    swab_dict[user.get_user_id()] = log
    db['SwabLogs'] = swab_dict

    chats_dict = {}
    chat = Chat.Chat('Gabriel Seet',"gabeseet@gmail.com","96322451","Hotel booking error")
    chats_dict[chat.get_chat_id()] = chat
    db["Chats"] = chats_dict

    rooms_dict = {}
    room1 = Room.Room("Studio", "Studio Mini", 12, 12, 70, [[0,1]],[
                "1 Single Bed",
                "Private Toilet",
                "Small Desk",
                "Smart TV",
                "Small Kitchen",
                "Free Wi-Fi"
            ])
    room2 = Room.Room("Studio", "Studio Deluxe", 7, 7, 130, [[0,2], [1,1]],[
                "1 Double Bed",
                "Private Toilet",
                "Large Table",
                "Smart TV",
                "Regular Kitchen",
                "Free Wi-Fi"
            ])
    room3 = Room.Room("Regular", "Regular Single", 18, 18, 90, [[0,1]],[
                "1 Single Bed",
                "Private Toilet",
                "Small Desk",
                "Smart TV",
                "Free Wi-Fi"
            ])
    room4 = Room.Room("Regular", "Regular Double", 15, 15, 140, [[0,2], [1,1]],[
                "1 Double Bed",
                'Couch',
                "Private Toilet",
                "Medium Table",
                "Smart TV",
                "Free Wi-Fi"
            ])
    room5 = Room.Room("Regular", "Regular Family", 18, 18, 260, [[0,4], [1,3], [2,2], [3,1], [0,3], [1,2], [2,1]],[
                "1 Double Bed",
                "1 Single Bed",
                "Private Toilet",
                "2 Medium Tables",
                "1 Large Table",
                "2 Armchairs and 1 Double Couch",
                "Smart TV",
                "Small Kitchen",
                "Free Wi-Fi"
            ])
    room6 = Room.Room("Suite", "Mini Suite", 6, 6, 230, [[0,2], [1,1]],[
                "1 Double Bed",
                "Private Toilet",
                "Large Table",
                "Large Couch",
                "Smart TV",
                "Free Wi-Fi"
            ])
    room7 = Room.Room("Suite", "Suite", 10, 10, 300, [[0,2], [1,1]],[
                "1 Double Bed",
                "Private Toilet",
                "Large Table",
                "Large Couch",
                "Smart TV",
                "Private Swimming Pool",
                "Free Wi-Fi",
                "Complimentary Coffee and Biscuits"
            ])
    room8 = Room.Room("Suite", "Presidential Suite", 5, 5, 400, [[0,4], [1,3], [2,2], [3,1], [0,3], [1,2], [2,1]],[
                "2 Double Bed",
                "Private Toilet",
                "1 Large 9-seater Table",
                "1 Large Table",
                "2 Double Couches",
                "Smart TV",
                "Small Kitchen",
                "Free Wi-Fi",
                "Complimentary Coffee and Biscuits"
            ])
    rooms_dict[room1.get_room_id()] = room1
    rooms_dict[room2.get_room_id()] = room2
    rooms_dict[room3.get_room_id()] = room3
    rooms_dict[room4.get_room_id()] = room4
    rooms_dict[room5.get_room_id()] = room5
    rooms_dict[room6.get_room_id()] = room6
    rooms_dict[room7.get_room_id()] = room7
    rooms_dict[room8.get_room_id()] = room8

    db["Rooms"] = rooms_dict
    db['ChatLogs'] = {}
    db['TempLogs'] = {}
    db['Bookings'] = {1:Booking.Booking(1,"Admin1","Studio Mini",datetime.datetime.strptime("12/04/2021","%d/%m/%Y"),datetime.datetime.strptime("14/04/2021","%d/%m/%Y"))}
    db['BookingLogs'] = {1:BookingLog.BookingLog(1,"Admin1","Studio",datetime.datetime.strptime("11/03/2021","%d/%m/%Y"),datetime.datetime.strptime("12/03/2021","%d/%m/%Y"))}
    db['Contacts'] = {1:Contact.Contact("Admin","1","email",96322451,"msg")}
    db['Reviews'] = {1:Review.Review("Gabriel Seet","gabeseet@gmail.com",4,"Extremely cool","Very cool"),2:Review.Review("John Tan","johntan849@gmail.com",4,"Great service","Customer service was great!")}

    fillerOpeningHours = {"Monday":"11:30 am-9:30 pm","Tuesday":"11:30 am-9:30 pm","Wednesday":"11:30 am-9:30 pm","Thursday":"11:30 am-9:30 pm","Friday":"11:00 am-10:00 pm","Saturday":"11:00 am-10:00 pm","Sunday":"11:30 am-9:30 pm"}

    staff1 = Staff.Staff("Alice Low","Atlas","Head Chef","5490", datetime.datetime.strptime("23/05/2000","%d/%m/%Y"))
    staff2 = Staff.Staff("Dave Koh", "Arch", "Head Chef", "5490", datetime.datetime.strptime("27/08/1997","%d/%m/%Y"))
    stafflist1 = {staff1.get_staff_id():staff1}
    stafflist2 = {staff2.get_staff_id():staff2}
    menu1 = {1:Dish.Dish("Fish N Chips","Fried cod with a side of chips and tartar sauce","10"), 2:Dish.Dish("Spam Musubi","Fried spam on top of Japanese rice wrapped with seaweed","6")}
    menu2 = {1: Dish.Dish("Teriyaki Chicken Don", "Japanese rice and fried chicken slices with teriyaki sauce drizzled over", "12"), 2: Dish.Dish("Assorted Yakitori", "A variety of styles of cooking and seasoning with chicken and pork on skewers", "15")}
    restaurant1 = Restaurant.Restaurant("Atlas","Western","A Western cuisine restaurant",fillerOpeningHours,menu1,menu1,menu1,stafflist1)

    restaurant2 = Restaurant.Restaurant("Arch", "Japanese", "A Japanese cuisine restaurant", fillerOpeningHours, menu2, menu2, menu2, stafflist2)


    db['Restaurants'] = {"Atlas":restaurant1,"Arch":restaurant2}
    db['Staff'] = {staff1.get_staff_id():staff1,staff2.get_staff_id():staff2}
    db.close()
    app.run()
