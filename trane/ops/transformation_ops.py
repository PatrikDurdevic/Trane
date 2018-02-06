from ..utils.table_meta import TableMeta as TM
from .op_base import OpBase

TRANSFORMATION_OPS = ["IdentityTransformationOp", "DiffTransformationOp", "ObjectFrequencyTransformationOp"]
__all__ = ["TransformationOpBase", "TRANSFORMATION_OPS"] + TRANSFORMATION_OPS

class TransformationOpBase(OpBase):
    """super class for all Transformation Operations. (deprecated)"""
    pass

class IdentityTransformationOp(TransformationOpBase):
    PARAMS = [{}, {}]
    IOTYPES = [(TM.TYPE_FLOAT, TM.TYPE_FLOAT), (TM.TYPE_BOOL, TM.TYPE_BOOL)]
    def execute(self, dataframe):
        return dataframe

class DiffTransformationOp(TransformationOpBase):
    PARAMS = [{}]
    IOTYPES = [(TM.TYPE_FLOAT, TM.TYPE_FLOAT)]
    def execute(self, dataframe):
        index = dataframe.index
        for i in range(len(index) - 1, 0, -1):
            dataframe.at[index[i], self.column_name] -= dataframe.at[index[i-1], self.column_name]
        dataframe.at[index[0], self.column_name] = 0
        return dataframe

class ObjectFrequencyTransformationOp(TransformationOpBase):
    PARAMS = [{}]
    IOTYPES = [(TM.TYPE_FLOAT, TM.TYPE_FLOAT)]
    def execute(self, dataframe):
        objects = dataframe.copy()[self.column_name].unique()
        objects_to_frequency = {}    
        for obj in objects:
            objects_to_frequency[obj] = 0
        
        for val in dataframe[self.column_name]:
            objects_to_frequency[val] = objects_to_frequency[val] + 1

        for idx, obj in enumerate(objects):
            dataframe.at[idx, 'count'] = objects_to_frequency[obj]

        num_rows_to_drop = len(dataframe) - len(objects_to_frequency)
        assert(num_rows_to_drop >= 0)
        if num_rows_to_drop == 0:
            return dataframe
        print(dataframe[:-num_rows_to_drop])
        return dataframe[:-num_rows_to_drop]


