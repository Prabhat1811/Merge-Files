This is a python script for file merging.

What this does is:
*Takes 2 text files from a specified folder.
*Merges the text from the two files.
*Creates a new file with the merged text in a new folder.
*Sends a conformation email.
*if script was run successfully and all the operations were successfull, it send email about 
which files were merged and the name of the merged file
*if any operation failed, it sends an email containing the logs for that particular script.


Libraries used:
'os' for changing path and other os related functions
'smtplib' for sending email
'logging' for creating logs
