import json
from flask import request, Response, jsonify, render_template
from . import app, db, vapid_public_key, send_web_push, Subscriptions


@app.route('/')
def index():
    subs = list(Subscriptions.query.all())
    return render_template("index.html")


@app.route("/subscription/", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients use to send around push notification
    """
    if request.method == "GET":
        return Response(
            response=json.dumps({"public_key": vapid_public_key}),
            headers={"Access-Control-Allow-Origin": "*"},
            content_type="application/json"
        )
    browser_subscription = request.get_json()
    endpoint = browser_subscription.get('endpoint')
    expiration_time = browser_subscription.get('expirationTime')
    keys_auth = browser_subscription.get('keys', {}).get('auth')
    keys_p256dh = browser_subscription.get('keys', {}).get('p256dh')
    if endpoint is None or keys_auth is None or keys_p256dh is None:
        return Response("Given subscription is incomplete", 400)

    sub = Subscriptions(
        endpoint=endpoint,
        expiration_time=expiration_time,
        keys_auth=keys_auth,
        keys_p256dh=keys_p256dh
    )
    db.session.add(sub)
    db.session.commit()
    return Response(status=201, mimetype="application/json")


@app.route("/push_v1/", methods=['POST'])
def push_v1():
    message = "Push Test v1"
    print("is_json", request.is_json)

    if not request.json or not request.json.get('sub_token'):
        return jsonify({'failed': 1})

    print("request.json", request.json)

    token = request.json.get('sub_token')
    try:
        token = json.loads(token)
        send_web_push(token, message)
        return jsonify({'success': 1})
    except Exception as e:
        print("error", e)
        return jsonify({'failed': str(e)})
