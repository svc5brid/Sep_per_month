import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import datetime
import sqlite3
import re

DBName = "TEST.db"

con = sqlite3.connect(DBName)
cur = con.cursor()
try:
    # Userを登録するテーブル
    cur.execute("""CREATE TABLE Users (Name text, ID blog, Password blog)""")
    cur.execute("INSERT INTO Users VALUES('User', 1, 1)")
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
    def __init__(self, lang):
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
        self.AuthWindowUserLabelText = "ユーザー名"
        # 認証画面のパスワード入力フォーム説明用のテキスト
        self.AuthWindowPassLabelText = "パスワード"
        # メインウインドウのログイン中のユーザー表示用テキスト
        self.InformationAboutNowUserText = "ログイン中のユーザー："
        # メインウインドウ、支出登録ボタンのテキスト
        self.RegistButtonText = "支出登録"
        # メインウインドウのリスト確認と変更ボタンのテキスト
        self.ConfirmAndEditButtonText = "リスト確認、変更(変更には権限が必要)"
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
        self.SettingsConfirmButtonText = "確認"
        # 設定画面のユーザーネームのところのテキスト
        self.SettingsUserLabelText = "ユーザー名"
        # ユーザー1の名前
        self.RegistUser1 = "ユーザー1："
        # ユーザー2の名前
        self.RegistUser2 = "ユーザー2："
        # 登録画面のタイトル未入力時のエラーメッセージ
        self.RegistTitleErrorMessage = "タイトルが未入力です。"
        # 登録画面の金額未入力時のエラーメッセージ
        self.RegistAmountErrorMessage = "金額が未入力です。"
        # 登録画面の書き込みOKメッセージ
        self.RegistOK = "完了しました。"
        # 登録画面の書き込みNGメッセージ
        self.RegistNG = "失敗しました。"
    def English(self):
        pass
    def Tame(self):
        pass


# iniファイルを読み込んで、以下の設定を。
# 色を変えるときはテーマを設定できるようにしたいので、classを作成しよう。
lang = Language("Jp")




