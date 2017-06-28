#tested and worked Succesfully
import arcrest

if __name__ == "__main__":
    #url for the admin site your accessing
    url = "https://services7.arcgis.com/LLWzNvydeNCpjeTo/arcgis/rest/admin"
    username = raw_input("Enter User Name: ")
    password = raw_input("Enter Password: ")
    #name of layer contained within feature service
    feature_layer_names = ["mta_bicycle_route_network"] # must be all lowercase
    #definition of the domain
    definition = {
        "fields": [
            {
                "name": "BIKEROUTE",
                "domain": {
                    "type": "codedValue",
                    "name": "RouteType",
                    "codedValues": [
                        {
                            "name": "Option A",
                            "code": "type_a"
                        },
                        {
                            "name": "Option B",
                            "code": "type_b"
                        },
                        {
                            "name": "Option C",
                            "code": "type_c"
                        }
                    ]
                }
            }
        ]
    }
    #retrieve the security handle for the token
    security_handler = arcrest.AGOLTokenSecurityHandler(username, password)
    #retrieve the services by passing url and token
    agol_services = arcrest.hostedservice.Services(url, security_handler)
    print "url is ", url
    print agol_services
    print agol_services.services
    #loop over each service to find a field to assign domain to
    for service in agol_services.services:
        print service
        #check if service has layers
        if service.layers is not None:
            print service.url
            #get the lyr name in service
            for lyr in service.layers:
                print lyr.name
                #if the layer is in your list as all lower update the definition
                if lyr.name.lower() in feature_layer_names:
                    print lyr.updateDefinition(definition)
