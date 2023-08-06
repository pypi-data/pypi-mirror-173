# toybox.py

[![MIT License](https://img.shields.io/github/license/toyboxpy/toybox.py)](https://spdx.org/licenses/MIT.html) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/toyboxpy.svg)](https://python.org) [![PyPI - Version](https://img.shields.io/pypi/v/toyboxpy.svg)](https://pypi.org/project/toyboxpy) [![Python package](https://github.com/toyboxpy/toybox.py/actions/workflows/python-package.yml/badge.svg)](https://github.com/toyboxpy/toybox.py/actions/workflows/python-package.yml)

A **Lua**, **C** and asset dependency manager for the [**Playdate**](https://play.date) **SDK**.

**toybox.py** lets you easily use, create and share third party libraries, called **toyboxes**, for any **Playdate** project. It handles all dependencies between **toyboxes** automatically and provides precise versioning for each **toybox**.

Some **toyboxes** may provide **C** code, some may provide **Lua** code or **Lua** extensions written in **C** and some may provide just assets. Some **toyboxes** may provide all three or only two of these, it's completely up to the **toybox** creator and maintainer.

The main website for the project is at [**toyboxpy.io**](https://toyboxpy.io), there is also a [**blog**](https://toyboxpy.io/blog) and you can join the community around the project on its [**discussions**](https://github.com/toyboxpy/toybox.py/discussions) forum.

You can also follow the project on [**Mastodon**](https://mastodon.social/@toyboxpy) or [**Twitter**](https://twitter.com/toyboxpy).

Playdate is a registered trademark of [**Panic**](https://panic.com).

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Using Lua toyboxes](#using-lua-toyboxes)
- [Using C toyboxes](#using-c-toyboxes)
- [Creating your own toyboxes](#creating-your-own-toyboxes)
- [License](#license)

### Installation

**toybox.py** is a pure python project and it requires at least [Python](https://python.org) 3.7 and access to the [git](https://git-scm.com) command line tool. Make sure you have a [supported version](https://toyboxpy.io/blog/installing-python) of **Python** before proceeding.

You can install **toybox.py** by typing the following in a terminal window:

```console
pip install toyboxpy
```

### Usage

**toybox.py** supports various commands, sometimes with one extra argument:

```console
toybox <command> <argument>
```

The following commands are supported:

```console
help                 - Show a help message.
help <topic>         - Show a help message on a topic (use 'help topics' for a list).
version              - Get the Toybox version.
license              - Show the license for the app.
info                 - Describe your dependency set.
add <url>            - Add a new dependency.
add <url> <version>  - Add a new dependency with a specific version.
remove <ulr>         - Remove a dependency.
update               - Update all the dependencies.
update <dependency>  - Update a single dependency.
check                - Check for updates.
set <name> <value>   - Set a configuration value for this toybox.
```

**toybox.py** should always be run from your project's root directory. Although it doesn't use and `git` commands directly on your project folder, some `git` commands that **toybox.py** uses do require that your project folder already be a `git` repo. A simple `git init` suffices. This also makes it easy for you to also back-track any unwanted changes.

**toybox.py** creates and uses a local file at the root of your project's directory named `Boxfile`. You can use the `add` and `remove` commands to modify it.

#### Adding dependencies

The `add` command takes up to two arguments:

```console
toybox add <url> <version>
```

The `url` argument should either be the full url to a **git** repository which contains the **toybox** you would like to add, such as `https://github.com/DidierMalenfant/modplayer.git` or any of the short forms below, which all point to the same repository:

```
https://github.com/DidierMalenfant/modplayer
github.com/DidierMalenfant/modplayer
DidierMalenfant/modplayer
```

**toyboxes** do not need to be hosted on [Github](https://github.com) but, as shown above, if the server url is omitted then Github is assumed.

Adding a dependency with a `url` which already exists for your project will replace the `version` used for that dependency.

The `version` parameter is optional and allows you to select a specific or a range of versions for the **toybox** but also lets you specify the name of a branch when, for example, using a development version of a given **toybox**.

To require a specific version, just set `version` to a valid [semver](https://semver.org) such as `'1.4.12'`.

You can also require a specific minor version with `'1.4'` or a specific major version with `'1'`. In that case, the latest version with the given minor or major version numbers will be used which allows a developer using your **toybox** to stay up to date with bug fixes or new features without risking an API change from breaking your project.

If you would like to fine tune your version requirement even more, you can instead use up to two comparaison operators in the `version` argument. For example `'>1.2.3 <=3.0.0'`. Keep in mind that, here too, valid [semver](https://semver.org) version numbers should be used. Major or minor versions can be still used in combination with comparaisons. For example, a version requirement like `'3 <3.9.0'` results in all versions higher or equal to `3.0.0` but less than `3.9.0`. Supported comparaison operators are `>`, `<`, `>=`, `<=`.

You can also request a specific branch for any given **toybox** just by using the name of the branch, as in ``develop``, instead of a version number. In that case, the latest commit from that branch is used when updating.

There may be times, like during development of a **toybox**, when you'll want to use a local version of a **toybox** instead of one found on a server. In order to do that, just replace `version` by the path to the local folder that contains your **toybox** and then use the `update` command. This path need to start with either `~` or `/`. In order to prevent you from committing files that come from a local **toybox** by mistake, using local **toyboxes** will also create a pre-commit hook that will prevent you from making any commits while local **toyboxes** are used.

On **macOS** and **linux**, the content of a local **toybox** is be soft-linked inside your project instead of copied. This way, any modifications you make during development will modify the actual local **toybox** directly. On **Windows**, the files from the local **toybox** are just copied over.

In order to restore everything after using local **toyboxes**, just add back the regular version and use the `update` command again.

Finally if no `version` argument is provided then the default branch for the **toybox**'s repo is used.

#### Removing dependencies

You can remove a **toybox** with the remove command:

```console
toybox remove <url>
```

#### Updating dependencies

Once you've added or modified a dependency, you can update its content within your project by using the `update` command:

```console
toybox update <dependency>
```

The `dependency` argument used here is the name of the dependency, which is the name of the repo and not its `url`. If no `dependency` argument is used then all dependencies are updated.

**toybox** records the current version of any dependency installed in your project so keep in mind that this may modify the `Boxfile` for your project.

#### Checking for updates

You can check to see if any of the **toyboxes** you use have been updated by using the `check` command:

```console
toybox check
```

This will not modify anything within your project, it will just let you know if anything new is available for you.

### Using Lua toyboxes

Any **toybox** will be installed in a subfolder named `toyboxes` at the root folder of your project. If any of the **toyboxes** provides **Lua** code, a file named `toyboxes.lua` will be created in that folder. All you need to do to start using your **toyboxes** is import that file anywhere in your project.

Assuming you are using the standard [project structure](https://sdk.play.date/1.12.2/Inside%20Playdate.html#_structuring_your_project) suggested by the **Playdate SDK** and have your **Lua** source files in a subfolder named `source` then you can do this by adding this import statement in any file that uses the **toyboxes**:

```lua
import '../toyboxes/toyboxes.lua'
```

Note that due to a bug in the `pdc` app used by the **Playdate SDK** to process source files, the `.lua` extension is required here. Once this bug is fixed, this will no longer be needed.

### Using C toyboxes

Any **toybox** will be installed in a subfolder named `toyboxes` at the root folder of your project. If any of the **toyboxes** provides **C** code, a file named `toyboxes.mk` and a file named `toyboxes.h` will be created in that folder.

Assuming your makefile is in your project's root folder, you will need to include this makefile in your own before you include the **Playdate** SDK's common makefile:

```make
include toyboxes/toyboxes.mk

...

include $(SDK)/C_API/buildsupport/common.mk
```

You will then need to call the **toyboxes** init macro `REGISTER_TOYBOXES` during the `kEventInitLua` event and pass it a `PlaydateAPI*`:

```c
#include "toyboxes.h"

#include "pd_api.h"

int eventHandler(PlaydateAPI* playdate, PDSystemEvent event, uint32_t arg)
{
    if(event == kEventInitLua) {
        REGISTER_TOYBOXES(playdate)
    }
    
    return 0;
}
```

If you don't know how to setup your project to use **C** extensions, you can check out the [modplayer-sample](https://github.com/DidierMalenfant/modplayer-sample) project which is a simple project using the **C** extension **toybox** named `modplayer`.

### Using assets from toyboxes

If you want, or need, to access a **toybox**'s assets directly they will, if any, be located in a folder named `toybox_assets` inside the `source` folder of your project. The folder is organised by **toybox** URLs so, for example, an asset named `MyPic` in a **toybox** named `MyRepo` from user `Usernmame` on `github` will be located at
```
source/toybox_assets/github.com/Username/MyRepo/MyPic
```
More often than not, **toyboxes** will provide **Lua** methods to access their assets though so you shouldn't need to do this.

#### Adding the toybox powered badge

If your projects use **toyboxes**, you can let others know that they are [![Toybox Powered](https://img.shields.io/badge/toybox.py-powered-orange)](https://toyboxpy.io) by adding this badge to your `README.md` file:

```
[![Toybox Powered](https://img.shields.io/badge/toybox.py-powered-orange)](https://toyboxpy.io)
```

### Creating your own toyboxes

Of course the best part of **toybox.py** is that anyone can create, distribute and maintain their own **toyboxes** for others to use. All you need it a **git** repo (which can be located anywhere on the internet) and to make sure that some of your code is laid out in a way that **toybox** can process and understand.

For starters, the name of your **git** repo will be the name **toybox** uses for a lot of things. It's better not to use the name of an existing **toybox** as this could cause clashes with future **toybox.py** features (i.e. search for **toyboxes** on the **toyboxpy.io** website or add your **toybox** to a potential registry of **toyboxes**).

**toyboxes** can provide **Lua** methods, either written in **Lua** or in **C** as extensions to the **Lua** language, or **C** methods that can be used by others when writing their own **C** code for the **Playdate**. Your **toybox** can provide just one, two or all three of these types of extensions.

Versionning for **toyboxes** is done via tags in the git repo for your **toybox**. Those tags should be a valid [semver](https://semver.org) version and can optionally be prefixed by a `v`. For example `v2.3.0` is correct, `v2.3` is not. The most important part for users of your **toybox** is to make sure that you only fix issues when incrementing a patch version, that you only add new functionality when incrementing a minor version and that you always increment the major version when adding things to your **toybox** that may break things for your users (removing deprecated methods or changing the API for example).

It's usually a good idea, rather than provide a swiss-army knife type of **toybox**, to try and make sure your **toyboxes** provide just one service and do it well. Split different functionality into separate **toyboxes** so developers can only add the ones they need.

**toyboxes** can depend on other **toyboxes**. All you need is to add a `Boxfile` in the root directory of your **toybox** and it will be taken care of automatically when resolving dependencies. Be careful, during development for example, to not resolve that dependency directly in your project folder. You could end up committing the resulting **toyboxes** folder which would be redundant when others use your **toybox**. Instead you can use it as a local **toybox** in a test project.

A **Lua** **toybox** can depend on a **C** **toybox** and a **C** **toybox** can depend on another **C** **toybox**. You don't even need any extra import statements because any **Lua** **toyboxes** your **toybox** depends on should already be imported before your **toyboxe**'s import file is imported.

Try to make sure that **toyboxes** don't cross-depend on each other (**A** require **B** and **B** also requires **A**) as this is usually a sign of some API design issues and can complicate things in the long run.

#### Creating a Lua toybox

Creating a **Lua** **toybox** is as simple as adding one **Lua** file at the root to your project's repo or in a subfolder named `source` or `Source`. That file can be named `import.lua` or the same as your project and must contain all the import statements required to use your **toybox**. For example, the fictional `MyPdPi` **toybox**, if written in **Lua**, would contain one file named `MyPdPi.lua` which would look like this:

```lua
--
--  MyPdPi - Calculate Pi to an infinite number of decimals.
--

import "math"
import "picalc"
import "utils"
```

The source code itself in your **toybox** can be laid out any way you want (additional `Source` subfolder, etc...) as long as this file imports all the other files correctly.

If you wish to use a completely custom name for the **Lua** file **toybox** will import for your project, you can use the `set lua_import` command:

```console
toybox set lua_import mycustomfile.lua
```

This will create a `Boxfile` in your project, if one didn't already exist, and will set a configuration parameter for **toybox** to use that **Lua** file when importing your **toybox** instead of the default.

#### Creating a C toybox

Creating a **C** **toybox** is almost as simple and requires three things. First you need to create a makefile for your **toybox** in the root folder of your project and name it after your project. Once again, if the fictional `MyPdPi` **toybox** was written in **C**, it would contain one file named `MyPdPi.mk` which would look like this: 

```make
#
#  MyPdPi - Calculate Pi to an infinite number of decimals.
#

# -- Find out more about where this file is relative to the Makefile including it
_RELATIVE_FILE_PATH := $(lastword $(MAKEFILE_LIST))
_RELATIVE_DIR := $(subst /$(notdir $(_RELATIVE_FILE_PATH)),,$(_RELATIVE_FILE_PATH))

# -- Add us as an include search folder only if it's not already there
uniq = $(if $1,$(firstword $1) $(call uniq,$(filter-out $(firstword $1),$1)))
UINCDIR := $(call uniq, $(UINCDIR) $(_RELATIVE_DIR))

# -- Add our source files.
SRC := $(SRC) \
       $(_RELATIVE_DIR)/MyPdPi/MyPdPi.c
```

The first section is very important and makes sure that the makefile is relocatable, i.e. can work no matter where the includer's makefile is located. The second part adds the root folder of your **toybox** as an include path. The last section adds the source files that need to be compiled for your **toybox**. Don't forget the `$(SRC)` on the first line to make sure that any previous sources files from other **toyboxes** are included.

The use of `:=` instead of `=` is also very important here as it force make to resolve the value right here and there, instead of when it is used because it could have been overwritten by another **toybox** at that point.

Header files for your project should be located in a subfolder named after your project, in our case `MyPdPi` and it should contain at least an include header named after your project, i.e. `MyPdPi.h` which, at a minimum, looks like this:

```c
/*
*  MyPdPi - Calculate Pi to an infinite number of decimals.
*/

#ifndef MYPDPI_H
#define MYPDPI_H

#include "pd_api.h"

// -- Globals
extern PlaydateAPI* pd;

// -- toybox registration function
void register_MyPdPi(PlaydateAPI* playdate);

#endif
```

As shown above, your **toybox** header file needs to declare at least one function and that's the function called during the `kEventInitLua` event. The name of that function needs to be `register_<toybox_name>` and take a `PlaydateAPI* playdate` as an argument. If you're registering extensions to the **Lua** language this is where that would take place.

You can also declare any other functions your **toybox** exposes or include any other header files that may be needed. If your **toybox** is just providing **C** code for other projects and doesn't require any particular initialisation you can leave this method empty or just grab the `PlaydateAPI*` for future use elsewhere in your code, like so:

```c
/*
 *  MyPdPi - Calculate Pi to an infinite number of decimals.
 */
 
#include "MyPdPi/MyPdPi.h"

// -- Globals
PlaydateAPI* pd = NULL;

// -- toybox registration function
void register_MyPdPi(PlaydateAPI* playdate)
{
    pd = playdate;
}
```

#### Providing assets in your toybox

If your **toybox** uses or provides assets, they should be located in a folder named `assets` at the root of your **toybox** folder. This folder will be moved into the end-user's `source` folder during installation so that it can be accessible by `pdc` during compilation of the project. You will therefore need to use a specific path in order to reach those assets from your code.

For example, if our `MyPdPi` **toybox** contained an image named `MyPic.png` in `assets/images` and was available via a `github` repo named `MyRepo` from user `MyUsername` then accessing the asset can be done as follows:
```
image = playdate.graphics.image.new(`toybox_assets/github.com/MyUsername/MyRepo/images/MyPic`)
```
While this works when the code is internal to your **toybox**, when you need to provide assets to the end-user of your **toybox**, it is much more elegant to provide utility methods in order to access your assets, like this:
```
function MyPdPi.getMyPic()
    return playdate.graphics.image.new(`toybox_assets/github.com/MyUsername/MyRepo/images/MyPic`)
end
```
That way they do not have to deal with the path to your asset. Check out the [FontSample](https://github.com/DidierMalenfant/FontSample) sample **toybox** for an examples of how to do this.

You can override the subfolder used for your **toybox**'s assets by using the `set assets_sub_folder` command:

```console
toybox set assets_sub_folder My/Custom/Path
```

This will create a `Boxfile` in your project, if one didn't already exist, and will set a configuration parameter for **toybox** to use that subfolder inside the **toybox_assets** folder. This is **not recommended** to use for production **toyboxes** as is could cause name collisions. It can still be useful if you forked a **toybox** repo for development but want to still keep the assets' path the same as the original repo.

#### Letting others know about your toybox

It's not required, but it's always a good idea, to add a word about **toybox.py** in the README.md of your **toybox** repo so developers know what it contains and how to use it:

```console
**MyPdPi** is a [**Playdate**](https://play.date) **toybox** which lets you calculate Pi to an infinite number of decimals.

You can add it to your **Playdate** project by installing [**toybox.py**](https://toyboxpy.io), going to your project folder in a Terminal window and typing:

    toybox add MyGitHubUsername/MyPdPi
    toybox update

This **toybox** contains both **Lua** and **C** toys for you to play with.
```
You can also add a nice [![Toybox Compatible](https://img.shields.io/badge/toybox.py-compatible-brightgreen)](https://toyboxpy.io) badge like this:

```
[![Toybox Compatible](https://img.shields.io/badge/toybox.py-compatible-brightgreen)](https://toyboxpy.io)
```

Don't forget to also let us know about your **toyboxes** via social media (`#toyboxpy`, mentions or DM) so that we can spread the word too... 

### License

**toybox.py** is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
