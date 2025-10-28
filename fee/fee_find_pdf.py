import io
import sys
import json
import datetime
from flask import request
from _mod import mod_base, mod_datetime, mod_other

# from _mod_fis import mod_common
from fee import fee_find_sql

# Reportlab
from reportlab.pdfgen import canvas

# from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm

# from reportlab.graphics import shapes, renderPDF
# from reportlab.graphics.barcode import code39, eanbc, qr


def fee_pdf():
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
        c.setTitle("実収手数料リスト-" + file_name_datetime)
        c.setSubject("実収手数料リスト-" + file_name_datetime)

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

        key_list_obj = json.loads(key_list)
        for id in key_list_obj:
            sql_data = fee_find_sql.pdf_sql(id)
            for dt in sql_data:
                nyu_date = mod_datetime.mz_mum2str_yymmdd_nen_tuki(dt["nyu_date"])
                siki_date = "始:" + mod_datetime.mz_num2date_hyphen(dt["siki_date"])
                manki_date = "満:" + mod_datetime.mz_num2date_hyphen(dt["manki_date"])
                section_name = dt["section_name"]

                coltd_name = dt["coltd_name"]
                syoken_cd_all = dt["syoken_cd_main"] + "-" + dt["syoken_cd_sub"]
                kei_name = dt["kei_name"]

                fee_num = mod_other.num_comma(dt["fee_num"])
                pay_num_name = dt["pay_num_name"]
                kaime = dt["kaime"] + "回目"
                kind_name = dt["kind_name"]

                staff_name = dt["staff_name"]

                gyotei_name = dt["gyotei_name"]
                if gyotei_name is None:
                    gyotei_name = ""

                pay_fee_per = str(dt["pay_fee_per"]) + "%"
                pay_fee_yen = mod_other.num_comma(dt["pay_fee_yen"])

                pay_gyotei_1year_over_name = dt["pay_gyotei_1year_over_name"]

            takasa = i * 18
            tate = 210 - takasa

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawCentredString(9 * mm, (tate + 1) * mm, str(cnt))

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawString(15 * mm, (tate + 1) * mm, nyu_date)
            c.drawString(15 * mm, (tate - 3) * mm, siki_date)
            c.drawString(15 * mm, (tate - 7) * mm, manki_date)
            c.drawString(15 * mm, (tate - 11) * mm, section_name)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawString(48 * mm, (tate + 1) * mm, coltd_name)
            c.drawString(48 * mm, (tate - 3) * mm, syoken_cd_all)
            c.drawString(48 * mm, (tate - 7) * mm, kei_name)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawRightString(152 * mm, (tate + 1) * mm, fee_num)
            c.drawRightString(152 * mm, (tate - 3) * mm, pay_num_name)
            c.drawRightString(152 * mm, (tate - 7) * mm, kaime)
            c.drawRightString(152 * mm, (tate - 11) * mm, kind_name)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawRightString(181 * mm, (tate + 1) * mm, staff_name)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawRightString(217 * mm, (tate + 1) * mm, gyotei_name)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawRightString(252 * mm, (tate + 1) * mm, pay_fee_per)

            c.setFont("HeiseiKakuGo-W5", 7)
            c.drawRightString(292 * mm, (tate + 1) * mm, pay_fee_yen)
            c.drawRightString(292 * mm, (tate - 11) * mm, pay_gyotei_1year_over_name)

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
    c.drawString(15 * mm, 198.5 * mm, "実収入金年月/営業所")
    c.drawString(48 * mm, 198.5 * mm, "保険会社/証券番号/契約者")
    c.drawRightString(152 * mm, 198.5 * mm, "手数料合計/払込方法/回目/種類")
    c.drawRightString(181 * mm, 198.5 * mm, "担当")
    c.drawRightString(217 * mm, 198.5 * mm, "提携")
    c.drawRightString(252 * mm, 198.5 * mm, "手数料配分(率)")
    c.drawRightString(292 * mm, 198.5 * mm, "手数料配分(円)")

    # sub title line
    c.setLineWidth(0.1)
    c.line(3 * mm, 197 * mm, 295 * mm, 197 * mm)
