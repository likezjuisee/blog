package main

import (
    "fmt"
    "time"
    "github.com/valyala/fasthttp"
)

const (
    Concurrency = 10
    Method = "GET"
    Url = "http://10.16.16.12:8080/perftest/index.html"
    PressTime = time.Second*3600
)

var (
    client *fasthttp.Client
)

type Performance struct {
    
}

func init() {
    client = &fasthttp.Client{
        MaxConnsPerHost:               int(Concurrency),
        DisableHeaderNamesNormalizing: true,
    }
}

func (p *Performance) prepareRequest() (*fasthttp.Request, *fasthttp.Response) {
    req := fasthttp.AcquireRequest()
    resp := fasthttp.AcquireResponse()
    req.Header.SetMethod(Method)
    req.SetRequestURI(Url)
    // 短链接
    // req.SetConnectionClose()
    // resp.SetConnectionClose()

    return req, resp
}

func (p *Performance) fireRequest(req *fasthttp.Request, resp *fasthttp.Response, successNum, failNum *uint64) {
    err := client.Do(req, resp)
    if err != nil {
        fmt.Println(err.Error())
        *failNum++
    } else {
        code := resp.StatusCode()
        if code == 200 {
            *successNum++
        } else {
            fmt.Println("status code: ", code)
            *failNum++
        }
    }
}

func (p *Performance) releaseRequest(req *fasthttp.Request, resp *fasthttp.Response) {
    fasthttp.ReleaseRequest(req)
    fasthttp.ReleaseResponse(resp)
}

func worker(successNum, failNum *uint64) {
    p := &Performance{}
    for {
        req, resp := p.prepareRequest()
        p.fireRequest(req, resp, successNum, failNum)
        p.releaseRequest(req, resp)
    }
}

func stats(successNums, failNums []uint64) {
    var successSum uint64
    var failSum uint64
    for {
        successSum = 0
        failSum = 0
        for _, successNum := range successNums {
            successSum += successNum
        }
        for _, failNum := range failNums {
            failSum += failNum
        }
        fmt.Println("successSum: ", successSum)
        fmt.Println("failSum: ", failSum)
        time.Sleep(time.Second*3)

    }
}


func main() {
    successNums := make([]uint64, Concurrency)
    failNums := make([]uint64, Concurrency)
    for i:=0; i<Concurrency; i++ {
        go worker(&successNums[i], &failNums[i])
    }
    go stats(successNums, failNums)
    fmt.Println("begin test...")
    time.Sleep(PressTime)
}

