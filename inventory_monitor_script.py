import gspread
import pandas as pd
import smtplib
import HashPassword as Hash
from datetime import date


def get_inventory_sheet():
    today = date.today()

    gc = gspread.oauth()

    sh = gc.open("Wine Inventory")

    worksheet = sh.get_worksheet(0)

    complete_inv = pd.DataFrame(worksheet.get_all_records())

    drink_soon = complete_inv.loc[(complete_inv["Consume By Date (Upper)"] >= today)]

    in_range = complete_inv.loc[
        (complete_inv["Consume By Date (Lower)"] >= today)
        & (complete_inv["Consume By Date (Upper)"] <= today)
    ]

    return drink_soon, in_range


def send_mail(user, pw, email_list):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(user, pw)

    for e in email_list:
        to = to + e + ";"

    subject = "Email Subject Line"
    body = "Email body"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(user, to, msg)

    print(f"Email sent to {to}")


if __name__ == "__main__":

    with open("encrypted.txt", "rb") as pw_file:
        key = pw_file.readline().strip()
        cipher_text = pw_file.readline()

    user = "vino.inventory.monitor@gmail.com"
    pw = Hash.decrypt(key, cipher_text).decode("utf-8")