# Changelog

## [5.0.0](https://github.com/depfac/bevault-mcp-server/compare/v4.0.2...v5.0.0) (2026-08-18)


### ⚠ BREAKING CHANGES

* **model:** create/update hub and link tools now require `businessName`; satellite mapping create/update requires `satelliteBusinessName`. Requires beVault 3.12+. Technical names are validated locally.

### Features

* **model:** require business names for hubs, links, and satellites ([c659356](https://github.com/depfac/bevault-mcp-server/commit/c659356bee75fa7fe97fa5d63f6f54efc8309c30))
* **staging-tables:** require scale and precision for numeric columns of staging tables ([a34cc8b](https://github.com/depfac/bevault-mcp-server/commit/a34cc8b3a01b2e794c949148a56dc301fee57b9d))

## [4.0.2](https://github.com/depfac/bevault-mcp-server/compare/v4.0.1...v4.0.2) (2026-07-23)


### Bug Fixes

* **projects:** increase the limit of projects returned ([eaccef3](https://github.com/depfac/bevault-mcp-server/commit/eaccef3b285276e5f9742e06281b6225ba00e62d))

## [4.0.1](https://github.com/depfac/bevault-mcp-server/compare/v4.0.0...v4.0.1) (2026-07-10)


### Bug Fixes

* **auth:** default OIDC required scopes to openid,profile ([284ca57](https://github.com/depfac/bevault-mcp-server/commit/284ca5781601179a05f1078bfb12ef3c4e62381e))
* **states:** coerce malformed defaultInput strings in API responses ([066b6b7](https://github.com/depfac/bevault-mcp-server/commit/066b6b76ff18c87b3868ef049e45e3d8dbbeccf6))

## [4.0.0](https://github.com/depfac/bevault-mcp-server/compare/v3.0.0...v4.0.0) (2026-07-02)


### ⚠ BREAKING CHANGES

* **states:** integrate States module with MCP tools

### Features

* **states:** integrate States module with MCP tools ([26f5643](https://github.com/depfac/bevault-mcp-server/commit/26f5643ed3cd17e39141ff4d14b6c1163dbdf996))
Add optional beVault States integration behind STATES_ENABLED, with OIDC-backed API client, Pydantic models, and conditional tool registration alongside MetaVault.

MCP tools:
* State machines: list, get, create, update, delete
* Executions: list, get, start
* Activities: get_activities
* Stores: get_stores

## [3.0.0](https://github.com/depfac/bevault-mcp-server/compare/v2.3.0...v3.0.0) (2026-05-06)


### ⚠ BREAKING CHANGES

* **source-systems:** search_source_systems now requires Metavault API 5.3.0 (beVault 3.9.6) or newer. Earlier releases do not expose the datapackage table list endpoint used for staging metadata.

### Performance Improvements

* **source-systems:** batch staging tables in search_source_systems ([9005ea1](https://github.com/depfac/bevault-mcp-server/commit/9005ea14fb1232105240dab4efec01ca4903a1c3))

## [2.3.0](https://github.com/depfac/bevault-mcp-server/compare/v2.2.0...v2.3.0) (2026-03-20)


### Features

* **tools:** add optional embedded satellites to get_hub and get_link ([84b7f6a](https://github.com/depfac/bevault-mcp-server/commit/84b7f6acd42715950dac64481c0c645bca736df1))
* **tools:** add pit table support for hubs and links ([eb02829](https://github.com/depfac/bevault-mcp-server/commit/eb02829b1cfe3700d30c77076dbcb08b13ad2ae8))


### Bug Fixes

* **main:** handle Ctrl+C for clean server shutdown ([ed65300](https://github.com/depfac/bevault-mcp-server/commit/ed65300d4b7ead627d32eef032ff82377a660b12))
* **tools:** make searchString optional in search_model ([dbac9b5](https://github.com/depfac/bevault-mcp-server/commit/dbac9b556f6571d9dbde2e7b7a0ba400030be4b2))

## [2.2.0](https://github.com/depfac/bevault-mcp-server/compare/v2.1.0...v2.2.0) (2026-03-04)


### Features

* add support for OIDC authentication ([7a971dc](https://github.com/depfac/bevault-mcp-server/commit/7a971dcf4709c50c91ea1565c228a657829225d5))

## [2.1.0](https://github.com/depfac/bevault-mcp-server/compare/v2.0.0...v2.1.0) (2026-02-27)


### Features

* add support for OpenTelemetry ([1067b3e](https://github.com/depfac/bevault-mcp-server/commit/1067b3e160aad082dbd1b75129e0af4dc21e9023))
* add support for Sentry ([75c20c9](https://github.com/depfac/bevault-mcp-server/commit/75c20c9b251a4578cda2d07c8fd95e89c0ca3107))
* add tool to delete a staging table ([118824b](https://github.com/depfac/bevault-mcp-server/commit/118824b17691b83ea1be198b97fda95eb947cc8b))
* **tools:** add get_projects tool to list available projects ([28bd6c6](https://github.com/depfac/bevault-mcp-server/commit/28bd6c65b0e20a4bd19f3912848baa04ddb939b9))


### Bug Fixes

* improve tool description to reduce errors when deleting objects ([4e422cb](https://github.com/depfac/bevault-mcp-server/commit/4e422cb8ce7ed32c2cf9fcad315543f56b09377a))

## [2.0.0](https://github.com/depfac/bevault-mcp-server/compare/v1.0.0...v2.0.0) (2026-02-26)


### ⚠ BREAKING CHANGES

* Replace Authorization header with bevault-api-key for beVault API token in your AI agent (see v1.1.0 migration note in README)

### Features

* migrate to FastMCP v3 and switch to bevault-api-key header ([fad345f](https://github.com/depfac/bevault-mcp-server/commit/fad345fb87c4b17e7c3b10ab705de0f128e6f272))
