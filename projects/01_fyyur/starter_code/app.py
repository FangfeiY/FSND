#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime, date, time
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database:
# postgresql://postgres:postgres@localhost:5432/fyyur
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    listed_time = db.Column(db.DateTime())
    shows = db.relationship('Show', backref='at_venue', lazy=True, cascade='all, delete-orphan')

    def getPastShowsInfo(self):
      #   "past_shows": [{
      #     "artist_id": 5,
      #     "artist_name": "Matt Quevedo",
      #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      #     "start_time": "2019-06-15T23:00:00.000Z"
      #   }]

      past_shows_info = []
      past_shows = Show.query.join(Venue).filter(Show.venue_id==self.id).filter(Show.start_time < datetime.today()).all()
      # Alternative: Show.query.filter_by(venue_id=self.id).filter(Show.start_time < datetime.today()).all()
                  
      for show in past_shows:
        past_shows_info.append({
          "artist_id": show.artist_id,
          "artist_name": show.playing_artist.name,
          "artist_image_link": show.playing_artist.image_link,
          "start_time": show.start_time.isoformat() + 'Z'
        })

      return past_shows_info
    
    def getUpcomingShowsInfo(self):
      #   "upcoming_shows": [{
      #     "artist_id": 6,
      #     "artist_name": "The Wild Sax Band",
      #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      #     "start_time": "2035-04-01T20:00:00.000Z"
      #   }]

      upcoming_shows_info = []
      upcoming_shows = Show.query.join(Venue).filter(Show.venue_id==self.id).filter(Show.start_time >= datetime.today()).all()
      # Alternative: Show.query.filter_by(venue_id=self.id).filter(Show.start_time >= datetime.today()).all()

      for show in upcoming_shows:
        upcoming_shows_info.append({
          "artist_id": show.artist_id,
          "artist_name": show.playing_artist.name,
          "artist_image_link": show.playing_artist.image_link,
          "start_time": show.start_time.isoformat() + 'Z'
        })

      return upcoming_shows_info

    def getUpcomingShowCount(self):
      return Show.query.join(Venue).filter(Show.venue_id==self.id).filter(Show.start_time >= datetime.today()).count()
      # Alternative: Show.query.filter_by(venue_id=self.id).filter(Show.start_time >= datetime.today()).count()

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    listed_time = db.Column(db.DateTime())
    shows = db.relationship('Show', backref='playing_artist', lazy=True, cascade='all, delete-orphan')

    def getUpcomingShowCount(self):
      return Show.query.join(Artist).filter(Show.artist_id==self.id).filter(Show.start_time >= datetime.today()).count()
      # Alternative: Show.query.filter_by(artist_id=self.id).filter(Show.start_time >= datetime.today()).count()

    def getPastShowsInfo(self):
      # "past_shows": [{
      #   "venue_id": 3,
      #   "venue_name": "Park Square Live Music & Coffee",
      #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      #   "start_time": "2019-06-15T23:00:00.000Z"
      #  }]
      past_shows_info = []
      past_shows = Show.query.join(Artist).filter(Show.artist_id==self.id).filter(Show.start_time < datetime.today()).all()
      # Alternative: Show.query.filter_by(artist_id=self.id).filter(Show.start_time < datetime.today()).all()

      for show in past_shows:
        past_shows_info.append({
          "venue_id": show.venue_id,
          "venue_name": show.at_venue.name,
          "venue_image_link": show.at_venue.image_link,
          "start_time": show.start_time.isoformat() + 'Z'
        })
      return past_shows_info

    def getUpcomingShowsInfo(self):
      #   "upcoming_shows": [{
      #   "venue_id": 3,
      #   "venue_name": "Park Square Live Music & Coffee",
      #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      #   "start_time": "2035-04-01T20:00:00.000Z"
      # }]
      upcoming_shows_info = []
      upcoming_shows = Show.query.join(Artist).filter(Show.artist_id==self.id).filter(Show.start_time >= datetime.today()).all()
      # Alternative: Show.query.filter_by(artist_id=self.id).filter(Show.start_time >= datetime.today()).all()

      for show in upcoming_shows:
        upcoming_shows_info.append({
          "venue_id": show.venue_id,
          "venue_name": show.at_venue.name,
          "venue_image_link": show.at_venue.image_link,
          "start_time": show.start_time.isoformat() + 'Z'
        })
      return upcoming_shows_info

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime())
  # AM / PM
  am = db.Column(db.Boolean, default=True)
  # Monday, Tuesday, ...
  day = db.Column(db.String(10))

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  recent_venues = Venue.query.order_by(Venue.listed_time.desc()).limit(10).all()
  recent_artists = Artist.query.order_by(Artist.listed_time.desc()).limit(10).all()
  return render_template('pages/home.html', venues=recent_venues, artists=recent_artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]

  data =[]
  # {state: {city: [venue1, venue2, ...]}
  states = {}

  venues = Venue.query.all()

  for venue in venues:
    venue_output = {
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": venue.getUpcomingShowCount()
    }
    if venue.state not in states.keys():
      states[venue.state] = {venue.city: [venue_output]}
    elif venue.city not in states[venue.state].keys():
      states[venue.state][venue.city] = [venue_output]
    else:
      states[venue.state][venue.city].append(venue_output)
    
  for stateName in states:
    for cityName in states[stateName]:
      data.append({
        "city": cityName,
        "state": stateName,
        "venues": states[stateName][cityName]
      })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  search_term = request.form.get('search_term', '')
  db_search_term = f'%{search_term}%'
  search_res = Venue.query.filter(Venue.name.ilike(db_search_term))

  data = []
  for venue in search_res.all():
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": venue.getUpcomingShowCount()
    })
  
  response = {
    "count": search_res.count(),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

  venue = Venue.query.get(venue_id)

  past_shows = venue.getPastShowsInfo()
  upcoming_shows = venue.getUpcomingShowsInfo()

  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  if venue.seeking_talent:
    data['seeking_description'] = venue.seeking_description

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm()
  if form.validate_on_submit():
    return create_venue()
  else:
    for error in form.errors:
      flash(error)
    return render_template('forms/new_venue.html', form=form)

def create_venue():
  error = False
  try:
    venue = Venue(
      name=request.form.get('name',''),
      city=request.form.get('city',''),
      state=request.form.get('state',''),
      address=request.form.get('address',''),
      phone=request.form.get('phone',''),
      genres=request.form.getlist('genres'),
      facebook_link=request.form.get('facebook_link',''),
      seeking_talent=request.form.get('seeking_artist', type=bool),
      seeking_description=request.form.get('seeking_description',''),
      listed_time=datetime.today()
    )
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred while adding venue ' + request.form['name'], 'error')
  finally:
    db.session.close()

  if error:
    abort(500)
  else:
    return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  #return None

  error = False
  try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
      flash('Venue ' + venue.name + ' was deleted!')
  except:
      error = True
      db.session.rollback()
      flash('An error occurred while deleting venue ' + venue.name, 'error')
  finally:
      db.session.close()

  if error:
      abort(500)
  else:
      return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }]

  data = []
  artists = Artist.query.all()

  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  search_term = request.form.get('search_term', '')
  db_search_term = f'%{search_term}%'
  search_res = Artist.query.filter(Artist.name.ilike(db_search_term))

  data = []
  for artist in search_res.all():
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": artist.getUpcomingShowCount()
    })
  
  response = {
    "count": search_res.count(),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

  artist = Artist.query.get(artist_id)
  past_shows_info = artist.getPastShowsInfo()
  upcoming_shows_info = artist.getUpcomingShowsInfo()
  
  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": "" if artist.seeking_description is None else artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows_info,
    "upcoming_shows": upcoming_shows_info,
    "past_shows_count": len(past_shows_info),
    "upcoming_shows_count": len(upcoming_shows_info),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = [] if artist.genres is None else artist.genres.split(',')
  form.facebook_link.data = artist.facebook_link

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  artist = Artist.query.get(artist_id)
  artist.name = request.form.get('name','')
  artist.city = request.form.get('city','')
  artist.state = request.form.get('state','')
  artist.phone = request.form.get('phone','')
  artist.genres = request.form.getlist('genres')
  artist.facebook_link = request.form.get('facebook_link','')

  try:
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred while updating artist ' + request.form['name'], 'error')
  finally:
    db.session.close()
  
  if error:
    abort (500)
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id)

  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = [] if venue.genres is None else venue.genres.split(',')
  form.facebook_link.data = venue.facebook_link

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  venue = Venue.query.get(venue_id)
  venue.name = request.form.get('name','')
  venue.city = request.form.get('city','')
  venue.state = request.form.get('state','')
  venue.address = request.form.get('address','')
  venue.phone = request.form.get('phone','')
  venue.genres = request.form.getlist('genres')
  venue.facebook_link = request.form.get('facebook_link','')

  try:
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred while updating venue ' + request.form['name'], 'error')
  finally:
    db.session.close()
  
  if error:
    abort (500)
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artiist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  # Input fails validation:
  form = ArtistForm()
  if not form.validate_on_submit():
    for error in form.errors:
      flash(error)
    return render_template('forms/new_artist.html', form=form)
  
  # Input passes validation:
  return create_artist()

