from websocket import create_connection, WebSocketConnectionClosedException
import json
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import numpy as np
method = 'coinbase'


def update(frame, ws):
    try:
        data = json.loads(ws.recv())
        if data['type'] == 'ticker':
            price = float(data['price'])
            time = datetime.strptime((data['time'][:19]), '%Y-%m-%dT%H:%M:%S')
            lower_threshold = float(data['open_24h']) * 0.90
            upper_threshold = float(data['open_24h']) * 1.10
            x_data.append(time)
            y_data.append(price)
            line.set_data(x_data, y_data)
            plt.text(10000,max(y_data)+0.25,'Price:'+str(price))
            figure.gca().relim()
            figure.gca().autoscale_view()
    except Exception as e:
        print(e)
        pass
    return line,

if method =='yfinance':
    ws = create_connection("wss://streamer.finance.yahoo.com/")
    ws.send(
        json.dumps(
            {
                "subscribe": ['BTC-USD']
            }
        )
    )
else:
    ws = create_connection("wss://ws-feed.exchange.coinbase.com")
    ws.send(
        json.dumps(
            {
                "type": "subscribe",
                "product_ids": ["BTC-USD"],
                "channels": ["heartbeat", {"name": "ticker", "product_ids": ["BTC-USD"]}]
            }
        )
    )

x_data, y_data = [], []

figure = plt.figure()
line, = plt.plot_date(x_data, y_data, '-')

animation = FuncAnimation(figure, update,frames=[1], fargs=(ws,), interval=1)
plt.show()
k=2
