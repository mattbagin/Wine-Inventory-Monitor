# Wine-Inventory-Monitor
Simple script that reads a wine inventory stored on Google Sheets and sends emails when wine should be drank.

## Procedure:
Users add entries to the shared wine inventory Google Sheet including the purchase date and vintage.
Currently users are required to enter the max and min range of years for which the style of wine can be aged.
When script is run, it looks through the inventory and identifies wines that are within the suggested age range as well as those that have exceed it and should be drank ASAP.
Script sends an email to the specified users' email addresses with the summarized information above. The email is sent from gmail account **vino.inventory.monitor@gmail.com**. The gmail account is accessed via SMTP using an app password created the Google Account Security page. Password is encrypted for security but stored in a text file within the working directory. Additional security measures can be implemented.
Script would work best if put on a scheduler to run automatically.


## Inputs
Script can be modified to send the emails from other gmail accounts if the user creates an app password for that gmail account. HTML message for the body of the email can be modified as needed, it might be cleaner to store and edit this in a separate text file. Email addresses of recipients are read from file.