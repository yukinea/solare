# solare

# 環境変数
```
$ export ROOT_DIR=/home/user/solare/
$ export GOOGLE_CALENDAR_ID=<ID>
$ export GOOGLE_CREDENTIALS_FILE=${ROOT_DIR}/ENV/certain-hogehoge.json
```

# pip install
```
$ mkdir lib
$ pip install -t lib/ -r ./requirements.txt
```

# zip化
解凍したときにlambda_function.py が置いてあるディレクトリがむき出しで展開されるようにする
```
$ cd solare
$ zip -r solare.zip * -x \*/__pycache__/\*
```



