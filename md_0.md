Recursive URL \| 🦜️🔗 LangChain

Skip to main contentLangChain 0\.2 is out! Leave feedback on the v0\.2 docs here. You can view the v0\.1 docs here.![🦜️🔗 LangChain](/v0.2/img/brand/wordmark.png)![🦜️🔗 LangChain](/v0.2/img/brand/wordmark-dark.png)IntegrationsAPI ReferenceMore* People

* Contributing
* Templates
* Cookbooks
* 3rd party tutorials
* YouTube
* arXiv
v0\.2* v0\.2
* v0\.1
🦜️🔗* LangSmith
* LangSmith Docs
* Templates GitHub
* Templates Hub
* LangChain Hub
* JS/TS Docs
💬Search* Providers
	+ Providers
	+ Anthropic
	+ AWS
	+ Google
	+ Hugging Face
	+ Microsoft
	+ OpenAI
	+ More
* Components
	+ Chat models
	+ LLMs
	+ Embedding models
	+ Document loaders
		- Document loaders
		- acreom
		- AirbyteLoader
		- Airbyte CDK (Deprecated)
		- Airbyte Gong (Deprecated)
		- Airbyte Hubspot (Deprecated)
		- Airbyte JSON (Deprecated)
		- Airbyte Salesforce (Deprecated)
		- Airbyte Shopify (Deprecated)
		- Airbyte Stripe (Deprecated)
		- Airbyte Typeform (Deprecated)
		- Airbyte Zendesk Support (Deprecated)
		- Airtable
		- Alibaba Cloud MaxCompute
		- Amazon Textract
		- Apify Dataset
		- ArcGIS
		- ArxivLoader
		- AssemblyAI Audio Transcripts
		- AstraDB
		- Async Chromium
		- AsyncHtml
		- Athena
		- AWS S3 Directory
		- AWS S3 File
		- AZLyrics
		- Azure AI Data
		- Azure Blob Storage Container
		- Azure Blob Storage File
		- Azure AI Document Intelligence
		- BibTeX
		- BiliBili
		- Blackboard
		- Blockchain
		- Brave Search
		- Browserbase
		- Browserless
		- Cassandra
		- ChatGPT Data
		- College Confidential
		- Concurrent Loader
		- Confluence
		- CoNLL\-U
		- Copy Paste
		- Couchbase
		- CSV
		- Cube Semantic Layer
		- Datadog Logs
		- Dedoc
		- Diffbot
		- Discord
		- Docugami
		- Docusaurus
		- Dropbox
		- DuckDB
		- Email
		- EPub
		- Etherscan
		- EverNote
		- Facebook Chat
		- Fauna
		- Figma
		- FireCrawl
		- Geopandas
		- Git
		- GitBook
		- GitHub
		- Glue Catalog
		- Google AlloyDB for PostgreSQL
		- Google BigQuery
		- Google Bigtable
		- Google Cloud SQL for SQL server
		- Google Cloud SQL for MySQL
		- Google Cloud SQL for PostgreSQL
		- Google Cloud Storage Directory
		- Google Cloud Storage File
		- Google Firestore in Datastore Mode
		- Google Drive
		- Google El Carro for Oracle Workloads
		- Google Firestore (Native Mode)
		- Google Memorystore for Redis
		- Google Spanner
		- Google Speech\-to\-Text Audio Transcripts
		- Grobid
		- Gutenberg
		- Hacker News
		- Huawei OBS Directory
		- Huawei OBS File
		- HuggingFace dataset
		- iFixit
		- Images
		- Image captions
		- IMSDb
		- Iugu
		- Joplin
		- Jupyter Notebook
		- Kinetica
		- lakeFS
		- LarkSuite (FeiShu)
		- LLM Sherpa
		- Mastodon
		- MediaWiki Dump
		- Merge Documents Loader
		- mhtml
		- Microsoft Excel
		- Microsoft OneDrive
		- Microsoft OneNote
		- Microsoft PowerPoint
		- Microsoft SharePoint
		- Microsoft Word
		- Near Blockchain
		- Modern Treasury
		- MongoDB
		- News URL
		- Notion DB 1/2
		- Notion DB 2/2
		- Nuclia
		- Obsidian
		- Open Document Format (ODT)
		- Open City Data
		- Oracle Autonomous Database
		- Oracle AI Vector Search: Document Processing
		- Org\-mode
		- Pandas DataFrame
		- Pebblo Safe DocumentLoader
		- Polars DataFrame
		- Psychic
		- PubMed
		- PyPDFLoader
		- PySpark
		- Quip
		- ReadTheDocs Documentation
		- Recursive URL
		- Reddit
		- Roam
		- Rockset
		- rspace
		- RSS Feeds
		- RST
		- scrapfly
		- ScrapingAnt
		- Sitemap
		- Slack
		- Snowflake
		- Source Code
		- Spider
		- Spreedly
		- Stripe
		- Subtitle
		- SurrealDB
		- Telegram
		- Tencent COS Directory
		- Tencent COS File
		- TensorFlow Datasets
		- TiDB
		- 2Markdown
		- TOML
		- Trello
		- TSV
		- Twitter
		- Unstructured
		- Upstage
		- URL
		- Vsdx
		- Weather
		- WebBaseLoader
		- WhatsApp Chat
		- Wikipedia
		- XML
		- Xorbits Pandas DataFrame
		- YouTube audio
		- YouTube transcripts
		- Yuque
	+ Document transformers
	+ Vector stores
	+ Retrievers
	+ Tools/Toolkits
	+ Key\-value stores
	+ Model caches
	+ Graphs
	+ Memory
	+ Callbacks
	+ Chat loaders
	+ Adapters
