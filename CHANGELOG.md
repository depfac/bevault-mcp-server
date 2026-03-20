# Changelog

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
