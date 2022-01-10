SECRET_KEY = "sna4slack"
SQLALCHEMY_DATABASE_URI = "postgresql://ftfguzup:R_qNlD8OnmwAWUol5EDgFuhuv2ioJ2L7@castor.db.elephantsql.com/ftfguzup"
DEBUG=True
LAYOUT = {
    0: "Random Layout",
    1: "Circular Layout",
    2: "Planar Layout",
    3: "Spiral Layout"
}

METRIC = {
    0: "Degree Centrality",
    1: "Bridges",
    2: "PageRank"
}

UPLOAD_FOLDER="static/uploads"
SQLALCHEMY_TRACK_MODIFICATIONS=True
WAIT_IN_MINUTES=0
WAIT_IN_HOURS=24
WAIT_IN_DAYS=0

DELETE_ELAPSED_STATUS="hours" # hours
DELETE_ELAPSED_TIME_VALUE=24