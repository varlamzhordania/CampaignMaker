from django.contrib import messages


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
