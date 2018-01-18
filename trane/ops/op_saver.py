from .op_base import OpBase
from .aggregation_ops import *
from .filter_ops import *
from .row_ops import *
from .transformation_ops import *
import json

__all__ = ["op_to_json", "op_from_json"]

def op_to_json(op):
    """
    Convert a operation object to a json string. 
    args:
        op: a subclass of OpBase
    returns:
        str: a json string of op
    """
    return json.dumps({
        "OpType": op.__class__.__bases__[-1].__name__,
        "SubopType": type(op).__name__,
        "column_name": op.column_name,
        "iotype": (op.itype, op.otype),
        "param_values": op.param_values
    })

def op_from_json(json_data):
    """
    Convert a operation json string to a operation object.
    args:
        json_data: a json string of op
    returns:
        object: subclass of OpBase
    """
    data = json.loads(json_data)
    op = globals()[data['SubopType']](data['column_name'])
    op.itype, op.otype = data['iotype']
    op.param_values = data['param_values']
    return op