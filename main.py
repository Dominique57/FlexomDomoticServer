import json
import os
from flask import request, Response, render_template, jsonify, Flask
from pywebpush import webpush
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


vapid_dir = os.environ.get("VAPID_DIR")
with open(os.path.join(vapid_dir, "private_key.pem"), "r+") as f:
    vapid_private_key = f.readline().strip("\n")
with open(os.path.join(vapid_dir, "public_key.pem"), "r+") as f:
    vapid_public_key = f.read().strip("\n")

vapid_claims = {
    "sub": os.environ.get("VAPID_CLAIM_EMAIL")
}


def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=vapid_private_key,
        vapid_claims=vapid_claims
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/subscription/", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients uses to send around push notification
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
