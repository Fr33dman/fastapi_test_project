import uvicorn
from fastapi import FastAPI
import json
from settings import Settings
from database import RedisConnector
from models import DeviceModel, DevicesModel, Anagrams, DeviceTypeListModel
from utils import *


settings = Settings()
app = FastAPI()


@app.get('/')
def index():
    return 'ok'


@app.post('/anagram/')
async def anagram(anagrams: Anagrams):
    s1, s2 = anagrams.s1, anagrams.s2
    answer = await is_anagram(s1, s2)
    response = {'message': answer}
    if answer:
        connector = RedisConnector().connector
        val = int(await connector.get('anagrams'))
        if val or val == 0:
            val += 1
            await connector.set('anagrams', val)
            val = int(await connector.get('anagrams'))
        else:
            await connector.set('anagrams', 0)
            val = await connector.get('anagrams')
        response['anagrams'] = val
        connector.close()
        await connector.wait_closed()
    return response


@app.post('/device/', status_code=201)
async def create_device(device: DeviceModel):
    connector = RedisConnector().connector
    device_exists = await connector.hexists('devices', device.dev_id)
    if device_exists:
        response = {'error': 'already exists'}
    elif not is_valid_mac_address(device.dev_id):
        response = {'error': 'MAC Address not valid'}
    else:
        if device.endpoint:
            endpoint_exists = await connector.hexists('endpoints', device.endpoint)
            if endpoint_exists:
                response = {'error': 'This endpoint is occupied'}
                return response
            await connector.hmset('endpoints', device.endpoint, device.dev_id)
        await connector.hmset('devices', device.dev_id, device.json())
        response = {'message': 'ok'}
    connector.close()
    await connector.wait_closed()
    return response


@app.get('/device/')
async def get_device(connected: bool = False):
    connector = RedisConnector().connector
    devices = await connector.hgetall('devices')
    response = {}
    for device in devices.values():
        device = DeviceModel(**json.loads(device))
        if connected and device.endpoint:
            if response.get(device.dev_type):
                response[device.dev_type].append(device)
                response[device.dev_type][0] += 1
            else:
                response[device.dev_type] = [1, device]
        elif not connected and device.endpoint == None:
            if response.get(device.dev_type):
                response[device.dev_type].append(device)
                response[device.dev_type][0] += 1
            else:
                response[device.dev_type] = [1, device]
    connector.close()
    await connector.wait_closed()
    type_devices = []
    for key, value in response.items():
        type_devices.append(DeviceTypeListModel(type=key, count=value[0], devices=value[1:]))
    response = DevicesModel(devices=type_devices)
    return response


@app.get('/device/{pk}')
async def get_device(pk: str):
    connector = RedisConnector().connector
    device_exists = await connector.hexists('devices', pk)
    if not device_exists:
        response = {'error': 'device not exists'}
    else:
        device = await connector.hget('devices', pk)
        device = DeviceModel(**json.loads(device))
        response = device
    connector.close()
    await connector.wait_closed()
    return response


@app.get('/endpoints/{pk}')
async def get_endpoints(pk: str):
    connector = RedisConnector().connector
    endpoint_exists = await connector.hexists('endpoints', pk)
    if not endpoint_exists:
        response = {'error': 'endpoint not exists'}
    else:
        device_id = await connector.hget('endpoints', pk)
        device = await connector.hget('devices', device_id)
        response = DeviceModel(**json.loads(device))
    connector.close()
    await connector.wait_closed()
    return response


if __name__ == "__main__":
    uvicorn.run(app, host=settings.server_host, port=settings.server_port)
