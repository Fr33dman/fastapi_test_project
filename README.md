# Test project (FastAPI + aioredis)

### Endpoints
* ``/anagram/``
Takes s1 (string) and s2 (string), if them are anagrams, increases the counter score and gives response like:
```
{
  message: bool,
  count: int
}
```

* ``/device/{pk}``
POST, GET, you can create new device accorfing to schema, get list of connected/disconnected devices (param: connected (bool))
or get device with his MAC address id, gives response like:
```
{
  "devices": [
    {
      "type": "emeter",
      "count": 1,
      "devices": [
        {
          "dev_id": "13:4C:12:11:3F:B7",
          "dev_type": "emeter",
          "endpoint": null
        }
      ]
    },
    {
      "type": "gsm",
      "count": 1,
      "devices": [
        {
          "dev_id": "57:DB:A2:16:BB:F3",
          "dev_type": "gsm",
          "endpoint": null
        }
      ]
    }
  ]
}
```

* ``/endpoints/{pk}``
GET device where pk is device's endpoint
