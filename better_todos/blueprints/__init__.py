from .categories import categories

__all__ = ["mapping"]

# A mapping from routes to blueprints
mapping = {
    "/v1/categories": categories,
}