* 
* Components
* Document loaders
* Recursive URL
On this pageRecursive URL
=============

The `RecursiveUrlLoader` lets you recursively scrape all child links from a root URL and parse them into Documents.

Overview​
---------

### Integration details​

| Class | Package | Local | Serializable | JS support |
| --- | --- | --- | --- | --- |
| RecursiveUrlLoader | langchain\_community | ✅ | ❌ | ✅ |

### Loader features​

| Source | Document Lazy Loading | Native Async Support |
| --- | --- | --- |
| RecursiveUrlLoader | ✅ | ❌ |

Setup​
------

### Credentials​

No credentials are required to use the `RecursiveUrlLoader`.

### Installation​

The `RecursiveUrlLoader` lives in the `langchain-community` package. There's no other required packages, though you will get richer default Document metadata if you have \``beautifulsoup4` installed as well.

```
%pip install -qU langchain-community beautifulsoup4  

```
Instantiation​
--------------

Now we can instantiate our document loader object and load Documents:

```
from langchain_community.document_loaders import RecursiveUrlLoader  

loader = RecursiveUrlLoader(  
    "https://docs.python.org/3.9/",  
    # max_depth=2,  
    # use_async=False,  
    # extractor=None,  
    # metadata_extractor=None,  
    # exclude_dirs=(),  
    # timeout=10,  
    # check_response_status=True,  
    # continue_on_failure=True,  
    # prevent_outside=True,  
    # base_url=None,  
    # ...  
)  

```
**API Reference:**RecursiveUrlLoaderLoad​
-----

Use `.load()` to synchronously load into memory all Documents, with one
Document per visited URL. Starting from the initial URL, we recurse through
all linked URLs up to the specified max\_depth.

Let's run through a basic example of how to use the `RecursiveUrlLoader` on the Python 3\.9 Documentation.

```
docs = loader.load()  
docs[0].metadata  

```

```
/Users/bagatur/.pyenv/versions/3.9.1/lib/python3.9/html/parser.py:170: XMLParsedAsHTMLWarning: It looks like you're parsing an XML document using an HTML parser. If this really is an HTML document (maybe it's XHTML?), you can ignore or filter this warning. If it's XML, you should know that using an XML parser will be more reliable. To parse this document as XML, make sure you have the lxml package installed, and pass the keyword argument `features="xml"` into the BeautifulSoup constructor.  
  k = self.parse_starttag(i)  

```

```
{'source': 'https://docs.python.org/3.9/',  
 'content_type': 'text/html',  
 'title': '3.9.19 Documentation',  
 'language': None}  

```
Great! The first document looks like the root page we started from. Let's look at the metadata of the next document

```
docs[1].metadata  

```

```
{'source': 'https://docs.python.org/3.9/using/index.html',  
 'content_type': 'text/html',  
 'title': 'Python Setup and Usage — Python 3.9.19 documentation',  
 'language': None}  

```
That url looks like a child of our root page, which is great! Let's move on from metadata to examine the content of one of our documents

```
print(docs[0].page_content[:300])  

```

