Here you go — a clean, well‑structured **dbt Macro Command Cheat Sheet**, formatted entirely as a Markdown file so you can drop it straight into your repo or documentation.

---

# 📘 **dbt Macro Command Cheat Sheet**
*A compact reference for all essential Jinja + dbt macro features*

---

## 🧱 **1. Macro Definition**
```jinja
{% macro macro_name(arg1, arg2) %}
    -- logic here
{% endmacro %}
```

- Defines a reusable function  
- Arguments are optional  
- Returns rendered SQL text

---

## 🧩 **2. Calling a Macro**
```jinja
{{ macro_name('value1', 'value2') }}
```

Inside another macro (no output):
```jinja
{% do macro_name('x') %}
```

---

## 📝 **3. Variable Assignment (`set`)**
```jinja
{% set my_var = 'hello' %}
{% set cols = ['id', 'name', 'email'] %}
{% set config = {'key': 'value'} %}
```

---

## 🔁 **4. Loops (`for`)**
```jinja
{% for col in cols %}
    {{ col }},
{% endfor %}
```

With whitespace trimming:
```jinja
{% for col in cols -%}
    {{ col }}
{%- endfor %}
```

---

## 🔀 **5. Conditionals (`if`, `elif`, `else`)**
```jinja
{% if target.type == 'snowflake' %}
    ...
{% elif target.type == 'bigquery' %}
    ...
{% else %}
    ...
{% endif %}
```

---

## 🧮 **6. Filters (`|`)**
Common filters:
```jinja
{{ 'hello' | upper }}          # HELLO
{{ cols | join(', ') }}        # id, name, email
{{ value | trim }}
{{ list | length }}
```

---

## 🧰 **7. `do` Statement (side effects only)**
```jinja
{% do cols.append('new_col') %}
```

Used when you want to modify a list or call a macro without printing output.

---

## 🧱 **8. Comments**

### Jinja comments (not compiled into SQL)
```jinja
{# this will NOT appear in compiled SQL #}
```

### SQL comments (will appear)
```sql
-- visible in compiled SQL
/* multi-line SQL comment */
```

---

## 🧩 **9. Using `ref()` and `source()`**
```jinja
{{ ref('orders') }}
{{ source('raw', 'customers') }}
```

Used inside macros to dynamically reference models or sources.

---

## 🧪 **10. String Concatenation**
```jinja
{{ col1 ~ '_' ~ col2 }}
```

---

## 🧼 **11. Whitespace Control**
Add `-` to trim whitespace:
```jinja
{% if condition -%}
    ...
{%- endif %}
```

---

## 🧬 **12. Environment Variables**
```jinja
{{ env_var('DBT_ENV') }}
```

---

## 🧱 **13. Returning SQL Expressions**
Macros output SQL text directly:
```jinja
{% macro safe_cast(col) %}
    coalesce(cast({{ col }} as varchar), '')
{% endmacro %}
```

---

## 🧩 **14. Dictionary & List Utilities**
### Looping with index:
```jinja
{% for col in cols %}
    {{ loop.index }}: {{ col }}
{% endfor %}
```

### Looping over dict:
```jinja
{% for key, value in config.items() %}
    {{ key }} = {{ value }}
{% endfor %}
```

---

## 🧠 **15. Built‑in Jinja Tests**
```jinja
{% if value is none %}
{% if value is string %}
{% if list is iterable %}
```

---

## 🧱 **16. Importing Macros**
```jinja
{% import 'macros/my_macros.sql' as my %}
{{ my.compute_hash(['id']) }}
```

---

## 🧩 **17. Macro Namespacing**
```jinja
{{ dbt_utils.generate_surrogate_key(['id']) }}
```

---

## 🧰 **18. Debugging Helpers**
```jinja
{{ log('message', info=True) }}
```

---
