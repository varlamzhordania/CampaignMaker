# CampaignMaker

Campaign maker details

This is a Django website project. Follow the steps below to set up and run the project locally.
<hr>

## Getting Started

1. Clone this repository to your local machine.

```
git clone https://github.com/varlamzhordania/CampaignMaker.git
```

2. Change directory to the `backend` folder.

```
cd backend
```

3. Create a virtual environment named `venv`.

```
python -m venv venv
```

4. Activate the virtual environment:

    - On Windows:

```
venv\Scripts\activate
```

- On macOS and Linux:

```
source venv/bin/activate
```

## Download Packages

5. Run the following commands for download and installing requirement packages:

```
pip install -r requirements.txt
```

## Database Setup

6. Run the following commands to set up the database:

```
python manage.py makemigrations

python manage.py migrate
```

## Create Superuser

7. To create a superuser account for administrative access, run the following command:

```
python manage.py createsuperuser
```

## Create Admin Group

8. To establish an administrative access group, navigate to the Django admin group page
   at `http://localhost:8000/admin/auth/group/`. Here, create a group named 'admin.' You do not need to configure
   permissions at this point. The group name is the primary concern. Afterward, assign your user to this 'admin' group.
   This will grant them access to the campaign page from the main dashboard, without providing access to the Django
   admin interface.

## Running the Server

9. Start the development server:

```
python manage.py runserver
```

The website should now be accessible at `http://localhost:8000/`.

## Settings Setup

In the core/settings directory, you'll find the following key files:

- `development.py`
- `production.py`
- `settings.py`

Please exercise caution when modifying `settings.py` unless you're well-acquainted with it.

The core and critical settings are managed in the .env file, where you can make adjustments to:

- `DJANGO_DEBUG`: Change the application mode to either development or production.
- `DJANGO_SECRET_KEY`: This field enhances Django's security and is crucial for production. Django provides tools for
  generating it using Python CLI.
- `STRIPE_SECRET_KEY`: Obtain this key from your Stripe Developer Dashboard.
- `STRIPE_WEBHOOK_ENDPOINT_SECRET_KEY`: When connecting webhooks through the Stripe CLI or Dashboard, you'll receive
  this field.
- `BASE_DOMAIN`: Set your domain for callback URLs.
- `DB_NAME`: Your database name.
- `DB_USER`: postgres
- `DB_PASSWORD`: Your database password.
- `DB_HOST`: 127.0.0.1
- `DB_PORT`: 5432
- `EXTERNAL_API_BASE_URL`: Flask Server Base Url
- `EMAIL_HOST`: your email service host.
- `EMAIL_PORT`: port
- `EMAIL_USE_TLS`: (False/True).
- `EMAIL_HOST_USER`: user
- `EMAIL_HOST_password`: password
- `CALLBACK_API_URL`: full url of campaign status approval call
  <h5>NOTE: for development you dont have to fill email service fields<h5/>
  <h5>NOTE: in production default database will be POSTGRESQL unless you change it at `production.py`<h5/>
  <h5>NOTE: in development mode will use SQLITE unless you change it at `development.py`<h5/>

## Stripe CLI

To learn how to use the Stripe CLI effectively, refer to
the [Stripe CLI Documentation](https://stripe.com/docs/stripe-cli). This resource provides detailed guidance and
instructions on its usage.

<h5>NOTE: without webhook, campaign status wont change after payment and set stripe webhook
at `localhost:8000/checkout/webhook/`<h5/>

## Webhook

To change the status of a campaign from your backend server, you can initiate a POST request to the following URL:

- URL: `<your_domain>/dashboard/campaign/webhook/`
- Method: `POST`
- Parameters:
  - `campaign_id`: The campaign ID you wish to update the status for.
  - `status`: The desired status to set for the campaign.

Note: Please select the desired status from the following list: [cancel, payment, disapproved, wait, processing, complete]

This webhook enables seamless integration for managing campaign statuses within your application.
## Additional Information

You can find more information and documentation for Django at [Django Documentation](https://docs.djangoproject.com/).
