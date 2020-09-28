#!/usr/bin/env python
from github import Github
import sys
import yaml
import mysql.connector
import lib.database

#データベース設定
db = lib.database.Database()

#テーブル作成
db.create("pull_requests",
            """id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            github_number INT,
            name VARCHAR(1000),
            creator_name VARCHAR(100),
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

db.create("pull_request_comments",
            """id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            pull_request_id INT,
            creator_name VARCHAR(100),
            created_at DATETIME,
            body VARCHAR(10000)""")

db.create("commits",
            """sha VARCHAR(100) PRIMARY KEY,
                pull_request_id INT,
                creator_name VARCHAR(100),
                created_at DATETIME,
                body VARCHAR(10000),
                state VARCHAR(100)""")

db.create("project_files",
            """id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE KEY""")

db.create("commits_files",
            """commit_sha VARCHAR(100),
            file_id INT""")


print("Created DB\n")
