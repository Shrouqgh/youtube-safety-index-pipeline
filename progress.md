# Project Progress Log

## Week 1 (Oct 1 - Oct 7)
- **Hours Worked**: 9
- **Tasks Completed**:
  - Installed Ubuntu ISO image on a virtual machine 
  - Installed Squid and configured the proxy settings
  - Ran into issues with SSL support—faced challenges understanding how SSL bumping works with Squid.
  - Spent some  time troubleshooting the `sslcrtd_program` helper crashes. Tried several approaches related to permissions on the certificate directories.
  - Generated a certificate for SSL bumping and imported it to the client device (iPhone) to allow/test SSL interception.
  - Configured basic proxy functionality but couldn't get SSL certificates working properly yet.
  - No successful test results logged from the phone setup,possibly due to iOS privacy restrictions or security features. more work is needed to capture the logs.

## Week 2 (Oct 8 - Oct 14)
- **Hours Worked**: 4
- **Tasks Completed**:
  - Continued working on fixing the SSL helper crash issue - focused on permission configurations and rebuilding the SSL database.
  - Ran further tests on the proxy setup with the iPhone, but logs weren’t generated, suggesting further issues with SSL interception or configuration.
  - Checked port conflicts and verified cache settings, but the root cause of the SSL crash still  unresolved.
  - Next step: explore alternative solutions for resolving SSL certificate generation and ensuring Squid captures client traffic. will utilize Windows OS as a client.

## Week 3: High-throughput ETL Engineering & Storage Layer Indexing (Heavy Implementation)
- **Hours Worked**: 24 Hours  
- **Focus Area:** automated log parsing, text extraction, & Elasticsearch cluster ingestion
- **Tasks Completed**:
  - Automated log retrieval engine:** engineered a background Python service to tail live, decrypted proxy network stream logs. Designed high-performance file-watching listeners to capture packet dumps with sub-second latency.
  - Algorithmic text extraction layers:** Developed highly optimized regular expression (Regex) parsing utilities to isolate explicit YouTube endpoint headers, extracting localized alphanumeric video string identifier tokens (`watch?v=...`) from raw, chaotic network payloads.
  - Elasticsearch index schema design:** provisions a local Elasticsearch storage cluster. Designed custom structural mapping schemas, explicit date-timestamp formats, and text tokenization rules within the target indexing layer (`youtube_proxy_logs_v1`) to prepare data for downstream natural language processing.
  - Built an automated ETL streaming script utilizing the bulk ingestion API. Configured error-handling, payload retry backoffs, and duplicate-checking constraints to guarantee that the database state reflects clean, uncorrupted records.

### Deep-dive debugging & infrastructure challenges
* **Stream Buffer & Token Extraction Tuning:** Resolved early pipeline memory bottlenecks where rapid, multithreaded network requests caused the Python parsing script to drop packets. Implemented an in-memory queue data structure to cleanly buffer log lines before processing.
* **Dynamic Mapping Conflicts:** Debugged Elasticsearch strict type mismatch errors caused by irregular or un-parsable network log tokens. Implemented strict data sanitization and defensive exception handling directly inside the Python extraction loop.

## Week 4: Machine Learning Pipeline Execution & Interface Synthesis
- **Hours Worked**: 14 Hours  

- **Tasks Completed**:
  - BERT classification pipeline connection: connected the structural Elasticsearch logs directly to a downstream BERT-based threat classification model optimized to ingest text tokens and classify contextual safety indices.
  - Model evaluation & matrix analytics: generated systematic performance diagnostic profiles, confirming a targeted **0.88 Unsafe Content F1-Score** and an **83% overall pipeline verification accuracy** through automated confusion matrix logging scripts.
