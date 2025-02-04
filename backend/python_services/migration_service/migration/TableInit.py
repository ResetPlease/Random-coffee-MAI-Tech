from typing import Any
from alembic import op
from sqlalchemy import Table
from hashlib import sha256
import random

class TableInit:
    
    @staticmethod
    def serialize_row(columns_info : dict[str, type], row : str, ignore_rows : list[int] | None = None) -> dict[str, Any]:
        dict_item : dict[str, Any] = {}
        if ignore_rows is None:
            ignore_rows = []
            
        row = row.replace('\n', '')
        for index, (name, type_) in enumerate(columns_info.items()):
            if row == '':
                dict_item[name] = None
                continue
            if index in ignore_rows:
                _, row = row.split(',', 1)
                continue
            match str(type_):
                case "<class 'str'>":
                    value, row = row.removeprefix('"').split('"', 1)
                    dict_item[name] = value
                    row = row.removeprefix(',')
                case _:
                    if row.count(',') > 0:
                        value, row = row.split(',', 1)
                    else:
                        value, row = row, ''
                    dict_item[name] = type_(value)       
                    
        return dict_item
    
    
    @staticmethod 
    def parse_data(table : Table, 
                  file_name : str, 
                  colums_names : list[str],
                  ignore_rows : list[int] | None = None
                ) -> None:
        columns_info : dict[str, type] = {}    
        items : list[dict[str, Any]] = []

        for name in colums_names:
            columns_info[name] = table.columns[name].type.python_type
        with open(file = file_name, mode = 'r') as file:
            for item in file:
                items.append(TableInit.serialize_row(columns_info, item, ignore_rows))
        return items
    
    @classmethod
    def insert_data_from_file(cls,
                              table : Table, 
                              file_name : str, 
                              colums_names : list[str],
                              ignore_rows : list[int] | None = None
                              ) -> None:
            
        op.bulk_insert(table, cls.parse_data(table, file_name, colums_names, ignore_rows))
                
    @classmethod           
    def update_data_from_file(cls,
                              table : Table, 
                              file_name : str, 
                              colums_names : list[str],
                              where_columns : list[str],
                              ignore_rows : list[int] | None = None
                              ) -> None:
        for item in cls.parse_data(table, file_name, colums_names, ignore_rows):
            where = []
            for if_column in where_columns:
                where.append(table.c.__dict__[if_column] == item.pop(if_column))
            query_for_update = table.update().where(*where).values(item)
            op.execute(query_for_update)


    @classmethod
    def get_list_movies_from_file(cls,
                              file_name: str
                              ) -> list[int]:
        items : list[int]
        items = []
        with open(file=file_name, mode='r') as file:
            for item in file:
                items += item.split(',')
        for i in range(len(items)):
            items[i] = int(items[i])
        return items
                


