def mz_siki_manki_date_str(siki_manki_date):
    siki_manki_date_str = ""

    if siki_manki_date == 0:
        siki_manki_date_str = "0"
    else:
        str_date = str(siki_manki_date)
        yy = str_date[0:4]
        mm = str_date[4:6]
        dd = str_date[6:8]
        siki_manki_date_str = yy + "/" + mm + "/" + dd

    return siki_manki_date_str
