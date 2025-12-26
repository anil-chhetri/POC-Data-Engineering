{%- macro compute_hash(columns) -%}
    {# 1. Create an empty list to store transformed column expressions #}
    {%- set safe_cols = [] -%}

    {# 2. Loop through each column provided to the macro #}
    {%- for col in columns -%}

        {# 3. Append a null‑safe, type‑safe expression for each column #}
        {%- do safe_cols.append("coalesce(cast(" ~ col ~ " as varchar), '')") -%}

    {%- endfor -%}

    {{ log("Computing hash for columns: " ~ safe_cols | join(", "), info=True) }}

    {# 4. Join all transformed columns with a delimiter and hash them #}
    md5({{ safe_cols | join(" || '|' || ") }})

{%- endmacro -%}
