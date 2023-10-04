import os
from bs4 import BeautifulSoup
import requests
from .models import Settings

from bs4 import BeautifulSoup


def call_api(model):
    setting = Settings.objects.first()
    url = os.getenv("CALLBACK_API_URL")
    try:
        zips = [item.code for item in model.zips.all()]

        # Get the plain text from the email body
        striped_html = BeautifulSoup(model.campaign_email.body, "html.parser").get_text()

        # Read the audio file
        with open(model.campaign_audio.file.path, "rb") as f:
            audio_file = f.read()

        # Prepare data for the API request
        data = {
            "campaign_id": model.id,
            "package_type_id": model.type.id,
            "zip_code_1": zips[0] if zips else "",
            "zip_code_2": zips[1] if len(zips) > 1 else "",
            "zip_code_3": zips[2] if len(zips) > 2 else "",
            "sms_msg": model.campaign_sms.body,
            "email_subject": model.campaign_email.subject,
            "plain_email": striped_html,
            "html_email": model.email_template.get_rendered_content(
                {"body": model.campaign_email.body, "greeting": model.campaign_email.type.name}
            ),
            "audio_filename": audio_file,
        }

        # Make the API request
        result = requests.post(url=url, headers={"X-API-Key": setting.api_token}, data=data)

        if result.ok:
            print("Call successful")
        else:
            print("Call failed")
            print(result.text)

    except Exception as e:
        print(f"An error occurred: {e}")