```

<!DOCTYPE html>  

<html xmlns="http://www.w3.org/1999/xhtml">  
  <head>  
    <meta charset="utf-8" /><title>3.9.19 Documentation</title><meta name="viewport" content="width=device-width, initial-scale=1.0">  

    <link rel="stylesheet" href="_static/pydoctheme.css" type="text/css" />  
    <link rel=  

```
That certainly looks like HTML that comes from the url https://docs.python.org/3\.9/, which is what we expected. Let's now look at some variations we can make to our basic example that can be helpful in different situations. 

Lazy loading​
-------------

If we're loading a large number of Documents and our downstream operations can be done over subsets of all loaded Documents, we can lazily load our Documents one at a time to minimize our memory footprint:

```
page = []  
for doc in loader.lazy_load():  
    page.append(doc)  
    if len(page) >= 10:  
        # do some paged operation, e.g.  
        # index.upsert(page)  

        page = []  

```

```
/var/folders/4j/2rz3865x6qg07tx43146py8h0000gn/T/ipykernel_73962/2110507528.py:6: XMLParsedAsHTMLWarning: It looks like you're parsing an XML document using an HTML parser. If this really is an HTML document (maybe it's XHTML?), you can ignore or filter this warning. If it's XML, you should know that using an XML parser will be more reliable. To parse this document as XML, make sure you have the lxml package installed, and pass the keyword argument `features="xml"` into the BeautifulSoup constructor.  
  soup = BeautifulSoup(html, "lxml")  

```
In this example we never have more than 10 Documents loaded into memory at a time.

Adding an Extractor​
--------------------

By default the loader sets the raw HTML from each link as the Document page content. To parse this HTML into a more human/LLM\-friendly format you can pass in a custom `extractor` method:

```
import re  

from bs4 import BeautifulSoup  

def bs4_extractor(html: str) -> str:  
    soup = BeautifulSoup(html, "lxml")  
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()  

loader = RecursiveUrlLoader("https://docs.python.org/3.9/", extractor=bs4_extractor)  
docs = loader.load()  
print(docs[0].page_content[:200])  

```

```
/var/folders/td/vzm913rx77x21csd90g63_7c0000gn/T/ipykernel_10935/1083427287.py:6: XMLParsedAsHTMLWarning: It looks like you're parsing an XML document using an HTML parser. If this really is an HTML document (maybe it's XHTML?), you can ignore or filter this warning. If it's XML, you should know that using an XML parser will be more reliable. To parse this document as XML, make sure you have the lxml package installed, and pass the keyword argument `features="xml"` into the BeautifulSoup constructor.  
  soup = BeautifulSoup(html, "lxml")  
/Users/isaachershenson/.pyenv/versions/3.11.9/lib/python3.11/html/parser.py:170: XMLParsedAsHTMLWarning: It looks like you're parsing an XML document using an HTML parser. If this really is an HTML document (maybe it's XHTML?), you can ignore or filter this warning. If it's XML, you should know that using an XML parser will be more reliable. To parse this document as XML, make sure you have the lxml package installed, and pass the keyword argument `features="xml"` into the BeautifulSoup constructor.  
  k = self.parse_starttag(i)  
``````output  
3.9.19 Documentation  

Download  
Download these documents  
Docs by version  

Python 3.13 (in development)  
Python 3.12 (stable)  
Python 3.11 (security-fixes)  
Python 3.10 (security-fixes)  
Python 3.9 (securit  

```
This looks much nicer!

You can similarly pass in a `metadata_extractor` to customize how Document metadata is extracted from the HTTP response. See the API reference for more on this.

API reference​
--------------

These examples show just a few of the ways in which you can modify the default `RecursiveUrlLoader`, but there are many more modifications that can be made to best fit your use case. Using the parameters `link_regex` and `exclude_dirs` can help you filter out unwanted URLs, `aload()` and `alazy_load()` can be used for aynchronous loading, and more.

For detailed information on configuring and calling the `RecursiveUrlLoader`, please see the API reference: https://api.python.langchain.com/en/latest/document\_loaders/langchain\_community.document\_loaders.recursive\_url\_loader.RecursiveUrlLoader.html.

Related​
--------

* Document loader conceptual guide
* Document loader how\-to guides
Edit this page

---

#### Was this page helpful?

#### You can also leave detailed feedback on GitHub.

PreviousReadTheDocs DocumentationNextReddit* Overview
	+ Integration details
	+ Loader features
* Setup
	+ Credentials
	+ Installation
* Instantiation
* Load
* Lazy loading
* Adding an Extractor
* API reference
* Related
Community* Twitter
GitHub* Organization
* Python
* JS/TS
More* Homepage
* Blog
* YouTube
Copyright © 2024 LangChain, Inc.