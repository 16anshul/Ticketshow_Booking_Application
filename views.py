from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from . import db
from sqlalchemy import or_
from .models import User, Venue, Show, Summary, Ticket
from datetime import date, datetime
import matplotlib.pyplot as plt
import numpy as np
import random
import string
import matplotlib
matplotlib.use('Agg')

views = Blueprint('views', __name__)

# Home page


@views.route("/")
@login_required
def home():
    admin = User.query.filter_by(user_type='admin').first()
    show = Show.query.all()
    venue = Venue.query.all()
    user = current_user
    show_venue_id = []
    for row in show:
        show_venue_id.append(row.venue_id)
    if current_user == admin:
        return render_template('adminhome.html', venue=venue, admin=admin)
    else:
        return render_template('user_dashboard.html', venue=venue, show=show, user=user, show_venue_id=show_venue_id)

# user profile


@views.route("/userprofile", methods=['GET', 'POST'])
def profile():
    user = User.query.filter_by(user_type='user', id=current_user.id).first()
    if request.method == "POST":
        name = request.form['name']
        if name:
            user.name = name
        db.session.commit()
        db.session.close()
        return redirect(url_for('views.profile'))
    return render_template('userprofile.html', user=user)


# Create venue
@views.route("/createvenue", methods=['GET', 'POST'])
@login_required
def cvenue():
    admin = User.query.filter_by(user_type='admin').first()
    if request.method == "POST":

        vname = request.form["name"]
        location = request.form['location']
        address = request.form['address']
        capacity = request.form['capacity']
        venue_pic = request.files['venue_pic']
        letters = string.ascii_lowercase

        if venue_pic:
            venue_pic_name = secure_filename(venue_pic.filename)
            pic_name = ''.join(random.choice(letters)
                               for i in range(10)) + '.png' + venue_pic_name
            venue_pic.save(os.path.join(
                app.root_path, 'static\\venueimages', pic_name))

        else:
            pic_name = ""

        new_venue = Venue(vname=vname, location=location,
                          address=address, capacity=capacity, venue_pic=pic_name
                          )
        db.session.add(new_venue)
        db.session.commit()
        return redirect('/venuepage')
    return render_template('venuecreate.html', admin=admin)


# Venue view page
@views.route("/venuepage", methods=["GET"])
@login_required
def venuepage():
    venue = Venue.query.all()
    show = Show.query.all()
    admin = User.query.filter_by(user_type='admin').first()

    return render_template('venues.html', venue=venue, show=show, admin=admin)


# Edit venue
@views.route("/venuepage/edit/<int:vid>", methods=['GET', 'POST'])
def editvenue(vid):
    venue = Venue.query.filter_by(id=vid).first()
    admin = User.query.filter_by(user_type='admin').first()
    if request.method == "POST":
        name = request.form["name"]
        location = request.form['location']
        address = request.form['address']
        capacity = request.form['capacity']
        if name:
            venue.vname = name
        if location:
            venue.location = location
        if address:

            venue.address = address
        if capacity:
            venue.capacity = capacity

        db.session.commit()
        db.session.close()
        return redirect('/venuepage')
    return render_template('editvenue.html', venue=venue, admin=admin)

# Delete venue


@views.route("/venuepage/delete/<int:vid>")
def venuedelete(vid):
    venue = Venue.query.filter_by(id=vid).first()
    shows = Show.query.filter_by(venue_id=vid).all()

    for row in shows:
        db.session.delete(row)

    db.session.delete(venue)
    db.session.commit()
    db.session.close()
    venue = Venue.query.filter_by(id=vid).all()
    if venue == []:
        return redirect(url_for("views.home"))
    return redirect(url_for("views.venuepage"))

# Create show


