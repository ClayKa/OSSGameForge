app/services/postprocessor.py:203: error: Incompatible return value type (got "dict[str, int]", expected "dict[str, float]")  [return-value]
app/services/postprocessor.py:203: note: "Dict" is invariant -- see https://mypy.readthedocs.io/en/stable/common_issues.html#variance
app/services/postprocessor.py:203: note: Consider using "Mapping" instead, which is covariant in the value type
app/services/context_builder.py:52: error: Incompatible types in assignment (expression has type "list[dict[str, Any]]", target has type "str")  [assignment]
app/services/context_builder.py:53: error: Incompatible types in assignment (expression has type "int", target has type "str")  [assignment]
app/schemas/project.py:24: error: Incompatible types in assignment (expression has type "str | None", base class "ProjectBase" defined the type as "str")  [assignment]
app/storage.py:168: error: Argument "expires" to "presigned_get_object" of "Minio" has incompatible type "int"; expected "timedelta"  [arg-type]
app/config.py:20: error: Unexpected keyword argument "env" for "Field"  [call-arg]
/opt/hostedtoolcache/Python/3.10.18/x64/lib/python3.10/site-packages/pydantic/fields.py:623: note: "Field" defined here
app/config.py:21: error: Unexpected keyword argument "env" for "Field"  [call-arg]
/opt/hostedtoolcache/Python/3.10.18/x64/lib/python3.10/site-packages/pydantic/fields.py:623: note: "Field" defined here
app/services/asset_service.py:200: error: Item "None" of "Minio | None" has no attribute "bucket_exists"  [union-attr]
app/services/asset_service.py:201: error: Item "None" of "Minio | None" has no attribute "make_bucket"  [union-attr]
app/services/asset_service.py:238: error: Argument 1 to "write" of "_TemporaryFileWrapper" has incompatible type "bytes | None"; expected "Buffer"  [arg-type]
app/routers/health.py:38: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
app/routers/health.py:41: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
app/routers/health.py:47: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
app/routers/health.py:50: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
app/routers/health.py:52: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
app/routers/health.py:55: error: Unsupported target for indexed assignment ("Collection[str]")  [index]
app/routers/generation.py:124: error: "GenerationRequest" has no attribute "user_id"  [attr-defined]
app/routers/generation.py:146: error: Unexpected keyword argument "constraints" for "build_generation_prompt" of "ContextBuilder"  [call-arg]
app/routers/generation.py:151: error: "GenerationRequest" has no attribute "constraints"  [attr-defined]
app/services/context_builder.py:21: note: "build_generation_prompt" of "ContextBuilder" defined here
app/routers/generation.py:157: error: "GenerationRequest" has no attribute "model_version"  [attr-defined]
app/routers/generation.py:202: error: Unexpected keyword argument "metadata" for "GenerationResponse"  [call-arg]
app/routers/generation.py:204: error: Argument "scene" to "GenerationResponse" has incompatible type "dict[str, Any]"; expected "Scene"  [arg-type]
app/routers/assets.py:110: error: Argument "filename" to "create_initial_asset_record" has incompatible type "str | None"; expected "str"  [arg-type]
app/routers/assets.py:117: error: Argument "original_filename" to "process_and_store_file" has incompatible type "str | None"; expected "str"  [arg-type]
Found 24 errors in 9 files (checked 23 source files)
Error: Process completed with exit code 1.