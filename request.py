import requests
url="https://eur-lex.europa.eu/eurlex-ws?wsdl"
#headers = {'content-type': 'application/soap+xml'}
headers = {'content-type': 'text/xml'}
body = """<?xml version="1.0" encoding="UTF-8"?>
        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
xmlns:sear="http://eur-lex.europa.eu/search">
<soap:Header>
 <wsse:Security soap:mustUnderstand="true" xmlns:wsse="http://docs.oasisopen.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"

xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility1.0.xsd">

 <wsse:UsernameToken wsu:Id="UsernameToken-1">
 <wsse:Username>n0024qg2</wsse:Username>
 <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-
wss-username-token-profile-1.0#PasswordText">HdezS3rrano41</wsse:Password>
 </wsse:UsernameToken>
 </wsse:Security>
 </soap:Header>
 <soap:Body>
 <sear:searchRequest>
 <sear:expertQuery>
 SELECT *
 WHERE DN=62006CJ*
 </sear:expertQuery>
 <sear:searchLanguage>en</sear:searchLanguage>
 </sear:searchRequest>
 </soap:Body>
</soap:Envelope> """

response = requests.get(url,data=body,headers=headers)
print (response.content)

#<sear:page>1</sear:page>
#<sear:pageSize>2</sear:pageSize>