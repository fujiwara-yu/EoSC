#!/usr/bin/env python
from github import Github
import sys
import mysql.connector

#データベース設定
db=mysql.connector.connect(host="localhost", user="test")

cursor=db.cursor()

cursor.execute("USE test_db")
db.commit()

#テーブル作成
cursor.execute("""CREATE TABLE IF NOT EXISTS pulls(
                id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
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
                branch VARCHAR(32));""")
db.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS pullreq_comments(
                id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                pr_id INT,
                username VARCHAR(100),
                created_at DATETIME,
                comment VARCHAR(10000));""")
db.commit()

##commitのDB
cursor.execute("""CREATE TABLE IF NOT EXISTS project_commits(
                sha VARCHAR(100),
                username VARCHAR(100),
                filename VARCHAR(100),
                created_at DATETIME,
                comment VARCHAR(10000),
                additions INT,
                deletions INT,
                changes INT);""")
db.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS pull_commits(
                sha VARCHAR(100),
                pr_id INT,
                username VARCHAR(100),
                filename VARCHAR(100),
                created_at DATETIME,
                comment VARCHAR(10000));""")
db.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS title(
                id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                number INT,
                title VARCHAR(1000),
                url VARCHAR(1000));""")
db.commit()

print("Created DB\n")