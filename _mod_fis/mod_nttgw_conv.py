# 証券番号セット
def mz_syoken_cd_conv(kind_main, main, sub):
    if main == "":
        main = ""
        sub = ""

    if main != "":
        sub = sub.zfill(4)

    # old_syoken_cd
    if kind_main == "AA":
        main = ""
        sub = ""

    return main, sub


# 保険料計算
def mz_hoken_ryo_conv(pay_num_cd, bun, total):
    # 年払い保険料の計算は未完成、符号は無視
    hoken_ryo = 0
    hoken_ryo_year = 0

    if pay_num_cd == "00":  # 一部前納　※生保損保の共通項目で存在しないため合計保険料をセット
        hoken_ryo = total
        hoken_ryo_year = total

    if pay_num_cd == "01":  # A方式 月払
        hoken_ryo = bun
        hoken_ryo_year = bun * 12

    if pay_num_cd == "02":  # B方式
        hoken_ryo = bun
        hoken_ryo_year = bun * 12

    if pay_num_cd == "03":  # C方式
        hoken_ryo = bun
        hoken_ryo_year = bun * 12

    if pay_num_cd == "04":  # D方式
        hoken_ryo = bun
        hoken_ryo_year = bun * 12

    if pay_num_cd == "05":  # 火災価協6分割型　損保マニュアル参照
        hoken_ryo = bun
        hoken_ryo_year = bun * 12

    if pay_num_cd == "06":  # 初回翌月払　損保マニュアル参照　※暫定の計算、分割保険料が0円の場合が存在するので
        if bun == 0:
            hoken_ryo = total
            hoken_ryo_year = total
        else:
            hoken_ryo = bun
            hoken_ryo_year = bun * 12

    if pay_num_cd == "11":  # 1ヶ月おき
        hoken_ryo = bun
        hoken_ryo_year = bun * 12

    if pay_num_cd == "12":  # 2ヶ月おき
        hoken_ryo = bun
        hoken_ryo_year = bun * 6

    if pay_num_cd == "13":  # 3ヶ月おき
        hoken_ryo = bun
        hoken_ryo_year = bun * 4

    if pay_num_cd == "14":  # 半年払
        hoken_ryo = bun
        hoken_ryo_year = bun * 2

    if pay_num_cd == "15":  # 年払
        hoken_ryo = bun
        hoken_ryo_year = bun * 1

    if pay_num_cd == "99":  # その他　※暫定の計算、分割保険料が0円の場合が存在するので
        if bun == 0:
            hoken_ryo = total
            hoken_ryo_year = total
        else:
            hoken_ryo = bun
            hoken_ryo_year = bun * 12

    if pay_num_cd == "":  # データがスペースの場合がある
        hoken_ryo = total
        hoken_ryo_year = total

    return hoken_ryo, hoken_ryo_year


# 異動・解約保険料
def mz_ido_kai_hoken_ryo_conv(fugo, hoken_ryo):
    ido_kai_hoken_ryo = 0

    if hoken_ryo != "":
        if fugo == "{":
            ido_kai_hoken_ryo = int(hoken_ryo) * (10)
        if fugo == "}":
            ido_kai_hoken_ryo = int(hoken_ryo) * (-10)

    return ido_kai_hoken_ryo


# 申込年月日、計上年月、始期年月日、満期年月日、異動解約日
def mz_gene_date_conv(date):
    gene_date = "0"

    if date == "" or date == "999999" or int(date) == 0:
        gene_date = "0"
    else:
        if int(date[0:2]) >= 90:
            gene_date = "19" + date
        else:
            gene_date = "20" + date

    return int(gene_date)


# 契約状況をセットする
def mz_keiyaku_conv(cd, old_ms, ido_reason):
    keiyaku_cd = "1"  # 未設定

    # 新規
    if cd == "init" and old_ms == "":
        keiyaku_cd = "2"

    # 更改
    if cd == "init" and old_ms != "":
        keiyaku_cd = "3"

    # 新規
    if cd == "0" and old_ms == "":
        keiyaku_cd = "2"

    # 更改
    if cd == "0" and old_ms != "":
        keiyaku_cd = "3"

    # 異動
    if cd == "1":
        keiyaku_cd = "7"

    # 解約
    if cd == "2":
        if ido_reason == "23":
            keiyaku_cd = "9"  # 失効
        else:
            keiyaku_cd = "6"  # 解約

    # 未設定
    if cd == "3" or cd == "4" or cd == "5" or cd == "6" or cd == "9":
        keiyaku_cd = "1"

    return keiyaku_cd


# 符号付きのデータを数字に置き換え
def mz_nttgw_fugo_conv(str_data):
    num_data = 0

    if str_data != "":
        fugo = str_data[-1:]  # 符号
        dt = str_data[:-1]  # 符号以外

        if fugo == "{":
            num_data = int(dt + "0")
        if fugo == "A":
            num_data = int(dt + "1")
        if fugo == "B":
            num_data = int(dt + "2")
        if fugo == "C":
            num_data = int(dt + "3")
        if fugo == "D":
            num_data = int(dt + "4")
        if fugo == "E":
            num_data = int(dt + "5")
        if fugo == "F":
            num_data = int(dt + "6")
        if fugo == "G":
            num_data = int(dt + "7")
        if fugo == "H":
            num_data = int(dt + "8")
        if fugo == "I":
            num_data = int(dt + "9")

        if fugo == "}":
            num_data = int(dt + "0") * (-1)
        if fugo == "J":
            num_data = int(dt + "1") * (-1)
        if fugo == "K":
            num_data = int(dt + "2") * (-1)
        if fugo == "L":
            num_data = int(dt + "3") * (-1)
        if fugo == "M":
            num_data = int(dt + "4") * (-1)
        if fugo == "N":
            num_data = int(dt + "5") * (-1)
        if fugo == "O":
            num_data = int(dt + "6") * (-1)
        if fugo == "P":
            num_data = int(dt + "7") * (-1)
        if fugo == "Q":
            num_data = int(dt + "8") * (-1)
        if fugo == "R":
            num_data = int(dt + "9") * (-1)

    return num_data


# ngw 消費税区分 0=5%, 1=3%, 2=0%, 3=8%, 4=10%
def mz_ngw_tax_kubun_conv(tax_kubun):
    result_tax = 0

    if tax_kubun == "0":
        result_tax = 5
    if tax_kubun == "1":
        result_tax = 3
    if tax_kubun == "2":
        result_tax = 0
    if tax_kubun == "3":
        result_tax = 8
    if tax_kubun == "4":
        result_tax = 10

    return result_tax


# アクセス用データを作成するために契約状況を作成する。MS Accessなので使用していない。
# def mz_access_keiyaku_cd_conv(keiyaku_cd):

#     # fis -> Tnet(nttgw)
#     # 1未設定 -> 0
#     # 2新規 -> 0
#     # 3更改 -> 0
#     # 4満期落ち -> 2
#     # 6解約 -> 2
#     # 7異動 -> 1

#     keiyaku_cd_conv = 0

#     if keiyaku_cd == '1' or keiyaku_cd == '2' or keiyaku_cd == '3':
#         keiyaku_cd_conv = '0'

#     if keiyaku_cd == '4' or keiyaku_cd == '6':
#         keiyaku_cd_conv = '2'

#     if keiyaku_cd == '7':
#         keiyaku_cd_conv = '1'

#     return keiyaku_cd_conv
