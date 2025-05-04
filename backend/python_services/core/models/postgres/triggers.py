from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from alembic_utils.replaceable_entity import ReplaceableEntity
from typing import Iterable




def get_all_pg_obj() -> Iterable[ReplaceableEntity]:
    for obj in globals().values():
        if isinstance(obj, ReplaceableEntity):
            yield obj
            
            