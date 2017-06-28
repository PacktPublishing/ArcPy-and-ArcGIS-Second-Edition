import arcrest
import json
from arcresthelper import featureservicetools
from arcresthelper import common

if __name__ == "__main__":


    #create empty dictionary called "securityinfo"
    login_info = {}
    #create Key:Pair values for dictionary
    login_info['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    login_info['username'] = "arcpybook"#<UserName>
    login_info['password'] = "arcpyguy123"#<Password>
    login_info['org_url'] = "http://www.arcgis.com"

    print login_info

    item_Id = "0e8ea33c42f040aaa51ef845c0a9cd23"#<Item ID>
    layer_name='mta_Bicycle_Route_Network'#Name of layer in the service
    feature_class=r'C:\PythonBook\Scripts\SanFrancisco.gdb\SanFrancisco\mta_Bicycle_Route_Network'#Path to Feature Class
    atTable=None

    #activate the feature service tool
    fea_service_tool = featureservicetools.featureservicetools(login_info)
    if fea_service_tool.valid == False:
        print fea_service_tool.message
    else:
        feature_service = fea_service_tool.GetFeatureService(itemId=item_Id,returnURLOnly=False)
        if feature_service is not None:
            feature_layer = fea_service_tool.GetLayerFromFeatureService(fs=feature_service,layerName=layer_name,returnURLOnly=False)
            if feature_layer is not None:
                #add the features from the feature class to the feature service
                results = feature_layer.addFeatures(fc=feature_class,attachmentTable=atTable)
                print json.dumps(results)
            else:
                print "Layer %s was not found, please check your credentials and layer name" % layer_name
        else:
            print "Feature Service with id %s was not found" % fsId
