#-------------------------------------------------------------------------------
# Name:        ThreeGoodThings.py
# Purpose:
#
# Author:      TOMOKIYO Hisayoshi
#
# Created:     16/07/2014
# Copyright:   (c) TOMOKIYO Hisayoshi 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#*******************************************************************************
import sqlite3
class DbPrc(object):
    """good_thingsＤＢの操作
    """
    DB_NAME = "good_things.db"

    #-------------------------------------------------------------------------------
    @classmethod
    def createTable(cls):
        """テーブル作成
        """
        DLL = """create table IF NOT EXISTS good_things(
            date text not null CHECK( date like '____-__-__'),
            seq  integer not null CHECK(seq IN (1,2,3)),
            thing text,
            primary key(date, seq)
        )"""

        with cls.GtDb(cls.DB_NAME) as gtDb:
            gtDb.con.executescript(DLL)

    #-------------------------------------------------------------------------------
    @classmethod
    def gatThings(cls, **kwargs):
        """データ取得
        """

        #引数取得
        try:
            date = kwargs["date"]
        except KeyError:
            date = None

        try:
            limit = kwargs["limit"]
        except KeyError:
            limit = 3

        try:
            offset =  kwargs["offset"]
        except KeyError:
            offset = 0

        #SQL文作成
        if date:
            sql = "SELECT * FROM good_things WHERE date = ? ORDER BY date,seq"
            par = (date,)
        else:
            sql = "SELECT * FROM good_things WHERE thing != '' ORDER BY date DESC ,seq LIMIT ? OFFSET ?"
            #次のデータの存在を確認する為に「self.limit+1」行取得する
            par = (limit+1,offset,)

        #データ取得
        with cls.GtDb(cls.DB_NAME) as gtDb:

            #データ取得
            getCur=gtDb.cur.execute(sql, par)

            #戻り値設定
            cnt = 0
            gtList = []
            next = False
            for row in getCur:
                #self.limitより行数が多い場合は次がある
                #戻り値はlimitと同じ行数にする為break
                if cnt >= limit:
                    next = True
                    break

                #GoodThingオブジェクト設定
                gt = GoodThing(row["date"], row["seq"], row["thing"])
                gtList.append(gt)

                #レコードカウント
                cnt = cnt + 1

        return gtList,next
    #-------------------------------------------------------------------------------
    @classmethod
    def upsert(cls,gtList):
        """更新
        """
        with cls.GtDb(cls.DB_NAME) as gtDb:
            for gt in gtList:
                sql = "INSERT OR REPLACE INTO good_things (date,seq,thing) VALUES (?,?,?)"
                gtDb.cur.execute(sql, (gt.date,gt.seq,gt.thing,))

            #コミット
            gtDb.con.commit()


    #===============================================================================
    class GtDb(object):
        """接続とカーソル取得
        """
        #-------------------------------------------------------------------------------
        def __init__(self,database):
            """コンストラクタ
            """
            self.database = database
            self.con = None
            self.cur = None

        #-------------------------------------------------------------------------------
        def __enter__(self):
            """開始
            """
            self.con = sqlite3.connect(self.database)
            self.con.row_factory = sqlite3.Row
            self.cur = self.con.cursor()
            return self

        #-------------------------------------------------------------------------------
        def __exit__(self, exc_type, exc_value, traceback):
            """終了
            """
            #close
            if "close" in dir(self.cur):
                self.cur.close()
            if "close" in dir(self.con):
                self.con.close()

            #削除
            self.cur = None
            self.con = None

            #エラー
            if exc_type:
                return False
            else:
                return True

#*******************************************************************************
class GoodThing(object):
    """GoodThingエンティティ
    """
    __slots__ = ['date','seq','thing']

    def __init__(self,date,seq ,thing,):
            self.date = date
            self.seq =  seq
            self.thing = thing


#*******************************************************************************
#bottle
import datetime
from bottle import route,run,request,redirect,template,auth_basic
#-------------------------------------------------------------------------------
#DBとテーブル作成
DbPrc.createTable()

#-------------------------------------------------------------------------------
@route("/")
def todayThing():
    """ルートを表示
    """
    #今日のレコード取得
    today = str(datetime.date.today())
    gtList, next = DbPrc.gatThings(date = today)

    #値を辞書に設定
    gtDct = {1:"",2:"",3:""}
    for row in gtList:
        gtDct[row.seq]  = row.thing

    #html作成
    return template("today_Thing",day=today,thing1=gtDct[1],thing2=gtDct[2],thing3=gtDct[3])

#-------------------------------------------------------------------------------
@route('/save', method='POST')
def save():
    """更新
    """
    #request内容でＤＢ更新
    if request.forms.get('save','').strip():
        gtList=[]
        rsDay = request.forms.get('day','').strip()
        for iSeq in range(1,4):
            #入力値取得
            rsThing = request.forms.get('thing'+str(iSeq),'').strip().decode('utf-8')

            #GoodThingオブジェクト設定
            gt = GoodThing(rsDay, iSeq,rsThing)
            gtList.append(gt)

        #更新
        DbPrc.upsert(gtList)

    #ルートを表示
    redirect("/")

#-------------------------------------------------------------------------------
@route('/history:page#[0-9]+#')
def history(page):
    """履歴表示
    """
    LIMT = 21                   #表示件数
    offset = int(page) * LIMT   #表示開始位置

    #履歴情報取得取得
    gtList, next = DbPrc.gatThings(limit = LIMT, offset = offset)

    #前次ページ設定 値が負の数の場合はページリンクを作成しない
    prevPage = int(page) -1
    nextPage = int(page) +1 if next else -1

    #html作成
    return template("history",rows = gtList,prev = prevPage,next = nextPage,)

#*******************************************************************************
if __name__ == "__main__":
    """実行
    """
    #run(host='localhost', port=8000, debug=False, reloader=True)
    run(host='localhost', port=8000, debug=True, reloader=False)
