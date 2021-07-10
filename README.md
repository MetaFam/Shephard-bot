# shepherd-bot

## What does this bot do?

#### Problem Statement-
> Right now people need to come to meetings to check-in their progress by reporting answers to 3 questions: "What did you do last week?" "What will you do this week?" & "What do you need help with?"

#### Features-
- This bot allows you to report your progress by answering using the `^standup` command-
  ```
  ^standup
  I did something on Saturday.
  I also did some work on Sunday, and implemented XYZ.
  ```
- The bot would also send a weekly reminder to everyone in the bot's DB, to remind them that they need to report their progress for this week.

- Bonus: The bot keeps track of whether the person sticks to what they say they will do by checking if they received a checkmark emoji on their report from the guild leader or "verifier".

## How to contribute to this project?

### 1. Fork this repo and get the code locally-
First, [fork this repository to your own account](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo).\
Then use `git clone <url-of-your-fork-of-the-repo>` to clone your forked repository down to your local machine (remember to get the URL for your repository - the _fork_, not the original repository). Use `git remote add upstream MetaFam/shepherd-bot` to add the original repository as the `upstream` (this is helpful for keeping your fork up-to-date).

You could go to the `shepherd-bot` folder, to see the code-
`cd shepherd-bot`

### 2. Sync your fork with the project-
Before starting any work, it is highly recommended that you ensure that your forked version of the repo is up to date. If you set the upstream as mentioned above:
- Switch to the `main` branch:
  ```rb
  git checkout main
  ```
- Get the current state of the original repo, without pulling down the changes to your local machine:
  ```css
  git fetch upstream
  ```
- Reset the state of your local files to match the current state of the original repo:
  ```rb
  git reset --hard upstream/main
  ```
- Force the changes to your forked repo on github (thus making it match the original):
  ```css
  git push -f
  ```
> NOTE: Before you do the above, keep in mind that you will lose any changes you are currently working on. Do this with care.

