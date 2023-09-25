from django.contrib import messages
import re


def is_admin(user):
    return user.is_superuser or user.is_staff or user.groups.filter(name="admin").exists()


def fancy_message(request, body, level="info"):
    if isinstance(body, dict):
        for field_name, error_list in body.items():
            for error in error_list:
                messages.add_message(
                    request,
                    messages.ERROR if level == "error" else messages.INFO,
                    f"{field_name}: {error}"
                )
    elif isinstance(body, str):
        messages.add_message(request, messages.ERROR if level == "error" else messages.INFO, body)
    else:
        raise ValueError("Unsupported message body type")


def string_to_context(input_string):
    # Define a regular expression pattern to match context variables like '{{ variable_name }}'
    pattern = r'\{\{([\w\s\?,]+)\}\}'

    # Use regular expressions to find all matches in the input string
    matches = re.findall(pattern, input_string)

    # Create a context dictionary to store variable names and their values
    context = {}

    for match in matches:
        # Split the match into variable name and value using ','
        parts = match.split(',')

        # The first part is the variable name (trimmed of whitespace)
        variable_name = parts[0].strip()

        # The second part (if present) is the value (trimmed of whitespace)
        variable_value = parts[1].strip() if len(parts) > 1 else ''

        # Add the variable and its value to the context dictionary
        context[variable_name] = variable_value

    return context
