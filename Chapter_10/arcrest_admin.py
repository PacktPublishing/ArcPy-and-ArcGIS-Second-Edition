import arcrest
from arcresthelper import securityhandlerhelper

#build dictionary of log in info to be used in security handler
login_info = {'username': raw_input("Enter User Name: "), 'password': raw_input("Enter Password: ")}
token = securityhandlerhelper.securityhandlerhelper(login_info)
#access admin rights
admin = arcrest.manageorg.Administration(securityHandler=token.securityhandler)
content = admin.content
# Get the logged in user
user_info = content.users.user()
# List titles and sharing status for items in users' home folder
for item in user_info.items:
    print item.id
    print "[%s]\t%s" % (item.sharing['access'], item.title)
