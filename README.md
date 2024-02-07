
# Py-Waku

## Introduction

Py-Waku exposes a Waku module that can be used within Python projects.
It is fundamentally a wrapper around [nwaku](https://github.com/waku-org/nwaku)

This repo has been tested with Python3 in Ubuntu.

If need a different setup, don't hesitate con contact us on Discord. The Discord server can be found at https://docs.waku.org/.

## Prepare the development environment

Run the following commands from the root folder:
```bash
mkdir venv
```
```bash
python3 -m venv venv/
```
```bash
source venv/bin/activate
```
```bash
./venv/bin/python -m pip install -r requiremets.txt
```

## Create a Py-Waku package

Run the following commands from the root folder:
```bash
source venv/bin/activate
```
```bash
./venv/bin/python3 -m build
```

## Test the package

For that, we have a very simple example in `tests/waku_example.py`.

In order to use the waku module, please install it from the local `dist/` folder, that can be created by following the
instructions from the previous section.

The following command is an example on how to install the local
package to your local virtual env.

```bash
./venv/bin/python3 -m pip install dist/waku-0.0.1-cp310-cp310-linux_x86_64.whl
```

## Update the libwaku.so library

Given that `Py-Waku` conforms a wrapper around `libwaku.so`,
it is likely that you would need to upgrade it.
For that, you will need to update the submodule pointer
to a more recent nwaku version:

1. ```cd vendor/nwaku```
2. Check out to the commit/tag as you wish

Then, follow the following steps from the root folder
to rebuild the `libwaku.so` library:

```bash
cd vendor/nwaku
```
```bash
make libwaku -j8
```
```bash
cd ../../
```
```bash
cp vendor/nwaku/build/libwaku.so lib/
```

Notice that the `libwaku.so` library is also distributed within
the `Py-Waku` package.
