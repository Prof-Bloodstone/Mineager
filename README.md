# THIS IS NOT READY!

# What is Mineager?

It's a plugin manager for your Minecraft server, but not in it's traditional sense.
It provides a simple CLI to check if there are plugin updates available, and can download them for you.

# How to use

Create `plugins.yml` file in your minecraft server root directory and list plugins in it. For example:
```yml
---
- type: Spigot
  name: "Simple Anti-Mob Lag"
  resource: 67484
- type: Github
  name: WanderfulAdditions
  resource: Prof-Bloodstone/WanderfulAdditions
```
Alternatively, you can pass path to your file using `--config-path` option or `MINEAGER_CONFIG_PATH` environment variable.

See `mineager --help` for more information.

# Developing Mineager

I **HIGHLY** recommend using a virtualenv - I personally prefer using [pyenv](https://github.com/pyenv/pyenv)
with the [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) module.
It also has an easy to use [pyenv-installer](https://github.com/pyenv/pyenv-installer).

I'm developing it on Python 3.7.6, but it _should_ work on Python 3.6+.

To install newest version of all packages and be able to use `mineager` command with all the changes you make,
I recommend using `pip install --editable .`.