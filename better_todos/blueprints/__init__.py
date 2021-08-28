from .categories import categories
from .tags import tags

__all__ = ["mapping"]

# A mapping from routes to blueprints
mapping = {
    "/v1/categories": categories,
    "/v1/tags": tags,
}
