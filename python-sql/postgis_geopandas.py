import geopandas as gpd
from sqlalchemy import *
from configparser import ConfigParser
import geoalchemy2


def main():
    try:
            
        parser = ConfigParser()
        parser.read(r'../config.ini')
    
        username = parser.get('db', 'user')
        pwd = parser.get('db', 'password')
        server = parser.get('db', 'server')
        db = 'CamargoDB'
    
        connection_string = f"""postgresql://{username}:{pwd}@{server}/{db}"""

        engine = create_engine(connection_string)
        metadata = MetaData()

        sql = '''SELECT * from shapefiles.tracts'''
        gdf = gpd.read_postgis(sql, engine, geom_col="geometry")
                
        gdf['col'] = gdf.col.apply(lambda x: transform(x))
        
        gdf.to_postgis('transformed_gdf',engine, index=True, index_label='Index',schema = 'shapefiles')
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
          
        error_type = str(exc_type)
        line = exc_tb.tb_lineno
        word =  error_type + ' at Line '
        error = word+str(line)

        message = (error + ': ' + str(e))
        
        print(message)

if __name__ == '__main__':
    main()