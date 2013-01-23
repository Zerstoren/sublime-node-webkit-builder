sublime-node-webkit
===============

Sublime Text 2 plugin for node-webkit.
Creates .nw archive and executes it on the fly.


Installation
===============

Make sure you have [node-webkit](https://github.com/rogerwang/node-webkit) installed.

Checkout this git repository into your Sublime Text 2 packages dir ( refer to Subltime Text 2 > Preferences > Browse Packages ):

```
cd to/your/sublime/config
git clone git@github.com:Zerstoren/sublime-node-webkit-builder.git Nodewebkit
```

Edit plugin settings to reflect proper location of node-webkit on your system.



Using
===============

Assuming you already have a proper node-webkit project with a package.json, just open your
project in Sublime Text 2 and press F8 ( on OS X default hotkey is Ctrl+Alt+N ). Sublime-node-webkit will
run and pack your node-webkit project if needed.


Issues
==============

Not tested in Windows. May destroy all you files and kill your cat.
