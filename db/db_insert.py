import logging
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, Integer, Numeric

logging.basicConfig(filename='logger.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def insert_all(data):
    engine = create_engine('mysql+pymysql://root:9713@localhost:3306/sa_test', echo=True)
    metadata = MetaData(engine)

    data['flag'] = data.apply(lambda row: row['时间'][0:8], axis=1)
    columns_list = data.columns.values.tolist()
    grouped = data.groupby('flag')
    logging.info("%d行数据分组完毕，等待插入..." % len(data))
    for name, grouped_df in grouped:
        data_table = Table(name, metadata,
                           Column('时间', String(14), primary_key=True),
                           Column('压强', Float),
                           Column('温度', Float),
                           Column('湿度', Float),
                           Column('闪烁指数', Float),
                           Column('TEC', Float),
                           Column('卫星编号1', Integer),
                           Column('码伪距1', Numeric(15, 5)),
                           Column('相伪距1', Numeric(15, 5)),
                           Column('卫星编号2', Integer),
                           Column('码伪距2', Numeric(15, 5)),
                           Column('相伪距2', Numeric(15, 5)),
                           Column('卫星编号3', Integer),
                           Column('码伪距3', Numeric(15, 5)),
                           Column('相伪距3', Numeric(15, 5)),
                           Column('卫星编号4', Integer),
                           Column('码伪距4', Numeric(15, 5)),
                           Column('相伪距4', Numeric(15, 5)),
                           Column('卫星编号5', Integer),
                           Column('码伪距5', Numeric(15, 5)),
                           Column('相伪距5', Numeric(15, 5)),
                           Column('卫星编号6', Integer),
                           Column('码伪距6', Numeric(15, 5)),
                           Column('相伪距6', Numeric(15, 5)),
                           Column('卫星编号7', Integer),
                           Column('码伪距7', Numeric(15, 5)),
                           Column('相伪距7', Numeric(15, 5)),
                           Column('卫星编号8', Integer),
                           Column('码伪距8', Numeric(15, 5)),
                           Column('相伪距8', Numeric(15, 5)),
                           Column('卫星编号9', Integer),
                           Column('码伪距9', Numeric(15, 5)),
                           Column('相伪距9', Numeric(15, 5)),
                           Column('卫星编号10', Integer),
                           Column('码伪距10', Numeric(15, 5)),
                           Column('相伪距10', Numeric(15, 5))
                           )
        data_table.create(checkfirst=True)

        table_tuple = []
        for i in range(0, len(grouped_df)):
            arr = data.iloc[i].values
            data_row = {}
            for x in range(0, len(arr) - 1):
                data_row[columns_list[x]] = float(arr[x])
            table_tuple.append(data_row)

        ins = data_table.insert()
        conn = engine.connect()
        result = conn.execute(ins, table_tuple)
        logging.info("所有数据插入完毕")
