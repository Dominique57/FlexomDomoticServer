import json
from flask import request, Response, jsonify
from . import app, vapid_public_key, send_web_push


@app.route('/')
def index():
    # sub = Subscriptions(
    #     url="https://lol.fr",
    #     token="lolMDRxd"
    # )
    # db.session.add(sub)
    # db.session.commit()
    # subs = db.session.execute(db.select(Subscriptions).order_by(Subscriptions.id)).scalars()
    # subs = list(subs)
    return "Hello World !"


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
    subscription_token = request.get_json().get("subscription_token")
    print(subscription_token)
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
