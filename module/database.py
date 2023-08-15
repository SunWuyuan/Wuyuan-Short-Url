from typing import Optional
import config
import pymysql
import re
import time

class DataBase:
    def __init__(self) -> None:
        self.tablePrefix = config.DATABASE['tablePrefix']
        self.coreTableName = f'{self.tablePrefix}core'
        self.domainTableName = f'{self.tablePrefix}domain'
        self.urlTableName = f'{self.tablePrefix}url'
        self.connect = pymysql.connect(
            host=config.DATABASE['host'],
            port=int(config.DATABASE['port']),
            user=config.DATABASE['username'],
            passwd=config.DATABASE['password'],
            db=config.DATABASE['name'],
            ssl_ca=config.DATABASE['ssl']['caPath'],
            ssl_key=config.DATABASE['ssl']['keyPath'],
            ssl_cert=config.DATABASE['ssl']['certPath']
        )
        self.cursor = self.connect.cursor(pymysql.cursors.DictCursor)

    def __del__(self) -> None:
        self.cursor.close()
        self.connect.close()

    def existenceTable(self, name: str) -> bool:
        sql = 'show tables'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = re.findall('(\'.*?\')', str(data))
        data = [re.sub("'", '', dataItem) for dataItem in data]
        return f'{self.tablePrefix}{name}' in data
    
    def createCoreTable(self) -> None:
        sql = f'''
            CREATE TABLE {self.coreTableName} (
                name varchar(255) NOT NULL,
                content varchar(255) DEFAULT NULL,
                PRIMARY KEY (name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

        sql = f'''
            INSERT INTO {self.coreTableName} (name, content)
            VALUES(
                "title", "氧化氢短网址"
            );
        '''
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'''
            INSERT INTO {self.coreTableName} (name, content)
            VALUES(
                "keyword", "氧化氢短网址"
            );
        '''
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'''
            INSERT INTO {self.coreTableName} (name, content)
            VALUES(
                "description", "一切是那么的简约高效."
            );
        '''
        self.cursor.execute(sql)
        self.connect.commit()

    def createDomainTable(self) -> None:
        sql = f'''
            CREATE TABLE {self.domainTableName} (
                domain varchar(255) NOT NULL,
                protocol varchar(255) DEFAULT NULL,
                PRIMARY KEY (domain) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

    def createUrlTable(self) -> None:
        sql = f'''
            CREATE TABLE {self.urlTableName} (
                id int(11) NOT NULL AUTO_INCREMENT,
                type_ int(1) DEFAULT NULL,
                domain varchar(255) DEFAULT NULL,
                long_url varchar(255) DEFAULT NULL,
                signature varchar(255) DEFAULT NULL,
                valid_day int(10) DEFAULT NULL,
                count int(11) DEFAULT NULL,
                timestamp int(10) DEFAULT NULL,
                PRIMARY KEY (id) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

    def insertUrl(self, type_: int, domain: str, longUrl: str, validDay: int) -> int:
        sql = f'''
            INSERT INTO {self.urlTableName} (type_, domain, long_url, valid_day, count, timestamp)
            VALUES(
                {type_},
                "{domain}",
                "{longUrl}",
                {validDay},
                0,
                {int(time.time())}
            );
        '''
        self.cursor.execute(sql)
        id_ = self.connect.insert_id()
        self.connect.commit()
        return id_
    
    def updateUrl(self, id_: int, signature: str) -> None:
        sql = f'''
            UPDATE {self.urlTableName} 
            SET signature = "{signature}" 
            WHERE
                id = {id_} 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        self.connect.commit()
    
    def deleteUrl(self, id_: int) -> None:
        sql = f'''
            DELETE 
            FROM
                {self.urlTableName} 
            WHERE
                id = "{id_}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        self.connect.commit()

    def addUrlCount(self, domain: str, signature: str) -> None:
        sql = f'''
            UPDATE {self.urlTableName} 
            SET count = count + 1 
            WHERE
                domain = "{domain}" 
                AND signature = "{signature}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        self.connect.commit()
    
    def queryWebsiteInfo(self) -> dict:
        sql = f'''
            SELECT
                * 
            FROM
                {self.coreTableName} 
            WHERE
                name = "title" 
                OR name = "keyword" 
                OR name = "description" 
            LIMIT 3;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data_ = {}
        for datum in data:
            data_[datum['name']] = datum['content']
        return data_

    def queryDomain(self) -> dict:
        sql = f'''
            SELECT
                * 
            FROM
                {self.domainTableName};
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data_ = {}
        for datum in data:
            data_[datum['domain']] = datum['protocol']
        return data_

    def queryUrlByLongUrl(self, domain: str, longUrl: str) -> Optional[dict]:
        sql = f'''
            SELECT
                * 
            FROM
                {self.urlTableName} 
            WHERE
                domain = "{domain}" 
                AND long_url = "{longUrl}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return None

    def queryUrlBySignature(self, domain: str, signature: str) -> Optional[dict]:
        sql = f'''
            SELECT
                * 
            FROM
                {self.urlTableName} 
            WHERE
                domain = "{domain}" 
                AND signature = "{signature}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return None