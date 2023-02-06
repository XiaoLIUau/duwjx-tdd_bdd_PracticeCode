from flask import Flask
import status

app = Flask(__name__)

COUNTERS = {}

@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Creates a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS

    if name in COUNTERS:
        return {"message":f"Counter {name} already exists"}, status.HTTP_409_CONFLICT

    COUNTERS[name] = 0
    return { name: COUNTERS[name] }, status.HTTP_201_CREATED

@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """Update a counter"""
    app.logger.info(f"Request to Update counter: {name}")
    global COUNTERS

    if name not in COUNTERS:
        return {"message":f"Counter {name} dosen't exist"}, status.HTTP_404_NOT_FOUND

    COUNTERS[name] += 1
    return { name: COUNTERS[name] }, status.HTTP_200_OK

@app.route("/counters/<name>", methods=["GET"])
def read_counter(name):
    """Read a counter"""
    app.logger.info(f"Request to Read counter: {name}")
    global COUNTERS

    if name not in COUNTERS:
        return {"message":f"Counter {name} dosen't exist"}, status.HTTP_404_NOT_FOUND

    return { name: COUNTERS[name] }, status.HTTP_200_OK

@app.route("/counters/<name>", methods=["DELETE"])
def delete_counter(name):
    """Delete a counter"""
    app.logger.info(f"Request to Delete counter: {name}")
    app.logger.info(f"Counter: {name} has been deleted")
    global COUNTERS
    
    if name not in COUNTERS:
        return {"message":f"Counter {name} dosen't exist"}, status.HTTP_404_NOT_FOUND

    # delete the count
    del(COUNTERS[name])

    return '', status.HTTP_204_NO_CONTENT