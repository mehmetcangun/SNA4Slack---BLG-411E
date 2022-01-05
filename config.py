SECRET_KEY = "sna4slack"
SQLALCHEMY_DATABASE_URI = "postgresql://ftfguzup:R_qNlD8OnmwAWUol5EDgFuhuv2ioJ2L7@castor.db.elephantsql.com/ftfguzup"
DEBUG=True
LAYOUT = {
    0: "Bipartite Layout",
    1: "Circular Layout",
    2: "Planar Layout",
    3: "Spiral Layout"
}

METRIC = {
    0: "Degree Centrality",
    1: "Bridges",
    2: "All Pairs Node Connectivity"
}

UPLOAD_FOLDER="static/uploads"