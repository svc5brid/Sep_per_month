import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import datetime
import sqlite3
import re
import csv
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import cm
import hashlib
import configparser

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')


DBName = config_ini['Settings']['DBName']
Changes = None

con = sqlite3.connect(DBName)
cur = con.cursor()
try:
    # Userを登録するテーブル
    cur.execute("""CREATE TABLE Users (Number integer, Name Unique, ID text, Password text)""")
    cur.execute("INSERT INTO Users VALUES('1', 'User1', 'e12e115acf4552b2568b55e93cbd39394c4ef81c82447fafc997882a02d23677', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4')")
    cur.execute("INSERT INTO Users VALUES('2', 'User2', 'e59e4dc24c482ed5ea574fb4f5367f340cb0c77d504bd5b1a982038e2d861954', 'f8638b979b2f4f793ddb6dbd197e0ee25a7a6ea32b0ae22f5e3c5d119d839e75')")
except:
    pass
try:
    # すべての記録を登録しておくテーブル
    cur.execute("""CREATE TABLE AllRecords (ID integer, Title text, Amount integer, ClaimPer integer, Details text, Path text, User text, YearMonth integer, day integer)""")
except:
    pass
# 以下予備。
# try:
#     # Table作成をやってみる。
#     cur.execute("""CREATE TABLE AllTasks (ID integer, Name text, Details text, ParentsTask integer, Repetition integer, Repetition2 integer, Repetition3 text, TimeRequired integer, Power integer, ICOrule integer)""")
# except:
#     pass
con.commit()
con.close()



