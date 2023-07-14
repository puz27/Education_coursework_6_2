import smtplib
from django.core.mail import send_mail
from django.conf import settings
from django.template.defaultfilters import slugify as d_slugify
import schedule
import time
import mailing.models
import pytz
from datetime import datetime


def convert_word(words: str) -> str:
    """Slugify for russian language"""
    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                'и': 'i',
                'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e',
                'ю': 'yu',
                'я': 'ya'}

    return d_slugify(''.join(alphabet.get(w, w) for w in words.lower()))


def sendmail_registration(new_user_email: list, message_theme: str, message_body: str):
    """Send mail for registration"""
    send_mail(message_theme, message_body, settings.EMAIL_HOST_USER, [new_user_email], fail_silently=True)


def sendmail(transmission_id: str, emails_base: list, message_theme: str, message_body: str) -> None:
    """Send mail"""
    try:
        send_mail(message_theme, message_body, settings.EMAIL_HOST_USER, emails_base, fail_silently=True)

        statistic = mailing.models.Statistic.objects.get(transmission_id=transmission_id)
        statistic.status = "FINISHED"
        statistic.mail_answer = "OK"
        statistic.time = datetime.now(pytz.timezone('Europe/Moscow'))
        statistic.save()

        change_transmission_status = mailing.models.Transmission.objects.get(id=transmission_id)
        change_transmission_status.status = "FINISHED"
        change_transmission_status.save()

        print("SEND MAIL")

    except smtplib.SMTPException as send_error:

        print("PROBLEMS WITH SEND MAIL")
        statistic = mailing.models.Statistic.objects.get(transmission_id=transmission_id)
        statistic.status = "FINISHED"
        statistic.mail_answer = "ERROR"
        statistic.time = datetime.now(pytz.timezone('Europe/Moscow'))
        statistic.save()

        change_transmission_status = mailing.models.Transmission.objects.get(id=transmission_id)
        change_transmission_status.status = "FINISHED_WITH_ERROR"
        change_transmission_status.save()


def run_schedule():
    """Work with scheduler"""
    schedule.clear()
    active_transmissions = mailing.models.Transmission.objects.filter(is_published=True)
    print("PREPARE SEND")

    # DAILY SCHEDULER
    for transmission in active_transmissions:
        emails_base = []
        print("TRANSMISSION TITLE:", transmission.title)

        if transmission.frequency == "DAILY":
            print("TYPE: SEND DAILY")
            print("ID:", transmission.pk)
            convert_time = str(transmission.time)[:5]
            print("TIME:", convert_time)
            message = transmission.get_messages()
            print("MESSAGE THEME:", message.theme)
            print("MESSAGE BODY:", message.body)
            for client_mail in transmission.get_clients():
                print("EMAIL:", client_mail.email)
                emails_base.append(client_mail.email)
                print(emails_base)

                schedule.every().day.at(convert_time).do(sendmail,
                                                         emails_base=emails_base,
                                                         message_theme=message.theme,
                                                         message_body=message.body,
                                                         transmission_id=transmission.pk
                                                         )
                change_transmission_status = mailing.models.Transmission.objects.get(id=transmission.pk)
                change_transmission_status.status = "READY"
                change_transmission_status.save()

        # WEEKLY SCHEDULER
        today = datetime.today().weekday()
        if transmission.frequency == "WEEKLY":
            print("TYPE: SEND WEEKLY")
            print("ID:", transmission.pk)
            convert_time = str(transmission.time)[:5]
            print("TIME:", convert_time)
            message = transmission.get_messages()
            print("MESSAGE THEME:", message.theme)
            print("MESSAGE BODY:", message.body)
            for client_mail in transmission.get_clients():
                print("EMAIL:", client_mail.email)
                emails_base.append(client_mail.email)
                print(emails_base)

                if today == 0:
                    schedule.every().sunday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                message_theme=message.theme, message_body=message.body,
                                                                transmission_id=transmission.pk)
                if today == 1:
                    schedule.every().monday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                message_theme=message.theme, message_body=message.body,
                                                                transmission_id=transmission.pk)
                if today == 2:
                    schedule.every().tuesday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                 message_theme=message.theme, message_body=message.body,
                                                                 transmission_id=transmission.pk)
                if today == 3:
                    schedule.every().wednesday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                   message_theme=message.theme, message_body=message.body,
                                                                   transmission_id=transmission.pk)
                if today == 4:
                    schedule.every().thursday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                  message_theme=message.theme, message_body=message.body,
                                                                  transmission_id=transmission.pk)
                if today == 5:
                    schedule.every().friday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                message_theme=message.theme, message_body=message.body,
                                                                transmission_id=transmission.pk)
                if today == 6:
                    schedule.every().saturday.at(convert_time).do(sendmail, emails_base=emails_base,
                                                                  message_theme=message.theme, message_body=message.body,
                                                                  transmission_id=transmission.pk)

                change_transmission_status = mailing.models.Transmission.objects.get(id=transmission.pk)
                change_transmission_status.status = "READY"
                change_transmission_status.save()

        # MONTHLY SCHEDULER
        if transmission.frequency == "MONTHLY":
            print("TYPE: SEND MONTHLY")
            print("ID:", transmission.pk)
            convert_time = str(transmission.time)[:5]
            print("TIME:", convert_time)
            message = transmission.get_messages()
            print("MESSAGE THEME:", message.theme)
            print("MESSAGE BODY:", message.body)
            for client_mail in transmission.get_clients():
                print("EMAIL:", client_mail.email)
                emails_base.append(client_mail.email)
                print(emails_base)
                schedule.every(4).weeks.do(sendmail, emails_base=emails_base, message_theme=message.theme,
                                           message_body=message.body, transmission_id=transmission.pk)

                change_transmission_status = mailing.models.Transmission.objects.get(id=transmission.pk)
                change_transmission_status.status = "READY"
                change_transmission_status.save()

        print("ALL JOBS:")
        print(schedule.get_jobs())

    while True:
        schedule.run_pending()
        time.sleep(1)