@views.route("/createshow/<vid>", methods=['GET', 'POST'])
def cshow(vid):
    venue = Venue.query.filter_by(id=vid).first()
    admin = User.query.filter_by(user_type='admin').first()
    if request.method == "POST":
        sname = request.form['name']
        date_str = (request.form['date'])
        sdate = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_str = request.form['time']
        stime = datetime.strptime(time_str, '%H:%M').time()
        duration_str = request.form['duration']
        sduration = datetime.strptime(duration_str, '%H:%M').time()
        sdescription = request.form['description']
        Tag = request.form['tag']
        Ticket_Price = request.form['price']
        show_pic = request.files['show_pic']
        letters = string.ascii_lowercase
        if show_pic:
            venue_pic_name = secure_filename(show_pic.filename)
            pic_name = ''.join(random.choice(letters)
                               for i in range(10)) + '.png' + venue_pic_name
            show_pic.save(os.path.join(
                app.root_path, 'static\\showimages', pic_name))

        else:
            pic_name = ""

        venue_id = vid
        new_show = Show(sname=sname, sdate=sdate, stime=stime, sduration=sduration,
                        sdescription=sdescription, Tag=Tag, Ticket_Price=Ticket_Price, show_pic=pic_name, venue_id=venue_id)
        db.session.add(new_show)
        db.session.commit()

        return redirect('/venuepage')
    return render_template('showcreate.html', venue=venue, admin=admin)


# Edit Show
@views.route("/venuepage/editshow/<int:sid>", methods=['GET', 'POST'])
def editshow(sid):
    admin = User.query.filter_by(user_type='admin').first()
    show = Show.query.filter_by(id=sid).first()
    date_today = date.today()
    if request.method == "POST":
        sname = request.form['name']
        date_str = (request.form['date'])
        sdate = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_str = request.form['time']
        stime = datetime.strptime(time_str, '%H:%M').time()
        duration_str = request.form['duration']
        sduration = datetime.strptime(duration_str, '%H:%M').time()
        sdescription = request.form['description']
        Tag = request.form['tag']
        Ticket_Price = request.form['price']
        if sname:
            show.sname = sname
        if sdate:
            show.sdate = sdate
        if stime:
            show.stime = stime
        if sduration:
            show.sduration = sduration
        if sdescription:
            show.sdescritption = sdescription
        if Tag:
            show.Tag = Tag
        if Ticket_Price:
            show.Ticket_Price = Ticket_Price

        db.session.commit()
        db.session.close()

        return redirect('/venuepage')
    return render_template('editshow.html', show=show, admin=admin, date_today=date_today)

# Delete vshow


@views.route("/venuepage/deleteshow/<int:sid>")
def showdelete(sid):
    show = Show.query.filter_by(id=sid).first()
    db.session.delete(show)
    db.session.commit()
    db.session.close()
    return redirect(url_for("views.venuepage"))


# Create Summary
@views.route("/createsummary/<int:sid>", methods=['GET', 'POST'])
@login_required
def csummary(sid):
    show = Show.query.filter_by(id=sid).first()
    user = current_user

    if request.method == "POST":
        story = request.form['story']
        visuals = request.form['visuals']
        acting = request.form['acting']
        rewatchability = request.form['rewatchability']
        overall_rating = request.form['rating']
        show_id = sid

        new_summary = Summary(story=story, visuals=visuals, acting=acting,
                              rewatchability=rewatchability, overall_rating=overall_rating, show_id=show_id)
        db.session.add(new_summary)
        db.session.commit()

        flash('Rating Stored Successfully!',
              category='success')
        return redirect(url_for('views.home'))
    return render_template('summarycreate.html', show=show, user=user)

# view details


@views.route("/viewdetails/<int:sid>", methods=['GET'])
@login_required
def view_details(sid):
    # venue = Venue.query.all()
    show = Show.query.filter_by(id=sid).all()

    return render_template('view.html', show=show)


# Show summary page


@views.route("/summarypage/<int:sid>", methods=["GET"])
@login_required
def summarypage(sid):
    show = Show.query.filter_by(id=sid).all()
    summary = Summary.query.filter_by(show_id=sid).all()
    # barchart
    story = []
    visuals = []
    acting = []
    rewatchability = []
    overall_rating = []
    for sum in summary:
        story.append(float(sum.story))
        visuals.append(float(sum.visuals))
        acting.append(float(sum.acting))
        rewatchability.append(float(sum.rewatchability))
        overall_rating.append(float(sum.overall_rating))
    l = len(story)
    if l != 0:
        # average of parameters
        m_story = np.mean(story)
        m_visuals = np.mean(visuals)
        m_acting = np.mean(acting)
        m_rewatch = np.mean(rewatchability)
        m_rate = np.mean(overall_rating)
        # plotting
        y = [m_story, m_visuals, m_acting, m_rewatch, m_rate]
        X = ["a_story", "a_visuals", "a_acting", "a_rewatch", "a_rate"]
        y_pos = np.arange(len(X))
        plt.bar(y_pos, y, align='center', color=['r', 'g', 'y', 'b', 'black'])
        plt.xlabel('Categories')
        plt.xticks(np.arange(6), ['story', 'visuals',
                                  'acting', 'rewatch', 'overall_rating', ''])
        plt.ylabel('Average Ratings')
        plt.yticks(np.arange(7), ['0', '1', '2', '3', '4', '5', '6'])
        plt.title('Histogram')

        # generate a random filename for the chart image
        letters = string.ascii_lowercase
        filename = ''.join(random.choice(letters) for i in range(10)) + '.png'

        # save the chart as a PNG image with the random filename
        filepath = os.path.join(app.static_folder, 'rating', filename)
        plt.savefig(filepath)
        plt.close()
        return render_template('summary.html', summary=summary, show=show, plot=str(filename), l=l)
    l = 0
    return render_template('summary.html', summary=summary, show=show, l=l)


