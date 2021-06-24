from utils import generate_md_file
import bibtexparser
from config import *

file_name = 'bibtex.bib'
with open(file_name) as bibtex_file:
    bibtex_str = bibtex_file.read()
bib_db = bibtexparser.loads(bibtex_str, parser=bibtexparser.bparser.BibTexParser(ignore_nonstandard_types=False))


def check_repetition(DB=bib_db):
    bib_dict = {}
    for entry in DB.entries:
        title = entry["title"]
        title = str(title).strip()
        title = title.replace("{", "").replace("}", "")
        if title in bib_dict.keys():
            bib_dict[title] = bib_dict[title] + 1
        else:
            bib_dict[title] = 1
    repet_bib = [i for i in bib_dict.keys() if bib_dict[i] > 1]
    
    if len(repet_bib) != 0:
        print("Attention! Repetition detected in the bibtex file! Please check the following entries:")
        print("---------------------------")
    for i, title in enumerate(repet_bib):
        print(i + 1, title)


def plot_titles(titles):
    return '\n' + "## " + titles[0] + '\n'


def get_outline(list_classif, count_list, filename, dicrib, add_hyperlink=False):
    if filename.startswith("" + your_research_topic + "4nlp"):
        str_outline = "# " + your_research_topic_full_name + " Literature in NLP \n"
    elif filename.startswith("" + your_research_topic + "4cv"):
        str_outline = "# " + your_research_topic_full_name + " Literature in CV \n"
    else:
        str_outline = "# " + your_research_topic_full_name + " Literature \n"
    
    # Todo 1: Change to your description
    str_outline += "This repository is maintained by [{author_info}]({personal_link}). " \
                   "Please don't hesitate to send me an email to collaborate or fix some entries (wutong8023 AT gmail.com). \n" \
                   "The automation script of this repo is powered by " \
                   "[Auto-Bibfile](https://github.com/wutong8023/Auto-Bibfile.git).\n\n".format(author_info=author_info,
                                                                                                personal_link=personal_link)
    str_outline += dicrib + "\n\n"
    
    str_outline += "## Outline \n"
    
    if add_hyperlink:
        hyperlink = "![](https://img.shields.io/badge/Hyperlink-blue)"
        link = base_link + filename + '#hyperlink'
        str_outline += "- [" + hyperlink + "](" + link + ')\n'
    
    for i, item in enumerate(list_classif):
        paper_number = "![](https://img.shields.io/badge/{}-{}-blue)".format(
            item[0].replace(" ", "_").replace("-", "_"), str(count_list[i]))
        link = base_link + "" + filename + "#" + item[0].replace(" ", "-").lower()
        paper_number = "[{}]({})".format(paper_number, link)
        
        str_outline += "- " + paper_number + '\n'
    
    return str_outline


def get_hyperlink(hyperlinks, mapping_name):
    str_hyperlink = "## Hyperlink \n"
    
    # Todo 2: Change to your own link
    # Note: please check the branch name carefully!
    str_hyperlink += "- Homepage [Overview](" + base_link + "README.md)\n"
    for i, item in enumerate(hyperlinks):
        str_hyperlink += "- " + mapping_name[item]
        all_link = "![](https://img.shields.io/badge/ALL-green)"
        nlp_link = "![](https://img.shields.io/badge/NLP-green)"
        cv_link = "![](https://img.shields.io/badge/CV-green)"
        
        str_hyperlink += " of [All](" + base_link + "" + your_research_topic + "4all/" + item + ')'
        str_hyperlink += " | [NLP](" + base_link + "" + your_research_topic + "4nlp/" + item + ')'
        str_hyperlink += " | [CV](" + base_link + "" + your_research_topic + "4cv" + item + ')\n'
    
    return str_hyperlink


def plot_content(index, keys, dir_path, disc, list_type, plot_titles=plot_titles, sub_dirs=None, mapping_name=None):
    generate_md_file(DB=bib_db, list_classif=list_type, key=keys, plot_title_fct=plot_titles,
                     filename="README.md", add_comments=True, dir_path=sub_dirs[0][index], filter_key="keywords",
                     filter_content=["NLP", "Multi-Modal"], mapping_name=mapping_name,
                     discrib=disc + ", filtered by NLP area.", add_hyperlink=True, hyperlinks=dir_path,
                     get_outline=get_outline, get_hyperlink=get_hyperlink)
    generate_md_file(DB=bib_db, list_classif=list_type, key=keys, plot_title_fct=plot_titles,
                     filename="README.md", add_comments=True, dir_path=sub_dirs[1][index],
                     filter_key="keywords", mapping_name=mapping_name,
                     filter_content=["CV", "Multi-Modal", ],
                     discrib=disc + ", filtered by CV area.", add_hyperlink=True,
                     hyperlinks=dir_path, get_outline=get_outline, get_hyperlink=get_hyperlink)
    for dir_ in [sub_dirs[2][index], "./"]:
        generate_md_file(DB=bib_db, list_classif=list_type, key=keys, plot_title_fct=plot_titles,
                         filename="README.md", add_comments=True, dir_path=dir_,
                         mapping_name=mapping_name,
                         discrib=disc + ".", add_hyperlink=True, hyperlinks=dir_path, get_outline=get_outline,
                         get_hyperlink=get_hyperlink)
        if index != 0:
            break