Version = "1.0"
#言語設定クラス
class Language():
    # ここで分ける。引数にJp、EnまたはTmが必要。
    def GetUsers(self):
        con = sqlite3.connect(DBName)
        cur = con.cursor()
        sql = f"SELECT Name FROM Users"
        cur.execute(sql)
        a = cur.fetchall()
        con.commit()
        con.close()
        return a
    def __init__(self, lang):
        a = self.GetUsers()
        # ユーザー1の名前
        self.UserName1 = a[0][0]
        # ユーザー2の名前
        self.UserName2 = a[1][0]
        if lang == "Jp":
            self.Japanese()
        elif lang == "En":
            self.English()
        elif lang == "Tm":
            self.Tame()
    def Japanese(self):
        # メインウインドウのタイトル
        self.title = "会計管理ソフト"
        # 認証画面のタイトル
        self.AuthWindowTitle = "ユーザー認証"
        # 認証画面の確認ボタンのテキスト
        self.AuthWindowConfirmText = "ログイン"
        # 認証画面のユーザー入力フォーム説明用のテキスト
        self.AuthWindowUserLabelText = "ユーザーID"
        # 認証画面のパスワード入力フォーム説明用のテキスト
        self.AuthWindowPassLabelText = "パスワード"
        # 設定画面の確認ボタンのテキスト
        self.CAuthWindowConfirmText = "照合"
        # 設定画面の元ユーザー入力フォーム説明用のテキスト
        self.CAuthWindowUserLabelText = "現在のユーザーID"
        # 設定画面の元パスワード入力フォーム説明用のテキスト
        self.CAuthWindowPassLabelText = "現在のパスワード"
        # 設定画面の確認ボタンのテキスト
        self.CDAuthWindowConfirmText = "登録"
        # 設定画面の元ユーザー入力フォーム説明用のテキスト
        self.CDAuthWindowUserLabelText = "新規ユーザーID"
        # 設定画面の元パスワード入力フォーム説明用のテキスト
        self.CDAuthWindowPassLabelText = "新規パスワード"
        # メインウインドウのログイン中のユーザー表示用テキスト
        self.InformationAboutNowUserText = "ログイン中のユーザー："
        # メインウインドウ、支出登録ボタンのテキスト
        self.RegistButtonText = "支出登録"
        # メインウインドウのリスト確認と変更ボタンのテキスト
        self.ConfirmAndEditButtonText = "リスト確認、変更(作成者のみ変更が可能)"
        # メインウインドウの清算表出力ボタンのテキスト
        self.OutputTheSheetText = "清算表出力"
        # メインウインドウの設定ボタンのテキスト
        self.SettingsText = "設定"
        # メインウインドウのメニューバーのファイルのテキスト
        self.MenuBarFileText = "ファイル"
        # メインウインドウのメニューバーの設定のテキスト
        self.MenuBarSettingsText = "設定"
        # メインウインドウのメニューバーの言語変更のテキスト
        self.MenuBarSettingsLangText = "言語変更"
        # メインウインドウのテーマ変更のテキスト
        self.MenuBarSettingsThemeText = "テーマ変更"
        # メインウインドウのユーザー変更のテキスト
        self.MenuBarFileChangeUserText = "ユーザー変更"
        # メインウインドウの終了ボタンのタイトル
        self.MenuBarFileExitText = "終了"
        # メインウインドウの終了確認画面のタイトル
        self.DestroyConfirmText = "終了確認"
        # メインウインドウの終了確認画面の詳細テキスト
        self.DestroyConfirmDetailsText = "ウインドウを閉じます。\nよろしいですか？"
        # 認証画面のユーザー認証成功ウインドウのタイトル
        self.AuthPassedText = "認証成功"
        # 認証画面のユーザー認証成功のウインドウの詳細テキスト
        self.AuthPassedDetails = "ユーザー認証に成功しました。\nユーザー："
        # メインウインドウのユーザー変更確認の詳細テキスト
        self.ChangeUserConfirmDetailsText = "ログアウトします。よろしいですか?"
        # メインウインドウのユーザー変更確認画面のタイトル
        self.ChangeUserConfirmText = "ログアウト確認"
        # 認証画面のユーザー認証失敗のウインドウのタイトル
        self.AuthMissedText = "認証失敗"
        # 認証画面のユーザー認証失敗の詳細テキスト
        self.AuthMissedDetails = "認証に失敗しました。\n入力内容を再確認してください。"
        # 支出登録ウインドウのタイトル
        self.RegistWindowTitle = "支出登録"
        # 支出登録ウインドウのラベルフレームのテキスト
        self.RegistLabelFrameText = "入力フォーム"
        # 支出登録ウインドウのタイトル入力フォーム用ラベルのテキスト
        self.RegistTitleLabelText = "タイトル"
        # 支出登録ウインドウの金額入力フォーム用ラベルのテキスト
        self.RegistAmountLabelText = "金額"
        # 支出登録ウインドウの割合入力フォーム用のラベルのテキスト
        self.RegistClaimLabelText = "分配割合"
        # 支出登録ウインドウの詳細入力フォーム用のラベルのテキスト
        self.RegistDetailsText = "詳細情報"
        # 支出ウインドウ、レシートパスの入力
        self.RegistPictureSelectText = "画像を選択"
        # 支出ウインドウ、確認ボタンのテキスト
        self.RegistConfirmButtonText = "確認"
        # 参照
        self.Reference = "参照"
        # 確認ウインドウのタイトル
        self.CEWindowTitle = "確認、編集"
        # 確認ウインドウの検索ラベルフレームのテキスト
        self.CESearchFormsText = "検索フォーム"
        # 検索ウインドウの検索年-月入力のためのテキスト
        self.CEYearEntryText = "年-月を選択"
        # 検索ウインドウの検索ボタン用のテキスト
        self.CESearchText = "検索"
        # 検索ウインドウの結果表示ラベルフレームのテキスト
        self.CEResult = "検索結果"
        # 設定ウインドウタイトル
        self.SettingsWindowTitle = "設定"
        # 設定画面の大枠のタイトル
        self.SettingsFrameTitle = "設定"
        # 設定画面のバージョン情報のテキスト
        self.SettingsVersionText = "バージョン："
        # 設定画面の言語ラベルのテキスト
        self.SettingsLanguageLabelText = "言語"
        # 設定画面の確認ボタンのテキスト
        self.SettingsConfirmButtonText = "ユーザー名変更の確定"
        # 設定画面のユーザーネームのところのテキスト
        self.SettingsUserLabelText = "ユーザー名"
        # ユーザー1の名前
        self.RegistUser1 = self.UserName1 + "："
        # ユーザー2の名前
        self.RegistUser2 = self.UserName2 + "："
        # 登録画面のタイトル未入力時のエラーメッセージ
        self.RegistTitleErrorMessage = "タイトルが未入力です。"
        # 登録画面の金額未入力時のエラーメッセージ
        self.RegistAmountErrorMessage = "金額が未入力です。"
        # 登録画面の書き込みOKメッセージ
        self.RegistOK = "完了しました。"
        # 登録画面の書き込みNGメッセージ
        self.RegistNG = "失敗しました。"
        # 編集画面の編集できませんメッセージ
        self.CEAuthError = "作成者が異なるため編集できません。"
        # 編集画面から登録画面に入ったときのウインドウタイトル
        self.CERegistWindowTitle = "変更画面"
        # 登録確認画面のタイトル
        self.RegistConfirmTitle = "確認"
        # 登録確認画面のメッセージ
        self.RegistConfirmMessage = "登録します。よろしいですか？"
        # 編集画面、登録失敗メッセージ
        self.CEChangeErrorMessage = "変更に失敗しました。"
        # 編集後の登録画面の確認ウインドウタイトル
        self.CERegistConfirmTitle = "確認"
        # 編集後の登録画面の確認ウインドウメッセージ
        self.CERegistConfirmMessage = "変更します。よろしいですか？"
        # 精算表出力画面のタイトル
        self.PTSSheetTitle = "精算表出力"
        # 精算表出力画面の形式選択案内
        self.PTSTypeEntryText = "出力形式を選択"
        # 精算表出力画面の出力ボタンテキスト
        self.PTSPrintText = "出力"
        # 精算表出力画面のラベルフレームのテキスト
        self.PTSSelectForm = "出力選択フォーム"
        # 精算表出力画面のパス選択案内
        self.PTSPathSelect = "出力パスを選択"
        # 精算表出力画面の年、月を入力していないエラーメッセージ
        self.PTSYearInputErrorMessage = "年-月は入力必須です。"
        # 精算表出力画面の形式を入力していないエラーメッセージ
        self.PTSTypeInputErrorMessage = "形式は入力必須です。"
        # 精算表出力画面のパスを入力していないエラーメッセージ
        self.PTSPathInputErrorMessage = "パスは入力必須です。"
        # 精算表出力画面の形式エラーメッセージ
        self.PTSTypeErrorMessage = "正しい形式を入力してください。"
        # 合計
        self.PTSSum = "合計"
        # 書き出しエラーメッセージ
        self.PTSWriteErrorMessage = "書き出しに失敗しました。"
        # 書き出し成功メッセージ
        self.PTSWriteSuccessMessage = "書き出しに成功しました。\nパス:"
        # 編集画面 作成日
        self.CEDate = "作成日"
        # 編集画面 タイトル
        self.CETitle = "タイトル"
        # 編集画面 金額
        self.CEAmount = "金額"
        # 編集画面 割合
        self.CEClaim = "請求割合"
        # 編集画面 ID
        self.CEID = "ID"
        # 出力画面 登録日
        self.PTSDate = "登録日"
        # 出力画面 タイトル
        self.PTSTitle = "タイトル"
        # 出力画面 金額
        self.PTSAmount = "金額"
        # 出力画面 ユーザー1負担額
        self.PTSUser1 = self.UserName1 + "への請求額"
        # 出力画面 ユーザー2負担額
        self.PTSUser2 = self.UserName2 + "への請求額"
        # 出力画面 支払い（合計みたいな位置)メッセージ
        self.PTSMustPay = "支払い"
        # 出力画面 支払い無しの人への表示
        self.PTSNone = "なし"
        # 認証画面 入力していない時メッセージ
        self.AuthNothingEntry = "ユーザー名、パスワードを入力してください。"
        # 言語の変更
        self.SettingsChangeLanguage = "言語の変更"
        # 確認
        self.Check = "確認"
        # ユーザーの名前変更の確認
        self.SChangeUserNameMessage = "ユーザー名を変更します。\nよろしいですか？"
        # 言語変更の確認
        self.SChangeLanguageMessage = "言語を変更します。\nよろしいですか？"
        # 支払った人
        self.PTSPaidPerson = "支払い者"
        # ユーザーID変更ボタン
        self.SettingsChangeLoginInfoButton = "ログイン情報変更"
        # 変更が完了しました。
        self.ChangeSuccessful = "変更が完了しました。"
        # パスワード変更に失敗
        self.ChangeFaild = "変更に失敗しました。"
        # パスワード登録ボタン
        self.IDRegist = "変更を登録"
        # 再起動を促す
        self.AskReboot = "再起動して設定を反映してください。"
        # ユーザーIDを変更するときにエラーが起きた感じ。
        self.ChangeUserError = "ユーザーID変更に失敗しました。"
        # ログイン情報を変更したので再起動。
        self.PChangeSuccessful = "ログイン情報を変更しました。\nアプリケーションを終了して設定を反映します。"
        # ログイン情報、現在の情報照合画面のタイトル
        self.ChangeLoginInfoWindowTitle = "現在の情報の確認"
        # 新しいログイン情報の入力画面のタイトル
        self.ChangeLoginInfoNewWindowTitle = "新しいログイン情報を入力"
        # けす
        self.CEDelete = "削除"
        # 消すときの確認ウインドウのタイトル
        self.CEDeleteConfirmWindowTitle = "削除確認"
        # 消すときの確認ウインドウのメッセージ
        self.CEDeleteConfirmWindowMessage = "削除します。よろしいですか？"
        # 削除成功メッセージ
        self.DeleteOK = "削除成功しました。"
        # 削除失敗メッセージ
        self.DeleteNG = "削除失敗しました。"
    def English(self):
        # メインウインドウのタイトル
        self.title = "AccountManagement"
        # 認証画面のタイトル
        self.AuthWindowTitle = "Auth User"
        # 認証画面の確認ボタンのテキスト
        self.AuthWindowConfirmText = "Login"
        # 認証画面のユーザー入力フォーム説明用のテキスト
        self.AuthWindowUserLabelText = "User ID"
        # 認証画面のパスワード入力フォーム説明用のテキスト
        self.AuthWindowPassLabelText = "Password"
        # 設定画面の確認ボタンのテキスト
        self.CAuthWindowConfirmText = "Auth"
        # 設定画面の元ユーザー入力フォーム説明用のテキスト
        self.CAuthWindowUserLabelText = "Current User ID"
        # 設定画面の元パスワード入力フォーム説明用のテキスト
        self.CAuthWindowPassLabelText = "Current Password"
        # 設定画面の確認ボタンのテキスト
        self.CDAuthWindowConfirmText = "Regist"
        # 設定画面の元ユーザー入力フォーム説明用のテキスト
        self.CDAuthWindowUserLabelText = "New User ID"
        # 設定画面の元パスワード入力フォーム説明用のテキスト
        self.CDAuthWindowPassLabelText = "New Password"
        # メインウインドウのログイン中のユーザー表示用テキスト
        self.InformationAboutNowUserText = "Logging User："
        # メインウインドウ、支出登録ボタンのテキスト
        self.RegistButtonText = "Cost Regist"
        # メインウインドウのリスト確認と変更ボタンのテキスト
        self.ConfirmAndEditButtonText = "Check And Edit(Edit only can Register)"
        # メインウインドウの清算表出力ボタンのテキスト
        self.OutputTheSheetText = "Output the Monthly Report"
        # メインウインドウの設定ボタンのテキスト
        self.SettingsText = "Settings"
        # メインウインドウのメニューバーのファイルのテキスト
        self.MenuBarFileText = "Files"
        # メインウインドウのメニューバーの設定のテキスト
        self.MenuBarSettingsText = "Settings"
        # メインウインドウのメニューバーの言語変更のテキスト
        self.MenuBarSettingsLangText = "Change Language"
        # メインウインドウのテーマ変更のテキスト
        self.MenuBarSettingsThemeText = "Change Theme"
        # メインウインドウのユーザー変更のテキスト
        self.MenuBarFileChangeUserText = "Change User"
        # メインウインドウの終了ボタンのタイトル
        self.MenuBarFileExitText = "Exit"
        # メインウインドウの終了確認画面のタイトル
        self.DestroyConfirmText = "Exit Confirm"
        # メインウインドウの終了確認画面の詳細テキスト
        self.DestroyConfirmDetailsText = "May I close the window?"
        # 認証画面のユーザー認証成功ウインドウのタイトル
        self.AuthPassedText = "Success"
        # 認証画面のユーザー認証成功のウインドウの詳細テキスト
        self.AuthPassedDetails = "Successed User Authentication\nUser："
        # メインウインドウのユーザー変更確認の詳細テキスト
        self.ChangeUserConfirmDetailsText = "May I logout the session?"
        # メインウインドウのユーザー変更確認画面のタイトル
        self.ChangeUserConfirmText = "Confirm Logout"
        # 認証画面のユーザー認証失敗のウインドウのタイトル
        self.AuthMissedText = "Failed"
        # 認証画面のユーザー認証失敗の詳細テキスト
        self.AuthMissedDetails = "We Failed the Authentication\nPlease check information inputted"
        # 支出登録ウインドウのタイトル
        self.RegistWindowTitle = "Regist the cost"
        # 支出登録ウインドウのラベルフレームのテキスト
        self.RegistLabelFrameText = "Input Forms"
        # 支出登録ウインドウのタイトル入力フォーム用ラベルのテキスト
        self.RegistTitleLabelText = "Title"
        # 支出登録ウインドウの金額入力フォーム用ラベルのテキスト
        self.RegistAmountLabelText = "Amount"
        # 支出登録ウインドウの割合入力フォーム用のラベルのテキスト
        self.RegistClaimLabelText = "Percentage"
        # 支出登録ウインドウの詳細入力フォーム用のラベルのテキスト
        self.RegistDetailsText = "Details(optical)"
        # 支出ウインドウ、レシートパスの入力
        self.RegistPictureSelectText = "Choose Files"
        # 支出ウインドウ、確認ボタンのテキスト
        self.RegistConfirmButtonText = "Confirm"
        # 参照
        self.Reference = "Reference"
        # 確認ウインドウのタイトル
        self.CEWindowTitle = "Check, Edit"
        # 確認ウインドウの検索ラベルフレームのテキスト
        self.CESearchFormsText = "Search Form"
        # 検索ウインドウの検索年-月入力のためのテキスト
        self.CEYearEntryText = "Select Year-Month"
        # 検索ウインドウの検索ボタン用のテキスト
        self.CESearchText = "Search"
        # 検索ウインドウの結果表示ラベルフレームのテキスト
        self.CEResult = "Result"
        # 設定ウインドウタイトル
        self.SettingsWindowTitle = "Settings"
        # 設定画面の大枠のタイトル
        self.SettingsFrameTitle = "Settings"
        # 設定画面のバージョン情報のテキスト
        self.SettingsVersionText = "Version："
        # 設定画面の言語ラベルのテキスト
        self.SettingsLanguageLabelText = "Language"
        # 設定画面の確認ボタンのテキスト
        self.SettingsConfirmButtonText = "Regist the UserName"
        # 設定画面のユーザーネームのところのテキスト
        self.SettingsUserLabelText = "UserName"
        # ユーザー1の名前
        self.RegistUser1 = self.UserName1 + "："
        # ユーザー2の名前
        self.RegistUser2 = self.UserName2 + "："
        # 登録画面のタイトル未入力時のエラーメッセージ
        self.RegistTitleErrorMessage = "Please input the Title"
        # 登録画面の金額未入力時のエラーメッセージ
        self.RegistAmountErrorMessage = "Plese input the Amount"
        # 登録画面の書き込みOKメッセージ
        self.RegistOK = "Successful"
        # 登録画面の書き込みNGメッセージ
        self.RegistNG = "Failed"
        # 編集画面の編集できませんメッセージ
        self.CEAuthError = "Can't Edit because it created other person"
        # 編集画面から登録画面に入ったときのウインドウタイトル
        self.CERegistWindowTitle = "ChangeWindow"
        # 登録確認画面のタイトル
        self.RegistConfirmTitle = "Confirm"
        # 登録確認画面のメッセージ
        self.RegistConfirmMessage = "May I regist the information?"
        # 編集画面、登録失敗メッセージ
        self.CEChangeErrorMessage = "We failed to change"
        # 編集後の登録画面の確認ウインドウタイトル
        self.CERegistConfirmTitle = "Confirm"
        # 編集後の登録画面の確認ウインドウメッセージ
        self.CERegistConfirmMessage = "May I regist to change?"
        # 精算表出力画面のタイトル
        self.PTSSheetTitle = "Print the Sheet"
        # 精算表出力画面の形式選択案内
        self.PTSTypeEntryText = "Choose the file type"
        # 精算表出力画面の出力ボタンテキスト
        self.PTSPrintText = "Print"
        # 精算表出力画面のラベルフレームのテキスト
        self.PTSSelectForm = "Type select forms"
        # 精算表出力画面のパス選択案内
        self.PTSPathSelect = "Choose the path"
        # 精算表出力画面の年、月を入力していないエラーメッセージ
        self.PTSYearInputErrorMessage = "Please input Year-Month"
        # 精算表出力画面の形式を入力していないエラーメッセージ
        self.PTSTypeInputErrorMessage = "Please input file type"
        # 精算表出力画面のパスを入力していないエラーメッセージ
        self.PTSPathInputErrorMessage = "Please input output path"
        # 精算表出力画面の形式エラーメッセージ
        self.PTSTypeErrorMessage = "Please input currect type"
        # 合計
        self.PTSSum = "Sum"
        # 書き出しエラーメッセージ
        self.PTSWriteErrorMessage = "We was failed to write"
        # 書き出し成功メッセージ
        self.PTSWriteSuccessMessage = "Successed to write \nPath:"
        # 編集画面 作成日
        self.CEDate = "Created Date"
        # 編集画面 タイトル
        self.CETitle = "Title"
        # 編集画面 金額
        self.CEAmount = "Amount"
        # 編集画面 割合
        self.CEClaim = "Percentage"
        # 編集画面 ID
        self.CEID = "ID"
        # 出力画面 登録日
        self.PTSDate = "Registed Date"
        # 出力画面 タイトル
        self.PTSTitle = "Title"
        # 出力画面 金額
        self.PTSAmount = "Amount"
        # 出力画面 ユーザー1負担額
        self.PTSUser1 = "Pay" + self.UserName1
        # 出力画面 ユーザー2負担額
        self.PTSUser2 = "Pay" + self.UserName2
        # 出力画面 支払い（合計みたいな位置)メッセージ
        self.PTSMustPay = "Pay"
        # 出力画面 支払い無しの人への表示
        self.PTSNone = "None"
        # 認証画面 入力していない時メッセージ
        self.AuthNothingEntry = "Please input username or password"
        # 言語の変更
        self.SettingsChangeLanguage = "Change language"
        # 確認
        self.Check = "confirm"
        # ユーザーの名前変更の確認
        self.SChangeUserNameMessage = "May I Change your username?"
        # 言語変更の確認
        self.SChangeLanguageMessage = "May I change language?"
        # 支払った人
        self.PTSPaidPerson = "buyer"
        # ユーザーID変更ボタン
        self.SettingsChangeLoginInfoButton = "Change login information"
        # 変更が完了しました。
        self.ChangeSuccessful = "Successed to change"
        # パスワード変更に失敗
        self.ChangeFaild = "Failed to change"
        # パスワード登録ボタン
        self.IDRegist = "Regist to change"
        # 再起動を促す
        self.AskReboot = "Please reboot the application "
        # ユーザーIDを変更するときにエラーが起きた感じ。
        self.ChangeUserError = "We failed to change the user id"
        # ログイン情報を変更したので再起動。
        self.PChangeSuccessful = "The change was successed\nPlease close the application to reflect"
        # ログイン情報、現在の情報照合画面のタイトル
        self.ChangeLoginInfoWindowTitle = "Check current information"
        # 新しいログイン情報の入力画面のタイトル
        self.ChangeLoginInfoNewWindowTitle = "Please enter new login information"
        # けす
        self.CEDelete = "delete"
        # 消すときの確認ウインドウのタイトル
        self.CEDeleteConfirmWindowTitle = "delete confirm"
        # 消すときの確認ウインドウのメッセージ
        self.CEDeleteConfirmWindowMessage = "May I delete it?"
        # 削除成功メッセージ
        self.DeleteOK = "Success to delete"
        # 削除失敗メッセージ
        self.DeleteNG = "Failed to delete"
    def Tame(self):
        # メインウインドウのタイトル
        self.title = "分配するよん"
        # 認証画面のタイトル
        self.AuthWindowTitle = "正しい人か確かめるよん"
        # 認証画面の確認ボタンのテキスト
        self.AuthWindowConfirmText = "入ろうとしてみる"
        # 認証画面のユーザー入力フォーム説明用のテキスト
        self.AuthWindowUserLabelText = "あなたのID"
        # 認証画面のパスワード入力フォーム説明用のテキスト
        self.AuthWindowPassLabelText = "あなたのパスワード"
        # 設定画面の確認ボタンのテキスト
        self.CAuthWindowConfirmText = "照合する！"
        # 設定画面の元ユーザー入力フォーム説明用のテキスト
        self.CAuthWindowUserLabelText = "いまのユーザーID"
        # 設定画面の元パスワード入力フォーム説明用のテキスト
        self.CAuthWindowPassLabelText = "いまのパスワード"
        # 設定画面の確認ボタンのテキスト
        self.CDAuthWindowConfirmText = "登録するっ！"
        # 設定画面の元ユーザー入力フォーム説明用のテキスト
        self.CDAuthWindowUserLabelText = "あたらしいユーザーID"
        # 設定画面の元パスワード入力フォーム説明用のテキスト
        self.CDAuthWindowPassLabelText = "あたらしいパスワード"
        # メインウインドウのログイン中のユーザー表示用テキスト
        self.InformationAboutNowUserText = "あなたのおなまえ："
        # メインウインドウ、支出登録ボタンのテキスト
        self.RegistButtonText = "取引のとーろく"
        # メインウインドウのリスト確認と変更ボタンのテキスト
        self.ConfirmAndEditButtonText = "見たり変えたり。"
        # メインウインドウの清算表出力ボタンのテキスト
        self.OutputTheSheetText = "表を出すよ！"
        # メインウインドウの設定ボタンのテキスト
        self.SettingsText = "せってー"
        # メインウインドウのメニューバーのファイルのテキスト
        self.MenuBarFileText = "ファイル"
        # メインウインドウのメニューバーの設定のテキスト
        self.MenuBarSettingsText = "せってー"
        # メインウインドウのメニューバーの言語変更のテキスト
        self.MenuBarSettingsLangText = "言葉かえる"
        # メインウインドウのテーマ変更のテキスト
        self.MenuBarSettingsThemeText = "テーマをかえる"
        # メインウインドウのユーザー変更のテキスト
        self.MenuBarFileChangeUserText = "ユーザーを変える。"
        # メインウインドウの終了ボタンのタイトル
        self.MenuBarFileExitText = "おわる！"
        # メインウインドウの終了確認画面のタイトル
        self.DestroyConfirmText = "おわるのの確認"
        # メインウインドウの終了確認画面の詳細テキスト
        self.DestroyConfirmDetailsText = "とじるよ！\nいーい？"
        # 認証画面のユーザー認証成功ウインドウのタイトル
        self.AuthPassedText = "おっけーです"
        # 認証画面のユーザー認証成功のウインドウの詳細テキスト
        self.AuthPassedDetails = "成功したよーん\nユーザー："
        # メインウインドウのユーザー変更確認の詳細テキスト
        self.ChangeUserConfirmDetailsText = "もう帰っちゃうんだ...？"
        # メインウインドウのユーザー変更確認画面のタイトル
        self.ChangeUserConfirmText = "悲しんでいます。"
        # 認証画面のユーザー認証失敗のウインドウのタイトル
        self.AuthMissedText = "残念でしたぁ笑"
        # 認証画面のユーザー認証失敗の詳細テキスト
        self.AuthMissedDetails = "なんか違ったみたいやね\n確認してみて？"
        # 支出登録ウインドウのタイトル
        self.RegistWindowTitle = "とーろく"
        # 支出登録ウインドウのラベルフレームのテキスト
        self.RegistLabelFrameText = "いれるとこ"
        # 支出登録ウインドウのタイトル入力フォーム用ラベルのテキスト
        self.RegistTitleLabelText = "タイトル"
        # 支出登録ウインドウの金額入力フォーム用ラベルのテキスト
        self.RegistAmountLabelText = "金額"
        # 支出登録ウインドウの割合入力フォーム用のラベルのテキスト
        self.RegistClaimLabelText = "わけかた！"
        # 支出登録ウインドウの詳細入力フォーム用のラベルのテキスト
        self.RegistDetailsText = "詳しい情報"
        # 支出ウインドウ、レシートパスの入力
        self.RegistPictureSelectText = "画像とか選んでみて"
        # 支出ウインドウ、確認ボタンのテキスト
        self.RegistConfirmButtonText = "かくにん"
        # 参照
        self.Reference = "オオサンショウウオ"
        # 確認ウインドウのタイトル
        self.CEWindowTitle = "かくにんしたりいじったり。"
        # 確認ウインドウの検索ラベルフレームのテキスト
        self.CESearchFormsText = "検索するとこ！"
        # 検索ウインドウの検索年-月入力のためのテキスト
        self.CEYearEntryText = "年と月がつながってるやつを選んでね。"
        # 検索ウインドウの検索ボタン用のテキスト
        self.CESearchText = "探すぜ"
        # 検索ウインドウの結果表示ラベルフレームのテキスト
        self.CEResult = "けっかはっぴょおおおおおおおお"
        # 設定ウインドウタイトル
        self.SettingsWindowTitle = "せってー"
        # 設定画面の大枠のタイトル
        self.SettingsFrameTitle = "せってー"
        # 設定画面のバージョン情報のテキスト
        self.SettingsVersionText = "これのバージョン："
        # 設定画面の言語ラベルのテキスト
        self.SettingsLanguageLabelText = "ことば"
        # 設定画面の確認ボタンのテキスト
        self.SettingsConfirmButtonText = "名前変えるわよ"
        # 設定画面のユーザーネームのところのテキスト
        self.SettingsUserLabelText = "おなまえ。"
        # ユーザー1の名前
        self.RegistUser1 = self.UserName1 + "："
        # ユーザー2の名前
        self.RegistUser2 = self.UserName2 + "："
        # 登録画面のタイトル未入力時のエラーメッセージ
        self.RegistTitleErrorMessage = "タイトルいれてよぉ"
        # 登録画面の金額未入力時のエラーメッセージ
        self.RegistAmountErrorMessage = "お金も入れてよぉ"
        # 登録画面の書き込みOKメッセージ
        self.RegistOK = "でけた"
        # 登録画面の書き込みNGメッセージ
        self.RegistNG = "ミスった"
        # 編集画面の編集できませんメッセージ
        self.CEAuthError = "お前が作ったんじゃねーよな？"
        # 編集画面から登録画面に入ったときのウインドウタイトル
        self.CERegistWindowTitle = "変えまーす"
        # 登録確認画面のタイトル
        self.RegistConfirmTitle = "かくにん"
        # 登録確認画面のメッセージ
        self.RegistConfirmMessage = "とーろくするよ！\nいいかなぁ？？"
        # 編集画面、登録失敗メッセージ
        self.CEChangeErrorMessage = "ミスったわぁー"
        # 編集後の登録画面の確認ウインドウタイトル
        self.CERegistConfirmTitle = "確認"
        # 編集後の登録画面の確認ウインドウメッセージ
        self.CERegistConfirmMessage = "変更するよ？いーい？"
        # 精算表出力画面のタイトル
        self.PTSSheetTitle = "かみを出す。"
        # 精算表出力画面の形式選択案内
        self.PTSTypeEntryText = "形式を選んでね。"
        # 精算表出力画面の出力ボタンテキスト
        self.PTSPrintText = "押すとこ"
        # 精算表出力画面のラベルフレームのテキスト
        self.PTSSelectForm = "ひつようなことを教えてねん。"
        # 精算表出力画面のパス選択案内
        self.PTSPathSelect = "どこに出すのか教えてねん"
        # 精算表出力画面の年、月を入力していないエラーメッセージ
        self.PTSYearInputErrorMessage = "いつのやつ出すか教えてねん"
        # 精算表出力画面の形式を入力していないエラーメッセージ
        self.PTSTypeInputErrorMessage = "どんなふうにだすのかおしえてねん"
        # 精算表出力画面のパスを入力していないエラーメッセージ
        self.PTSPathInputErrorMessage = "どこに出すのか教えてねん"
        # 精算表出力画面の形式エラーメッセージ
        self.PTSTypeErrorMessage = "出し方がちがうみたいよ"
        # 合計
        self.PTSSum = "合計"
        # 書き出しエラーメッセージ
        self.PTSWriteErrorMessage = "ミスった"
        # 書き出し成功メッセージ
        self.PTSWriteSuccessMessage = "でけたよ\n場所:"
        # 編集画面 作成日
        self.CEDate = "作成日"
        # 編集画面 タイトル
        self.CETitle = "タイトル"
        # 編集画面 金額
        self.CEAmount = "金額"
        # 編集画面 割合
        self.CEClaim = "請求割合"
        # 編集画面 ID
        self.CEID = "ID"
        # 出力画面 登録日
        self.PTSDate = "登録日"
        # 出力画面 タイトル
        self.PTSTitle = "タイトル"
        # 出力画面 金額
        self.PTSAmount = "金額"
        # 出力画面 ユーザー1負担額
        self.PTSUser1 = self.UserName1 + "への請求額"
        # 出力画面 ユーザー2負担額
        self.PTSUser2 = self.UserName2 + "への請求額"
        # 出力画面 支払い（合計みたいな位置)メッセージ
        self.PTSMustPay = "支払い"
        # 出力画面 支払い無しの人への表示
        self.PTSNone = "なし"
        # 認証画面 入力していない時メッセージ
        self.AuthNothingEntry = "ユーザー名とパスワードを入力してね"
        # 言語の変更
        self.SettingsChangeLanguage = "言葉を変えようか"
        # 確認
        self.Check = "いいかね"
        # ユーザーの名前変更の確認
        self.SChangeUserNameMessage = "名前変えるけどいいか？"
        # 言語変更の確認
        self.SChangeLanguageMessage = "言葉変えるけどいいか？"
        # 支払った人
        self.PTSPaidPerson = "支払い者"
        # ユーザーID変更ボタン
        self.SettingsChangeLoginInfoButton = "入るときの情報を変えよう。"
        # 変更が完了しました。
        self.ChangeSuccessful = "でけた"
        # パスワード変更に失敗
        self.ChangeFaild = "ぴえん"
        # パスワード登録ボタン
        self.IDRegist = "とーろくする"
        # 再起動を促す
        self.AskReboot = "再起動、、、してほしいな！"
        # ユーザーIDを変更するときにエラーが起きた感じ。
        self.ChangeUserError = "うぅ。。ごめんなさい、、できませんでした、、"
        # ログイン情報を変更したので再起動。
        self.PChangeSuccessful = "変更できたよ！ほめて！"
        # ログイン情報、現在の情報照合画面のタイトル
        self.ChangeLoginInfoWindowTitle = "いまのあなたのプロフィール"
        # 新しいログイン情報の入力画面のタイトル
        self.ChangeLoginInfoNewWindowTitle = "新しいこと"
        # けす
        self.CEDelete = "けすよ"
        # 消すときの確認ウインドウのタイトル
        self.CEDeleteConfirmWindowTitle = "いい、、かなぁ？"
        # 消すときの確認ウインドウのメッセージ
        self.CEDeleteConfirmWindowMessage = "消してもいいんだよね、、？"
        # 削除成功メッセージ
        self.DeleteOK = "けせた！！"
        # 削除失敗メッセージ
        self.DeleteNG = "ごめん、、ミスった。"


