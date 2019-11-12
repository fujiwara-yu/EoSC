#!/usr/bin/env python
from github import Github
import sys
import yaml
import mysql.connector
import lib.database

#データベース設定
db = lib.database.Database()

#テーブル作成
db.create("pulls", 
            """id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            number INT,
            username VARCHAR(100),
            body VARCHAR(10000),
            created_at DATETIME,
            closed_at DATETIME,
            merged_at DATETIME,
            state VARCHAR(32),
            commits INT,
            additions INT,
            deletions INT,
            changed_files INT,
            branch VARCHAR(32)""")

db.create("pullreq_comments", 
            """id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            pr_id INT,
            username VARCHAR(100),
            created_at DATETIME,
            comment VARCHAR(10000)""")

###commitのDB
db.create("project_commits",
            """sha VARCHAR(100),
            username VARCHAR(100),
            filename VARCHAR(100),
            created_at DATETIME,
            comment VARCHAR(10000),
            additions INT,
            deletions INT,
            changes INT""")


db.create("pull_commits", 
            """sha VARCHAR(100),
                pr_id INT,
                username VARCHAR(100),
                filename VARCHAR(100),
                created_at DATETIME,
                comment VARCHAR(10000)""")

#cursor.execute("""CREATE TABLE IF NOT EXISTS 
db.create("title", 
            """id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                number INT,
                title VARCHAR(1000),
                url VARCHAR(1000)""")

print("Created DB\n")