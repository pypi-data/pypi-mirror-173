# The Jira CLI - Manage Jira from the Terminal

<p align="center">
  <img src="https://github.com/jllovet/jira_cli/blob/master/jira_logo.png?raw=true" alt="Jira Logo"/>
</p>

The Jira CLI allows you to configure and manage your Jira instance using simple commands from your terminal.

## Usage

The Jira CLI comes with built-in help to explain how you can use each command.

```shell
python jira.py --help
```

To get an overview of the commands that are available, you can use the tree command.

```shell
python jira.py tree
```

This will output a tree of the commands available to you.

All output to stdout will be in json format, so that the cli can be consumed easily by other systems. A powerful command line tool for dealing with json is [jq](https://stedolan.github.io/jq/). The Jira CLI and jq go hand-in-hand together.

For instance, you can pass a user from the Jira CLI to jq to extract and transform information after you've retrieved it from Jira. Here's a simple transformation you might do before passing the user on to another command.

```shell
python jira.py user get --username mproust | jq '{"email": .emailAddress, "displayName": .displayName, "isActive": .active}'
```

## Setup

We strongly recommend that you use either a docker container or a python virtual environment to separate your configuration from your host.

To use a virtual environment, you can follow the steps below.

Where possible, we're going to use `make`, which wraps up some standard commands for us and helps us run through the same steps every time. Standardization comes in handy.

First, we need to set up and activate the virtual environment.

```shell
make setup
source .venv/bin/activate
```

After this, we are going to install our dependencies.
> Note: You have to have your virtual environment activated before running this command.

```shell
make install
```

There is a file called .example.env that contains a template for environment variables that are going to be used by the CLI. Using make, we're going to copy it, and then you should fill it in with values for your instance of Jira.

```shell
make environment
```
