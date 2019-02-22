import urequests


class RippleDataAPI:

    def __init__(self):

        self.node = 'https://data.ripple.com'
        self.apiVersion = 'v2'


    def call(self, urlParams, queryParams):

        endpoint = [self.node, self.apiVersion]
        endpoint.extend(urlParams)
        endpoint = '/'.join(endpoint)

        parameters = '&'.join([qp + '=' + queryParams[qp] for qp in queryParams])

        return urequests.get(endpoint + '?' + parameters).json()


    def getExchangeVolume(self, queryParams={}):

        return self.call(['network', 'exchange_volume'], queryParams)


    def getPaymentVolume(self, queryParams={}):

        return self.call(['network', 'payment_volume'], queryParams)


    def getExternalMarkets(self, queryParams={}):

        return self.call(['network', 'external_markets'], queryParams)


    def getExchanges(self, params, queryParams={}):

        urlParams = ['exchanges']
        urlParams.extend(params)

        return self.call(urlParams, queryParams)


    def getExchangeRates(self, params, queryParams={}):
        
        urlParams = ['exchange_rates']
        urlParams.extend(params)

        return self.call(urlParams, queryParams)