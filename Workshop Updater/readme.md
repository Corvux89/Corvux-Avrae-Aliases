# Avrae Utilities for PyCharm
A runnable configuration for [Pycharm](https://www.jetbrains.com/pycharm/) for the [Avrae](https://avrae.io/) Discord bot

## Important Note
This package makes a remote connection to the Avrae API in order to collect and update the information. It only does this by request, and will not make any outward connection without being prompted to by the user.

## Setup
In order for this plugin to have your permissions to grab and update your GVARs, Workshop Aliases, or Workshop Snippets, you need to give it your token.

1. Setup a run configuration in PyCharm to run the ``avrae.py`` file
2. Go to [Avrae](https://avrae.io) and log in to the dashboard
3. Press F12 to open the DevTools
4. Go to the 'Application' tab
5. On the left, select 'https://avrae.io' under 'Local Storage'
6. Copy the 'Value' next to the 'avrae-token' key
7. In your PyCharm run configuration or OS variables set a variable names ``AVRAE_TOKEN`` to the copied value
8. In your Pycharm run configuration setup a ``$FilePath$`` in your Parameters

### Note
Please keep this token private, as anyone who gains access to this token could potentially gain access to your Discord account.

### Get Collection Information
You can use the ``Pull New Collection Data`` button to collect a json of all of the aliases and snippets ids within a collection. This expects the collection ID. You can find this by going to the collection on the Workshop, and looking at the url. Everything after ``avrae.io/dashboard/workshop/`` is your ID.

Once you've ran the ``Pull New Collection Data`` command, save the result as `collection.id` in the folder you wish to save your collection in. This will also automatically download the collection description if the collection has one and save it in a `readme.md`

Now that you have the `collection.id` anytime you run this updator in the directory it resides, it will assume we are working with this collection.

## Updating 
When working within a collection file, if this application is set to the default configuration you can hit `shift + f10` to run it. It will prompt for what you want to do.

1. Push Update -> Select this or hit `1` to push an update. It will handle checking if this is a snippet, alias, or markdown descriptions for an alias, snippet, or 


#### Folder Structure
Support for editing the documentation will come in a future update.

Here is an example collection folder structure:
```bash
root
 | # This is the folder your collection will live in
 ├ Collection Name
 | | # This contains the json collected by the `Pull New Collection Data` command
 | ├ collection.id 
 | | # This contains the markdown for the collection description
 | ├ readme.md 
 | | # This contains the alias itself
 | ├ aliasName.alias 
 | | # This contains the alias itself, collected by the `Get Workshop Alias` command, and updated with the `Update Workshop Alias` command
 | ├ aliasName.md 
 | | # This contains the markdown the alias description
 | ├ aliasName subAalias.alias 
 | | # This contains the markdown the alias description
 | ├ aliasName subAalias.md 
 | | # This contains the snippet itself, collected by the `Get Workshop Snippet` command, and updated with the `Update Workshop Snippet` command
 | ├ snippetName.snippet 
 | | # This contains the markdown the snippet description
 | └ snippetName.md 
```