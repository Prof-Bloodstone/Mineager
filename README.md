# What is Mineager?

It's a plugin manager for your Minecraft server, but not in it's traditional sense.
It provides a simple CLI to check if there are plugin updates available, and can download them for you.

# Current state

Mineager is in alpha - bugs are expected.

# How to use
See `mineager --help` for more information.

### Install a new plugin from URL
Mineager tries to automatically detect plugin information from URLs.

To install new plugin, run `mineager plugin install <URL>`.
It'll try to detect the name of the plugin, but it can be overwritten by `--name` option.

If you want to track the plugin, but don't want to download it, run `mineager plugin add <URL>`.
The plugin will be added to the config, and can be later downloaded with `mineager plugin update`.

##### Important note

Some plugin types can extract all necessary information just from the plugin page,
but some, i.e. Jenkins, require direct link to jar file.
It's always safer to use full download URL.

### Install a new plugin directly
##### Github.com releases
All github repositories are in `https://github.com/<OWNER>/<REPO_NAME>`.
Mineager uses `<OWNER>/<REPO_NAME>` part, to identify the resource.

Let's say you want to install WanderfulAdditions plugin which has GH releases.
Head over to github page: https://github.com/Prof-Bloodstone/WanderfulAdditions
Copy resource identification (`Prof-Bloodstone/WanderfulAdditions`), and run:
```sh
mineager plugin manual install --type github --name 'WanderfulAdditions' --resource 'Prof-Bloodstone/WanderfulAdditions'
```
The latest release will automatically be downloaded and installed.

##### Spigot.com
Unfortunately, Spigot download page is behind CloudFlare, which makes it not possible to automatically download plugins.

Mineager will still provide information about plugin status,
and give direct download links to manually download it.

All spigot resources are under: `https://www.spigotmc.org/resources/<NAME>.<ID>/`.
Mineager uses `<ID>` to identify the plugin.

Let's say you want to install EssentialsX from Spigot website for some reason.
From https://www.spigotmc.org/resources/essentialsx.9089/, the resource id is `9089`.
Install it by running:
```sh
mineager plugin manual install --type spiget --name 'EssentialsX' --resource '9089'
```

### Adding new plugins, without installing
If you want to add new plugin to config list, without downloading it first, use the `add` command.
Its usages is just like for `install` command.

### Checking for plugin updates
If you want to check, if there are any updates available, simply run: `mineager plugin status`

### Updating all plugins
After checking that there are plugin updates available and you want to download newer versions,
simply run `mineager plugin update`. If you have a plugin that needs to be downloaded from CloudFlare protected site,
you'll be given a direct download link for it.

# Developing Mineager

I **HIGHLY** recommend using a virtualenv - I personally prefer using [pyenv](https://github.com/pyenv/pyenv)
with the [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) module.
It also has an easy to use [pyenv-installer](https://github.com/pyenv/pyenv-installer).

I'm developing it on Python 3.7.6, but it _should_ work on Python 3.6+.

To install newest version of all packages and be able to use `mineager` command with all the changes you make,
I recommend using `pip install --editable .`.
