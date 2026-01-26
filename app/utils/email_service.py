from os import getenv


def send_email(to_email: str, subject: str, body: str):
    env = getenv("ENVIRONMENT", "development")
    if env == "production":
        # Implement actual email sending logic here using an email service provider
        pass
    # Placeholder function to simulate sending an email
    print(
        f"Sending email to {to_email} with subject '{subject}' and body:\n{body}"
    )
