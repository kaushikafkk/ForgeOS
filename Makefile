.PHONY: test build validate prototype

test:
	go test ./...

build:
	mkdir -p bin
	go build -o bin/forged ./cmd/forged
	go build -o bin/forge ./cmd/forge

validate:
	./scripts/validate-config.sh

prototype:
	python3 -m http.server 4173 --directory config/includes.chroot/usr/share/forgeos/prototype

