# How People Are Entertained: The Consequences of the 1983 Great Video Game Crash
## 2nd Edition (Improved grammar, checked sources and general fixes)

<iframe frameborder="0" src="https://itch.io/embed/243601" width="552" height="167"></iframe>

Download the e-book in PDF, ePub and Mobi formats on [itch.io](https://inferno986return.itch.io/how-we-are-entertained). If you really like the article, you can give feedback or even buy me a coffee via https://www.paypal.me/HalMotley :-)

## Overview:

This is an article I wrote up on the North American 1983 Video Game Crash and the death + revival of open consoles (game consoles that formally allow/encourage homebrew and modification).

I have typeset it in LaTeX originally using LyX (now I use [ShareLaTeX](https://www.sharelatex.com/)) to make it look presentable on both print and screen. Currently I am happy enough with this document in its current state, but I may add/modify a few things.

## E-book:

I have provided an ePub and the code needed to recreate it, feel free to use the code for your own projects as per the licenses stated below. Currently the ePub passes [epubcheck 4.0.2](https://github.com/IDPF/epubcheck) with `No errors or warnings detected.`

### Compiling:

A new ePub file can be made by using the provided `ebookbuild.py` via installing [Python 3](https://www.python.org/downloads/) and then running the script on IDLE, [Thonny](http://thonny.org/) or the `python3 ebookbuild.py` command on Bash (the macOS/GNU-Linux terminal, Bash can also be installed on Windows 10 via [Windows Subsystem for Linux](https://lifehacker.com/how-to-get-started-with-the-windows-subsystem-for-linux-1828952698)). The script however **does not** work with Python 2 and I have no plans to backport.

At the same time you can ensure the ePub complies with the standard using the command `python3 ebookbuild.py && java -jar epubcheck.jar HowWeAreEntertained.epub`.

XHTML, CSS and the `metadata.json` files can be edited using a text editor such as [Atom](https://atom.io/) and [Notepad++](https://notepad-plus-plus.org/).

The `toc.ncx` and `content.opf` are generated by the `ebookbuild.py` and shouldn't be edited as they would be overwritten.

## Licensing:

Book content such as text and images are licensed under the **Creative Commons Attribution-ShareAlike 4.0 International Public License**.

Book code such as the .lyx, .xhtml, .css and .xml files are licensed under **Creative Commons Zero 1.0 Universal (CC0 1.0)**.
