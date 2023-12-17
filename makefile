.PHONY: run
run:
	python3 main.py

.PHONY: client
client:
	python3 client.py "$(protocol)"

.PHONY: server
server:
	python3 server.py "$(protocol)"