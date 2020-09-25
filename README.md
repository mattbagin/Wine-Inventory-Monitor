# Wine-Inventory-Monitor
Simple script that reads a wine inventory stored on Google Sheets and sends emails when wine should be drank.

Procedure:
Users add entries to the shared wine inventory Google Sheet including the purchase date and vintage.
Currently users are required to enter the max and min range of years for which the style of wine can be aged.
When script is run, it looks through the inventory and identifies wines that are within the suggested age range as well as those that have exceed it and should be drank ASAP.
Script sends an email to the specified users' email addresses with the summarized information above. The email is sent from gmail account vino.inventory.monitor@gmail.com.
Script would work best if put on a scheduler to run automatically.
