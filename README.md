# pyrdian

Unoffical simple terminal RSS client for [The Guardian](https://www.theguardian.com/international/rss) implemented in Python3.

## Installation

Clone the repository using `git clone` and use the [pip](https://pip.pypa.io/en/stable/) package manager to install pyrdian dependencies:

```bash
git clone https://github.com/Mon-mon-mik/pyrdian.git && pip3 install -r pyrdian/requrements.txt
```
## Usage

Print help for all command-line options to learn more details:

```bash
python3 pyrdian -h
```
or

```bash
cd pyrdian && python3 . -h
```

Optional arguments:

```bash
  -c COUNT, --count COUNT                        show no more than count articles
  -t, --show-title                               show titles
  -u, --show-url                                 show links
  -s, --sort                                     sort articles in alphabetical order, from A to Z
  -n, --newest                                   sort articles by newest to oldest
  -o, --oldest                                   sort articles by oldest to newest
  -D, --show-tags                                show tags
  -T TAGS [TAGS ...], --tags TAGS [TAGS ...]     show articles with at least one tag from the list
  -d, --show-date                                show publish dates
```
If none of the options is specified, all options are printed.
If you do not give any argument from list: -t, --show title, - u, --show url, -D, --show tags, -d, --show date, all values are printed

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)