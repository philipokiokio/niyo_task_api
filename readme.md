# Niyo Task API

## setup 
post cloning the repo, and setting up resources using the ```.env.dist``` as a proof for creating ```.env```.


Then the next step is to create a virtualenv I used venv for this product.

I have a make file that helped set the code environment.
Here is the setup terminal code for setting the codebase locally before starting the server.

```make venv ```: this creates a virtual environment.

```source venv/bin/activate```: this activates the virtualenv.

``` make install```: this installs all the requirements for the codebase.

```make local-migrate```: This runs migration scripts.

```make run-server```: This starts the server on port 8080.

### The below does not need to be run. 
```make local-migrate-init```: this creates a local-migrations folder for generating local_migration script. 

This is an approach i use with team mates to make db migration independent of collaborations. In a collobratory capacity this folder would not be pushed to the repo but for the reason of proof of work I am showing this.


```make local-migraion```: This is used to generate migration scripts.


## The Documentation for this server.
FastAPI ships with swagger and redoc documentation automatically generated, and it can be editted and formatted via YAML and arguments settings.

Here is the documentation url: ```localhost:8000/docs```

For the Websocket connection that does not show up in swagger nor redoc, however here is the ws url that can be connected to via postman.


```ws://localhost:8000/ws/task/?access_token=.eJwVzF13giAAgOH_0n2dQXMbl50yhgs8Foh4l-wDQhdLyuTX567f57yzrzEzDdY2txkRkQBmSU9-94lekxfifFWuM7SYENCwHKtl6ev_0O1djpmlvAA7_pNQngaGszY_AEs3ZbvjOtKNeMqlADV3UY3TtCuDkm1PTmersfENbocGBt9AdDlKtKohMEc5XBVEgdjB1pUZJntnMV0yLsacu-S7WLz57a2Dz0l471ev6n746G0Q0hXX22nOaYq2Rv118TL_rM6zBxFwSwI.Zki1Jw.q2tvuzFzNMv7Sd9XdPBdG1UjvWY```

The access_token is gotten when a user signs_up or logs-in.