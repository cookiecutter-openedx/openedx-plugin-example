def get_dashboard_context(existing_context, *args, **kwargs):
    print("#########################################3")
    print(existing_context, args, kwargs)
    print("#########################################3")

    additional_context = {"some_plugin_value": 10}
    if existing_context.get("some_core_value"):
        additional_context.update({"some_other_plugin_value": True})
    return additional_context