# check repetition
check_repetition()

dir_path = ["./", "type", "time", "application", "supervision", "approach", "setting",
            "research_question", "backbone_model", "dataset", "metrics", "author", "venue"]

mapping_name = {
    "./": "Summary",
    "venue": "Published Venue",
    "time": "Published Time",
    "application": "Application",
    "type": "Resource Type",
    "supervision": " Learning Paradigm",
    "approach": "Approach",
    "setting": "Setting",
    "research_question": "Research Questions",
    "backbone_model": "Backbone Model",
    "dataset": "Dataset",
    "metrics": "Metrics",
    "author": "Author",
}
dir_path_IE4all = ["" + your_research_topic + "4all/" + dp for dp in dir_path]
dir_path_IE4nlp = ["" + your_research_topic + "4nlp/" + dp for dp in dir_path]
dir_path_IE4cv = ["" + your_research_topic + "4cv/" + dp for dp in dir_path]
sub_dirs = [dir_path_IE4nlp, dir_path_IE4cv, dir_path_IE4all]

# 0 Home
list_type = [[venue] for venue in fined_taxonomy["Conference"]]
list_type += fined_taxonomy["Journal"]
list_type.append(fined_taxonomy["Preprint"])
indexs = [0, -1]
disc = "This page categorizes the literature by the **Published Venue**"
for index in indexs:
    plot_content(index=index, keys=["booktitle", "journal"], dir_path=dir_path, disc=disc, list_type=list_type,
                 sub_dirs=sub_dirs, mapping_name=mapping_name)

# 1 Resource Type
list_type = [[typ] for typ in fined_taxonomy["Type"]]
index = 1
disc = "This page categorizes the literature by the Resource Type"
plot_content(index=index, keys=["keywords"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 2 time
list_type = [[str(year)] for year in range(1980, 2030)][::-1]
index = 2
disc = "This page categorizes the literature by the **Last Post**"
plot_content(index=index, keys=["year"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 3 application
list_type = [[app] for app in fined_taxonomy["Application"]]
index = 3
disc = "This page categorizes the literature by the **Continual Learning Application**"
plot_content(index=index, keys=["keywords"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 4 supervision
list_type = [[sp] for sp in fined_taxonomy["Supervision"]]
index = 4
disc = "This page categorizes the literature by the **Learning Paradigm**"
plot_content(index=index, keys=["keywords"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 5 approach
list_type = []
for key in fined_taxonomy["Approach"]:
    if key in fined_taxonomy.keys():
        list_type += [[k] for k in fined_taxonomy[key]]
    else:
        list_type.append([key])
index = 5
disc = "This page categorizes the literature by the **Continual Learning Approach**"
plot_content(index=index, keys=["keywords"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 6 setting
list_type = [[setting] for setting in fined_taxonomy["Setting"]]
index = 6
disc = "This page categorizes the literature by the **Continual Learning Setting**"
plot_content(index=index, keys=["keywords"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 8 research question
list_type = [[rq] for rq in fined_taxonomy["RQs"]]
list_type.sort()
index = 7
disc = "This page categorizes the literature by the **Research Questions**"
plot_content(index=index, keys=["keywords"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 9 backbone model
list_type = [[bm] for bm in fined_taxonomy["Backbone"]]
index = 8
disc = "This page categorizes the literature by the **Backbone Model**"
plot_content(index=index, keys=["keywords"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 10 dataset
list_type = [[bm] for bm in fined_taxonomy["Dataset"]]
list_type.sort()
index = 9
disc = "This page categorizes the literature by the **Dataset**"
plot_content(index=index, keys=["keywords"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 11 Metric
list_type = [[bm] for bm in fined_taxonomy["Metrics"]]
list_type.sort()
index = 10
disc = "This page categorizes the literature by the **Metrics**"
plot_content(index=index, keys=["keywords"], dir_path=dir_path, disc=disc, list_type=list_type, sub_dirs=sub_dirs,
             mapping_name=mapping_name)

# 12 Author
index = 11
disc = "This page categorizes the literature by the **Author**"
plot_content(index=index, keys=["author"], dir_path=dir_path, disc=disc, list_type=None, sub_dirs=sub_dirs,
             mapping_name=mapping_name)
