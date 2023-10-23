# CampaignMaker

Campaign maker details

This is a Django website project. Follow the steps below to set up and run the project locally.
<hr>

# Local

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
- `CALLBACK_API_ENDPOINT`: full url of campaign status approval call
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

Note: Please select the desired status from the following
list: [cancel, payment, disapproved, wait, processing, complete]

This webhook enables seamless integration for managing campaign statuses within your application.

## Additional Information

You can find more information and documentation for Django at [Django Documentation](https://docs.djangoproject.com/).

# Deployment

## Using Docker and Docker Compose

Follow these steps to set up and run your Django project using Docker and Docker Compose:

1. **Install Docker and Docker Compose on your virtual machine.** You can find installation instructions in
   the [Docker documentation](https://docs.docker.com/get-docker/)
   and [Docker Compose documentation](https://docs.docker.com/compose/install/).

2. **Navigate to the project root directory:**

```
cd /path/to/your/project
```

3. **Build and run Docker containers for the first time:**

```
docker-compose up --build -d
```

For subsequent runs, you can simply use:

```
docker-compose up -d
```

4. **Access the Django container's bash:**

```
docker exec -it django /bin/bash
```

Now you are inside the Django container, and you can interact with it directly. Use `ls` to explore the container's
root.

5. **Create a superuser within the Django container:**

```
python manage.py createsuperuser
```

6. **Collect static files:**

   If your project uses static files, run the following command:

```
python manage.py collectstatic
```

7. **Shutdown the containers:**

   To stop and remove the containers, use:

```
docker-compose down
```

8. **View container logs:**

   To view container logs, you can use:

```
docker-compose logs
```

These instructions will help you set up, run, and manage your Project using Docker and Docker Compose

# Obtaining SSL Certificates with Certbot

Before running your Docker containers, it's recommended to secure your project with SSL certificates. You can obtain a
free SSL certificate using Certbot, and here's how:

1. **Install Certbot:**

   You can install Certbot by following the instructions provided in
   the [Certbot documentation](https://certbot.eff.org/).

2. **Generate SSL Certificate:**

   Use the following command to generate a free SSL certificate for your domain. Replace `"your domain"` with your
   actual domain name.
```
certbot certonly --standalone -d "your domain" --register-unsafely-without-email --agree-tos
```
Certbot will create the necessary certificate files and display the path to these files.

3. **Copy the Certificate Files:**

   You'll need to copy the certificate files to your project's `cert` folder before running your Docker containers.
   Replace `path_to_fullchain.pem` with the path provided by Certbot.
```
cp path_to_fullchain.pem /fullchain.pem path_to_project_directory/cert/cert.crt
cp path_to_privkey.pem /privkey.pem path_to_project_directory/cert/private.key
```
Make sure to replace `path_to_project_directory` with the actual path to your project directory.

4. **Run Docker Containers:**

   After copying the certificate files, you can proceed to run your Docker containers as described in the previous
   section.

By following these steps, your Django project will be accessible via HTTPS using the SSL certificates you obtained with
Certbot.

Remember to replace `"your domain"` and `path_to_project_directory` with the actual domain name and project directory
path. These instructions will guide users on how to secure their Django project with SSL certificates.