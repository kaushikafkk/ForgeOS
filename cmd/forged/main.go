package main

import (
	"flag"
	"log"
	"net"
	"os"
	"strconv"

	"github.com/kaushikafkk/ForgeOS/internal/server"
)

func main() {
	socket := flag.String("socket", "/run/forgeos/forged.sock", "Unix socket path")
	flag.Parse()

	if os.Getenv("LISTEN_FDS") == "1" && os.Getenv("LISTEN_PID") == strconv.Itoa(os.Getpid()) {
		file := os.NewFile(3, "forged.socket")
		if file == nil {
			log.Fatal("systemd announced a socket without descriptor 3")
		}
		listener, err := net.FileListener(file)
		if err != nil {
			log.Fatalf("use systemd socket: %v", err)
		}
		_ = file.Close()
		log.Printf("starting forged milestone-zero service with systemd socket activation")
		if err := server.New().ServeListener(listener); err != nil {
			log.Fatal(err)
		}
		return
	}

	log.Printf("starting forged milestone-zero service on %s", *socket)
	if err := server.New().Serve(*socket); err != nil {
		log.Fatal(err)
	}
}