# iniファイルを読み込んで、以下の設定を。
# 色を変えるときはテーマを設定できるようにしたいので、classを作成しよう。
lang = Language(config_ini["Settings"]["Language"])




class main():
    def __init__(self, userID):
        # GUIの作成
        global root
        self.subwindow = None
        self.UserID = userID[0][1]
        self.UserNumber = userID[0][0]
        root = Tk()
        root.title(lang.title)
        # ここからパーツ
        UserLabel = ttk.Label(root, text=lang.InformationAboutNowUserText+str(userID[0][1]))
        RegistButton = ttk.Button(root, text=lang.RegistButtonText, command=lambda:[self.RegistTheCash()])
        ConfirmAndEditButton = ttk.Button(root, text=lang.ConfirmAndEditButtonText, command=lambda:[self.ConfirmAndEdit()])
        OutputTheSheetButton = ttk.Button(root, text=lang.OutputTheSheetText, command=lambda:[self.PrintTheSheet()])
        SettingsButton = ttk.Button(root, text=lang.SettingsText, command=lambda:[self.Settings()])

        RegistButton.grid(row=1, column=1, padx=10, pady=10)
        ConfirmAndEditButton.grid(row=1, column=2, padx=10, pady=10)
        OutputTheSheetButton.grid(row=2, column=1, padx=10, pady=10)
        SettingsButton.grid(row=2, column=2, padx=10, pady=10)
        UserLabel.grid(row = 0, column=2, padx=10)

        # メニューバーの設定
        MenuBar = Menu(root)
        root.config(menu=MenuBar)
        FileMenu = Menu(MenuBar, tearoff=0)
        MenuBar.add_cascade(label=lang.MenuBarFileText, menu=FileMenu)
        SettingMenu = Menu(MenuBar, tearoff=0)
        MenuBar.add_cascade(label=lang.MenuBarSettingsText, menu=SettingMenu)
        FileMenu.add_command(label=lang.MenuBarFileChangeUserText, command=lambda:[self.ChangeUserExit()])
        FileMenu.add_command(label=lang.MenuBarFileExitText, command=lambda:[self.Exit()])
        SettingMenu.add_command(label=lang.MenuBarSettingsLangText, command=lambda:[])
        SettingMenu.add_command(label=lang.MenuBarSettingsThemeText, command=lambda:[])

        root.mainloop()
    def NumValidate(self, val):
        if val == '':
            return True
        elif re.match(r'^\d*$', val):
            return True
        else:
            return False
    
    def Exit(self):
        # 終了確認画面を表示して、メインウインドウを閉じる。
        a = messagebox.askyesno(lang.DestroyConfirmText, lang.DestroyConfirmDetailsText)
        if a == True:
            root.destroy()
        else:
            pass

    def ChangeUserExit(self):
        # 変更確認画面を表示して、ユーザー変更をする。
        a = messagebox.askyesno(lang.ChangeUserConfirmText, lang.ChangeUserConfirmDetailsText)
        if a == True:
            root.destroy()
            Authentication()
        else:
            pass
    def RegistTheCash(self):
        # 登録画面
        global Changes
        if self.subwindow == None or not self.subwindow.winfo_exists() or Changes == 1:
            self.subwindow = Toplevel(root)
            if Changes == 1:
                self.subwindow.title(lang.CERegistWindowTitle)
            else:
                self.subwindow.title(lang.RegistWindowTitle)
            # ここからパーツ
            self.ClaimValue = IntVar(value=50)

            labelframe = ttk.LabelFrame(self.subwindow, text = lang.RegistLabelFrameText)
            TitleLabel = ttk.Label(labelframe, text = lang.RegistTitleLabelText)
            self.TitleEntry = ttk.Entry(labelframe, width=40)
            AmountLabel = ttk.Label(labelframe, text= lang.RegistAmountLabelText)
            validate = root.register(self.NumValidate)
            self.AmountEntry = ttk.Entry(labelframe, width=40, validate="key", validatecommand=(validate, "%P"))

            
            

            DetailsLabel = ttk.Label(labelframe, text=lang.RegistDetailsText)
            self.DetailsEntry = Text(labelframe, width=35, height=10)
            PictureSelectLabel = ttk.Label(labelframe, text=lang.RegistPictureSelectText)
            PathFrame = ttk.Frame(labelframe)
            PictureSelectButton = ttk.Button(PathFrame, text=lang.Reference, command=lambda:[self.GetFilePath()])
            self.PathBox = ttk.Entry(PathFrame, width=25)
            if Changes == 1:
                ConfirmButton = ttk.Button(labelframe, text=lang.RegistConfirmButtonText, command=lambda:[self.CERegistConfirm()])
                DeleteButton = ttk.Button(labelframe, text=lang.CEDelete, command=lambda:[self.Delete()])
                DeleteButton.grid(row=6, column=1, padx=10, pady=10)
            else:
                ConfirmButton = ttk.Button(labelframe, text=lang.RegistConfirmButtonText, command=lambda:[self.RegistConfirm()])

            ClaimFrame = ttk.Frame(labelframe)
            ClaimLabel = ttk.Label(labelframe, text = lang.RegistClaimLabelText)
            self.ClaimPartLabel1 = ttk.Label(ClaimFrame, text = lang.RegistUser1 + str(self.ClaimValue.get()) + "%")
            self.ClaimPartLabel2 = ttk.Label(ClaimFrame, text = lang.RegistUser2 + str(100 - self.ClaimValue.get()) + "%")
            self.ClaimEntry = Scale(ClaimFrame, length=250, orient=HORIZONTAL, to=100, resolution=5, variable=self.ClaimValue, command=lambda ClaimValue: [self.WriteClaimPer()], showvalue="FALSE")
            

            # ここから配置
            labelframe.pack()
            TitleLabel.grid(row=0, column=0, padx=10, pady=10)
            self.TitleEntry.grid(row=0, column=1, padx=10, pady=10)
            AmountLabel.grid(row=1, column=0, padx=10, pady=10)
            self.AmountEntry.grid(row=1, column=1, padx=10, pady=10)
            ClaimFrame.grid(row=2, column=1, padx=10, pady=10)
            ClaimLabel.grid(row=2, column=0, padx=10, pady=10)
            self.ClaimEntry.grid(row=1, column=0, padx=10, columnspan=3)
            self.ClaimPartLabel1.grid(row=0, column=0)
            self.ClaimPartLabel2.grid(row=0, column=2)
            DetailsLabel.grid(row=3, column=0, padx=10, pady=10)
            self.DetailsEntry.grid(row=3, column=1, padx=10, pady=10)
            PictureSelectLabel.grid(row=4, column=0, padx=10, pady=10)
            PathFrame.grid(row=4, column=1, padx=10, pady=10)
            PictureSelectButton.grid(row=0, column=0, padx=10, pady=10)
            self.PathBox.grid(row=0, column=1, padx=10, pady=10)
            ConfirmButton.grid(row=5, column=1, padx=10, pady=10)
        else:
            pass
    def WriteClaimPer(self):
        a = self.ClaimValue.get()
        self.ClaimPartLabel1["text"] = lang.RegistUser1 + str(a) + "%"
        self.ClaimPartLabel2["text"] = lang.RegistUser2 + str(100 - a) + "%"
    
    def RegistConfirm(self):
        a = self.GetRegistValues()
        try:
            if re.match(r'Error：*', a):
                messagebox.showerror("Error", a)
                root.lower()
                return
        except:
            pass
        c = messagebox.askokcancel(lang.RegistConfirmTitle, lang.RegistConfirmMessage)
        if c == True:
            b = self.WriteToDB(tuple(a))
            if b == "OK":
                messagebox.showinfo("OK", lang.RegistOK)
                root.lower()
                self.ClearForms()
            else:
                messagebox.showerror("NG", lang.RegistNG)
                root.lower()
        else:
            return

    

    def ClearForms(self):
        self.TitleEntry.delete(0, "end")
        self.AmountEntry.delete(0, "end")
        self.DetailsEntry.delete("1.0", "end")
        self.PathBox.delete(0, "end")
        pass
    
    def WriteToDB(self, Data):
        try:
            con = sqlite3.connect(DBName)
            cur = con.cursor()
            sql = f"INSERT INTO AllRecords values {Data}"
            cur.execute(sql)
            con.commit()
            con.close()
            return "OK"
        except:
            return "NG"
            
    
    def GetRegistValues(self):
        # リストに取得したデータを入力、DBへのちに入力
        # 空のリスト
        Value = []

        # ハッシュ値生成
        time = str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day)+str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)+str(datetime.datetime.now().second)+str(datetime.datetime.now().microsecond)
        timehash = hash(time)

        # 生成したハッシュ値をリストに追加
        Value.append(timehash)

        # タイトルの値を取得、リストに追加
        a = self.TitleEntry.get()
        if re.match(r'^\s*$', a) == None:
            Value.append(a)
        else:
            return "Error：" + lang.RegistTitleErrorMessage
        # 金額を取得、リストに追加
        b = self.AmountEntry.get()
        if re.match(r'^\s*$', b) == None:
            Value.append(b)
        else:
            return "Error：" + lang.RegistAmountErrorMessage
        # 分配割合を取得、リストに追加
        Value.append(self.ClaimValue.get())
        # 詳細情報を取得、改行を置き換え、リストに追加。
        Raw = self.DetailsEntry.get("1.0", "end"+"-1c")
        Data = Raw.replace("\n", "*kaigyo*")
        Value.append(Data)
        
        
        # レシートパスを取得、リストに追加
        # ☆☆☆☆☆☆☆☆☆アプリ内のパスに保存して、そのパスを入力するほうが管理が楽だと思う。というかそうするべきだと思う。
        Value.append(self.PathBox.get())


        Value.append(self.UserNumber)
        # 登録年、月を取得
        Value.append(str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month))

        # 登録日を取得
        Value.append(str(datetime.datetime.now().day))
        return Value
    
    def GetFilePath(self):
        FilePath = filedialog.askopenfilename(filetypes=[('pdf', "*.pdf"), ("jpg", "*.jpg")])
        root.lower()
        self.PathBox.delete(0, END)
        self.PathBox.insert(END, FilePath)
    

    def ConfirmAndEdit(self):
        # 確認と変更モード 
        # 月、年を選択するウインドウ
        if self.subwindow == None or not self.subwindow.winfo_exists():
            self.subwindow = Toplevel(root)
            self.subwindow.title(lang.CEWindowTitle)

            # データベースに登録されている月と年を取得
            a = self.GetDayandYear()

            # ここからパーツ
            validate = root.register(self.Validation)
            SearchForms = ttk.Labelframe(self.subwindow, text=lang.CESearchFormsText)
            self.YearPull = ttk.Combobox(SearchForms, validate="key", validatecommand=(validate, "%P"))
            try:
                self.YearPull["values"] = a[0]
            except:
                pass
            
            YearLabel = ttk.Label(SearchForms, text=lang.CEYearEntryText)
            SearchButton = ttk.Button(SearchForms, text=lang.CESearchText, command=lambda:[self.CEResultShow(self.YearPull.get())])
            self.SearchedLists = ttk.Labelframe(self.subwindow, text=lang.CEResult)
            # ここから配置
            SearchForms.pack()
            self.YearPull.grid(row=0, column=1, padx=10, pady=10)
            YearLabel.grid(row=0, column=0, padx=10, pady=10)
            SearchButton.grid(row=2, column=1, padx=10, pady=10)
            self.SearchedLists.pack()
            self.CEResultShow(0)
            
        else:
            pass
    def GetDayandYear(self):
        con = sqlite3.connect(DBName)
        cur = con.cursor()
        sql = f"SELECT DISTINCT YearMonth FROM AllRecords"
        cur.execute(sql)
        a = cur.fetchall()
        con.commit()
        con.close()
        return a

    def CEResultShow(self, YearMonth):
        # 表でデータを表示する。そこにバインドして詳細を表示、ユーザーIDによって動作を分ける。(編集可能か否か。)
        a = self.CEGetData(YearMonth)
        try:
            self.tree.pack_forget()
            self.tree.delete()
        except:
            pass
        self.tree = ttk.Treeview(self.SearchedLists)
        self.tree["columns"] = (1, 2, 3, 4, 5)
        self.tree["show"] = "headings"
        self.tree.heading(1, text=lang.CEDate)
        self.tree.heading(2, text=lang.CETitle)
        self.tree.heading(3, text=lang.CEAmount)
        self.tree.heading(4, text=lang.CEClaim)
        self.tree.heading(5, text=lang.CEID)

        self.tree.column(1, width=80)
        self.tree.column(2, width=130)
        self.tree.column(3, width=70)
        self.tree.column(4, width=50)
        self.tree.column(5, width=130)
        if YearMonth != 0:    
            for i in range(len(a)):
                self.tree.insert("", "end", values=(a[i][7] + "-" + str(a[i][8]), a[i][1], a[i][2], str(a[i][3]) + ":" +  str(100-a[i][3]), a[i][0]))
                self.tree.bind("<<TreeviewSelect>>", self.DetailsShow)
        self.tree.pack()

    def DetailsShow(self, event):
        a = self.tree.selection()[0]
        b = self.tree.set(a)
        c = self.CEDetailsGetData(b["5"])
        print(c)
        self.ShowDataDetails(c)
        # # -----------------ここから------------------
        # item = self.tree.identify('item', event.x, event.y)
        # item_text = self.tree.item(item, "text")
        # print(item_text)
        pass
    def ShowDataDetails(self, List):
        if List[0][6] == str(self.UserNumber):
            a = List[0]
            global Changes
            Changes = 1
            self.CEEditData = list(a)
            self.RegistTheCash()
            Changes = None
            self.TitleEntry.insert(0, a[1])
            # 金額を取得、リストに追加
            self.AmountEntry.insert(0, a[2])
            
            # 詳細情報を取得、改行を置き換え、リストに追加。
            Raw = a[4]
            Data = Raw.replace("*kaigyo*", "\n")
            self.DetailsEntry.insert("1.0", Data)
            
            
            # レシートパスを入力
            self.PathBox.insert(0, a[5])

        else:
            messagebox.showerror("Error", lang.CEAuthError)
        
        pass
    def Delete(self):
        a = self.CEGetRegistValues()
        try:
            if re.match(r'Error：*', a):
                messagebox.showerror("Error", a)
                root.lower()
                return
        except:
            pass
        c = messagebox.askokcancel(lang.CEDeleteConfirmWindowTitle, lang.CEDeleteConfirmWindowMessage)
        if c == True:
            b = self.CEDeleteDB(tuple(a))
            if b == "OK":
                messagebox.showinfo("OK", lang.DeleteOK)
                root.lower()
                self.subwindow.destroy()
            else:
                messagebox.showerror("NG", lang.DeleteNG)
                root.lower()
        else:
            return
    def CERegistConfirm(self):
        a = self.CEGetRegistValues()
        try:
            if re.match(r'Error：*', a):
                messagebox.showerror("Error", a)
                root.lower()
                return
        except:
            pass
        c = messagebox.askokcancel(lang.CERegistConfirmTitle, lang.CERegistConfirmMessage)
        if c == True:
            b = self.CEChangeDB(tuple(a))
            if b == "OK":
                messagebox.showinfo("OK", lang.RegistOK)
                root.lower()
                self.subwindow.destroy()
            else:
                messagebox.showerror("NG", lang.RegistNG)
                root.lower()
        else:
            return
    def CEGetRegistValues(self):
        # リストに取得したデータを入力、DBへのちに入力
        EditRawData = self.CEEditData
        # タイトルの値を取得、リストに追加
        a = self.TitleEntry.get()
        if re.match(r'^\s*$', a) == None:
            EditRawData[1] = a
        else:
            return "Error：" + lang.RegistTitleErrorMessage
        # 金額を取得、リストに追加
        b = self.AmountEntry.get()
        if re.match(r'^\s*$', b) == None:
            EditRawData[2] = b
        else:
            return "Error：" + lang.RegistAmountErrorMessage
        # 分配割合を取得、リストに追加
        EditRawData[3] = self.ClaimValue.get()
        # 詳細情報を取得、改行を置き換え、リストに追加。
        Raw = self.DetailsEntry.get("1.0", "end"+"-1c")
        Data = Raw.replace("\n", "*kaigyo*")
        EditRawData[4] = Data
        
        
        # レシートパスを取得、リストに追加
        # ☆☆☆☆☆☆☆☆☆アプリ内のパスに保存して、そのパスを入力するほうが管理が楽だと思う。というかそうするべきだと思う。
        EditRawData[5] = self.PathBox.get()

        # 登録年、月を取得
        EditRawData[7] = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month)

        # 登録日を取得
        EditRawData[8] = str(datetime.datetime.now().day)
        
        return EditRawData

    def CEDeleteDB(self, List):
        try:
            con = sqlite3.connect(DBName)
            cur = con.cursor()
            sql = f"DELETE FROM AllRecords WHERE ID = '{List[0]}'"
            cur.execute(sql)
            con.commit()
            con.close()
            return "OK"
        except:
            return "NG"
    def CEChangeDB(self, List):
        try:
            # 消す
            con = sqlite3.connect(DBName)
            cur = con.cursor()
            a = ["ID", "Title", "Amount", "ClaimPer", "Details", "Path", "User", "YearMonth", "day"]
            for i in range(len(List)):
                sql = f"UPDATE AllRecords set {a[i]} = '{List[i]}' WHERE ID = '{List[0]}'"
                cur.execute(sql)
            con.commit()
            con.close()
            return "OK"
        except:
            return "NG"
    def CEDetailsGetData(self, ID):
        con = sqlite3.connect(DBName)
        cur = con.cursor()
        sql = f"SELECT * FROM AllRecords WHERE ID = '{ID}'"
        cur.execute(sql)
        a = cur.fetchall()
        con.commit()
        con.close()
        return a

    def CEGetData(self, YearMonth):
        con = sqlite3.connect(DBName)
        cur = con.cursor()
        sql = f"SELECT * FROM AllRecords WHERE YearMonth = '{YearMonth}'"
        cur.execute(sql)
        a = cur.fetchall()
        con.commit()
        con.close()
        return a
    def Validation(self, val):
        return False
    def PrintTheSheet(self):
        if self.subwindow == None or not self.subwindow.winfo_exists():
            self.subwindow = Toplevel(root)
            self.subwindow.title(lang.PTSSheetTitle)
            # データベースに登録されている月と年を取得
            a = self.GetDayandYear()
            validate = root.register(self.Validation)

            # ここからパーツ
            SelectForm = ttk.Labelframe(self.subwindow, text=lang.PTSSelectForm)
            self.YearPull = ttk.Combobox(SelectForm, validate="key", validatecommand=(validate, "%P"))
            self.TypePull = ttk.Combobox(SelectForm, validate="key", validatecommand=(validate, "%P"))
            try:
                self.YearPull["values"] = a[0]
            except:
                pass
            self.TypePull["values"] = ("PDF", "CSV")
            YearLabel = ttk.Label(SelectForm, text=lang.CEYearEntryText)
            TypeLabel = ttk.Label(SelectForm, text=lang.PTSTypeEntryText)
            PrintButton = ttk.Button(SelectForm, text=lang.PTSPrintText, command=lambda:[self.PrintMethod()])
            SelectDirectoryFrame = ttk.Frame(SelectForm)
            SelectDirectoryLabel = ttk.Label(SelectForm, text=lang.PTSPathSelect)
            SelectDirectoryButton = ttk.Button(SelectDirectoryFrame, text=lang.Reference, command=lambda:[self.SelectPrintFilePath()])
            self.PathBox = ttk.Entry(SelectDirectoryFrame)
            # ここから配置
            SelectForm.pack()
            self.YearPull.grid(row=0, column=1, padx=10, pady=10)
            self.TypePull.grid(row=1, column=1, padx=10, pady=10)

            YearLabel.grid(row=0, column=0, padx=10, pady=10)
            TypeLabel.grid(row=1, column=0, padx=10, pady=10)
            PrintButton.grid(row=3, column=1, padx=10, pady=10)
            SelectDirectoryFrame.grid(row=2, column=1, padx=10, pady=10)
            SelectDirectoryLabel.grid(row=2, column=0, padx=10, pady=10)
            SelectDirectoryButton.grid(row=0, column=0)
            self.PathBox.grid(row=0, column=1)

            
            
        else:
            pass
        pass
    def SelectPrintFilePath(self):
        FilePath = filedialog.askdirectory()
        root.lower()
        self.PathBox.delete(0, END)
        self.PathBox.insert(END, FilePath)
    def PrintMethod(self):
        Year = self.YearPull.get()
        if re.match(r'^\s*$', Year) != None:
            messagebox.showerror("Error", lang.PTSYearInputErrorMessage)
            root.lower()
            return
        Type = self.TypePull.get()
        if re.match(r'^\s*$', Type) != None:
            messagebox.showerror("Error", lang.PTSTypeInputErrorMessage)
            root.lower()
            return
        Path = self.PathBox.get()
        if re.match(r'^\s*$', Path) != None:
            messagebox.showerror("Error", lang.PTSPathInputErrorMessage)
            root.lower()
            return
        a = self.CEGetData(Year)
        b = []
        b.append([lang.PTSDate, lang.PTSTitle, lang.PTSPaidPerson, lang.PTSAmount, lang.PTSUser1, lang.PTSUser2])
        for i in a:
            if i[6] == "1":
                b.append([i[7]+"-"+str(i[8]), i[1], i[6], i[2], 0, i[2]-math.floor(i[2]*i[3]/100)])
            else:
                b.append([i[7]+"-"+str(i[8]), i[1], i[6], i[2], math.floor(i[2]*i[3]/100), 0])
        c = 0
        d = 0
        e = 0
        for i in range(len(b)):
            if i != 0:
                c += b[i][4]
                d += b[i][5]
                e += b[i][3]
        b.append(["", "", lang.PTSSum, e, c, d])
        if c < d:
            # b.append(["", "", "", "", lang.PTSMustPay])
            b.append(["", "", "", lang.PTSMustPay, lang.PTSNone, d-c])
        else:
            # b.append(["", "", "", lang.PTSMustPay, ""])
            b.append(["", "", "", lang.PTSMustPay, c-d, lang.PTSNone])

        if Type == "PDF":
            f = self.PrintToPDF(b, Path, Year)
            if f == "NG":
                messagebox.showerror("Error", lang.PTSWriteErrorMessage)
            else:
                messagebox.showinfo("Success", lang.PTSWriteSuccessMessage + Path + "/" + Year + ".pdf")
        elif Type == "CSV":
            f = self.PrintToCSV(b, Path, Year)
            if f == "NG":
                messagebox.showerror("Error", lang.PTSWriteErrorMessage)
            else:
                messagebox.showinfo("Success", lang.PTSWriteSuccessMessage + Path + "/" + Year + ".csv")
        else:
            messagebox.showerror("Error", lang.PTSTypeErrorMessage)
        
    def PrintToPDF(self, List, Path, Date):
        try:
            
            file_name = f"{Path}/{Date}.pdf"
            pdf = canvas.Canvas(file_name, pagesize = portrait(A4))
            pdf.saveState()
            pdf.setAuthor(str(self.UserID))
            pdf.setTitle(Date)
            # フォント、サイズの設定
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

            pdf.setFont('HeiseiKakuGo-W5', 20)    # フォントサイズの変更
            width, height = A4  # A4用紙のサイズ
            pdf.drawCentredString(width / 2, height - 2*cm, Date)
            ### 文字を描画 ###
            for i in range(len(List)-2):
                if i <= len(List):
                    pdf.setLineWidth(0.5)
                    pdf.line(0*cm, (26.7-i)*cm, 21*cm, (26.7-i)*cm)
                pdf.setFont('HeiseiKakuGo-W5', 12)
                pdf.drawString(0.5*cm, (26-i)*cm, str(List[i][0]))
                pdf.drawString(4*cm, (26-i)*cm, str(List[i][1]))
                pdf.drawString(8.5*cm, (26-i)*cm, str(List[i][2]))
                pdf.drawString(11*cm, (26-i)*cm, str(List[i][3]))
                pdf.drawString(13*cm, (26-i)*cm, str(List[i][4]))            
                pdf.drawString(17.25*cm, (26-i)*cm, str(List[i][5]))            
            for i in (1, 2):
                pdf.setFont('HeiseiKakuGo-W5', 12)
                pdf.drawString(0.5*cm, (2+i)*cm, str(List[-i][0]))
                pdf.drawString(4*cm, (2+i)*cm, str(List[-i][1]))
                pdf.drawString(8.5*cm, (2+i)*cm, str(List[-i][2]))
                pdf.drawString(11*cm, (2+i)*cm, str(List[-i][3]))
                pdf.drawString(13*cm, (2+i)*cm, str(List[-i][4]))   
                pdf.drawString(17.25*cm, (2+i)*cm, str(List[-i][5]))   
            pdf.setLineWidth(2)
            pdf.line(3.5*cm, 5*cm, 3.5*cm, 26.7*cm)
            pdf.line(8*cm, 5*cm, 8*cm, 26.7*cm)
            pdf.line(10.5*cm, 5*cm, 10.5*cm, 26.7*cm)
            pdf.line(12.5*cm, 5*cm, 12.5*cm, 26.7*cm)
            pdf.line(16.75*cm, 5*cm, 16.75*cm, 26.7*cm)
            pdf.line(0*cm, 5*cm, 21*cm, 5*cm)

            pdf.restoreState()
            pdf.save()
            return "OK"
        except:
            return "NG"
        pass
    def PrintToCSV(self, List, Path, Date):
        try:
            with open(f"{Path}/{Date}.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(List)
            return "OK"
        except:
            return "NG"
        pass

    def langvalidation(self, val):
        if re.match(r'^Jp$', val):
            return True
        elif re.match(r'^En$', val):
            return True
        elif re.match(r'^Tm$', val):
            return True
        else:
            return False
    
    def Settings(self):
        if self.subwindow == None or not self.subwindow.winfo_exists():
            self.IDPSChangeWindow = None
            self.subwindow = Toplevel(root)
            self.subwindow.title(lang.SettingsWindowTitle)
            global Version
            # ここからパーツ
            SettingsFrame = ttk.Labelframe(self.subwindow,text=lang.SettingsFrameTitle)
            VersionLabel = ttk.Label(SettingsFrame, text=lang.SettingsVersionText + Version)
            LanguageLabel = ttk.Label(SettingsFrame, text=lang.SettingsLanguageLabelText)
            validate = root.register(self.langvalidation)
            self.LanguageBox = ttk.Combobox(SettingsFrame, validate="key", validatecommand=(validate, "%P"))
            self.LanguageBox.bind("<<ComboboxSelected>>", self.ChangeLanguage)
            self.LanguageBox["values"] = ("Jp", "En", "Tm")
            self.LanguageBox.insert(0, config_ini["Settings"]["Language"])
            UserNameLabel = ttk.Label(SettingsFrame, text=lang.SettingsUserLabelText)
            self.UserNameEntry = ttk.Entry(SettingsFrame)
            self.UserNameEntry.insert(0, self.UserID)
            ConfirmButton = ttk.Button(SettingsFrame, text=lang.SettingsConfirmButtonText, command=lambda:[self.ChangeUserName()])
            LoginChangeButton = ttk.Button(SettingsFrame, text=lang.SettingsChangeLoginInfoButton, command=lambda:[self.ChangePassword()])
        

            # ここから配置
            SettingsFrame.pack()
            VersionLabel.grid(row=1, column=0, pady=10, padx=10, columnspan=2)
            LanguageLabel.grid(row=2, column=0, pady=10, padx=10)
            self.LanguageBox.grid(row=2, column=1, pady=10, padx=10)
            UserNameLabel.grid(row=3, column=0, pady=10, padx=10)
            self.UserNameEntry.grid(row=3, column=1, pady=10, padx=10)
            ConfirmButton.grid(row=4, column=1, pady=10, padx=10)
            LoginChangeButton.grid(row=5, column=1, pady=10, padx=10)
            
            
        else:
            pass
        pass
    def ChangeLanguage(self, event):
        if messagebox.askyesno(lang.Check, lang.SChangeLanguageMessage) == True:
            Settings = config_ini["Settings"]
            Settings["Language"] = self.LanguageBox.get()
            with open('config.ini', "w")as configfile:
                config_ini.write(configfile)
    def ChangeUserName(self):
        a = messagebox.askyesno(lang.Check, lang.SChangeUserNameMessage)
        if a == True:
            try:
                con = sqlite3.connect(DBName)
                cur = con.cursor()
                sql = f"UPDATE Users set Name = '{self.UserNameEntry.get()}' WHERE Name = '{self.UserID}'"
                cur.execute(sql)
                con.commit()
                con.close()
                messagebox.showinfo("Success", lang.AskReboot)
            except:
                messagebox.showerror("Error", lang.ChangeUserError)
        else:
            pass
    def GetUsersInfo(self, ID):
        con = sqlite3.connect(DBName)
        cur = con.cursor()
        sql = f"SELECT * FROM Users WHERE ID = '{ID}'"
        cur.execute(sql)
        a = cur.fetchall()
        con.commit()
        con.close()
        return a
    def ChangePassword(self):
        if self.IDPSChangeWindow == None or self.IDPSChangeWindow.winfo_exists():
            self.IDPSChangeWindow = Toplevel(self.subwindow)
            self.IDPSChangeWindow.title(lang.ChangeLoginInfoWindowTitle)
            self.UserEntry = ttk.Entry(self.IDPSChangeWindow, width=30)
            self.PassEntry = ttk.Entry(self.IDPSChangeWindow, width=30)
            UserLabel = ttk.Label(self.IDPSChangeWindow, text=lang.CAuthWindowUserLabelText)
            PassLabel = ttk.Label(self.IDPSChangeWindow, text=lang.CAuthWindowPassLabelText)
            ConfirmButton = ttk.Button(self.IDPSChangeWindow, text = lang.CAuthWindowConfirmText, command=lambda:[self.Auth()])
            # ここから配置
            self.UserEntry.grid(row=0, column=1, padx=10, pady=10)
            self.PassEntry.grid(row=1, column=1, padx=10, pady=10)
            UserLabel.grid(row=0, column=0, padx=10, pady=10)
            PassLabel.grid(row=1, column=0, padx=10, pady=10)
            ConfirmButton.grid(row=2, column=1, padx=10, pady=10)
    def Auth(self):
        if self.UserEntry.get() == "":
            messagebox.showinfo("Error", lang.CAuthNothingEntry)
            return
        if self.PassEntry.get() == "":
            messagebox.showinfo("Error", lang.CAuthNothingEntry)
            return
        MID = self.UserEntry.get().encode()
        MHP = self.PassEntry.get().encode()
        

        HashedID = hashlib.sha256(MID).hexdigest()
        HashedPassword = hashlib.sha256(MHP).hexdigest()



        try:
            a = self.GetUsersInfo(HashedID)
            if a[0][3] == HashedPassword:
                self.passed(self.UserNumber)
            else:
                self.missed()
        except:
            self.missed()
            return
    def passed(self, UN):
        self.IDPSChangeWindow.destroy()
        self.IDPSChangeWindow = Toplevel(self.subwindow)
        self.IDPSChangeWindow.title(lang.ChangeLoginInfoNewWindowTitle)
        self.UserEntry = ttk.Entry(self.IDPSChangeWindow, width=30)
        self.PassEntry = ttk.Entry(self.IDPSChangeWindow, width=30)
        UserLabel = ttk.Label(self.IDPSChangeWindow, text=lang.CDAuthWindowUserLabelText)
        PassLabel = ttk.Label(self.IDPSChangeWindow, text=lang.CDAuthWindowPassLabelText)
        ConfirmButton = ttk.Button(self.IDPSChangeWindow , text = lang.CDAuthWindowConfirmText, command=lambda:[self.ChangeLoginInfo(UN)])
        # ここから配置
        self.UserEntry.grid(row=0, column=1, padx=10, pady=10)
        self.PassEntry.grid(row=1, column=1, padx=10, pady=10)
        UserLabel.grid(row=0, column=0, padx=10, pady=10)
        PassLabel.grid(row=1, column=0, padx=10, pady=10)
        ConfirmButton.grid(row=2, column=1, padx=10, pady=10)

    def ChangeLoginInfo(self, UN):
        if self.UserEntry.get() == "":
            messagebox.showinfo("Error", lang.CAuthNothingEntry)
            return
        if self.PassEntry.get() == "":
            messagebox.showinfo("Error", lang.CAuthNothingEntry)
            return
        MID = self.UserEntry.get().encode()
        MHP = self.PassEntry.get().encode()
        

        HashedID = hashlib.sha256(MID).hexdigest()
        HashedPassword = hashlib.sha256(MHP).hexdigest()

        a = messagebox.askyesno(lang.Check, lang.SChangeUserNameMessage)
        if a == True:
            try:
                con = sqlite3.connect(DBName)
                cur = con.cursor()
                self.UserEntry.get()
                sql = f"UPDATE Users set ID = '{HashedID}' WHERE Number = '{UN}'"
                cur.execute(sql)
                self.PassEntry.get()
                sql = f"UPDATE Users set Password = '{HashedPassword}' WHERE Number = '{UN}'"
                cur.execute(sql)
                con.commit()
                con.close()
                messagebox.showinfo("Success", lang.PChangeSuccessful)
                self.Exit()
            except:
                messagebox.showerror("Error", lang.ChangeFaild)
        else:
            pass
    def missed(self):
        messagebox.showinfo(lang.AuthMissedText, lang.AuthMissedDetails)


class Authentication():
    # ここで認証する。認証が終わったら引数にUserIDを渡してmainを実行
    def __init__(self):
        global root
        root = None
        self.AuthWindow = Tk()
        self.AuthWindow.title(lang.AuthWindowTitle)
        # ここからパーツ
        self.UserEntry = ttk.Entry(self.AuthWindow, width=25)
        self.PassEntry = ttk.Entry(self.AuthWindow, width=25)
        UserLabel = ttk.Label(self.AuthWindow, text=lang.AuthWindowUserLabelText)
        PassLabel = ttk.Label(self.AuthWindow, text=lang.AuthWindowPassLabelText)
        ConfirmButton = ttk.Button(self.AuthWindow, text = lang.AuthWindowConfirmText, command=lambda:[self.Auth()])
        # ここから配置
        self.UserEntry.grid(row=0, column=1, padx=10, pady=10)
        self.PassEntry.grid(row=1, column=1, padx=10, pady=10)
        UserLabel.grid(row=0, column=0, padx=10, pady=10)
        PassLabel.grid(row=1, column=0, padx=10, pady=10)
        ConfirmButton.grid(row=2, column=1, padx=10, pady=10)
        self.AuthWindow.mainloop()
    # 以下認証関数。戻り値はない。存在しなかった場合はウインドウで通知。した場合もウインドウで通知。
    # とりあえず認証できたということで、ユーザー1にしておく。
    def GetUsersInfo(self, ID):
        con = sqlite3.connect(DBName)
        cur = con.cursor()
        sql = f"SELECT * FROM Users WHERE ID = '{ID}'"
        cur.execute(sql)
        a = cur.fetchall()
        con.commit()
        con.close()
        return a
    def Auth(self):
        if self.UserEntry.get() == "":
            messagebox.showinfo("Error", lang.AuthNothingEntry)
            return
        if self.PassEntry.get() == "":
            messagebox.showinfo("Error", lang.AuthNothingEntry)
            return
        MID = self.UserEntry.get().encode()
        MHP = self.PassEntry.get().encode()
        

        HashedID = hashlib.sha256(MID).hexdigest()
        HashedPassword = hashlib.sha256(MHP).hexdigest()

        try:
            a = self.GetUsersInfo(HashedID)
            if a[0][3] == HashedPassword:
                self.passed(a)
            else:
                self.missed()
        except:
            self.missed()
            return


    def passed(self, User):
        if root == None or not root.winfo_exists():
            messagebox.showinfo(lang.AuthPassedText, lang.AuthPassedDetails + str(User[0][1]))
            self.AuthWindow.destroy()
            main(User)
        else:
            pass
    def missed(self):
        messagebox.showinfo(lang.AuthMissedText, lang.AuthMissedDetails)


if __name__ == "__main__":
    Authentication()

