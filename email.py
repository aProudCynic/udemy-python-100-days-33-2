import smtplib

from secrets import (
    TEST_EMAIL_ACCOUNT_USERNAME,
    TEST_EMAIL_ACCOUNT_PASSWORD,
)


def send_mail(content, target_email_address):
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(
            user=TEST_EMAIL_ACCOUNT_USERNAME,
            password=TEST_EMAIL_ACCOUNT_PASSWORD,
        )
        connection.sendmail(
            from_addr=TEST_EMAIL_ACCOUNT_USERNAME,
            to_addrs=target_email_address,
            msg=content,
        )