class main():
    def __init__(self, userID):
        # GUIの作成
        global root
        self.subwindow = None
        self.UserID = userID
        root = Tk()
        root.title(lang.title)
        # ここからパーツ
        UserLabel = ttk.Label(root, text=lang.InformationAboutNowUserText+str(userID))
        RegistButton = ttk.Button(root, text=lang.RegistButtonText, command=lambda:[self.RegistTheCash()])
        ConfirmAndEditButton = ttk.Button(root, text=lang.ConfirmAndEditButtonText, command=lambda:[self.ConfirmAndEdit()])
        OutputTheSheetButton = ttk.Button(root, text=lang.OutputTheSheetText)
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
        if self.subwindow == None or not self.subwindow.winfo_exists():
            self.subwindow = Toplevel(root)
            self.subwindow.title(lang.RegistWindowTitle)
            # ここからパーツ
            self.ClaimValue = IntVar(value=0)

            labelframe = ttk.LabelFrame(self.subwindow, text = lang.RegistLabelFrameText)
            TitleLabel = ttk.Label(labelframe, text = lang.RegistTitleLabelText)
            self.TitleEntry = ttk.Entry(labelframe, width=40)
            AmountLabel = ttk.Label(labelframe, text= lang.RegistAmountLabelText)
            self.AmountEntry = ttk.Entry(labelframe, width=40)

            
            

            DetailsLabel = ttk.Label(labelframe, text=lang.RegistDetailsText)
            self.DetailsEntry = Text(labelframe, width=35, height=10)
            PictureSelectLabel = ttk.Label(labelframe, text=lang.RegistPictureSelectText)
            PathFrame = ttk.Frame(labelframe)
            PictureSelectButton = ttk.Button(PathFrame, text=lang.Reference, command=lambda:[self.GetFilePath()])
            self.PathBox = ttk.Entry(PathFrame, width=25)
            ConfirmButton = ttk.Button(labelframe, text=lang.RegistConfirmButtonText, command=lambda:[self.RegistConfirm()])

            ClaimFrame = ttk.Frame(labelframe)
            ClaimLabel = ttk.Label(labelframe, text = lang.RegistClaimLabelText)
            self.ClaimPartLabel1 = ttk.Label(ClaimFrame, text = lang.RegistUser1 + str(self.ClaimValue.get()))
            self.ClaimPartLabel2 = ttk.Label(ClaimFrame, text = lang.RegistUser2 + str(100 - self.ClaimValue.get()))
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
        b = self.WriteToDB(tuple(a))
        if b == "OK":
            messagebox.showinfo("OK", lang.RegistOK)
            root.lower()
            self.ClearForms()
        else:
            messagebox.showerror("NG", lang.RegistNG)
            root.lower()
        
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


        Value.append(self.UserID)
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
            SearchForms = ttk.Labelframe(self.subwindow, text=lang.CESearchFormsText)
            self.YearPull = ttk.Combobox(SearchForms)
            self.YearPull["values"] = a[0]
            YearLabel = ttk.Label(SearchForms, text=lang.CEYearEntryText)
            SearchButton = ttk.Button(SearchForms, text=lang.CESearchText, command=lambda:[self.CEResultShow(self.YearPull.get())])
            self.SearchedLists = ttk.Labelframe(self.subwindow, text=lang.CEResult)
            # ここから配置
            SearchForms.pack()
            self.YearPull.grid(row=0, column=1, padx=10, pady=10)
            YearLabel.grid(row=0, column=0, padx=10, pady=10)
            SearchButton.grid(row=2, column=1, padx=10, pady=10)
            self.SearchedLists.pack()
            
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
        a = self.CEGetData(YearMonth)
        
        for i in range(len(a)):
            b = ttk.Label(self.SearchedLists, text=a[i][1])
            b.pack()
        pass

    def CEGetData(self, YearMonth):
        con = sqlite3.connect(DBName)
        cur = con.cursor()
        sql = f"SELECT * FROM AllRecords WHERE YearMonth = '{YearMonth}'"
        cur.execute(sql)
        a = cur.fetchall()
        con.commit()
        con.close()
        return a
    
    def Settings(self):
        if self.subwindow == None or not self.subwindow.winfo_exists():
            self.subwindow = Toplevel(root)
            self.subwindow.title(lang.SettingsWindowTitle)
            global Version
            # ここからパーツ
            SettingsFrame = ttk.Labelframe(self.subwindow,text=lang.SettingsFrameTitle)
            VersionLabel = ttk.Label(SettingsFrame, text=lang.SettingsVersionText + Version)
            LanguageLabel = ttk.Label(SettingsFrame, text=lang.SettingsLanguageLabelText)
            self.LanguageBox = ttk.Combobox(SettingsFrame)
            UserNameLabel = ttk.Label(SettingsFrame, text=lang.SettingsUserLabelText)
            UserNameEntry = ttk.Entry(SettingsFrame)
            ConfirmButton = ttk.Button(SettingsFrame, text=lang.SettingsConfirmButtonText)
        

            # ここから配置
            SettingsFrame.pack()
            VersionLabel.grid(row=1, column=0, pady=10, padx=10, columnspan=2)
            LanguageLabel.grid(row=2, column=0, pady=10, padx=10)
            self.LanguageBox.grid(row=2, column=1, pady=10, padx=10)
            UserNameLabel.grid(row=3, column=0, pady=10, padx=10)
            UserNameEntry.grid(row=3, column=1, pady=10, padx=10)
            ConfirmButton.grid(row=4, column=1, pady=10, padx=10)
            
            
        else:
            pass
        pass
        

class Authentication():
    # ここで認証する。認証が終わったら引数にUserIDを渡してmainを実行
    def __init__(self):
        global root
        root = None
        self.AuthWindow = Tk()
        self.AuthWindow.title(lang.AuthWindowTitle)
        # ここからパーツ
        UserEntry = ttk.Entry(self.AuthWindow)
        PassEntry = ttk.Entry(self.AuthWindow)
        UserLabel = ttk.Label(self.AuthWindow, text=lang.AuthWindowUserLabelText)
        PassLabel = ttk.Label(self.AuthWindow, text=lang.AuthWindowPassLabelText)
        ConfirmButton = ttk.Button(self.AuthWindow, text = lang.AuthWindowConfirmText, command=lambda:[self.Auth()])
        # ここから配置
        UserEntry.grid(row=0, column=1, padx=10, pady=10)
        PassEntry.grid(row=1, column=1, padx=10, pady=10)
        UserLabel.grid(row=0, column=0, padx=10, pady=10)
        PassLabel.grid(row=1, column=0, padx=10, pady=10)
        ConfirmButton.grid(row=2, column=1, padx=10, pady=10)
        self.AuthWindow.mainloop()
    # 以下認証関数。戻り値はない。存在しなかった場合はウインドウで通知。した場合もウインドウで通知。
    # とりあえず認証できたということで、ユーザー1にしておく。
    def Auth(self):
        # dbから値取得、認証。
        self.passed(2)
        a = True
        if a == False:
            self.missed()

    def passed(self, User):
        if root == None or not root.winfo_exists():
            messagebox.showinfo(lang.AuthPassedText, lang.AuthPassedDetails + str(User))
            self.AuthWindow.destroy()
            main(User)
        else:
            print("予期せぬErrorが発生しています。作成者に問い合わせてください。")
    def missed(self):
        messagebox.showinfo(lang.AuthMissedText, lang.AuthMissedDetails)


if __name__ == "__main__":
    Authentication()

