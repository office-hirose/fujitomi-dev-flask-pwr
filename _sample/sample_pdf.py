import io
import random

# Reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import cm, mm
from reportlab.graphics import shapes, renderPDF
from reportlab.graphics.barcode import code39, eanbc, qr


def pdf_download(kind):
    if kind == "pdf_basic":
        create_file, mime_type, file_name = pdf_basic()
    if kind == "pdf_line":
        create_file, mime_type, file_name = pdf_line()
    if kind == "pdf_randam":
        create_file, mime_type, file_name = pdf_randam()
    if kind == "pdf_barcode":
        create_file, mime_type, file_name = pdf_barcode()
    if kind == "pdf_ean":
        create_file, mime_type, file_name = pdf_ean()
    if kind == "pdf_qr":
        create_file, mime_type, file_name = pdf_qr()
    return create_file, mime_type, file_name


def pdf_basic():
    # PDF create section
    pdffile = io.BytesIO()
    c = canvas.Canvas(pdffile, pagesize=A4)
    c.setAuthor("tom")
    c.setTitle("PDF生成")
    c.setSubject("サンプル")

    # A4 size
    # c.setPageSize((210 * mm, 297 * mm))
    # B5 size
    # c.setPageSize((18.2 * cm,25.7 * cm))

    # font
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

    # --- page 1 ---

    # 文字
    c.setFont("HeiseiKakuGo-W5", 12)
    c.drawString(1 * cm, 28 * cm, "あいうえお")
    c.setFont("HeiseiKakuGo-W5", 14)
    c.drawString(1 * cm, 27 * cm, "かきくけこ")

    # 線
    c.setLineWidth(1)
    c.line(1 * cm, 26 * cm, 20 * cm, 26 * cm)

    # 四角 青い箱
    c.setFillColorRGB(0, 0, 100)
    c.rect(5 * cm, 20 * cm, 3 * cm, 3 * cm, stroke=1, fill=1)
    c.setFillColorRGB(0, 0, 0)

    # 文字カラー
    c.setFont("HeiseiKakuGo-W5", 14)

    arr = ["black", "red", "blue", "grey"]
    y = 1

    for i in arr:
        c.setFillColor(i)
        c.drawString(1 * cm, (25 - y) * cm, "あいうえお")
        y = y + 1

    # 1ページ確定
    c.showPage()

    # --- page 2 ---

    # 文字サイズ
    c.setFont("HeiseiKakuGo-W5", 8)
    c.drawString(5 * cm, 27 * cm, "文字サイズ 8point")

    c.setFont("HeiseiKakuGo-W5", 9)
    c.drawString(5 * cm, 26 * cm, "文字サイズ 9point")

    c.setFont("HeiseiKakuGo-W5", 10)
    c.drawString(5 * cm, 25 * cm, "文字サイズ 10point")

    c.setFont("HeiseiKakuGo-W5", 11)
    c.drawString(5 * cm, 24 * cm, "文字サイズ 11point")

    c.setFont("HeiseiKakuGo-W5", 12)
    c.drawString(5 * cm, 23 * cm, "文字サイズ 12point")

    c.setFont("HeiseiKakuGo-W5", 13)
    c.drawString(5 * cm, 22 * cm, "文字サイズ 13point")

    c.setFont("HeiseiKakuGo-W5", 14)
    c.drawString(5 * cm, 21 * cm, "文字サイズ 14point")

    c.setFont("HeiseiKakuGo-W5", 15)
    c.drawString(5 * cm, 20 * cm, "文字サイズ 15point")

    c.setFont("HeiseiKakuGo-W5", 16)
    c.drawString(5 * cm, 19 * cm, "文字サイズ 16point")

    c.setFont("HeiseiKakuGo-W5", 18)
    c.drawString(5 * cm, 18 * cm, "文字サイズ 18point")

    c.setFont("HeiseiKakuGo-W5", 20)
    c.drawString(5 * cm, 17 * cm, "文字サイズ 20point")

    c.setFont("HeiseiKakuGo-W5", 22)
    c.drawString(5 * cm, 15 * cm, "文字サイズ 22point")

    c.setFont("HeiseiKakuGo-W5", 24)
    c.drawString(5 * cm, 13 * cm, "文字サイズ 24point")

    c.setFont("HeiseiKakuGo-W5", 26)
    c.drawString(5 * cm, 11 * cm, "文字サイズ 26point")

    c.setFont("HeiseiKakuGo-W5", 28)
    c.drawString(5 * cm, 9 * cm, "文字サイズ 28point")

    c.setFont("HeiseiKakuGo-W5", 30)
    c.drawString(5 * cm, 7 * cm, "文字サイズ 30point")

    c.setFont("HeiseiKakuGo-W5", 32)
    c.drawString(5 * cm, 5 * cm, "文字サイズ 32point")

    # 2ページ確定
    c.showPage()

    # --- page 3 ---

    # init
    c.setFont("HeiseiKakuGo-W5", 6)
    c.setLineWidth(0.1)

    # c.drawString(88 * mm, 186 * mm, 'aaaaa')

    # 罫線ヨコ
    x = 0
    xadd = 10
    for text in range(21):
        c.line((x + xadd) * mm, 297 * mm, (x + xadd) * mm, 0 * mm)
        c.drawCentredString((x + xadd - 2) * mm, 295 * mm, str(text + 1) + "0")
        xadd = xadd + 10

    # 罫線タテ
    range_list = [
        29,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        18,
        17,
        16,
        15,
        14,
        13,
        12,
        11,
        10,
        9,
        8,
        7,
        6,
        5,
        4,
        3,
        2,
        1,
    ]
    y = 297
    yadd = -10
    for text in range_list:
        c.line(0 * mm, (y + yadd) * mm, 210 * mm, (y + yadd) * mm)
        c.drawCentredString(5 * mm, (y + yadd + 1) * mm, str(text) + "0")
        yadd = yadd - 10

    # 3ページ確定
    c.showPage()

    # save
    c.save()

    # create pdf
    create_file = pdffile.getvalue()
    mime_type = "application/pdf;"
    file_name = "pdf_basic.pdf"
    return create_file, mime_type, file_name


