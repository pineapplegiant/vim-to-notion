# My Markdown to Notion 📝 

[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Repo Size](https://img.shields.io/github/repo-size/pineapplegiant/vim-to-notion)](https://img.shields.io/github/repo-size/pineapplegiant/vim-to-notion)
[![Made with Vim :)](https://img.shields.io/badge/madewith-vim%E2%9D%A4%EF%B8%8F-red)](https://img.shields.io/badge/madewith-vim%E2%9D%A4%EF%B8%8F-red)


## Inspiration

I like to write in Vim, but wanted to continue editing on the go in Notion... This helps me upload "faster", to achieve something of that nature idk.

![How it works](./vim-notion.gif)

## Tools
* pipenv
* python3.7

## Development
Put your env files in a `.env` file in the same directory
[Link to how to get your api token](https://medium.com/@jamiealexandre/introducing-notion-py-an-unofficial-python-api-wrapper-for-notion-so-603700f92369)
```
# Your API TOKEN -> 
API_TOKEN = "<MY_API_TOKEN>"

# Table full page
COLLECTION_VIEW = "<MY_URL_TO_THE_TABLE>"
```
First download necessary packages for pipenv:
`pipenv install`

Then run `pipenv run notion_scripts.py -f testMarkdownExample.md`


### Packages used:
* ["unofficial" notion api](https://github.com/jamalex/notion-py)
* [md2notion](https://github.com/Cobertos/md2notion)
* [python frontmatter parser](https://github.com/eyeseast/python-frontmatter)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [pprint](https://docs.python.org/3/library/pprint.html)
