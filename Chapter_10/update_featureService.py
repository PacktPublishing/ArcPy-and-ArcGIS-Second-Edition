from arcresthelper import securityhandlerhelper
from arcrest.agol import FeatureLayer
from arcrest.common.filters import LayerDefinitionFilter
import datetime

if __name__ == "__main__":
    # URL to Service
    url = 'http://services7.arcgis.com/LLWzNvydeNCpjeTo/arcgis/rest/services/BikeRoute/FeatureServer/0'
    sql = "streetname = 'SAN BRUNO'"# where clause

    fieldInfo =[
                {
                    'FieldName':'type',
                    'ValueToSet':'WAY'
                }
               ]

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI, ArcGIS
    securityinfo['username'] = raw_input("Enter User Name: ") #User Name
    securityinfo['password'] = raw_input("Enter Password: ") #password
    securityinfo['org_url'] = "http://www.arcgis.com"

    sec_handle = securityhandlerhelper.securityhandlerhelper(securityinfo=securityinfo)
    if sec_handle.valid == False:
        print sec_handle.message
    else:
        #create a feature layer of the AGOL service
        feature_layer = FeatureLayer(
            url=url,
            securityHandler=sec_handle.securityhandler,
            proxy_port=None,
            proxy_url=None,
            initialize=True)

        out_fields = ['objectid']
        #append the field info to each field
        for field in fieldInfo:
            out_fields.append(field['FieldName'])

        #query the feature layer
        query_feats = feature_layer.query(where=sql,
                            out_fields=",".join(out_fields))

        #loop over each feature and field to update
        for feat in query_feats:
            for field in fieldInfo:
                feat.set_value(field["FieldName"],field['ValueToSet'])

        #update features
        print feature_layer.updateFeature(features=query_feats)
