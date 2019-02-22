import time
import json
import display
import RippleDataAPI

tft = None

def initDisplay():

    global tft

    if tft is None:

        # Instantiate TFT
        tft = display.TFT()

        # Initialize TFT (set pins)
        tft.init(tft.ILI9341, spihost=tft.VSPI, speed= 40000000, width=240,
                height=320, miso=19, mosi=23, clk=18, dc=27, cs=14, rst_pin=33,
                backl_pin=32, backl_on=1, hastouch=tft.TOUCH_XPT, tcs=12, splash=False, bgr=True)

        # Load XRP logo
        tft.image(tft.CENTER, 0, 'xrp.jpg')

        # Set font
        tft.font('consola18', color=tft.WHITE)


# Initialize display
initDisplay()


class Plot:

    def __init__(self, size, x0, y0, x1, y1, color):

        self.data = [None for i in range(size)]
        self.maxVal = 0
        self.minVal = 1e10
        self.scale = 1
        self.barWidth = 4
        self.color = color
        self.coordinates = [[x0, y0], [x1, y1]]
        self.limitHeight = self.coordinates[1][1] - self.coordinates[0][1]

        # Set actual window to plot
        tft.setwin(self.coordinates[0][0],
                   self.coordinates[0][1],
                   self.coordinates[1][0],
                   self.coordinates[1][1])

        # Clear with grey
        tft.clearwin(tft.DARKGREY)

        # Show WAIT word centered on the screen
        tft.text(tft.CENTER, tft.CENTER, 'WAIT', color=tft.GREEN, transparent=True)

        # Reset window
        tft.resetwin()


    def update(self, newData):

        # Update data values
        self.data.pop(0)
        self.data.append(newData)

        # Update max and min values
        if newData > self.maxVal:
            self.maxVal = newData

        if newData < self.minVal:
            self.minVal = newData

        # Recalculate scale factor 
        if self.maxVal != self.minVal:
            self.scale = 0.8 * self.limitHeight / (self.maxVal - self.minVal)

        # Set actual window to plot
        tft.setwin(self.coordinates[0][0],
                   self.coordinates[0][1],
                   self.coordinates[1][0],
                   self.coordinates[1][1])

        # Clear with grey
        tft.clearwin(tft.DARKGREY)

        xStart = 0
        yStart = self.limitHeight

        # Shift data to fit min value with zero
        shiftedData = [None if i is None else (i - self.minVal) for i in self.data]

        # Draw bars: shortest bar will fit 20% of the height and tallest one the 100%
        for i in shiftedData:
            if i is not None:
                barHeight = int(round(0.2 * self.limitHeight + self.scale * i))
                #tft.line(xStart, yStart - barHeight, xStart + self.barWidth, yStart - barHeight, self.color)
                tft.rect(xStart, yStart - barHeight, self.barWidth, barHeight, tft.BLACK, self.color)

            xStart += self.barWidth

        # Reset window
        tft.resetwin()



def run():

    tft.clear()

    # Initialize UI
    tft.image(tft.CENTER, 10, 'xrp_basic.jpg', scale=2)
    tft.text(tft.CENTER, 60, 'LIVE XRPL 24h STATS', color=tft.WHITE)

    tft.text(tft.CENTER, 80, 'XRP/USD: WAIT')
    tft.text(tft.CENTER, 100, 'Exchange volume: WAIT')
    tft.text(tft.CENTER, 120, 'Payment volume: WAIT')
    tft.text(tft.CENTER, 140, 'External volume: WAIT')

    tft.rect(0, 160, 240, 160, tft.BLUE, tft.BLUE)

    # Initialize plots
    exchangeVolumePlot = Plot(58, 4, 164, 236, 212, tft.YELLOW)
    paymentVolumePlot = Plot(58, 4, 216, 236, 264, tft.RED)
    externalMarketsVolumePlot = Plot(58, 4, 268, 236, 316, tft.PURPLE)

    avgUSDXRPrate = 0

    while True:

        # Instantiate API
        api = RippleDataAPI.RippleDataAPI()

        # Get last 50 trades on Bitstamp
        exchanges = api.getExchanges(['XRP', 'USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B'], {'limit': '50', 'descending': 'true'})

        if exchanges['result'] == 'success':

            # Calculate XRP/USD price averaged by volume during the last 50 trades on Bitstamp
            avgUSDXRPrate = 0
            total_counter_amount = 0

            for i in exchanges['exchanges']:

                counter_amount = float(i['counter_amount'])
                avgUSDXRPrate += float(i['rate']) * counter_amount
                total_counter_amount += counter_amount

            avgUSDXRPrate /= total_counter_amount

        # Print XRP/USD price
        tft.text(tft.CENTER, 80, 'XRP/USD: {:.4f}'.format(avgUSDXRPrate), color=tft.GREEN)

        # Get and print exchange  volume
        exchangeVolumes = api.getExchangeVolume()
        if exchangeVolumes['result'] == 'success':
            exchangeVolume = float(exchangeVolumes['rows'][0]['total'])
            tft.text(tft.CENTER, 100, 'Exchange volume: {:.2f}M$'.format(exchangeVolume * avgUSDXRPrate / 1e6), color=tft.YELLOW)

        # Get and print payment  volume
        paymentVolumes = api.getPaymentVolume()
        if paymentVolumes['result'] == 'success':
            paymentVolume = float(paymentVolumes['rows'][0]['total'])
            tft.text(tft.CENTER, 120, 'Payment volume: {:.2f}M$'.format(paymentVolume * avgUSDXRPrate / 1e6), color=tft.RED)

        # Get and print external  volume
        externalMarketsVolumes = api.getExternalMarkets()
        if externalMarketsVolumes['result'] == 'success':
            externalMarketsVolume = float(externalMarketsVolumes['data']['total'])
            tft.text(tft.CENTER, 140, 'External volume: {:.2f}M$'.format(externalMarketsVolume * avgUSDXRPrate / 1e6), color=tft.PURPLE)

        # Update plots
        exchangeVolumePlot.update(exchangeVolume)
        paymentVolumePlot.update(paymentVolume)
        externalMarketsVolumePlot.update(externalMarketsVolume)


