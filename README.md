# spotify-xai

### Prerequisites
- Python v3.12
- Ensure Docker and docker-compose are installed.
- Ensure Node.js (including npm) v20.15.1 (LTS) is installed.

### Initialization
To start the server and client, run `docker compose up` in a terminal.
Make sure the path points to the project root containing the `docker-compose.yml`.
Any info about initialization from the `README.md` within the client folder can be ignored.

If a docker file has been modified, run `docker compose build` before initializing.
In some cases where changes are not cloned to the docker image, the flag `--no-cache` might be necessary.

To stop the server and client, press `ctrl` + `c` in the same terminal.