If you didn't set the `upstream`, working on changes directly on Github, or are not comfortable with using `git`, you could also consider [using the `Fetch Upstream` button on Github's UI](https://twitter.com/i/status/1390382527588798477)

### 3. Create a new branch-
While not 100% necessary, creating a new branch is very helpful and really helps you ensure that you can easily sync your local instance or your fork with the project repo, without losing any of the changes that you made.
And it's always a good idea to avoid committing changes directly to your `main` branch - this keeps it clean and avoids errors when updating the fork(as done in above).

You could use this command to create and switch to a new branch -
```rb
git checkout -b <branchname>
```

(Alternatively, you could also make a branch on github's UI and use `git fetch` and `git checkout <branch-name>` to switch to the created branch)

It would be great, if the names of the branch reflect the essense of what the code-changes in that PR would do.

### 4. Setting up the dev-environment
This might be slightly confusing at first, due to the large amounts of ways of setting this up, however the exact set-up process tries to ensure that there are no errors for you, when you're trying to set this up. If at any point of the process, you feel like this is going south, or you are not able to understand the steps, it's not your fault - It's entirely on us! Do open an issue in those cases, to tell us about which step was confusing and what you didn't understand. Apart from us helping you out, this would also help us in improving upon this documentation and to better explain things. Telling us about what's not clear is very important - If there's something that's not clear in the documentation about how to set the project up, then there's probably something really wrong with the documentation and that needs correction. (*NOTE- Initially the project docs might be basic, and if you have any doubts contact the Bot Army or `Vyvy-vi#5040` on Discord)
> NOTE: For docs or text changes, setting up the dev-environment is not necessary, and you can skip this step :)


#### **A. Seting up a discord bot account**
- Go to [Discord Developers Portal](https://discordapp.com/developers/applications/) and click on `New Application`. Enter a suitable name, and click on `Create`.
- In this new discord application, go to the `Bot` tab, click `Add Bot`, and confirm `Yes, do it!`
- Get the Bot Token for the bot you just created, by clicking on `Copy` button below the `TOKEN` field near the bot name. **DO NOT SHARE THIS BOT TOKEN WITH _ANYONE_**, and don't post this anywhere public.
- Set the value of the environment variable `DISCORD_TOKEN` to the TOKEN that you just copied:
  - Copy the `.env.sample` file to a file called `.env`
    ```
    cp .env.sample .env
    ```
  - Set the value of the env variable in `.env`
    ```
    DISCORD_TOKEN="the token you just copied"
    ```
- Inviting this test-discord-bot to your server: Go to the `General Information` tab on that bot's dashboard on Discord Developers Portal, and copy the bot's Client ID:
  Replace `<INSERT_CLIENT_ID>` in below with the Client ID you just copied-
  ```
  https://discord.com/api/oauth2/authorize?client_id=<INSERT_CLIENT_ID>&permissions=85056&scope=bot
  ```
  Visit the link, and add this bot to a test server.


#### **B. Set up the dev environment**
This project adds some tools and dependencies to the project, so that it is easier for you to pass the CI, and checks on the repo, and also to maintain some amount of clean formatting and clean code. This would also add some pre-push hooks to your project.

- [OPTIONAL] Set up a virtual environment for the project:
  This isn't necessary, however could help you keep your Python Packages clean and prevent version clashes.
  - Making the virtual env-
    ```
    python -m venv env/
    ```
  - Activating the env(This is essential, if you want to use the python installation in the virtaul environment, instead of your global python installation)-
    ```
    source env/bin/activate
    ```
- [ESSENTIAL] Install developer dependencies, and install pre-push-hooks-
  For Dev-Dependencies
  ```
  python -m pip install -r requirements.dev.txt
  ```
  For pre-push hooks
  ```
  python -m pre-commit install --hook-type pre-commit --hook-type pre-push
  ```

- How to use the tools, we just installed?\
  To format the code, run-
  ```
  python -m black src
  ```
  To lint the code, run-
  ```
  python -m flake8 .
  ```
  Also, whenever you push code to the repo, this would auto-format and check the code(and suggest needed changes) :)
  > NOTE: Most of the changes suggested would either be stylistic suggestions or be related to syntax-errors.


#### **C. Set up the database**
The shepherd-bot needs a mongodb database to function properly.
Now, there are 2 choices to move forward with setting up the environment, either using Docker, OR setting up a free MongoDB Atlas instance. Both of these methods have been detailed further in **D1** and **D2**. You can move forward with either of the ways, whichever you find to be easier. (Ideally, if you already have docker and docker-compose installed, going forward with **D1** would be better. OR, say you alread have an account on MongoDB Atlas, you could set up a new Cluster and move forward with **D2**.)


#### **D1. Setting up the db and Running the bot with Docker-Compose**
Docker-Compose sets up a local container running MongoDB, and the bot, which streamlines the development process.
- Install [Docker Desktop](https://docs.docker.com/get-docker/) and [Docker-Compose]()
  Ideally, if you download [Docker Desktop](https://docs.docker.com/get-docker/), that should also bundle `docker-compose` with it. If it doesn't, run `pip install docker-compose` to install the tool.
  > NOTE: You _might_ face issues when downloading these on a device that runnning a Windows version older than Windows 7. If you do face these issues, going along with **D2** might be a good option.
  > NOTE: If you are on Linux, you may need to run these commands with `sudo` priveledges(unless you add this to your server group)

(this assumes that you're in the root directory of the repo)
- Running the bot-
  ```
  docker-compose up --build
  ```
  This should run a docker container with the bot and a local mongodb database(*Ensure that your docker daemon is runing when you're using this command, by opening Docker Desktop)

- Stopping the bot-
  ```
  docker-compose stop
  ```

- To view the bot logs-
  ```
  docker-compose logs bot
  ```

- Removing the docker containers-
  ```
  docker-compose down -v
  ```


Yaaaay! You're through the development environment setup 🎉\
Now you could start working on the code :D


#### **D2. Setting up MongoDB Atlas Cloud instance and Running the bot**
MongoDB Atlas has a rather generous free teir, which should be more than enough for our testing purposes.
- Go to https://www.mongodb.com/try and Sign up for an account.
- Select the `Shared Clusters` path and create a free cluster with default settings from Mongo. It might take a while for the Cluster to get created.
- Setup Connectivity:
  Click on the `CONNECT` button that shows up. Under the `Add a connection IP address`, select `Allow Access from Anywhere` or on `Add your current IP Address`, and click on `Add IP Address`.\
  After that, create a Database User - (choose any kinda simple `username` and `password`, write them down and close that menu)\
  Replace `<username>` and `<password>` in the string below with the username and password that you just wrote-down-
  ```
  mongodb+srv://<username>:<password>@cluster0.9y5sx.mongodb.net/players?retryWrites=true&w=majority
  ```
  > NOTE: Do not share this with anyone. (This is a testing env. so much harm won't be done, however, as a rule of thumb, it's always best to ensure that you keep all of your database credentials and access tokens secure and un-compromised)

- Open the `.env` file and set the `MONGO_URI` variable to the above value:
  ```
  MONGO_URI="mongodb+srv://<your-username>:<your-password>@cluster0.9y5sx.mongodb.net/players?retryWrites=true&w=majority"
  ```
- After this, you can run the bot locally with:
  ```
  python -m src
  ```


Yaaaay! You're through the development environment setup 🎉\
Now you could start working on the code :D


## How to deploy the bot?

**A. Via Docker-**
- Either pull the latest docker image of the bot from Github Container Registry, or clone this project and build it using `docker --tag shepherd-bot .`

- Copy the `.env.sample` file into the `.env` file, or open the Config Variables Setting/files on your deployment server. Set the `DISCORD_TOKEN` variable to your discord bot token. (if you don't have a bot token, scroll above to find out how to get one)

- If you're making quick changes, and don't want to got through the process of setting up a MongoDB cloud instance, you can run the bot with-
  ```
  docker-compose up
  ```

- If you've signed up for a free [Mongo Atlas Cloud instance](https://www.mongodb.com/try), you can set the environment variable `MONGO_URI` equal to the Mongo Connection URI from the MongoDb Atlas instance.
  After this, you can run the bot with-
  ```
  docker run -e PYTHONUNBUFFERED=1 shepherd-bot
  ```

**B. Normal Python Deployment-**
- Clone the repo: `git clone https://github.com/MetaFam/shepherd-bot.git`
- Install dependencies: `pip install -r requirements.txt`
- Run the bot: `python -m src`
