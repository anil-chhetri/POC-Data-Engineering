{% macro generate_schema_name(custom_schema_name, node) %}
    {{ log("Using schema: " ~ custom_schema_name, info=True) }}
    {{ custom_schema_name }}
{% endmacro %}
