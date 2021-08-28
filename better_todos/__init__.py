import warnings

# Ignore warnings about marshmallow-sqlalchemy being required since we aren't using that integration
warnings.filterwarnings("ignore", category=UserWarning, module="flask_marshmallow")

from .app import app  # noqa
