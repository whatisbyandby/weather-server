from quart import Quart, websocket, request
from influxdb import InfluxDBClient
from datetime import datetime

app = Quart(__name__)

new_points = []


def send_points():
    client = InfluxDBClient(host='192.168.1.44', port=8086, database='weather')
    print(client)
    print(client.write_points(new_points))
    new_points.clear()
    print('Saved Points')


@app.route('/weather', methods=['POST'])
async def hello():
    data = await request.json
    new_point = {
        "measurement": "weather",
        "tags": {
            "user": "weather-station"
        },
        "time": datetime.utcnow().isoformat(),
        "fields": data
    }
    new_points.append(new_point)
    if len(new_points) > 5:
        send_points()
    return 'True'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)