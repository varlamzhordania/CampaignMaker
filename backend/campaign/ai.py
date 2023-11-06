import openai

api_key = "your-key"
openai.api_key = api_key


def check_email_spam(client_email_header, client_email_content):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Check if the following email content is spam:\nHeader: {client_email_header}\nContent: {client_email_content}",
        max_tokens=50,
    )

    spam_check_result = response.choices[0].text.strip()

    return spam_check_result


def generate_email_versions(client_email_header, client_email_content):
    generated_versions = []
    for _ in range(20):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Generate a new version of the email header: {client_email_header}\nContent: {client_email_content}",
            max_tokens=50,
        )
        new_header = response.choices[0].text.strip()
        generated_versions.append((new_header, client_email_content))

    return generated_versions


def check_spam_free_versions(versions):
    spam_free_versions = []
    for header, content in versions:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Check if the following email content is spam:\nHeader: {header}\nContent: {content}",
            max_tokens=50,
        )
        spam_check_result = response.choices[0].text.strip()
        if "not spam" in spam_check_result:
            spam_free_versions.append((header, content))

    return spam_free_versions
