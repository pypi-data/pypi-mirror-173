# EasyUp
Easy Way to update your installed tools on os

> only support windows and download from GitHub only

### Command
`github`

### Option

```shell
  Options:
  -l, --repo-url TEXT  Github Repository Path {OWNER}/{REPO_NAME}
  --ext TEXT           Select Custom Extension
  --help
```

### Usage

```shell
  easy-up github [OPTIONS]
```

# Contribute

### Setup ENV
- clone repo `https://github.com/islam-kamel/package_manager.git`
- install `python 3` recommendation 3.10 or higher
- install `build` command `pip install build`
- install requirements from `requirements.txt`
- create build `python -m build`
- install local package `pip install dist/{PACKAGE_NAEM}.tar.gz`
- now run command 'easy-up'

push your code in new branch e.g `Fixbug`

