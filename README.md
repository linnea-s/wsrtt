# wsrtt

Simple websocket ping utility. It sends a timestamp to a websocket echo server,
receives it back and calculates round-trip time. Example:

```
pipenv run python3 wsrtt.py -c 3 wss://echo.websocket.org/
```
