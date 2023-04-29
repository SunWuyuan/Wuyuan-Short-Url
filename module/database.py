# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import config
import pymysql
import re
import time

class DataBase:
    def __init__(self) -> None:
        self.prefix = config.DATABASE['prefix']
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
        data = [re.sub("'", '', data_count) for data_count in data]
        return f'{self.prefix}{name}' in data

    def createCoreTable(self) -> None:
        sql = f'''
            CREATE TABLE `{self.prefix}core` (
                `key_` varchar(255) NOT NULL,
                `value_` varchar(255) DEFAULT NULL,
                PRIMARY KEY (`key_`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

        sql = f'''
            INSERT INTO `{self.prefix}core` (key_, value_)
            VALUES(
                "title", "氧化氢短网址"
            );
        '''
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'''
            INSERT INTO `{self.prefix}core` (key_, value_)
            VALUES(
                "keyword", "氧化氢短网址"
            );
        '''
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'''
            INSERT INTO `{self.prefix}core` (key_, value_)
            VALUES(
                "description", "一切是那么的简约高效."
            );
        '''
        self.cursor.execute(sql)
        self.connect.commit()

    def createDomainTable(self) -> None:
        sql = f'''
            CREATE TABLE `{self.prefix}domain` (
                `domain` varchar(255) NOT NULL,
                `protocol` varchar(255) DEFAULT NULL,
                PRIMARY KEY (`domain`) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

    def createUrlTable(self) -> None:
        sql = f'''
            CREATE TABLE `{self.prefix}url` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `type_` varchar(255) DEFAULT NULL,
                `domain` varchar(255) DEFAULT NULL,
                `long_url` varchar(255) DEFAULT NULL,
                `signature` varchar(255) DEFAULT NULL,
                `valid_day` int(11) DEFAULT NULL,
                `count` int(11) DEFAULT NULL,
                `timestmap` int(11) DEFAULT NULL,
                PRIMARY KEY (`id`) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

    def insert(self, type_: str, domain: str, longUrl: str, validDay: int) -> int:
        sql = f'''
            INSERT INTO {self.prefix}url (type_, domain, long_url, valid_day, count, timestmap)
            VALUES(
                "{type_}",
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
    
    def update(self, id_: int, signature: str) -> None:
        sql = f'''
            UPDATE {self.prefix}url 
            SET signature = "{signature}" 
            WHERE
                id = {id_} 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        self.connect.commit()
    
    def delete(self, id_: int) -> None:
        sql = f'''
            DELETE 
            FROM
                {self.prefix}url 
            WHERE
                id = "{id_}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        self.connect.commit()

    def addCount(self, domain: str, signature: str) -> None:
        sql = f'''
            UPDATE {self.prefix}url 
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
                {self.prefix}core 
            WHERE
                key_ = "title" 
                OR key_ = "keyword" 
                OR key_ = "description" 
            LIMIT 3;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data_ = {}
        for datum in data:
            data_[datum['key_']] = datum['value_']
        return data_

    def queryDomain(self) -> dict:
        sql = f'''
            SELECT
                * 
            FROM
                {self.prefix}domain;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data_ = {}
        for datum in data:
            data_[datum['domain']] = datum['protocol']
        return data_

    def queryUrlByLongUrl(self, domain: str, longUrl: str) -> bool:
        sql = f'''
            SELECT
                * 
            FROM
                {self.prefix}url 
            WHERE
                domain = "{domain}" 
                AND long_url = "{longUrl}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return False

    def queryUrlBySignature(self, domain: str, signature: str) -> bool:
        sql = f'''
            SELECT
                * 
            FROM
                {self.prefix}url 
            WHERE
                domain = "{domain}" 
                AND signature = "{signature}" 
            LIMIT 1;
        '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return False