class DatabaseRandomRowsGenrator:
    
    @classmethod
    def add_to_movie_file_movie_description(cls, movie_file_name : str, decription_file_name : str, new_file_name : str) -> None:
        with open(movie_file_name, 'r') as movie:
            with open(decription_file_name, 'r') as descr:
                with open(new_file_name, 'w+') as new:
                    for i, j in zip(movie, descr):
                        i = i.removesuffix('\n')
                        new.write(i + ',' + j.split(',', 1)[1])
    
    @staticmethod
    def clear_user_csv(file_name : str, new_file_name : str) -> None:
        emails : list[str] = []
        letters = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        with open(file_name, 'r') as readed_file:
            with open(new_file_name, 'w+') as write_file:
                for user in readed_file:
                    user = user.split(',')[:4]
                    id = user[0]
                    first, last = user[1].split(' ')[:2]
                    email : str = user[2]
                    
                        
                    while email in emails:
                        split_email = email.split('@')
                        split_email[0] += random.choice(letters)
                        email = '@'.join(split_email)    
                        
                    password = sha256(str.encode(email)).hexdigest()
                    
                    user = [id, first, last, email, password]
                    for i, str_ in enumerate(user[1:], start = 1):
                        user[i] = '"' + str_ + '"'
                    
                    write_file.write(','.join(user) + '\n')
                
                    emails.append(email)

    @staticmethod
    def get_ids(file_name : str) -> list[int]:
        ids : list[int] = []
        with open(file_name, 'r') as file:
            for item in file:
                ids.append(int(item.split(',')[0]))
                
        return ids


    @classmethod
    def create_random_movie_rating(cls, movie_file_name : str, user_file_name : str, new_file_name : str) -> None:
        user_ids : list[int] = cls.get_ids(user_file_name)
        movie_ids : list[int] = cls.get_ids(movie_file_name)   
        
        with open(new_file_name, 'w+') as file:
            for movie_id in movie_ids:
                rating_count = random.randint(5, 30)
                using_user_ids : list[int] = []      
                for _ in range(rating_count):
                    user_id = random.choice(user_ids)
                    while user_id in using_user_ids:
                       user_id = random.choice(user_ids)
                    using_user_ids.append(user_id)
                    file.write(f'{random.randint(1, 10)},{movie_id},{user_id}\n')
                    
                    
    @staticmethod
    def union_movies_and_links(movie_file_name : str, link_file_name : str, new_movie_file_name : str, new_link_file_name : str) -> None:
        data : dict[int, dict[str, str]] = {}
        with open(movie_file_name, 'r+') as movie_file:
            for movie in movie_file:
                id, movie_info = movie.split(',', 1)
                data[int(id)] = {}
                data[int(id)]['movie'] = movie_info.removesuffix('(no genres listed)').removesuffix('\n').removesuffix(',')
        with open(link_file_name, 'r') as link_file:
            for link in link_file:
                id, link_info = link.split(',', 1)
                data[int(id)]['link'] = link_info.removesuffix('\n')
        
        for new_file_name, type_ in zip([new_movie_file_name, new_link_file_name], ['movie', 'link']):
            with open(new_file_name, 'w+') as file:
                for id, data_id in enumerate(data.keys(), start=1):
                    file.write(f'{id},{data[data_id][type_]}\n')
    
    
    @classmethod
    def create_random_reviews(cls, user_file_name : str, movie_file_name : str, file_name : str, new_file_name : str) -> None:
        user_ids : list[int] = cls.get_ids(user_file_name)
        movie_ids : list[int] = cls.get_ids(movie_file_name)
        data : list[tuple[str, str]] = [] 
        with open(file_name, 'r+') as read_file:
            for review in read_file:
                text, statement = review.removesuffix('\n').rsplit(',', 1)
                text = '"' + text.replace('<br />', '').replace('"', '') + '"'
                data.append((text, statement))
                
                
        with open(new_file_name, 'w+') as write_file:
            for movie_id in movie_ids:
                using_user_ids : list[int] = []
                using_reviews : list[int] = []
                for _ in range(random.randint(1, 5)):
                    user_id = random.choice(user_ids)
                    while user_id in using_user_ids:
                       user_id = random.choice(user_ids)

                    using_user_ids.append(user_id)

                    review_id = random.randint(0, len(data) - 1)
                    while review_id in using_reviews:
                       review_id = random.randint(0, len(data) - 1)

                    using_reviews.append(review_id)
                    
                    text, statement = data[review_id]
                    statement = random.choice([statement, statement, statement, 'neutral'])
                    statement = '"' + statement + '"'
                    header = '"' + text[1:15] + '..."'
                    write_file.write(f'{movie_id},{user_id},{header},{text},{statement}\n')
                
        
            
            
            
#DatabaseRandomRowsGenrator.add_to_movie_file_movie_description(
#    'migration/versions/csv_data/new_movie_clear.csv',
#    'migration/versions/csv_data/movie_description.csv',
#    'migration/versions/csv_data/movie_with_description.csv'
#)


        
            
            
#print(TableInit.serialize_row({'id':int, 'title' : str, 'genres' : str}, '27250,"Standby (2014)","Comedy|Romance"', [0]))         
        
#DatabaseRandomRowsGenrator.create_random_reviews(
#                                                'migration/versions/csv_data/users_clear.csv',
#                                                'migration/versions/csv_data/new_movie_clear.csv',
#                                                'migration/versions/csv_data/user_reviews.csv',
#                                                'migration/versions/csv_data/user_reviews_clear.csv'
#                                                )
#                    
        
#DatabaseRandomRowsGenrator.union_movies_and_links('migration/versions/csv_data/movie_clear.csv',
#                                                  'migration/versions/csv_data/link_clear.csv',
#                                                  'migration/versions/csv_data/new_movie_clear.csv',
#                                                  'migration/versions/csv_data/new_link_clear.csv')
# 
 
#DatabaseRandomRowsGenrator.create_random_movie_rating('migration/versions/csv_data/new_movie_clear.csv',
#                                                      'migration/versions/csv_data/users_clear.csv',
#                                                     'migration/versions/csv_data/user_ratings.csv') 