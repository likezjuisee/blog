#!/usr/local/bin/python3.5
#coding=utf-8

import aiohttp
import asyncio
import async_timeout
import threading
import time

CONCURRENCY=500

class Result():
    def __init__(self):
        self.successNum = 0
        self.failNum = 0

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            if response.status == 200:
                return True

async def main(loop, result):
    async with aiohttp.ClientSession(loop=loop) as session:
        while True:
            ret = await fetch(session, 'http://10.16.16.12:8080/perftest/index.html')
            if ret:
                result.successNum+=1
            else:
                result.failNum+=1

async def stat(results):
    while True:
        successSum = 0
        failSum = 0
        for result in results:
            successSum += result.successNum
            failSum += result.failNum
        print('successSum: %d' % successSum)
        print('failSum: %d' % failSum)
        await asyncio.sleep(3)

def statInThread(results):
    while True:
        successSum = 0
        failSum = 0
        for result in results:
            successSum += result.successNum
            failSum += result.failNum
        print('successSum: %d' % successSum)
        print('failSum: %d' % failSum)
        time.sleep(3)

def run():
    loop = asyncio.get_event_loop()
    results = []
    for i in range(CONCURRENCY):
        result = Result()
        results.append(result)
        workers = asyncio.gather(main(loop, result))
    asyncio.gather(stat(results))
    loop.run_until_complete(workers)

if __name__ == '__main__':
    run()