#!/bin/bash

git init
git add ./
git commit -m "提交主文件"
git remote add origin https://github.com/amisher1/jm_pdfget-langbot-.git
git pull origin main
git push origin main

