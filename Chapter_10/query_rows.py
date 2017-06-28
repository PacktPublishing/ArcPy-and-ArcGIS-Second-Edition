
import arcrest
from arcresthelper import featureservicetools
from arcresthelper import common

def main():
    login_info = {}
    login_info['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    login_info['username'] = raw_input("Enter User Name: ")#<UserName>
    login_info['password'] = raw_input("Enter password: ")#<Password>
    login_info['org_url'] = "http://arcgis.com/"

    item_Id = "d4718e6a27a04deab6f764cd70e102f4"#<Item ID>
    sql = "OBJECTID>0"
    layerName = "Bus_Stops" #layer1, layer2
    saveLocation = r"C:\PythonBook\Scripts\SanFrancisco.gdb\demo"
    fea_service_tool = featureservicetools.featureservicetools(login_info)
    feature_service = fea_service_tool.GetFeatureService(item_Id,False)
    print "Service is ", feature_service
    if feature_service != None:
        feature_service_url = fea_service_tool.GetLayerFromFeatureService(feature_service,layerName,True)
        print "url is ", feature_service_url
        if feature_service_url != None:
            demo = fea_service_tool.QueryAllFeatures(feature_service_url,
                         where="1=1",
                         out_fields="*",
                         timeFilter=None,
                         geometryFilter=None,
                         returnFeatureClass=True,
                         out_fc=saveLocation,
                         outSR=None,
                         chunksize=1000,
                         printIndent="")

if __name__ == "__main__":
    main()
