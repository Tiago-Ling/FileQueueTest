# File Queue Service Test
Quick and dirty client / server application to read a file line by line and send its contents to the server, where a new file will be written with the contents of the one in the server.

The app was written using Python `3.11.1`.

## How to run it
I've used `pipenv` to run both apps, so I'm including it in the steps but it should be optional.

Start the server by running in a terminal or command prompt and writing:
```
pipenv shell
python server.py
```
Then run the client application, open a new terminal / command prompt and writing:
```
pipenv shell
python client.py
```
Once the client application is running, it'll ask for a filename to send to the server. I've included a simple `test.txt` to quickly test it, so write `test.txt` to start the reading -> sending -> writing process.

## Notes
* In order to quickly test it I've hardcoded the server host and port, these can be changed by modifying `SERVER_HOST` and `SERVER_PORT` inside `client.py` and `server.py` (currently set to `127.0.0.1` / `0.0.0.0` and `8081`)
* Due to time constraints no bonus challenges were implemented, but if I had more time I'd add these, in order:
  * Substitute the Threads for Processes
  * Add unit tests
  * Add proper error handling
  * Use only one thread for reading on the client and one for writing on the server
  * Implement proper support for multiple clients connections
  * Re-implement it in Golang for learning purposes



