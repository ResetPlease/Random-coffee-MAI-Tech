from typing import Any
from alembic import op
from sqlalchemy import Table
import pandas
import random
from datetime import datetime, timedelta
import numpy as np


class TableInit:
    
    
    @staticmethod 
    def parse_data(
                    table : Table, 
                    file_name : str, 
                    ignore_rows : list[str] | None = None
                ) -> list[dict[str, Any]]:
        
        items = pandas.read_csv(file_name)
        for column in table.columns:
            if column.type.python_type is datetime and items.get(column.name) is not None:
                items[column.name] = pandas.to_datetime(items[column.name])
        
        if ignore_rows:
            items.drop(ignore_rows, axis = 1, inplace = True)
        
        return items.to_dict(orient = 'records')
        
        
        
        
    
    @classmethod
    def insert_data_from_file(
                                cls,
                                table : Table, 
                                file_name : str, 
                                ignore_rows : list[str] | None = None
                            ) -> None:
            
        op.bulk_insert(table, cls.parse_data(table, file_name, ignore_rows))
      
      
      
                
    @classmethod           
    def update_data_from_file(cls,
                              table : Table, 
                              file_name : str, 
                              where_columns : list[str],
                              ignore_rows : list[str] | None = None
                              ) -> None:
        for item in cls.parse_data(table, file_name, ignore_rows):
            where = []
            for where_column in where_columns:
                where.append(table.c.__dict__[where_column] == item.pop(where_column))
            query_for_update = table.update().where(*where).values(item)
            op.execute(query_for_update)



