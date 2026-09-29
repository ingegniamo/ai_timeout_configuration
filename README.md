# AI Timeout Configuration

[![License: OPL-1](https://img.shields.io/badge/licence-OPL--1-F1972B)](https://www.odoo.com/documentation/user/19.0/legal/licenses/licenses.html)
[![Odoo](https://img.shields.io/badge/Odoo-19.0-F1972B)](https://www.odoo.com)
[![Maintained by STeSI](https://img.shields.io/badge/maintained%20by-STeSI%20Consulting-F1972B)](https://stesi.consulting)

Sets the read timeout of AI provider requests with a system parameter.

## The Problem

`LLMApiService._request` in the `ai` module declares `timeout=30`, and the Gemini
and OpenAI calls do not override it. A slow answer (large prompt, tool calls)
ends with:

```
UserError: ReadTimeout(ReadTimeoutError("HTTPSConnectionPool(host='generativelanguage.googleapis.com', port=443): Read timed out. (read timeout=30)"))
```

Enterprise code is read-only and `LLMApiService` is a plain class, so `_inherit`
cannot reach it.

## The Fix

The module wraps `LLMApiService._request`. When the caller passes no `timeout`,
the wrapper reads the system parameter and passes it on. A caller that sets its
own `timeout` (audio transcription uses 550) keeps that value.

## Configuration

| System parameter | Default | Meaning |
|------------------|---------|---------|
| `ai.request_timeout` | `120` | Read timeout in seconds. An empty or non-numeric value falls back to the default. |

Set it in Settings > Technical > System Parameters. The value takes effect on
the next request, with no restart.

A long timeout keeps the HTTP worker busy for the whole wait.

## Dependencies

- `ai` (Odoo Enterprise)

## Credits

Authors: STeSI Consulting

Contributors: Michele Di Croce — dicroce.m@stesi.consulting

## Changelog

### 19.0.1.0.0
- Initial release: AI provider request timeout read from `ai.request_timeout`,
  default 120 seconds instead of 30.
