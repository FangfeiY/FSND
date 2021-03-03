from fyyur_db import db
from datetime import datetime, date, time
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