Intro with some text [Docs]().

## Features

s
Some of it’s stand out features are:

- Healthstream API client

## Development

Install dev requirements

`make install-dev`

First install PNPM with Homebrew

`brew install pnpm`

Development for the healthstream package requires flake8 linter to pass. In order to commit and pass CI, install a pre-commit hook for that, you should run `pnpm install`

`pnpm install`

## Installation

Installing with:

```bash
pip install 'healthstream'
```

## Setup for production

Add a `healthstream.toml` to project directory, so healthstream can pick-up settings.

```toml
```

### Setup for local development

Start stubbed API if no Healthstream credentials are present or for development in local-mode.

```toml
```

Now start dev server

```shell
make dev
```

## Usage

Write more about using code in other projects

```python
from healthstream.settings import load_settings

# load config
config = load_settings('healthstream.toml')

```

## Run tests

- No tests yet

## CLI Usage

```shell
```

#### Get information about Healthstream CLI command

```shell
healthstream version
```

## Documentation

Our documentation is on [Docs]().

## Ideas

- 

## Is it any good?

[Yes.](http://news.ycombinator.com/item?id=3067434)

## License

The MIT License
