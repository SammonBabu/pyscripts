import requests,re,json
from bs4 import BeautifulSoup


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
    }

params = {
    "q": "google logo",          # search query
    "tbm": "isch",                # image results
    "hl": "en",                   # language of the search
    "gl": "us",                   # country where search comes from
    "ijn": "0"                    # page number
}

html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
soup = BeautifulSoup(html.text, "lxml")
all_script_tags = soup.select("script")

# # https://regex101.com/r/48UZhY/4
matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))

matched_images_data_fix = json.dumps(matched_images_data)
matched_images_data_json = json.loads(matched_images_data_fix)
matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",', matched_images_data_json)

# f = open( 'test.json', 'w' )
# f.write(matched_images_data_json)

matched_google_images_thumbnails = ", ".join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_images_data_json))).split(", ")
print(matched_google_images_thumbnails[0])
print("------------------------------------------------------------")
print(matched_google_image_data)

# a = []
# for results in soup.select('.isv-r.PNCib.MSM1fd.BUooTd'):
#     try:
#         title = results.select_one('.bytUYc').text
#     except:
#         title = ""
#     try:
#         link = results.select_one('.bRMDJf.islir').img['src']
#     except:
#         link = ""
#     # displayed_link = results.select_one('.TbwUpd.NJjxre').text
#     # snippet = results.select_one('.aCOpRe span').text
#     # uploaded_by = results.select_one('.uo4vr span').text.split(' ')[2]
#     # upload_date = results.select_one('.fG8Fp.uo4vr').text.split(' · ')[0]
#     # print(f'{title}\n{link}\n{displayed_link}\n{snippet}\n{upload_date}\n{uploaded_by}\n')
#     a.append({
#         "title":title,
#         "link":link
#     })
# print(a[0])