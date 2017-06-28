from arcrest.security import AGOLTokenSecurityHandler
from arcrest.agol import FeatureLayer

if __name__ == "__main__":
    username = raw_input("Enter User Name: ")
    password = raw_input("Enter Password: ")
    #list of urls to add a field to
    #you can add this field to muiltple feature services if you'd like. Just add them to this list
    urls = ["http://services7.arcgis.com/LLWzNvydeNCpjeTo/arcgis/rest/services/BikeRoute/FeatureServer/0"]
    #if you use a proxy generally for on site services like arcgis server or portal
    proxy_port = None
    proxy_url = None

    #get the security handle token
    agol_security_handler = AGOLTokenSecurityHandler(username=username,
                                      password=password)

    #loop over the urls in the list of urls
    for url in urls:
        #create feature layer using feature layer
        feature_layer = FeatureLayer(
            url=url,
            securityHandler=agol_security_handler,
            proxy_port=proxy_port,
            proxy_url=proxy_url,
            initialize=True)
        #access admin rights to feature layer
        admin_feature_layer = feature_layer.administration
        field_to_add = {
            "fields" : [
                {
                    "name" : "BIKEROUTE",
                    "type" : "esriFieldTypeString",
                    "alias" : "Bike Route",
                    "sqlType" : "sqlTypeOther", "length" : 10,
                    "nullable" : True,
                    "editable" : True,
                    "domain" : None,
                    "defaultValue" : None
                }  ]
        }
        #execute the add field method
        print admin_feature_layer.addToDefinition(field_to_add)