def create_artist():
  error = False
  try:
    artist = Artist(
      name=request.form.get('name',''),
      city=request.form.get('city',''),
      state=request.form.get('state',''),
      phone=request.form.get('phone',''),
      genres=request.form.getlist('genres'),
      facebook_link=request.form.get('facebook_link',''),
      seeking_venue=request.form.get('seeking_venue', type=bool),
      seeking_description=request.form.get('seeking_description',''),
      listed_time=datetime.today()
    )

    db.session.add(artist)
    db.session.commit()

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred while adding artist ' + request.form['name'], 'error')
  finally:
    db.session.close()
  
  if error:
    abort (500)
  else:
    return redirect(url_for('index'))
  
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }]

  data = []
  shows = Show.query.all()
  for show in shows:
    artist = Artist.query.get(show.artist_id)
    venue = Venue.query.get(show.venue_id)
    data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.isoformat() + 'Z'
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows_form():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm()
  if not form.validate_on_submit():
    for error in form.errors:
      flash(error)
    return render_template('forms/new_show.html', form=form)
  
  return create_show()
  
def create_show():
  error = False
  start_time_str = request.form.get('start_time','')
  print(start_time_str)
  print(type(start_time_str))

  start_time = datetime.fromisoformat(start_time_str)
  # string after strftime(): '2021-02-20 05:45 PM'
  am_pm = start_time.strftime(f'%Y-%m-%d %I:%M %p').split(' ')[2]

  try:
    show = Show(
      artist_id=request.form.get('artist_id',''),
      venue_id=request.form.get('venue_id',''),
      start_time=start_time,
      am= True if am_pm == 'AM' else False,
      day=start_time.weekday()
    )
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('Interal error. Failed to create the show.', 'error')
  finally:
    db.session.close()
  
  if error:
    abort (500)
  else:
    return redirect(url_for('shows'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
