import arcrest
username = raw_input("Enter username: ")
password = raw_input("Enter password: ")
#access security handler for AGOL account
security_handler = arcrest.AGOLTokenSecurityHandler(username,password)
print security_handler
