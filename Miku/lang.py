import os
import yaml

languages = {}


def get_string(lang: str):
    return languages[lang]


for filename in os.listdir(r"./lang/langs/"):
    if "en" not in languages:
        languages["en"] = yaml.safe_load(
            open(r"./lang/langs/en.yml", encoding="utf8")
        )
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "en":
            continue
        languages[language_name] = yaml.safe_load(
            open(r"./lang/langs/" + filename, encoding="utf8")
        )
        for item in languages["en"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["en"][item]
