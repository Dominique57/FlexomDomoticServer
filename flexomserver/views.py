import json
from flask import request, Response, render_template
from . import app, db, vapid_public_key, send_web_push, Subscriptions


@app.route('/')
def index():
    subs = list(Subscriptions.query.all())
    for sub in subs:
        print(sub)
    return render_template("index.html")


@app.route('/test', methods=["GET"])
def test():
    subs = list(Subscriptions.query.all())
    message = "Push Test v1"
    try:
        for sub in subs:
            res = send_web_push(sub.to_token(), message)
            if not res.ok:
                app.logger.info(
                    f"WebPush req code ({res.status_code}): deleting non-ok endpoint: {sub}) !")
                db.session.delete(sub)
    finally:
        db.session.commit()
    return render_template("index.html")


@app.route("/subscription/", methods=["GET", "POST"])
def subscription():
    # Return public VAPID key
    if request.method == "GET":
        return Response(
            response=json.dumps({"public_key": vapid_public_key}),
            headers={"Access-Control-Allow-Origin": "*"},
            content_type="application/json"
        )

    # Build subscription instance from request
    req_sub = Subscriptions.from_token(request.get_json())
    if req_sub is None:
        return Response("Given subscription is invalid !", 400)

    # Create instance if not already existing in the database
    sub = Subscriptions.query.filter_by(endpoint=req_sub.endpoint).one_or_none()
    if not req_sub.is_same_token(sub):
        sub = req_sub
        db.session.add(sub)
        db.session.commit()
        app.logger.info(f"New notification token: {sub} !")

    return Response(status=201, mimetype="application/json")
