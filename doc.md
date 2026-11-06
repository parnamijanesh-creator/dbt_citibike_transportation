# Master Sprint Curriculum & Concept Matrix

| Sprint | Concept Touched & Implemented | One-Sentence Architectural Role | dbt Certification Domain |
|---|---|---|---|
| **Sprint 0** | Business Problem Framing | Establishing explicit analytical questions, operational decisions, and target metrics before building. | Foundational Data Architecture |
| **Sprint 0** | Exploratory Data Analysis (EDA) | Profiling raw columns, data types, null counts, and edge cases directly in Snowflake. | Raw Object Dependencies |
| **Sprint 0** | Business-to-Technical Rules | Translating business definitions into deterministic SQL filtering criteria and boundaries. | Developing & Optimizing dbt Models |
| **Sprint 0** | Kimball Dimensional Modeling | Designing the star schema bus matrix, grain specifications, facts (fct_trips), and dimensions (dim_stations, dim_date). | Data Modeling & Architecture |
| **Sprint 1** | Sources & Raw Dependencies | Declaring raw tables in YAML to document lineage, define loaded timestamps, and track object dependencies. | Developing & Optimizing dbt Models |
| **Sprint 1** | Source Freshness | Configuring automated freshness thresholds in YAML to alert when raw ingestion falls behind expected schedules. | Implementing External Dependencies |
| **Sprint 1** | Staging Layer (Silver - 1:1 Views) | Cleaning raw string timestamps, casting coordinate floats, and standardizing column naming conventions as views. | Developing & Optimizing dbt Models |
| **Sprint 1** | Foundational DAG & ref() Mechanics | Connecting downstream models to upstream nodes using ref() to build a directed acyclic graph. | Creating a Logical Flow & Clean DAGs |
| **Sprint 1** | Core CLI (run, test, build, show) | Executing models, viewing preview results via show, and orchestrating end-to-end runs with build. | Using dbt Commands |
| **Sprint 1** | Generic Out-of-the-Box Tests | Asserting standard constraints (unique, not_null, accepted_values, relationships) across staging and marts. | Implementing dbt Tests |
| **Sprint 1** | Singular SQL Tests | Writing custom standalone SQL assertions to catch trips with negative durations or impossible end times. | Implementing dbt Tests |
| **Sprint 1** | Documentation & Lineage Graph | Generating and serving interactive documentation to inspect column descriptions and DAG flow visually. | Using dbt Commands & Docs |
| **Sprint 2** | Intermediate Layer Modeling | Isolating complex multi-table joins, station flow aggregations, and business logic into modular stepping stones. | Modularity & DRY Principles |
| **Sprint 2** | Jinja Expressions & Control Flow | Writing dynamic templating loops to eliminate repetitive SQL across ride types and membership classes. | Jinja & Macro Development |
| **Sprint 2** | Custom Macros | Packaging reusable SQL logic (such as the Haversine geographic distance formula) into modular functions. | Modularity & DRY Principles |
| **Sprint 2** | dbt Packages (dbt-utils, dbt-expectations) | Installing external ecosystem packages to generate surrogate keys, date spines, and distribution tests. | Using dbt Packages |
| **Sprint 2** | dbt Seeds | Managing version-controlled static lookup tables (such as NYC borough and neighborhood boundaries) directly in git. | Using dbt Commands & Seeds |
| **Sprint 2** | Custom Generic Tests | Authoring parameterized, reusable schema tests to validate latitude and longitude coordinate boundaries. | Implementing dbt Tests |
| **Sprint 2** | dbt Exposures | Declaring downstream analytics assets (e.g., Fleet Ops dashboard) in YAML to expose full dependency lineage. | Implementing External Dependencies |
| **Sprint 3** | Model Contracts (contract: enforced) | Locking down the schema shape, column names, and data types so downstream breaking changes halt compilation. | Managing dbt Models Governance |
| **Sprint 3** | Platform Constraints in YAML | Defining primary and foreign key constraints in dbt YAML that compile into native Snowflake DDL constraints. | Managing dbt Models Governance |
| **Sprint 3** | Model Versioning & Deprecation | Maintaining concurrent versions of models (v1 to v2) with configured deprecation dates for consumers. | Managing dbt Models Governance |
| **Sprint 3** | dbt Unit Testing | Validating complex intermediate business logic against mocked YAML inputs without querying Snowflake storage. | Implementing dbt Tests |
| **Sprint 3** | YAML & Compilation Debugging | Troubleshooting syntax errors, schema mismatches, and parsing issues using compiled SQL in /target. | Debugging Data Modeling Errors |
| **Sprint 3** | Access Grants Configuration | Managing object-level permissions programmatically across environments using the grants configuration block. | Managing dbt Models Governance |
| **Sprint 4** | Incremental Models (Merge Strategy) | Processing only new or updated ride batches using unique keys to optimize Snowflake compute costs. | Core & Advanced Materializations |
| **Sprint 4** | Snapshots (SCD Type 2) | Capturing historical station relocations and metadata changes over time using timestamp or check strategies. | Core & Advanced Materializations |
| **Sprint 4** | Microbatch Materialization | Batching large historical event-stream backfills into partitioned time windows to prevent warehouse memory spill. | Advanced Materializations |
| **Sprint 4** | Python Models (Snowpark) | Writing Python-based models directly inside the DAG to run statistical outlier detection on trip durations. | Creating Python Models |
| **Sprint 4** | Dry-Run & Sample Flags (--empty, --sample) | Validating DDL and contracts with zero data scanned using --empty, and testing logic fast using --sample. | Troubleshooting & Optimizing Pipelines |
| **Sprint 5** | Environment Isolation (dev vs prod) | Routing target schemas and configurations conditionally based on execution target and developer namespace. | Configurations in dbt_project.yml |
| **Sprint 5** | Snowflake Zero-Copy Cloning (dbt clone) | Instantly creating non-production sandbox environments from production tables without duplicating physical storage. | Troubleshooting & Optimizing Pipelines |
| **Sprint 5** | State Comparison & Slim CI (state:modified+) | Using manifest comparison to compile and test only models that have changed relative to the main branch. | Leveraging the dbt State |
| **Sprint 5** | Execution Recovery (dbt retry) | Resuming an interrupted or failed pipeline run directly from the point of failure without rerunning clean upstream models. | Leveraging the dbt State |
| **Sprint 5** | Pre-Hooks, Post-Hooks & Analyses | Automating Snowflake session audit tags via hooks and maintaining ad-hoc diagnostic SQL inside analyses/. | Developing & Optimizing dbt Models |