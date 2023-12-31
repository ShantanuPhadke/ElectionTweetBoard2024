from electiontweetboard import db

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_term = db.Column(db.String(40), unique=False, nullable=False)
    tweet = db.Column(db.String(280), unique=False, nullable=False)
    sentiment = db.Column(db.String(40), unique=False, nullable=False)

    def __repr__(self):
        return f"Tweet ('{self.query_term}', '{self.tweet}', '{self.sentiment}')"

class SentimentDistribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_term = db.Column(db.String(40), unique=False, nullable=False)
    positive_percent = db.Column(db.Float, unique=False, nullable=False)
    negative_percent = db.Column(db.Float, unique=False, nullable=False)
    neutral_percent = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f"SentimentDistribution ('{self.query_term}', '{self.positive_percent}', '{self.negative_percent}', '{self.neutral_percent}')"

class SentimentsOverTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_term = db.Column(db.String(40), unique=False, nullable=False)
    timestamp = db.Column(db.String(10), unique=False, nullable=False)
    positive_percent = db.Column(db.Float, unique=False, nullable=False)
    negative_percent = db.Column(db.Float, unique=False, nullable=False)
    neutral_percent = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f"SentimentsOverTime ('{self.query_term}', '{self.timestamp}', '{self.positive_percent}', '{self.negative_percent}', '{self.neutral_percent}')"

class QuickLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_term = db.Column(db.String(40), unique=False, nullable=False)
    link = db.Column(db.String(140), unique=False, nullable=False)
    source = db.Column(db.String(140), unique=False, nullable=True)
    title = db.Column(db.String(140), unique=False, nullable=True)
    subtitle = db.Column(db.String(140), unique=False, nullable=True)
    image_url = db.Column(db.String(140), unique=False, nullable=True)

    def __repr__(self):
        return f"QuickLink ('{self.query_term}', '{self.link}', '{self.source}', '{self.title}', '{self.subtitle}', '{self.image_url}')"