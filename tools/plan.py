VALID_PLAN_STATUSES = ("pending", "in_progress", "completed")


def update_plan(items: list) -> list:
    if not isinstance(items, list):
        raise ValueError("`items` must be a list of plan items.")

    normalized_items = []
    seen_ids = set()
    in_progress_count = 0

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Plan item #{index} must be an object.")

        item_id = str(item.get("id", "")).strip()
        content = str(item.get("content", "")).strip()
        status = str(item.get("status", "")).strip()

        if not item_id:
            raise ValueError(f"Plan item #{index} is missing a non-empty `id`.")

        if item_id in seen_ids:
            raise ValueError(f"Plan item id `{item_id}` is duplicated.")

        if not content:
            raise ValueError(f"Plan item `{item_id}` is missing a non-empty `content`.")

        if status not in VALID_PLAN_STATUSES:
            allowed_statuses = ", ".join(VALID_PLAN_STATUSES)
            raise ValueError(
                f"Plan item `{item_id}` has invalid status `{status}`. Allowed: {allowed_statuses}."
            )

        if status == "in_progress":
            in_progress_count += 1

        normalized_items.append({
            "id": item_id,
            "content": content,
            "status": status,
        })
        seen_ids.add(item_id)

    if in_progress_count > 1:
        raise ValueError("Only one plan item can be `in_progress` at a time.")

    return normalized_items


def format_plan(items: list) -> str:
    if not items:
        return "No active plan."

    lines = ["Current plan:"]

    for item in items:
        lines.append(f"- [{item['status']}] {item['id']}: {item['content']}")

    return "\n".join(lines)


UPDATE_PLAN_TOOL = {
    "type": "function",
    "function": {
        "name": "update_plan",
        "description": (
            "Create or replace the current execution plan for this task. "
            "Use this for multi-step work, keep at most one item as in_progress, "
            "and send the full updated list every time."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "description": (
                        "The full list of plan items in execution order. "
                        "Provide an empty list to clear the plan."
                    ),
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "A short stable identifier for the step, like `inspect`."
                            },
                            "content": {
                                "type": "string",
                                "description": "A concise description of the step."
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "description": "One of `pending`, `in_progress`, or `completed`."
                            }
                        },
                        "required": ["id", "content", "status"]
                    }
                }
            },
            "required": ["items"]
        }
    }
}
