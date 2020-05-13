#!/usr/bin/env python3
import asyncio
import websockets
import time
import sys
import argparse

async def echoping(args):
    pings = []
    async with websockets.connect(args.uri) as websocket:
        for seq in range(args.count):
            ns = time.perf_counter_ns()

            await websocket.send(str(ns))
            
            while True:
                try:
                    ans = await websocket.recv()
                    # strip any prefix added by server
                    ans = int(ans.split()[-1])
                    if ans == ns:
                        rtt = (time.perf_counter_ns() - ns) / 1000000
                        pings.append(rtt)
                        print(f'seq={seq} time={rtt:.2f} ms')
                        break
                except ValueError:
                    pass
            if seq+1 != args.count:
                await asyncio.sleep(args.interval / 1000.0)
    rtt_avg = sum(pings) / len(pings)
    print(f'round-trip min/avg/max = {min(pings):.2f}/{rtt_avg:.2f}/{max(pings):.2f} ms')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measure RTT using Websockets echo server')
    parser.add_argument('uri', metavar='URI', help='ws:// or wss:// URL')
    parser.add_argument('-c', '--count', metavar='count', type=int,
        help='number of pings to send', default=10)
    parser.add_argument('-i', '--interval', metavar='interval', type=int,
        help='interval in ms between pings', default=1000)
    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(echoping(args))
