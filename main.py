import threading
from flask import Flask, request, Response
import logging
import tp_link_api

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


@app.route("/sms", methods=["POST"])
def send_sms():
    # get phone number
    phone_number = request.form.get("phone_number")

    # get message
    message = request.form.get("message")

    max_message_length = 765
    if len(message) > max_message_length:
        return Response(status=400, response=f"Message is too long. Max length is {max_message_length} characters.")

    # send sms
    tp_link_api.send_sms(phone_number, message)

    return Response(status=200, response=f"Sent SMS to {phone_number}.")


if __name__ == "__main__":
    # init tp link api
    thread = threading.Thread(target=tp_link_api.init_sms)
    thread.start()

    app.run(host="0.0.0.0", port=8080)
