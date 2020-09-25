import gspread
import pandas as pd
import smtplib
import HashPassword as Hash
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_inventory_sheet():
    today = date.today()

    gc = gspread.oauth()

    sh = gc.open("Wine Inventory")

    worksheet = sh.get_worksheet(0)

    complete_inv = pd.DataFrame(worksheet.get_all_records())

    complete_inv["Date Purchased"] = pd.to_datetime(
        complete_inv["Date Purchased"]
    ).dt.date
    complete_inv["Consume By Date (Lower)"] = pd.to_datetime(
        complete_inv["Consume By Date (Lower)"]
    ).dt.date
    complete_inv["Consume By Date (Upper)"] = pd.to_datetime(
        complete_inv["Consume By Date (Upper)"]
    ).dt.date

    drink_soon = complete_inv.loc[(complete_inv["Consume By Date (Upper)"] <= today)]

    in_range = complete_inv.loc[
        (complete_inv["Consume By Date (Lower)"] <= today)
        & (complete_inv["Consume By Date (Upper)"] >= today)
    ]

    return drink_soon, in_range


def send_mail(user, pw, email_list, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(user, pw)

    to = ""
    for e in email_list:
        to = to + e + ";"

    email_msg = MIMEMultipart("alternative")

    email_msg["Subject"] = "Wine Inventory Notification - {}".format(
        date.today().strftime("%Y/%m/%d")
    )

    email_msg["From"] = user

    msg_body = MIMEText(msg, "html")

    email_msg.attach(msg_body)

    server.sendmail(user, to, email_msg.as_string())

    print(f"Email sent to {to}")


if __name__ == "__main__":

    with open("encrypted.txt", "rb") as pw_file:
        key = pw_file.readline().strip()
        cipher_text = pw_file.readline()

    user = "vino.inventory.monitor@gmail.com"
    pw = Hash.decrypt(key, cipher_text).decode("utf-8")

    drink_soon, in_range = get_inventory_sheet()

    email_body = """
        <html>
            <body>
                <p><span style="font-family:Arial;font-size:10pt">The following wines are past their optimal aging time. Please consider drinking very soon!</span>
                <br>
                {0}
                <br>
                <br>
                <span style="font-family:Arial;font-size:10pt">The following wines are within their suggested age range based on their style.</span>
                {1}
                </p>    
            </body>
        </html>""".format(
        drink_soon.to_html(index=False), in_range.to_html(index=False)
    )

    send_mail(user=user, pw=pw, email_list=["matthew.bagin@gmail.com"], msg=email_body)
