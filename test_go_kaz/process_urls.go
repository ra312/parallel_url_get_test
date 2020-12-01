//TODO: bounded parallelism
//TODO: Ctrl-C and result printing§
package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/signal"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"syscall"
	"time"
)

var userAgent = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'"

// one global client init
var client = &http.Client{Timeout: 10 * time.Second}

// counting routines finished
var m map[int]int

func check(e error, ch chan<- string) {
	if e != nil {
		// fmt.Println("Found panic")
		// Panic is a built-in function that stops the ordinary flow of control and begins panicking.
		panic(e)
	}
}

func readLines(path string) []string {
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	err = scanner.Err()
	if err != nil {
		panic(err)
	}
	return lines
}

func makeHTTPrequest(url string, ch chan<- string, id int) {
	rowElems := make([]string, 0)
	rowElems = append(rowElems, url)
	// setting new http request req
	req, err := http.NewRequest("GET", url, nil)
	req.Header.Set("User-Agent", userAgent)
	start := time.Now()
	// letting client do the formed request
	resp, err := client.Do(req)
	check(err, ch)

	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)

	strLenBody := string(strconv.Itoa(len(body)))
	rowElems = append(rowElems, strLenBody)

	code := resp.StatusCode
	strCode := strconv.Itoa(code)
	rowElems = append(rowElems, strCode)

	elapsed := time.Since(start).Seconds() * 1000
	s := fmt.Sprintf("%f", elapsed)
	rowElems = append(rowElems, s+"ms")
	message := strings.Join(rowElems[:], ";")
	ch <- fmt.Sprintf(message)
}

func printResults(urls []string, ch chan string, m map[int]int) {
	for range urls {
		fmt.Println(<-ch)
	}
	for id, timesCalled := range m {
		fmt.Println(id, ":", timesCalled)
	}
}
func httpReqPanicTakenCareOf(wg *sync.WaitGroup, url string, ch chan string, id int) {
	defer func() {
		wg.Done()
		if err := recover(); err != nil {
			s := fmt.Sprintf("%f", err)
			fmt.Println(id)
			ch <- s
		}
	}()
	makeHTTPrequest(url, ch, id)
	m[id]++
}
func main() {
	m = make(map[int]int)
	var wg sync.WaitGroup
	cpuNum := runtime.NumCPU()
	runtime.GOMAXPROCS(cpuNum)
	// maxGoroutines := cpuNum * 2
	// guard := make(chan struct{}, maxGoroutines)
	urls := readLines("list_of_urls")
	keyPressed := make(chan os.Signal, 1)
	signal.Notify(keyPressed, os.Interrupt)
	signal.Notify(keyPressed, syscall.SIGTERM)
	ch := make(chan string)

	for id, url := range urls {
		wg.Add(1)
		go httpReqPanicTakenCareOf(&wg, url, ch, id)
		go func() {
			<-keyPressed
			log.Println("Receved Ctrl + C")
			// possible a defer logic or goto printResults ?
			os.Exit(1)
		}()
	}

	for range urls {
		fmt.Println(<-ch)
	}
	for id, timesCalled := range m {
		fmt.Println(id, ":", timesCalled)
	}
	wg.Wait()
}
