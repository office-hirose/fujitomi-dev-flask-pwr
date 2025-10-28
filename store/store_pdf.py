import io
import sys
import json
import datetime

# from typing import Any, Dict, List
from flask import request
from _mod import mod_base, mod_datetime, mod_other
from _mod_fis import mod_common, mod_hoken_kikan
from store import store_sql

# Reportlab
from reportlab.pdfgen import canvas

# from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm

# from reportlab.graphics import shapes, renderPDF
# from reportlab.graphics.barcode import code39, eanbc, qr


def store_pdf():
    # obj
    obj = request.get_json()
    jwtg = obj["jwtg"]
    key_list = obj["key_list"]

    # base - level 2
    base_data = mod_base.mz_base(2, jwtg, sys._getframe().f_code.co_name)
    level_error = base_data["level_error"]
    user_email = base_data["google_account_email"]

    if level_error == "error":
        create_file = ""
        mime_type = ""
        file_name = ""
    else:
        # PDF create section
        file_name_datetime = mod_datetime.mz_tnow("for_filename_yyyy_mmdd_hhmm")

        pdffile = io.BytesIO()
        c = canvas.Canvas(pdffile)
        c.setAuthor(user_email)
        c.setTitle("リスト-" + file_name_datetime)
        c.setSubject("リスト-" + file_name_datetime)

        # A4 size yoko tate
        c.setPageSize((297 * mm, 210 * mm))
        # c.setPageSize((210 * mm, 297 * mm))

        # font
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

        # PDF file title, now datetime
        datetime_jp = datetime.datetime.now() + datetime.timedelta(hours=9)
        now_datetime = str(mod_datetime.mz_dt2str_yymmddhhmm_hyphen(datetime_jp))

        # int
        i = 1
        cnt = 1
        page = 1

        # title
        title(c, now_datetime, user_email, page)

        for fis_cd in key_list:
            # sql
            sql_data = store_sql.pdf_sql(fis_cd)
            for dt in sql_data:
                cat_cd = dt["cat_cd"]
                keiyaku_name = dt["keiyaku_name"]
                exe_sta = mod_common.mz_exe_sta_result(dt["exe_sta"])
                siki_date = "始:" + mod_datetime.mz_num2date_hyphen(dt["siki_date"])
                manki_date = "満:" + mod_datetime.mz_num2date_hyphen(dt["manki_date"])
                ido_kai_date = "異:" + mod_datetime.mz_num2date_hyphen(dt["ido_kai_date"])

                syoken_cd_all = dt["syoken_cd_main"] + "-" + dt["syoken_cd_sub"]
                old_syoken_cd_all = dt["old_syoken_cd_main"] + "-" + dt["old_syoken_cd_sub"]

                keijyo_date = mod_common.mz_keijyo_date_str(dt["keijyo_date"])

                coltd_name_simple = dt["coltd_name"]
                kind_name_main = dt["kind_name_main"]
                kind_name_sub = dt["kind_name_sub"]
                kind_name_ms = kind_name_main + " | " + kind_name_sub
                kei_name = dt["kei_name"]

                pay_num_name = dt["pay_num_name"]

                if dt["hoken_kikan_cd"] == "9999":
                    hoken_kikan = str(dt["hoken_kikan_year"]) + "年"
                else:
                    hoken_kikan = mod_hoken_kikan.mz_hoken_kikan_name(dt["hoken_kikan_cd"])

                hoken_ryo = mod_other.num_comma(dt["hoken_ryo"])
                # hoken_ryo_year = mod_other.num_comma(dt['hoken_ryo_year'])
                ido_kai_hoken_ryo = mod_other.num_comma(dt["ido_kai_hoken_ryo"])

                section_name = dt["section_name"]
                staff1_name_simple = dt["staff1_name"]
                staff2_name_simple = dt["staff2_name"]
                staff3_name_simple = dt["staff3_name"]
                gyotei1_name = dt["gyotei1_name"]
                gyotei2_name = dt["gyotei2_name"]
                gyotei3_name = dt["gyotei3_name"]

                fee_staff1 = str(dt["fee_staff1"])
                fee_staff2 = str(dt["fee_staff2"])
                fee_staff3 = str(dt["fee_staff3"])
                fee_gyotei1 = str(dt["fee_gyotei1"])
                fee_gyotei2 = str(dt["fee_gyotei2"])
                fee_gyotei3 = str(dt["fee_gyotei3"])

                fee_ritu_str = str(dt["fee_ritu"]) + "%"

                # 生保
                fee_seiho_kikan = mod_other.num_comma(dt["fee_seiho_kikan"])
                fee_seiho_first = mod_other.num_comma(dt["fee_seiho_first"])
                fee_seiho_next = mod_other.num_comma(dt["fee_seiho_next"])

                # memo_json
                # memo = mod_common.mz_memo_slice(dt["memo"])
                memo_json_obj = json.loads(dt["memo_json"])
                if len(memo_json_obj) == 0:
                    res_memo_json = ""
                else:
                    for dt in memo_json_obj:
                        res_memo_json = dt["text"]
                        break

            takasa = i * 18
            tate = 210 - takasa

            # QR
            # qr_base = shapes.Drawing(0 * mm, 0 * mm)
            # qr_code = qr.QrCodeWidget(fis_cd, barWidth=15 * mm, barHeight=15 * mm)
            # qr_base.add(qr_code)
            # renderPDF.draw(qr_base, c, 8.5 * mm, (tate - 11.5) * mm, showBoundary=1)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawCentredString(9 * mm, (tate + 1) * mm, str(cnt))
            c.drawCentredString(9 * mm, (tate - 3) * mm, keiyaku_name)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawString(15 * mm, (tate + 1) * mm, siki_date)
            c.drawString(15 * mm, (tate - 3) * mm, manki_date)
            c.drawString(15 * mm, (tate - 7) * mm, ido_kai_date)
            c.drawString(15 * mm, (tate - 11) * mm, exe_sta)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawString(43 * mm, (tate + 1) * mm, syoken_cd_all)
            c.setFont("HeiseiKakuGo-W5", 6)
            c.drawString(43 * mm, (tate - 3) * mm, old_syoken_cd_all)
            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawString(43 * mm, (tate - 7) * mm, section_name)
            c.drawString(43 * mm, (tate - 11) * mm, keijyo_date)

            c.drawString(80 * mm, (tate + 1) * mm, coltd_name_simple)
            c.drawString(80 * mm, (tate - 3) * mm, kind_name_ms)
            c.drawString(80 * mm, (tate - 7) * mm, kei_name)
            c.setFont("HeiseiKakuGo-W5", 6)
            c.drawString(80 * mm, (tate - 11) * mm, res_memo_json)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawRightString(202 * mm, (tate + 1) * mm, pay_num_name)
            c.drawRightString(202 * mm, (tate - 3) * mm, hoken_kikan)
            c.drawRightString(202 * mm, (tate - 7) * mm, str(hoken_ryo) + "円")
            # c.drawRightString(202 * mm, (tate - 11) * mm, hoken_ryo_year + '円')
            c.drawRightString(202 * mm, (tate - 11) * mm, str(ido_kai_hoken_ryo) + "円")

            c.setFont("HeiseiKakuGo-W5", 6)
            # c.drawString(205 * mm, (tate + 1) * mm, staff1_name_simple + '@' + section_name)
            c.drawString(205 * mm, (tate + 1) * mm, staff1_name_simple)
            c.drawString(205 * mm, (tate - 1.5) * mm, staff2_name_simple)
            c.drawString(205 * mm, (tate - 4) * mm, staff3_name_simple)
            c.drawString(205 * mm, (tate - 6.5) * mm, gyotei1_name[0:10])
            c.drawString(205 * mm, (tate - 9) * mm, gyotei2_name[0:10])
            c.drawString(205 * mm, (tate - 11.5) * mm, gyotei3_name[0:10])

            c.drawRightString(237 * mm, (tate + 1) * mm, fee_staff1)
            c.drawRightString(237 * mm, (tate - 1.5) * mm, fee_staff2)
            c.drawRightString(237 * mm, (tate - 4) * mm, fee_staff3)
            c.drawRightString(237 * mm, (tate - 6.5) * mm, fee_gyotei1)
            c.drawRightString(237 * mm, (tate - 9) * mm, fee_gyotei2)
            c.drawRightString(237 * mm, (tate - 11.5) * mm, fee_gyotei3)

            # 生保
            if cat_cd == "1":
                c.drawString(240 * mm, (tate + 1) * mm, "手数料支払年数")
                c.drawString(240 * mm, (tate - 3) * mm, "初年度手数料")
                c.drawString(240 * mm, (tate - 7) * mm, "次年度以降の年間手数料")
                c.drawRightString(292 * mm, (tate + 1) * mm, str(fee_seiho_kikan) + "年")
                c.drawRightString(292 * mm, (tate - 3) * mm, str(fee_seiho_first) + "円")
                c.drawRightString(292 * mm, (tate - 7) * mm, str(fee_seiho_next) + "円")

            # 損保・少短
            if cat_cd == "2" or cat_cd == "3":
                c.setFont("HeiseiKakuGo-W5", 7)
                c.drawString(240 * mm, (tate + 1) * mm, "手数料(概算)")
                c.drawRightString(292 * mm, (tate + 1) * mm, fee_ritu_str)

            # line yoko
            c.setLineWidth(0.1)
            c.line(3 * mm, (tate - 13) * mm, 295 * mm, (tate - 13) * mm)

            # line tate
            # c.line(166 * mm, (tate + 4) * mm, 166 * mm, (tate - 12) * mm)

            # next page
            if (i % 10) == 0:
                # ページ確定
                c.showPage()
                page = page + 1

                # create title
                title(c, now_datetime, user_email, page)

                i = 0

            i = i + 1
            cnt = cnt + 1

        # ページ確定
        c.showPage()

        # 保存
        c.save()

        # create pdf
        create_file = pdffile.getvalue()
        mime_type = "application/pdf"
        file_name = "temp.pdf"

        # base - level 2 - access log only
        acc_page_name = sys._getframe().f_code.co_name
        mod_base.mz_base(2, jwtg, acc_page_name)

    return create_file, mime_type, file_name


# main title
def title(c, now_datetime, user_email, page):
    # date, page number
    c.setFont("HeiseiKakuGo-W5", 7)
    c.drawString(15 * mm, 203 * mm, "印刷日時:" + now_datetime)
    c.drawRightString(292 * mm, 203 * mm, "page:" + str(page))

    # main title line
    c.setLineWidth(0.1)
    c.line(3 * mm, 202 * mm, 295 * mm, 202 * mm)

    # sub title
    c.drawString(15 * mm, 198.5 * mm, "始期/満期/異動")
    c.drawString(43 * mm, 198.5 * mm, "証番/旧証番/営業所/社内計上月")
    c.drawString(80 * mm, 198.5 * mm, "保険会社/種目/種類/契約者名/メモ")
    c.drawRightString(202 * mm, 198.5 * mm, "払込方法/保険期間/保険料/異解保険料")
    c.drawString(205 * mm, 198.5 * mm, "担当/提携")
    c.drawRightString(237 * mm, 198.5 * mm, "手数料配分")
    c.drawRightString(292 * mm, 198.5 * mm, "手数料")

    # sub title line
    c.setLineWidth(0.1)
    c.line(3 * mm, 197 * mm, 295 * mm, 197 * mm)
