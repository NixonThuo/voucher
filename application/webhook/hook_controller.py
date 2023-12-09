from flask import Blueprint, request
import json
from application.main.main_model import CreditServicesTr
from datetime import datetime
from application import db

hook = Blueprint('hook', __name__)


@hook.route('/paymenthook', methods=['POST'])
def payment_hook():
    request_body = request.get_data(as_text=True)

    print(request_body)
    #convert string to  object
    json_object = json.loads(request_body)

    hookid = json_object['payload']['id']
    yocoid = json_object['payload']['metadata']['checkoutId']
    status = json_object['payload']['status']
    paymentmethod = json_object['payload']['paymentMethodDetails']['type']

    success = False

    if status == "succeeded":
        success = True

    trans = CreditServicesTr.query.filter_by(
        yoco_paymentid=yocoid
    ).first()

    if trans:
        trans.hook_id = hookid
        trans.payment_method = paymentmethod
        trans.marked_paid = success
        trans.marked_paid_time = datetime.now()
        trans.full_webhook = request_body

    db.session.commit()

    return "", 200
