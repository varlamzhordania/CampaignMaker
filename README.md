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

5Run the following commands to set up the database:

```
python manage.py makemigrations

python manage.py migrate
```

## Create Superuser

6. To create a superuser account for administrative access, run the following command:

```
python manage.py createsuperuser
```

Follow the prompts to set up the superuser account.

## Running the Server

7. Start the development server:

```
python manage.py runserver
```

The website should now be accessible at `http://localhost:8000/`.

## Additional Information

You can find more information and documentation for Django at [Django Documentation](https://docs.djangoproject.com/).
