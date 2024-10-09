import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from ashpotexamine.config.django.base import FRONT_END_HOST_FULL_URL
from django.core.mail import BadHeaderError
from smtplib import SMTPException
import socket
from django.conf import settings
from django.http import request
from .logging import LoggingMixin
from ashpotexamine.config.settings.email_sending import EMAIL_HOST_USER

class EmailSender:
    def __init__(self, subject, from_email=EMAIL_HOST_USER):
        self.subject = subject
        self.from_email = from_email
        self.request = request

    def send_email_async(self, html_content, text_content, to):
        try:
            email = EmailMultiAlternatives(self.subject, text_content, self.from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()
        except BadHeaderError:
            LoggingMixin("Invalid header found in the email.").log()
        except SMTPException as e:
            LoggingMixin(f"SMTP error occurred: {e}").log()
        except socket.gaierror:
            LoggingMixin("Network error: Unable to connect to the mail server.").log()
        except TimeoutError:
            LoggingMixin("Timeout error: The connection to the mail server timed out.").log()
        except Exception as e:
            LoggingMixin(f"An unexpected error occurred: {e}").log()

    def _start_email_thread(self, html_content, text_content, to):
        email_thread = threading.Thread(target=self.send_email_async, args=(html_content, text_content, to))
        email_thread.start()

    def send_otp_email(self, email, first_name, otp_code, time):
        to = email
        html_content = render_to_string('otp_email_template.html', {
            'email': email,
            'first_name': first_name,
            'otp_code': otp_code,
            'time': time
        })
        text_content = strip_tags(html_content)
        # try:
        self._start_email_thread(html_content, text_content, to)
        # except Exception as e:
            # LoggingMixin(f"{e}")    

    # def send_forgot_password_link(self, request, email,first_name,uid, token, expiry):
    #     try:
    #         to = email
    #         # Automatically determine the scheme based on the request
    #         scheme = 'https' if request.is_secure() else 'http'
            
    #         link = f"{scheme}://{self.request.get_host()}?uid={uid}&token={token}"

    #         html_content = render_to_string('forgot-password_template.html', {
    #             'email': email,
    #             'first_name': first_name,
    #             'link': link,
    #             'expiry': expiry
    #         })
    #         text_content = strip_tags(html_content)
    #         self._start_email_thread(html_content, text_content, to)
    #     except BadHeaderError:
    #         ("Invalid header found in the email.")
    #     except SMTPException as e:
    #         return(f"SMTP error occurred while sending the forgot password email: {e}")
    #     except socket.gaierror:
    #         return("Network error: Unable to connect to the mail server.")
    #     except TimeoutError:
    #         return("Timeout error: The connection to the mail server timed out.")
    #     except ConnectionRefusedError:
    #         return("The connection was refused by the mail server.")
    #     except socket.error as e:
    #         return(f"Socket error: {e}")
    #     except Exception as e:
    #         return(f"An unexpected error occurred: {e}")

# Usage Example
# email_sender = EmailSender(subject='Reset Your Password')
# email_sender.send_forgot_password_link(request, email, user_id, first_name, token)
