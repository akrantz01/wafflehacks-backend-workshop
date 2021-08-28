from marshmallow import EXCLUDE
from flask_marshmallow import Marshmallow
from typing import Any, Dict, List

ma = Marshmallow()
init = ma.init_app


class Base(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    def from_object(self, obj: object) -> Dict[str, Any]:
        """
        Extract the fields from an arbitrary object
        :param obj: the object to get fields from
        :return: a validated dict
        """
        return self.dump({field: getattr(obj, field) for field in self.fields})

    def from_objects(self, objs: List[object]) -> List[Dict[str, Any]]:
        """
        Extract the fields from an arbitrary set of objects
        :param objs: the objects to get fields from
        :return: a list of validated dicts
        """
        return self.dump([self.from_object(obj) for obj in objs], many=True)