def pdf_line():
    # PDF create section
    pdffile = io.BytesIO()
    c = canvas.Canvas(pdffile, pagesize=A4)
    c.setAuthor("tom")
    c.setTitle("PDF生成 / line")
    c.setSubject("サンプル")
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))  # font

    xmargin = 0.84 * cm
    ymargin = 0.88 * cm
    swidth = 4.83 * cm
    sheight = 2.54 * cm

    def draw_label(c, x, y, data):
        c.setLineWidth(0.5)
        c.rect(x, y, 4.83 * cm, 2.54 * cm, stroke=1, fill=0)
        c.drawString(x, y, str(data))

    for i in range(44):
        # オフセット位置
        x = xmargin + swidth * (i % 4)
        y = ymargin + sheight * (10 - (i // 4))
        # ラベル印刷
        draw_label(c, x, y, i)

    # save
    c.showPage()
    c.save()

    # create pdf
    create_file = pdffile.getvalue()
    mime_type = "application/pdf"
    file_name = "pdf_line.pdf"
    return create_file, mime_type, file_name


def pdf_randam():
    # PDF create section
    pdffile = io.BytesIO()
    c = canvas.Canvas(pdffile, pagesize=A4)
    c.setAuthor("tom")
    c.setTitle("PDF生成 / randam")
    c.setSubject("サンプル")
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))  # font

    xmargin = 0.84 * cm
    ymargin = 0.88 * cm
    swidth = 4.83 * cm
    sheight = 2.54 * cm

    def get_random_code():
        s = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join([random.choice(s) for i in range(8)])

    def draw_label(c, x, y, data):
        c.setLineWidth(0.5)
        c.rect(x, y, 4.83 * cm, 2.54 * cm, stroke=1, fill=0)
        c.drawString(x + 1.46 * cm, y + 1.34 * cm, data)

    for i in range(44):
        # オフセット位置
        x = xmargin + swidth * (i % 4)
        y = ymargin + sheight * (10 - (i // 4))
        # ラベル固有のデータ
        code = get_random_code()
        # ラベル印刷
        draw_label(c, x, y, code)

    # save
    c.showPage()
    c.save()

    # create pdf
    create_file = pdffile.getvalue()
    mime_type = "application/pdf"
    file_name = "pdf_randam.pdf"
    return create_file, mime_type, file_name


def pdf_barcode():
    # PDF create section
    pdffile = io.BytesIO()
    c = canvas.Canvas(pdffile, pagesize=A4)
    c.setAuthor("tom")
    c.setTitle("PDF生成 / barcode")
    c.setSubject("サンプル")
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))  # font

    xmargin = 0.84 * cm
    ymargin = 0.88 * cm
    swidth = 4.83 * cm
    sheight = 2.54 * cm

    def get_random_code():
        s = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join([random.choice(s) for i in range(8)])

    def draw_label(c, x, y, data):
        c.setLineWidth(0.5)
        c.rect(x, y, 4.83 * cm, 2.54 * cm, stroke=1, fill=0)
        c.drawString(x + 1.46 * cm, y + 1.34 * cm, data)
        barcode = code39.Standard39("*" + data + "*", barWidth=0.026 * cm, barHeight=0.8 * cm, checksum=False)
        barcode.drawOn(c, x, y + 0.34 * cm)

    for i in range(44):
        # オフセット位置
        x = xmargin + swidth * (i % 4)
        y = ymargin + sheight * (10 - (i // 4))
        # ラベル固有のデータ
        code = get_random_code()
        # ラベル印刷
        draw_label(c, x, y, code)

    # save
    c.showPage()
    c.save()

    # create pdf
    create_file = pdffile.getvalue()
    mime_type = "application/pdf"
    file_name = "pdf_barcode.pdf"
    return create_file, mime_type, file_name


def pdf_ean():
    # PDF create section
    pdffile = io.BytesIO()
    c = canvas.Canvas(pdffile, pagesize=A4)
    c.setAuthor("tom")
    c.setTitle("PDF生成 / ean")
    c.setSubject("サンプル")
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))  # font

    xmargin = 8.4 * mm
    ymargin = 8.8 * mm
    swidth = 96.6 * mm
    sheight = 25.4 * mm

    def draw_label(c, x, y, data):
        c.setLineWidth(0.5)
        c.rect(x, y, 96.6 * mm, 25.4 * mm, stroke=1, fill=0)  # 線を表示する場合 storoke=1
        dmy = shapes.Drawing(int(0 * mm), int(0 * mm))
        barcode = eanbc.Ean13BarcodeWidget(data, barWidth=0.264 * mm, barHeight=18.29 * mm)
        dmy.add(barcode)
        renderPDF.draw(dmy, c, x + 35 * mm, y + 3.5 * mm)

    for i in range(22):
        # オフセット位置
        x = xmargin + swidth * (i % 2)
        y = ymargin + sheight * (10 - (i // 2))
        code = "4902011711936"
        # ラベル印刷
        draw_label(c, x, y, code)

    # save
    c.showPage()
    c.save()

    # create pdf
    create_file = pdffile.getvalue()
    mime_type = "application/pdf"
    file_name = "pdf_ean.pdf"
    return create_file, mime_type, file_name


def pdf_qr():
    # PDF create section
    pdffile = io.BytesIO()
    c = canvas.Canvas(pdffile, pagesize=A4)
    c.setAuthor("tom")
    c.setTitle("PDF生成 / qr")
    c.setSubject("サンプル")
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))  # font

    xmargin = 8.4 * mm
    ymargin = 8.8 * mm
    swidth = 96.6 * mm
    sheight = 25.4 * mm

    def draw_label(c, x, y, data):
        c.setLineWidth(0.5)
        c.rect(x, y, 96.6 * mm, 25.4 * mm, stroke=1, fill=0)  # 線を表示する場合 storoke=1
        dmy = shapes.Drawing(int(0 * mm), int(0 * mm))
        qrcode = qr.QrCodeWidget(data, barWidth=20 * mm, barHeight=20 * mm)
        dmy.add(qrcode)
        renderPDF.draw(dmy, c, x + 40 * mm, y + 1.5 * mm)

    for i in range(22):
        # オフセット位置
        x = xmargin + swidth * (i % 2)
        y = ymargin + sheight * (10 - (i // 2))
        code = "www.google.com"
        # ラベル印刷
        draw_label(c, x, y, code)

    # save
    c.showPage()
    c.save()

    # create pdf
    create_file = pdffile.getvalue()
    mime_type = "application/pdf"
    file_name = "pdf_qr.pdf"
    return create_file, mime_type, file_name
