Run ruff check backend --output-format=github
warning: The top-level linter settings are deprecated in favour of their counterparts in the `lint` section. Please update the following options in `pyproject.toml`:
  - 'ignore' -> 'lint.ignore'
  - 'select' -> 'lint.select'
  - 'per-file-ignores' -> 'lint.per-file-ignores'
Error: backend/alembic/env.py:7:1: I001 Import block is un-sorted or un-formatted
Error: backend/alembic/env.py:19:24: F401 `app.models.Asset` imported but unused
Error: backend/alembic/env.py:19:31: F401 `app.models.GenerationLog` imported but unused
Error: backend/alembic/env.py:19:46: F401 `app.models.Project` imported but unused
Error: backend/alembic/env.py:19:55: F401 `app.models.Scene` imported but unused
Error: backend/alembic/env.py:45:1: W293 Blank line contains whitespace
Error: backend/alembic/env.py:82:1: W293 Blank line contains whitespace
Error: backend/alembic/env.py:91:35: W291 Trailing whitespace
Error: backend/alembic/env.py:102:28: W292 No newline at end of file
Error: backend/app/config.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/config.py:16:1: W293 Blank line contains whitespace
Error: backend/app/config.py:21:1: W293 Blank line contains whitespace
Error: backend/app/config.py:24:1: W293 Blank line contains whitespace
Error: backend/app/config.py:31:1: W293 Blank line contains whitespace
Error: backend/app/config.py:36:1: W293 Blank line contains whitespace
Error: backend/app/config.py:39:1: W293 Blank line contains whitespace
Error: backend/app/config.py:41:21: UP007 Use `X | Y` for type annotations
Error: backend/app/config.py:44:1: W293 Blank line contains whitespace
Error: backend/app/config.py:50:1: W293 Blank line contains whitespace
Error: backend/app/config.py:53:1: W293 Blank line contains whitespace
Error: backend/app/config.py:57:1: W293 Blank line contains whitespace
Error: backend/app/config.py:61:69: W291 Trailing whitespace
Error: backend/app/config.py:67:22: W292 No newline at end of file
Error: backend/app/database.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/database.py:7:1: UP035 Import from `collections.abc` instead: `Generator`
Error: backend/app/database.py:51:23: F401 `.models` imported but unused
Error: backend/app/database.py:52:1: W293 Blank line contains whitespace
Error: backend/app/database.py:73:21: W292 No newline at end of file
Error: backend/app/main.py:5:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/main.py:22:20: ARG001 Unused function argument: `app`
Error: backend/app/main.py:30:1: W293 Blank line contains whitespace
Error: backend/app/main.py:41:1: W293 Blank line contains whitespace
Error: backend/app/main.py:82:66: W292 No newline at end of file
Error: backend/app/routers/__init__.py:3:4: W292 No newline at end of file
Error: backend/app/routers/assets.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/routers/assets.py:6:1: UP035 `typing.List` is deprecated, use `list` instead
Error: backend/app/routers/assets.py:26:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:28:14: UP015 Unnecessary open mode parameters
Error: backend/app/routers/assets.py:38:5: ARG001 Unused function argument: `tags`
Error: backend/app/routers/assets.py:38:11: UP007 Use `X | Y` for type annotations
Error: backend/app/routers/assets.py:38:20: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/routers/assets.py:42:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:49:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:53:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:60:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:78:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:88:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:98:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:100:9: F841 Local variable `storage_path` is assigned to but never used
Error: backend/app/routers/assets.py:106:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:112:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:114:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:120:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:123:9: B904 Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to distinguish them from errors in exception handling
Error: backend/app/routers/assets.py:128:61: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/routers/assets.py:140:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:172:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:177:1: W293 Blank line contains whitespace
Error: backend/app/routers/assets.py:189:6: W292 No newline at end of file
Error: backend/app/routers/export.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/routers/export.py:23:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:25:14: UP015 Unnecessary open mode parameters
Error: backend/app/routers/export.py:31:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:74:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:78:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:85:47: W291 Trailing whitespace
Error: backend/app/routers/export.py:91:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:103:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:106:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:112:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:124:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:130:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:133:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:153:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:162:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:166:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:173:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:199:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:203:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:232:1: W293 Blank line contains whitespace
Error: backend/app/routers/export.py:234:81: W292 No newline at end of file
Error: backend/app/routers/generation.py:11:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/routers/generation.py:13:8: F401 `json` imported but unused
Error: backend/app/routers/generation.py:17:1: UP035 `typing.List` is deprecated, use `list` instead
Error: backend/app/routers/generation.py:17:1: UP035 `typing.Dict` is deprecated, use `dict` instead
Error: backend/app/routers/generation.py:17:30: F401 `typing.List` imported but unused
Error: backend/app/routers/generation.py:19:22: F401 `datetime.datetime` imported but unused
Error: backend/app/routers/generation.py:19:32: F401 `datetime.timezone` imported but unused
Error: backend/app/routers/generation.py:22:22: F401 `..config.settings` imported but unused
Error: backend/app/routers/generation.py:41:22: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/routers/generation.py:42:23: UP007 Use `X | Y` for type annotations
Error: backend/app/routers/generation.py:42:32: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/routers/generation.py:43:12: UP007 Use `X | Y` for type annotations
Error: backend/app/routers/generation.py:47:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:83:17: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/routers/generation.py:84:24: UP007 Use `X | Y` for type annotations
Error: backend/app/routers/generation.py:88:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:119:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:128:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:131:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:137:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:141:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:150:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:158:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:165:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:173:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:177:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:180:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:183:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:198:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:207:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:222:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:226:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:240:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:241:9: B904 Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to distinguish them from errors in exception handling
Error: backend/app/routers/generation.py:251:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:264:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:277:1: W293 Blank line contains whitespace
Error: backend/app/routers/generation.py:287:18: W292 No newline at end of file
Error: backend/app/routers/health.py:6:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/routers/health.py:9:1: UP035 `typing.Dict` is deprecated, use `dict` instead
Error: backend/app/routers/health.py:17:33: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/routers/health.py:21:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:31:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:46:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:66:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:72:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:76:38: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/routers/health.py:80:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:87:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:90:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:92:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:95:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:99:37: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/routers/health.py:103:1: W293 Blank line contains whitespace
Error: backend/app/routers/health.py:107:27: W292 No newline at end of file
Error: backend/app/routers/projects.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/routers/projects.py:5:1: UP035 `typing.List` is deprecated, use `list` instead
Error: backend/app/routers/projects.py:22:1: W293 Blank line contains whitespace
Error: backend/app/routers/projects.py:24:14: UP015 Unnecessary open mode parameters
Error: backend/app/routers/projects.py:28:33: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/routers/projects.py:34:1: W293 Blank line contains whitespace
Error: backend/app/routers/projects.py:54:1: W293 Blank line contains whitespace
Error: backend/app/routers/projects.py:68:1: W293 Blank line contains whitespace
Error: backend/app/routers/projects.py:70:81: W292 No newline at end of file
Error: backend/app/schemas/__init__.py:3:4: W292 No newline at end of file
Error: backend/app/schemas/asset.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/schemas/asset.py:5:1: UP035 `typing.Dict` is deprecated, use `dict` instead
Error: backend/app/schemas/asset.py:40:15: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/asset.py:40:24: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/schemas/asset.py:44:1: W293 Blank line contains whitespace
Error: backend/app/schemas/asset.py:50:9: W292 No newline at end of file
Error: backend/app/schemas/export.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/schemas/export.py:16:87: W292 No newline at end of file
Error: backend/app/schemas/generation.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/schemas/generation.py:5:1: UP035 `typing.List` is deprecated, use `list` instead
Error: backend/app/schemas/generation.py:5:1: UP035 `typing.Dict` is deprecated, use `dict` instead
Error: backend/app/schemas/generation.py:36:14: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:37:16: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:38:13: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:39:11: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:48:13: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:49:12: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:50:14: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:51:17: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:51:26: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/schemas/generation.py:58:12: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:59:18: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:59:27: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/schemas/generation.py:69:15: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/schemas/generation.py:76:13: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:76:22: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/schemas/generation.py:77:12: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/generation.py:83:82: W292 No newline at end of file
Error: backend/app/schemas/project.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/schemas/project.py:10:18: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/project.py:18:11: UP007 Use `X | Y` for type annotations
Error: backend/app/schemas/project.py:28:1: W293 Blank line contains whitespace
Error: backend/app/schemas/project.py:34:9: W292 No newline at end of file
Error: backend/app/services/__init__.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/services/__init__.py:14:2: W292 No newline at end of file
Error: backend/app/services/asset_service.py:10:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/services/asset_service.py:13:8: F401 `os` imported but unused
Error: backend/app/services/asset_service.py:16:8: F401 `uuid` imported but unused
Error: backend/app/services/asset_service.py:18:1: UP035 `typing.Dict` is deprecated, use `dict` instead
Error: backend/app/services/asset_service.py:18:26: F401 `typing.Any` imported but unused
Error: backend/app/services/asset_service.py:19:24: F401 `PIL.ImageOps` imported but unused
Error: backend/app/services/asset_service.py:39:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:46:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:55:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:58:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:73:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:77:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:104:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:110:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:117:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:125:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:129:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:137:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:142:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:145:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:157:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:161:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:168:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:176:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:189:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:197:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:199:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:218:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:230:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:234:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:236:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:239:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:249:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:258:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:264:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:270:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:279:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:287:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:295:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:299:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:301:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:313:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:318:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:322:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:324:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:330:52: UP007 Use `X | Y` for type annotations
Error: backend/app/services/asset_service.py:333:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:337:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:347:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:351:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:358:76: UP007 Use `X | Y` for type annotations
Error: backend/app/services/asset_service.py:358:85: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/asset_service.py:361:1: W293 Blank line contains whitespace
Error: backend/app/services/asset_service.py:374:68: W292 No newline at end of file
Error: backend/app/services/context_builder.py:8:1: UP035 `typing.Dict` is deprecated, use `dict` instead
Error: backend/app/services/context_builder.py:8:1: UP035 `typing.List` is deprecated, use `list` instead
Error: backend/app/services/context_builder.py:8:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/services/context_builder.py:15:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:19:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:24:17: UP007 Use `X | Y` for type annotations
Error: backend/app/services/context_builder.py:24:26: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/services/context_builder.py:24:31: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:25:16: UP007 Use `X | Y` for type annotations
Error: backend/app/services/context_builder.py:26:29: UP007 Use `X | Y` for type annotations
Error: backend/app/services/context_builder.py:26:38: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:27:10: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:30:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:37:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:48:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:53:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:57:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:60:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:63:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:65:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:69:24: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:70:24: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:71:10: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:74:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:79:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:90:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:91:41: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:94:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:97:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:107:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:108:39: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/services/context_builder.py:108:44: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:108:64: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/services/context_builder.py:108:69: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:119:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:120:52: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:120:71: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:124:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:125:59: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:129:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:131:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:134:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:136:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:138:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:139:46: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/context_builder.py:147:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:149:1: W293 Blank line contains whitespace
Error: backend/app/services/context_builder.py:157:35: W292 No newline at end of file
Error: backend/app/services/inference_client.py:14:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/services/inference_client.py:18:8: F401 `hashlib` imported but unused
Error: backend/app/services/inference_client.py:20:8: F401 `asyncio` imported but unused
Error: backend/app/services/inference_client.py:21:1: UP035 `typing.Dict` is deprecated, use `dict` instead
Error: backend/app/services/inference_client.py:21:1: UP035 `typing.List` is deprecated, use `list` instead
Error: backend/app/services/inference_client.py:21:1: UP035 `typing.Tuple` is deprecated, use `tuple` instead
Error: backend/app/services/inference_client.py:30:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:36:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:41:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:50:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:54:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:83:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:87:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:90:26: UP015 Unnecessary open mode parameters
Error: backend/app/services/inference_client.py:92:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:113:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:116:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:121:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:127:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:130:18: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:131:24: UP007 Use `X | Y` for type annotations
Error: backend/app/services/inference_client.py:132:10: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:135:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:139:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:146:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:150:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:170:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:172:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:181:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:184:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:187:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:192:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:197:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:210:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:213:18: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:214:24: UP007 Use `X | Y` for type annotations
Error: backend/app/services/inference_client.py:215:10: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:218:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:224:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:227:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:243:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:252:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:256:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:259:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:261:13: B904 Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to distinguish them from errors in exception handling
Error: backend/app/services/inference_client.py:263:13: B904 Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to distinguish them from errors in exception handling
Error: backend/app/services/inference_client.py:265:13: B904 Within an `except` clause, raise exceptions with `raise ... from err` or `raise ... from None` to distinguish them from errors in exception handling
Error: backend/app/services/inference_client.py:266:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:267:45: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:267:64: UP006 Use `tuple` instead of `Tuple` for type annotation
Error: backend/app/services/inference_client.py:267:70: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:270:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:277:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:279:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:289:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:295:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:297:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:300:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:314:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:316:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:317:44: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:355:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:356:35: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:375:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:387:13: E722 Do not use bare `except`
Error: backend/app/services/inference_client.py:389:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:391:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:392:55: UP007 Use `X | Y` for type annotations
Error: backend/app/services/inference_client.py:392:64: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:395:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:398:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:406:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:407:38: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/services/inference_client.py:407:43: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/inference_client.py:410:1: W293 Blank line contains whitespace
Error: backend/app/services/inference_client.py:426:37: W292 No newline at end of file
Error: backend/app/services/postprocessor.py:7:1: UP035 `typing.Dict` is deprecated, use `dict` instead
Error: backend/app/services/postprocessor.py:7:1: UP035 `typing.List` is deprecated, use `list` instead
Error: backend/app/services/postprocessor.py:7:1: UP035 `typing.Tuple` is deprecated, use `tuple` instead
Error: backend/app/services/postprocessor.py:7:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/services/postprocessor.py:7:47: F401 `typing.Tuple` imported but unused
Error: backend/app/services/postprocessor.py:14:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:18:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:21:20: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:23:17: UP007 Use `X | Y` for type annotations
Error: backend/app/services/postprocessor.py:23:26: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/services/postprocessor.py:23:31: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:24:10: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:27:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:32:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:38:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:43:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:47:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:50:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:55:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:57:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:58:37: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:61:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:64:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:72:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:76:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:77:9: SIM110 Use `return all(self._validate_entity(entity) for entity in scene["entities"])` instead of `for` loop
Error: backend/app/services/postprocessor.py:80:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:82:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:85:16: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:86:23: UP007 Use `X | Y` for type annotations
Error: backend/app/services/postprocessor.py:86:32: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:87:10: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:90:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:94:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:99:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:104:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:111:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:113:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:116:16: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:118:10: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:122:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:125:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:128:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:131:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:134:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:136:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:137:43: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/services/postprocessor.py:137:48: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:137:68: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/services/postprocessor.py:137:73: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:140:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:145:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:148:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:154:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:160:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:168:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:170:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:172:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:173:40: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:178:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:183:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:188:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:190:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:191:53: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:205:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:206:45: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:214:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:215:54: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:225:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:229:21: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:230:10: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:234:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:238:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:241:16: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:242:17: UP006 Use `list` instead of `List` for type annotation
Error: backend/app/services/postprocessor.py:242:22: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:243:10: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:247:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:255:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:261:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:263:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:264:41: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:264:60: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:273:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:274:57: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:297:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:298:46: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:298:65: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:304:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:315:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:316:48: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:316:67: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:325:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:326:49: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:326:68: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:331:17: B007 Loop control variable `j` not used within loop body
Error: backend/app/services/postprocessor.py:336:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:337:37: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:337:57: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:346:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:347:43: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:347:62: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:354:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:355:38: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:355:57: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:362:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:363:47: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:371:1: W293 Blank line contains whitespace
Error: backend/app/services/postprocessor.py:372:49: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:372:59: UP006 Use `dict` instead of `Dict` for type annotation
Error: backend/app/services/postprocessor.py:384:32: W292 No newline at end of file
Error: backend/app/storage.py:7:1: I001 Import block is un-sorted or un-formatted
Error: backend/app/storage.py:22:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:27:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:33:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:40:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:42:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:59:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:66:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:72:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:77:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:86:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:89:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:101:6: UP007 Use `X | Y` for type annotations
Error: backend/app/storage.py:104:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:108:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:114:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:120:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:123:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:138:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:142:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:151:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:164:6: UP007 Use `X | Y` for type annotations
Error: backend/app/storage.py:167:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:172:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:184:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:195:13: UP007 Use `X | Y` for type annotations
Error: backend/app/storage.py:199:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:203:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:214:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:216:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:228:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:236:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:242:1: W293 Blank line contains whitespace
Error: backend/app/storage.py:248:10: W292 No newline at end of file
Error: backend/scripts/test_database.py:7:1: I001 Import block is un-sorted or un-formatted
Error: backend/scripts/test_database.py:8:8: F401 `os` imported but unused
Error: backend/scripts/test_database.py:11:1: I001 Import block is un-sorted or un-formatted
Error: backend/scripts/test_database.py:11:33: F401 `sqlalchemy.text` imported but unused
Error: backend/scripts/test_database.py:25:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:39:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:42:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:44:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:52:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:57:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:66:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:68:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:71:77: W291 Trailing whitespace
Error: backend/scripts/test_database.py:73:74: W291 Trailing whitespace
Error: backend/scripts/test_database.py:74:70: W291 Trailing whitespace
Error: backend/scripts/test_database.py:76:69: W291 Trailing whitespace
Error: backend/scripts/test_database.py:78:70: W291 Trailing whitespace
Error: backend/scripts/test_database.py:81:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:85:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:88:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:96:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:101:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:105:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:114:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:116:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:127:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:139:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:152:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:163:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:169:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:170:15: F541 f-string without any placeholders
Error: backend/scripts/test_database.py:175:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:183:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:185:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:200:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:207:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:212:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:219:1: W293 Blank line contains whitespace
Error: backend/scripts/test_database.py:230:24: W292 No newline at end of file
Error: backend/scripts/verify_task_2.1.py:7:1: I001 Import block is un-sorted or un-formatted
Error: backend/scripts/verify_task_2.1.py:10:24: F401 `PIL.ExifTags` imported but unused
Error: backend/scripts/verify_task_2.1.py:12:8: F401 `json` imported but unused
Error: backend/scripts/verify_task_2.1.py:22:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:25:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:31:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:35:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:40:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:45:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:47:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:53:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:58:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:65:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:76:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:78:1: I001 Import block is un-sorted or un-formatted
Error: backend/scripts/verify_task_2.1.py:80:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:82:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:89:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:95:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:103:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:111:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:122:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:124:1: I001 Import block is un-sorted or un-formatted
Error: backend/scripts/verify_task_2.1.py:126:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:129:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:135:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:136:15: F541 f-string without any placeholders
Error: backend/scripts/verify_task_2.1.py:138:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:145:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:156:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:164:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:173:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:178:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:187:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:189:1: I001 Import block is un-sorted or un-formatted
Error: backend/scripts/verify_task_2.1.py:191:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:196:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:198:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:208:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:211:38: ARG005 Unused lambda argument: `x`
Error: backend/scripts/verify_task_2.1.py:212:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:215:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:222:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:225:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:228:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:240:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:248:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:253:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:260:1: W293 Blank line contains whitespace
Error: backend/scripts/verify_task_2.1.py:281:21: W292 No newline at end of file
Error: backend/setup.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/setup.py:26:2: W292 No newline at end of file
Error: backend/tests/backend/integration/test_api_integration.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/integration/test_api_integration.py:5:32: F401 `fastapi.testclient.TestClient` imported but unused
Error: backend/tests/backend/integration/test_api_integration.py:6:34: F401 `unittest.mock.Mock` imported but unused
Error: backend/tests/backend/integration/test_api_integration.py:7:8: F401 `json` imported but unused
Error: backend/tests/backend/integration/test_api_integration.py:12:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:16:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:19:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:24:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:31:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:35:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:38:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:43:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:47:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:51:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:54:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:58:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:62:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:68:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:78:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:81:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:87:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:91:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:96:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:100:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:105:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:116:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:120:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:123:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:127:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:130:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:139:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:140:60: ARG002 Unused method argument: `test_db_session`
Error: backend/tests/backend/integration/test_api_integration.py:145:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:149:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:159:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:164:9: F841 Local variable `data` is assigned to but never used
Error: backend/tests/backend/integration/test_api_integration.py:165:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:169:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:174:9: F841 Local variable `data` is assigned to but never used
Error: backend/tests/backend/integration/test_api_integration.py:175:1: W293 Blank line contains whitespace
Error: backend/tests/backend/integration/test_api_integration.py:176:43: W292 No newline at end of file
Error: backend/tests/backend/run_all_tests.py:5:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/run_all_tests.py:6:8: F401 `os` imported but unused
Error: backend/tests/backend/run_all_tests.py:14:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:15:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/run_all_tests.py:22:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:25:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:33:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:41:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:49:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:57:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:65:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:74:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:77:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:81:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:87:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:104:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:107:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/run_all_tests.py:108:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:111:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:123:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:126:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/run_all_tests.py:130:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:133:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:136:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:139:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:150:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:154:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:156:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:165:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:174:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:175:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/run_all_tests.py:177:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:181:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:193:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:205:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:215:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:228:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:237:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:238:12: F811 Redefinition of unused `os` from line 6
Error: backend/tests/backend/run_all_tests.py:240:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:241:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/run_all_tests.py:244:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:247:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:251:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:266:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:282:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:300:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:316:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:329:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:338:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:341:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:346:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:351:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:356:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:361:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:370:1: W293 Blank line contains whitespace
Error: backend/tests/backend/run_all_tests.py:381:24: W292 No newline at end of file
Error: backend/tests/backend/test_health.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/test_health.py:4:8: F401 `pytest` imported but unused
Error: backend/tests/backend/test_health.py:11:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_health.py:23:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_health.py:34:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_health.py:44:82: W292 No newline at end of file
Error: backend/tests/backend/test_routers.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/test_routers.py:4:8: F401 `pytest` imported but unused
Error: backend/tests/backend/test_routers.py:6:34: F401 `unittest.mock.MagicMock` imported but unused
Error: backend/tests/backend/test_routers.py:7:8: F401 `json` imported but unused
Error: backend/tests/backend/test_routers.py:8:21: F401 `pathlib.Path` imported but unused
Error: backend/tests/backend/test_routers.py:11:32: F401 `backend.app.config.settings` imported but unused
Error: backend/tests/backend/test_routers.py:18:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:33:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:52:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:59:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:67:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:75:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:94:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:99:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:105:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:112:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:123:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:133:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:143:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:151:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:172:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:178:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:199:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:208:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:232:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:237:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:245:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:269:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:275:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:287:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:295:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:300:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:308:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:313:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:321:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:329:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:335:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_routers.py:343:42: W292 No newline at end of file
Error: backend/tests/backend/test_schemas.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/test_schemas.py:6:22: F401 `datetime.datetime` imported but unused
Error: backend/tests/backend/test_schemas.py:13:51: W291 Trailing whitespace
Error: backend/tests/backend/test_schemas.py:14:20: F401 `backend.app.schemas.generation.Scene` imported but unused
Error: backend/tests/backend/test_schemas.py:21:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:31:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:38:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:43:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:46:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:63:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:74:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:81:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:87:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:98:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:122:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:129:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:138:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:144:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:150:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:174:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:188:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:200:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:206:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:210:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:238:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:244:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:254:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_schemas.py:260:63: W292 No newline at end of file
Error: backend/tests/backend/test_services.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/test_services.py:5:21: F401 `pathlib.Path` imported but unused
Error: backend/tests/backend/test_services.py:7:34: F401 `unittest.mock.MagicMock` imported but unused
Error: backend/tests/backend/test_services.py:14:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:23:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:30:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:36:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:48:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:56:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:59:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:60:9: SIM117 Use a single `with` statement with multiple contexts instead of nested `with` statements
Error: backend/tests/backend/test_services.py:66:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:70:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:74:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:85:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:87:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:88:9: SIM117 Use a single `with` statement with multiple contexts instead of nested `with` statements
Error: backend/tests/backend/test_services.py:97:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:101:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:122:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:126:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:130:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:134:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:143:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:147:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:150:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:154:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:157:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:160:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/test_services.py:162:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:165:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:172:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:178:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:182:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:185:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:196:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:200:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:202:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_services.py:209:39: W292 No newline at end of file
Error: backend/tests/backend/test_simple_imports.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/test_simple_imports.py:10:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/test_simple_imports.py:14:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:23:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:30:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/test_simple_imports.py:31:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:41:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:48:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:50:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:59:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:62:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:65:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:68:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:71:1: W293 Blank line contains whitespace
Error: backend/tests/backend/test_simple_imports.py:72:42: W292 No newline at end of file
Error: backend/tests/backend/unit/test_config.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/unit/test_config.py:5:8: F401 `pytest` imported but unused
Error: backend/tests/backend/unit/test_config.py:6:34: F401 `unittest.mock.MagicMock` imported but unused
Error: backend/tests/backend/unit/test_config.py:17:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:21:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:24:34: E712 Comparison to `False` should be `cond is False` or `if not cond:`
Error: backend/tests/backend/unit/test_config.py:26:38: E712 Comparison to `False` should be `cond is False` or `if not cond:`
Error: backend/tests/backend/unit/test_config.py:27:44: E712 Comparison to `False` should be `cond is False` or `if not cond:`
Error: backend/tests/backend/unit/test_config.py:28:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:33:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:37:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:41:41: E712 Comparison to `False` should be `cond is False` or `if not cond:`
Error: backend/tests/backend/unit/test_config.py:43:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:47:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:51:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:55:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:58:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:62:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:68:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:73:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:74:38: E712 Comparison to `True` should be `cond is True` or `if cond:`
Error: backend/tests/backend/unit/test_config.py:75:44: E712 Comparison to `True` should be `cond is True` or `if cond:`
Error: backend/tests/backend/unit/test_config.py:76:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:81:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:83:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:88:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:90:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:94:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:98:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:102:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_config.py:103:68: W292 No newline at end of file
Error: backend/tests/backend/unit/test_database.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/unit/test_database.py:5:40: F401 `unittest.mock.MagicMock` imported but unused
Error: backend/tests/backend/unit/test_database.py:13:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/unit/test_database.py:18:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:24:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:27:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:30:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:33:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:35:13: SIM105 Use `contextlib.suppress(StopIteration)` instead of `try`-`except`-`pass`
Error: backend/tests/backend/unit/test_database.py:39:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:42:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:48:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:50:13: F841 Local variable `session` is assigned to but never used
Error: backend/tests/backend/unit/test_database.py:51:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:53:18: B017 `pytest.raises(Exception)` should be considered evil
Error: backend/tests/backend/unit/test_database.py:55:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:58:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:64:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:67:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:70:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:76:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:79:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:82:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:89:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:91:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:92:26: E712 Comparison to `True` should be `cond is True` or `if cond:`
Error: backend/tests/backend/unit/test_database.py:96:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:104:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:106:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:107:26: E712 Comparison to `False` should be `cond is False` or `if not cond:`
Error: backend/tests/backend/unit/test_database.py:110:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:115:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:119:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_database.py:122:40: W292 No newline at end of file
Error: backend/tests/backend/unit/test_main.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/backend/unit/test_main.py:5:34: F401 `unittest.mock.AsyncMock` imported but unused
Error: backend/tests/backend/unit/test_main.py:5:45: F401 `unittest.mock.MagicMock` imported but unused
Error: backend/tests/backend/unit/test_main.py:18:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:25:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:37:74: E712 Comparison to `True` should be `cond is True` or `if cond:`
Error: backend/tests/backend/unit/test_main.py:41:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:43:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:54:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:61:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:64:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:69:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:78:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:82:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:87:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:90:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:94:37: E712 Comparison to `True` should be `cond is True` or `if cond:`
Error: backend/tests/backend/unit/test_main.py:95:43: E712 Comparison to `False` should be `cond is False` or `if not cond:`
Error: backend/tests/backend/unit/test_main.py:96:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:101:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:104:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:105:37: E712 Comparison to `False` should be `cond is False` or `if not cond:`
Error: backend/tests/backend/unit/test_main.py:106:43: E712 Comparison to `True` should be `cond is True` or `if cond:`
Error: backend/tests/backend/unit/test_main.py:111:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:115:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:119:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:122:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:127:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:132:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:140:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:144:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:148:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:151:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:157:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:161:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:164:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:168:1: W293 Blank line contains whitespace
Error: backend/tests/backend/unit/test_main.py:170:48: W292 No newline at end of file
Error: backend/tests/conftest.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/conftest.py:6:1: UP035 Import from `collections.abc` instead: `Generator`, `AsyncGenerator`
Error: backend/tests/conftest.py:6:31: F401 `typing.AsyncGenerator` imported but unused
Error: backend/tests/conftest.py:14:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/conftest.py:70:1: W293 Blank line contains whitespace
Error: backend/tests/conftest.py:88:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/conftest.py:90:1: W293 Blank line contains whitespace
Error: backend/tests/conftest.py:96:1: W293 Blank line contains whitespace
Error: backend/tests/conftest.py:107:17: F821 Undefined name `BytesIO`
Error: backend/tests/conftest.py:130:1: W293 Blank line contains whitespace
Error: backend/tests/conftest.py:136:1: W293 Blank line contains whitespace
Error: backend/tests/conftest.py:138:1: W293 Blank line contains whitespace
Error: backend/tests/conftest.py:141:1: W293 Blank line contains whitespace
Error: backend/tests/conftest.py:142:37: W292 No newline at end of file
Error: backend/tests/test_simple.py:4:1: I001 Import block is un-sorted or un-formatted
Error: backend/tests/test_simple.py:6:8: F401 `pytest` imported but unused
Error: backend/tests/test_simple.py:14:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:20:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:26:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:32:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:37:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:40:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:46:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:50:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:56:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:61:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:63:14: UP015 Unnecessary open mode parameters
Error: backend/tests/test_simple.py:67:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:72:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:74:14: UP015 Unnecessary open mode parameters
Error: backend/tests/test_simple.py:77:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:82:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:85:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:88:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:93:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:95:14: UP015 Unnecessary open mode parameters
Error: backend/tests/test_simple.py:100:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:105:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:110:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:112:14: UP015 Unnecessary open mode parameters
Error: backend/tests/test_simple.py:121:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:126:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:131:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:136:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:141:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:147:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:155:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:160:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:162:14: UP015 Unnecessary open mode parameters
Error: backend/tests/test_simple.py:166:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:171:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:173:14: UP015 Unnecessary open mode parameters
Error: backend/tests/test_simple.py:177:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:182:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:184:14: UP015 Unnecessary open mode parameters
Error: backend/tests/test_simple.py:188:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:194:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:202:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:207:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:209:14: UP015 Unnecessary open mode parameters
Error: backend/tests/test_simple.py:218:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:222:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:230:1: W293 Blank line contains whitespace
Error: backend/tests/test_simple.py:233:80: W292 No newline at end of file
Error: Process completed with exit code 1.