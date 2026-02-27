# Changelog

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
