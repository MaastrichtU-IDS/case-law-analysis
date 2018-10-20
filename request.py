import requests
url="https://eur-lex.europa.eu/eurlex-ws?wsdl"
headers = {'content-type': 'application/soap+xml'}
#headers = {'content-type': 'text/xml'}
body = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sear="http://eur-lex.europa.eu/search">
  <soap:Header>
    <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" soap:mustUnderstand="true">
      <wsse:UsernameToken xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="UsernameToken-1">
        <wsse:Username>n0024qg2</wsse:Username>
        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">BP4H8wDldM3</wsse:Password>
      </wsse:UsernameToken>
    </wsse:Security>
  </soap:Header>
  <soap:Body>
    <sear:searchRequest>
      <sear:expertQuery>SELECT CELLAR_ID WHERE DN=62006CJ*</sear:expertQuery>
      <sear:page>1</sear:page>
      <sear:pageSize>10</sear:pageSize>
      <sear:searchLanguage>en</sear:searchLanguage>
    </sear:searchRequest>
  </soap:Body>
</soap:Envelope>"""

#encoded_request = body.encode('utf-8')
#headers = {"Content-Type": "text/xml; charset=UTF-8","Content-Length": len(body)}
response = requests.get(url,data=body,headers=headers)
print (response.content)


# form = """
#         <soapenv:Envelope
#             xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
#             xmlns:pos="http://testthis.com/xmlschema/pos">
#             <soapenv:Header>
#                 <wsse:Security soapenv:mustUnderstand="1"
#                     xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
#                     xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
#                     <wsse:UsernameToken>
#                         <wsse:Username>%s</wsse:Username>
#                         <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">%s</wsse:Password>
#                     </wsse:UsernameToken>
#                 </wsse:Security>
#             </soapenv:Header>
#             <soapenv:Body>
#                 <pos:CompleteReturnRequest>"
#                     <!--Optional:-->
#                     <pos:merchantCode>%s</pos:merchantCode>
#                     <pos:storeCode>%s</pos:storeCode>
#                     <pos:returnId>%d</pos:returnTrxId>
#                 </pos:CompleteReturnRequest>
#             </soapenv:Body>
#         </soapenv:Envelope>"""  %(Username, Password, merchantCode, storeCode, returnId)

	
# 	response = requests.post(url="https://testthis.pos.com:443/pos/soap/pos",headers = headers,data = encoded_request,verify=False)
	
# 	return response



#<sear:page>1</sear:page>
#<sear:pageSize>2</sear:pageSize>
# <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
# xmlns:sear="http://eur-lex.europa.eu/search">
# <soap:Header>
#  <wsse:Security soap:mustUnderstand="true" xmlns:wsse="http://docs.oasisopen.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"

# xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility1.0.xsd">

#  <wsse:UsernameToken wsu:Id="UsernameToken-1">
#  <wsse:Username>n0024qg2</wsse:Username>
#  <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-
# wss-username-token-profile-1.0#PasswordText">HdezS3rrano41</wsse:Password>
#  </wsse:UsernameToken>
#  </wsse:Security>
#  </soap:Header>
#  <soap:Body>
#  <sear:searchRequest>
#  <sear:expertQuery>
#  SELECT CELLAR_ID
#  WHERE DN=62006CJ*
#  </sear:expertQuery>
#  <sear:searchLanguage>en</sear:searchLanguage>
#  </sear:searchRequest>
#  </soap:Body>
# </soap:Envelope> """