# zipcode hyphen, 1010021 -> 101-0021
def mz_zipcd_hyphen_ari(zipcd):
    if zipcd == "":
        zipcd_hyphen = ""
    else:
        zipcd3 = zipcd[0:3]
        zipcd4 = zipcd[3:7]
        zipcd_hyphen = zipcd3 + "-" + zipcd4
    return zipcd_hyphen


# zipcode split, 101-0021 -> 101 0021
def mz_zipcd_split_hyphen_ari(zipcd):
    zipcd3 = zipcd[0:3]
    zipcd4 = zipcd[4:9]
    return zipcd3, zipcd4


# zipcode split, 1010021 -> 101 0021
def mz_zipcd_split_hyphen_nasi(zipcd):
    zipcd3 = zipcd[0:3]
    zipcd4 = zipcd[3:8]
    return zipcd3, zipcd4
