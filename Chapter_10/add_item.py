"""
   This sample shows how to add an item
   version 3.0.1
   Python 2
"""
import arcrest
from arcresthelper import securityhandlerhelper

def main():

    login_info = {}
    login_info['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    login_info['username'] = ""
    login_info['password'] = ""
    login_info['org_url'] = "http://www.arcgis.com"

    upload_file = r"c:\test\test.png"
    security_handler_helper = securityhandlerhelper.securityhandlerhelper(login_info)
    if security_handler_helper.valid == False:
        print security_handler_helper.message
    else:
        admin = arcrest.manageorg.Administration(securityHandler=security_handler_helper.securityhandler)
        content = admin.content
        userInfo = content.users.user()
        item_params = arcrest.manageorg.ItemParameter()
        item_params.title = 'Sample'
        item_params.type = "Image"
        item_params.overwrite = True
        item_params.description = "Test File"
        item_params.tags = "tags"
        item_params.snippet = "Test File"
        item_params.typeKeywords = "Data,Image,png"
        #itemParams.filename = upload_file
        item = userInfo.addItem(
            itemParameters=item_params,
            filePath= upload_file,
            overwrite=True,
            relationshipType=None,
            originItemId=None,
            destinationItemId=None,
            serviceProxyParams=None,
            metadata=None)
        print item.title + " created"

if __name__ == "__main__":
    main()