@views.route("/userviewshow", methods=["GET", "POST"])
@login_required
def userviewshow():
    if current_user:
        show = Show.query.all()
        return render_template('userviewdetails.html', user=current_user,  show=show)
    return render_template('error.html', message='Only user can access.')

# seat deatils


@views.route('/seatbook/<sid>', methods=['GET', 'POST'])
@login_required
def enter_seat(sid):

    seat = None
    show = Show.query.filter_by(id=sid).first()
    venue = Venue.query.filter_by(id=show.venue_id).first()
    current_seat = int(venue.capacity)
    user = User.query.filter_by(id=current_user.id).first()
    if user.user_type == "user":
        if request.method == 'POST':

            seat = request.form.get('seat')
            if int(seat) > int(current_seat):
                return render_template('error.html', message="Not enough seats.")
            remain_seat = current_seat-int(seat)
            avb_seat = current_user

            return render_template('seat.html', show=show, avb_seat=avb_seat, seat=seat, remain_seat=remain_seat, current_seat=current_seat, user=user)
        else:
            return render_template('seat.html', show=show, seat=seat, current_seat=current_seat, user=user)
    else:
        return render_template('error.html', message='Only user can book show.')


# Booking
@views.route('/booking/<int:sid>/<int:seat>', methods=['GET', 'POST'])
@login_required
def booking(sid, seat):
    seat = seat
    show = Show.query.filter_by(id=sid).first()
    venue = Venue.query.filter_by(id=show.venue_id).first()
    vaddress = venue.address
    sname = show.sname
    sdate = show.sdate
    stime = show.stime
    sid = show.id
    uid = current_user.id
    price = int(seat)*int(show.Ticket_Price)
    current_seat = int(venue.capacity)
    remain_seat = current_seat-seat
    if remain_seat or remain_seat == 0:
        venue.capacity = remain_seat
        db.session.commit()

    new_ticket = Ticket(sname=sname, vaddress=vaddress,
                        sdate=sdate, stime=stime, price=price, seats=seat, sid=sid, uid=uid)
    db.session.add(new_ticket)
    db.session.commit()
    return redirect(url_for("views.user_booking"))

# Booking Details


@views.route('/userbooking', methods=['GET'])
@login_required
def user_booking():
    user = current_user

    bookings = Ticket.query.filter_by(uid=current_user.id).all()
    return render_template('booking.html', bookings=bookings, user=user)

#venue_search

@views.route('/search', methods=['GET', 'POST'])
@login_required
def venue_search():
    shows = Show.query.all()

    if request.method == "POST":
        vsearch = request.form["key"]
        if vsearch:
            venues = db.session.query(Venue).filter(
                Venue.location.ilike(f'%{vsearch}%')).all()
            l = len(venues)
        return render_template('search.html', venues=venues, user=current_user, shows=shows, l=l)
    return render_template('search.html', user=current_user)

#show_search

@views.route('/showsearch', methods=['GET', 'POST'])
@login_required
def show_search():
    if request.method == "POST":
        tags = request.form.getlist('tags')
        like_expressions = [Show.Tag.like('%' + tag + '%') for tag in tags]
        shows = Show.query.filter(or_(*like_expressions)).all()
        l = len(shows)
        return render_template('showsearch.html', user=current_user, shows=shows, l=l)

    return render_template('showsearch.html', user=current_user)
