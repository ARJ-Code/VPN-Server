.PHONY: run
run:
	python3 src/main.py

.PHONY: client
client:
	python3 src/client.py "$(protocol)"

.PHONY: server
server:
	python3 src/server.py "$(protocol)"