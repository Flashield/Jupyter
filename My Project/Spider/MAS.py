import suds
from suds.client import Client
mas_appid = 'P288517643798085'

def mas_send_sms(msisdn,text_msg,msg_type='Normal'):
    url = "http://221.178.146.234:8379/MAS3/services/cmcc_mas_wbs?wsdl"
    client = Client(url)
    result = client.service.sendSms(ApplicationID=mas_appid,DestinationAddresses='tel:{}'.format(msisdn),ExtendCode='10657368121580001',\
                                    Message=text_msg,MessageFormat='ASCII',SendMethod=msg_type,DeliveryResultRequest=True)
    return result