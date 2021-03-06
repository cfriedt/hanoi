# Towers of Hanoi Game Engine

* [About](#about)
  + [Build Status](#build-status)
  + [Basic Requirements](#basic-requirements)
  + [Implementation Details](#implementation-details)
* [Step-by-Step Instructions for Running](#step-by-step-instructions-for-running)
* [Try it Out](#try-it-out)
  + [Create a Session](#create-a-session)
  + [Move a Disc](#move-a-disc)
  + [Try an Illegal Move](#try-an-illegal-move)
  + [Finish the Game!](#finish-the-game-)
* [Running Tests with Pytest](#running-tests-with-pytest)
* [Additional Areas of Expansion](#additional-areas-of-expansion)
  + [Next N Moves & Tips](#next-n-moves---tips)
  + [Authentication & Encryption](#authentication---encryption)
  + [Persistant Storage](#persistant-storage)
  + [Scaling](#scaling)
  + [Create a Frontend](#create-a-frontend)
  + [Remote Procedure Calls](#remote-procedure-calls)
* [Conclusion](#conclusion)

## About

This is a sample backend REST API implementation for a game engine that allows users to play the
[Towers of Hanoi](https://en.wikipedia.org/wiki/Tower_of_Hanoi).

It is not an algorithmic solution for the classic puzzle, which would optimally be completed in `2^N - 1` moves, but simply a means by which users
can play given a suitable frontend (e.g. a web browser).

### Build Status

![CI](https://github.com/cfriedt/hanoi/workflows/CI/badge.svg)

### Basic Requirements

The requirements were fairly minimal:
* allow a client implementation (not in scope) to modify the state of the game
* enforce the rules of the game
* apply effects of any valid move to the game state
* provide the client with the complete state of the game
* determine if the game is complete
* 4 discs must be supported

The basic requirements did not specify that more than a single game should be supported, but I added multi-game support via a `sessionId` parameter.
Additionally, there was no specification for how many simultaneous users should be supported nor for the backing storage of the system and so all games
states are stored in memory and there is only one instance of the service. Beyond that, the API itself supports up to 64 discs.

### Implementation Details

The REST API is specified via a YAML file conforming to the [OpenAPI Specification v3.0.3](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md).

To view the API in a more human readable format, copy and past the contents of [hanoi.yaml](https://github.com/cfriedt/hanoi/blob/main/src/hanoi/hanoi.yaml) into the [Swagger Editor](https://editor.swagger.io) or refer to the [Swagger UI](https://swagger.io/tools/swagger-ui/) of your running instance at 
[http://localhost:8080/v1/ui](http://localhost:8080/v1/ui).

## Step-by-Step Instructions for Running

We assume that you are using a relatively recent version of Ubuntu Linux, Focal Fossa. If that is the case, skip to step 4 below, otherwise
start at step 1.

1. [Install Docker Desktop](https://www.docker.com/get-started)
2. Start up an Ubuntu Focal Fossa Docker container
  ```bash
  docker run -it -p 8080:8080 ubuntu:focal
  ```
3. Install [Git](https://git-scm.com/) and [Pip](https://pypi.org/project/pip/)
  ```bash
  apt-get update && apt install -y git python3-pip
  ```
4. Clone the git repository
  ```bash
  git clone https://github.com/cfriedt/hanoi.git
  cd hanoi
  ```
5. Install any necessary Python runtime requirements
  ```bash
  pip3 install -r requirements.txt
  ```
6. Run the server
  ```bash
  ./run.py
  ```
7. Open a web browser to [http://localhost:8080/v1/ui](http://localhost:8080/v1/ui) to access the [Swagger UI](https://swagger.io/tools/swagger-ui/)
   in order to test out the backend.

## Try it Out

Let's perform some manual testing of our backend to verify that the game engine works.

### Create a Session

For example, to create a new session click on the `POST /sessions Create a session` button to expand the menu for creating a session.

![Create a Session](https://github.com/cfriedt/hanoi/raw/main/doc/post-create-a-session.png "Create a Session")

Then, click `Try it out`.

![Try it Out](https://github.com/cfriedt/hanoi/raw/main/doc/try-it-out.png "Try it out")

Add the desired parameters - e.g. 4 discs, starting on tower 0 and finishing on tower 2. Then, click execute. The backend will respond with error
messages for any invalid input.

![Execute](https://github.com/cfriedt/hanoi/raw/main/doc/execute.png "Execute")

The response should resemble the one below, which includes the newly generated `sessionId` (0 in this case).

![Create Session Response](https://github.com/cfriedt/hanoi/raw/main/doc/response.png "Create Session Response")

Collapse the `POST /sessions Create a session` menu by clicking on it a second time.

### Move a Disc

Next, to move a disc from tower 0 to tower 1, expand the `PUT /sessions/{sessionId}/move Move a disc` menu by clicking on it, select `Try it out` again.
Enter the `sessionId` that was just created, 0, the `fromTower`, 0, and the `toTower`, 1, and then execute.

![Move a Disc](https://github.com/cfriedt/hanoi/raw/main/doc/move.png "Move a Disc")

The response should have code 200 to indicate success.

![Move Response](https://github.com/cfriedt/hanoi/raw/main/doc/move-response.png "Move Reponse")

### Try an Illegal Move

We just moved the smallest disc (diameter 1) from tower 0 to tower 1. What happens if we try to move the next smallest disc (diameter 2) from
tower 0 to tower 1? We know that it would violate the rules of the game, but can we verify that the game engine knows that? Yes!

If the same instructions are followed to attempt to move a disc from tower 0 to tower 1, this time, a descriptive error message is returned with the
error code 201 indicating that the HTTP PUT operation failed.

![Move Error](https://github.com/cfriedt/hanoi/raw/main/doc/move-error.png "Move Error")

### Finish the Game!

Rather than pointing and clicking our way to victory, let's use `curl` to speed things up.

```bash
MOVES=(0 2 1 2 0 1 2 0 2 1 0 1 0 2 1 2 1 0 2 0 1 2 0 1 0 2 1 2)
for (( i=0; i < ${#MOVES[@]}; i += 2 )); do
	FROM=${MOVES[$i]}
	TO=${MOVES[$((i+1))]}
	curl -X PUT "http://localhost:8080/v1/sessions/0/move?fromTower=${FROM}&toTower=${TO}" \
		-H  "accept: application/json"
done
```

Finally, using the UI, expand the `GET /sessions/{sessionId}/complete` menu by clicking it, and selecting `Try it out`. Enter our `sessionId`, 0, and select "Execute".

![Check Completion](https://github.com/cfriedt/hanoi/raw/main/doc/complete.png "Check Completion")

The response should resemble the following.

![Complete](https://github.com/cfriedt/hanoi/raw/main/doc/victory.png "Complete")

Yay! We're done! 🥳

## Running Tests with Pytest

First, check that the unit tests are passing and verify code coverage is reasonably complete. 

```bash
PYTHONPATH=$PWD/src \
	pytest --cov=hanoi --cov-report term-missing \
	tests/HanoiState_test.py tests/Hanoi_test.py
```

The output of `pytest` is below:
```bash
============================ test session starts =============================
platform linux -- Python 3.8.5, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/cfriedt/workspace/hanoi
plugins: subtests-0.2.1, schemathesis-1.1.0, cov-2.10.1, hypothesis-5.41.4, xdist-1.31.0, forked-1.1.3
collected 23 items                                                           

tests/HanoiState_test.py ........                                      [ 34%]
tests/Hanoi_test.py ...............                                    [100%]

----------- coverage: platform linux, python 3.8.5-final-0 -----------
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src/hanoi/Hanoi.py           63      0   100%
src/hanoi/HanoiState.py      35      0   100%
src/hanoi/__init__.py         3      0   100%
-------------------------------------------------------
TOTAL                       101      0   100%
```

Next, let's run an integration test with `pytest`.

```bash
PYTHONPATH=$PWD/src \
	pytest tests/app_test.py
```

The output of `pytest` is below.

```bash
============================= test session starts =============================
platform linux -- Python 3.8.5, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/cfriedt/workspace/hanoi
plugins: subtests-0.2.1, schemathesis-1.1.0, cov-2.10.1, hypothesis-5.41.4, xdist-1.31.0, forked-1.1.3
collected 13 items                                                            

tests/app_test.py ...s.........                                         [100%]

======================== 12 passed, 1 skipped in 0.97s ========================
```

One test is actually skipped, because it was rather difficult to inject a fault for the `/sessions` endpoint, which does
not accept any parameters.

Unfortunately, we are not able to get coverage on `app.py` due to a strange bug that exists in
`pytest-cov` that prevents python's `requests` library from reaching the server on the default port.
However, since all of the tests are successful, and it is apparent that app.py is a very thin wrapper,
we can conclude that coverage is at or near 100% for `hanoi.app`.

## Additional Areas of Expansion

### Next N Moves & Tips

Sometimes people get stuck. It would be helpful if the game engine could suggest a possible next move (or next N moves) to help the user along.

For a small number of discs, that would be relatively straightforward to do using [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming).

Each time the user requests a next move, the server could look into an array (or consult a database) for the optimal next step to make. If the entry
was not available, then the server could recursively (or non-recursively) come up with an optimal solution given the current state. It's very much
a key-value lookup, where the key is the current state of the game - that is, the number of discs, the source tower, the target tower, and the state
of the towers currently.

As mentioned, for a small number of discs, that would be feasible. However, even the optimal solution of the Towers of Hanoi has a time-complexity
of O(2^N). For 32 Discs, the optimal solution would be reached after 4-billion moves! That could take a significant amount of time, even on today's
advanced processors. The space complexity of the DP solution is (possibly) O(N!), which is a number of astronomical scale.

### Authentication & Encryption

Secure communications are important.

It would be smart to prevent an unauthorized user from modifying the state of any game. Currently there is no
authentication, since that was not a requirement. However, I would probably look to using [OAuth 2.0](https://en.wikipedia.org/wiki/OAuth) for user
authentication and associating a particular `sessionId` with a specific user, if it were a requirement.

Additionally, it would make sense to use industry standard [TLS encryption](https://en.wikipedia.org/wiki/Transport_Layer_Security) for a possible 
deployment of this game engine, so that officemates or the ISP cannot steal the very impressive moves that we come up with in the process of playing
the game.

### Persistant Storage

Currently, the API uses in-memory storage for all game states. If the server is stopped and restarted, all previous game states are lost.

It would make sense to store game states in a database of some kind. For development, it might make sense to use a small
[SQLite](https://www.sqlite.org/index.html) server. However, for a larger number of game states, possibly more than one game per user, it might
make sense to adopt a more scalable database engine.

### Scaling

We previously mentioned scaling when we discussed getting the game engine to solve the problem for us. However, even without that feature, supporting
a large (say 10^6) number of users would be challenging.

While it's fine to use in-memory storage for 1, 2, or even 100 users, (when the number of discs is relatively low), supporting 10M users would likely
require multiple instances of the game engine in place all over the world, with one or more load-balancers for each region. Furthermore, we would likely
require a distributed database of some kind to store game information.

To achieve a very large scale service, it would probably make sense to orchestrate the game engines, databases, load balancers, reverse proxies, and so
on using [Kubernetes](https://kubernetes.io/).

Also, when it comes to scale, there are a lot of ways to optimize things. For example, reimplementing the game engine in C++.

### Create a Frontend

There are many Javascript frontends out there. I am no Picasso when it comes to frontends. If you want some rectangles on an HTML5 `<canvas>` element
though, I can hook you up, and even write the client-side JavaScript to communicate with the backend too! 😉

A number of websites previously, and probably still use [jQuery](https://jquery.com/). However, now that the
[JavaScript Fetch API](https://developers.google.com/web/updates/2015/03/introduction-to-fetch) is supported on most if not all major browsers,
I tend to prefer to write my client-side JS with that. I've even stored my client-side JS a gziped resource on a microcontroller with an embedded HTTP
server on it (which I also wrote).

### Remote Procedure Calls

While REST is great for prototyping web services, when we get to a certain scale, it makes more sense to use binary communication instead of string-based
communication between various web services (and even the client!).

With an HTTP2 proxy like [Envoy](https://www.envoyproxy.io/), binary [gRPC](https://grpc.io/) messages could be exchanged between nodes at any scale.
Actually, I would be lying if I said I didn't implement this service first with gRPC. 😬

While gRPC is nice, my personal preference for RPC frameworks is [Apache Thrift](https://thrift.apache.org). It's nice in that it is one tool in a single
repository and that it uses the same client / server classes while abstracting away the actual transports. The only thing that Thrift is missing compared
to gRPC is [bidirectional communication](https://grpc.io/docs/what-is-grpc/core-concepts/).

## Conclusion

Thanks for reading to the end.

I hope you enjoyed learning about REST, the Towers of Hanoi, the OpenAPI standard, Connexion, and the other topics mentioned.
