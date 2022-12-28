from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def sendTemplate(
        to_emails,
        template_id,
        data_keys,
        data_values,
        from_email=settings.SENDGRID_DEFAULT_SENDER):

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
    )

    template_data = {}

    for key, value in zip(data_keys, data_values):
        template_data[key] = value

    message.template_id = template_id
    message.dynamic_template_data = template_data

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Dynamic Messages Sent!")
    except Exception as e:
        return str("Error: {0}".format(e))
    return str(response.status_code)
