# Tor Hidden Service Crawler

A Python-based tool for crawling the Tor network and analyzing `.onion` hidden services. This crawler starts with a base `.onion` URL (such as the Hidden Wiki), recursively explores links within the dark web, and extracts structured metadata for research and intelligence analysis.  

Developed and maintained by **Logisec** for security research, intelligence gathering, and darknet infrastructure mapping. Might add more later one for AI development and research.

---

## Overview

This tool performs the following:

- Connects through the Tor SOCKS5 proxy
- Crawls `.onion` sites recursively, scoped per domain
- Extracts metadata: titles, links, status codes, response times
- Outputs structured CSV data per onion domain
- Supports link graph generation and network mapping
- Includes logging and configurable crawling depth/page limits

---

## Requirements

- Python 3.8 or higher
- Tor service installed and running (`tor.exe` or system service)
- Access to the Tor network (default proxy: `127.0.0.1:9050`)

---

## Installation

```bash
git clone https://github.com/Logisec/tor-crawler
cd tor-crawler
pip install -r requirements.txt
```

> ⚠ If you're on Windows, install the [Tor Expert Bundle](https://www.torproject.org/download/tor/), extract it, and run `tor.exe` manually.

---

## Usage

### Basic example

```bash
python main.py --start-url http://example.onion
```

### Advanced usage

```bash
python main.py \
  --start-url http://zqktlwi4fecvo6ri.onion \
  --max-depth 2 \
  --max-pages 30 \
  --data-dir ./output \
  --log-level DEBUG
```

### CLI Options

| Argument      | Description                               | Default  |
| ------------- | ----------------------------------------- | -------- |
| `--start-url` | Starting `.onion` URL to crawl (required) | —        |
| `--max-depth` | Maximum link depth per domain             | `3`      |
| `--max-pages` | Max number of pages per domain            | `50`     |
| `--data-dir`  | Output directory for crawl results        | `./data` |
| `--log-level` | Logging verbosity (DEBUG, INFO, etc)      | `INFO`   |

---

## Output Structure

Each crawl creates the following:

* `data/{domain}.csv`
  Contains crawl metadata:

  * `timestamp`, `url`, `title`, `status_code`, `response_time`, `links_found`

* `data/links_{domain}.csv`
  Contains link graph:

  * `source_url`, `target_url`, `link_text`, `link_title`, `timestamp`

* `crawler.log`
  Detailed log file for debugging and audit trails

---

## Use Cases

* Whatever makes you happy!

---

## Disclaimer

Let’s be honest — nobody reads disclaimers. But here’s ours anyway:

This project is **intended solely for research, education, and legal security analysis**. It’s your responsibility to:

* Know what laws apply to you
* Avoid accessing anything you shouldn’t
* Not do anything stupid with this tool

Logisec does not accept liability if you use this code to break things — including your own system. Don’t crawl illegal content. Don’t generate traffic you can’t explain. Don’t brag about it on Reddit.

You are responsible for what you do with this.

---
## Provided By

**Logisec** — Independent cybersecurity research and tool development.
[https://logisec.net](https://logisec.net)

---

## License

MIT License — use it, modify it, break it, improve it. Just don’t remove the name.
