from glob import glob
import datetime

# from paperlist import make_publication_list


# open main page template
with open('index.template', 'r') as f:
    index = f.read().strip()


# about me section
with open('about/aboutme.html', 'r') as f:
    aboutme = f.read()

# research section
research = {}
for fname in glob('research/*.html'):
    identifier = "research-{0:s}".format(fname.replace('.html', '')).split('/')[-1]
    with open(fname, 'r') as f:
        research[identifier] = f.readlines()

research_menu = []
research_text = []

research_menu_fmt = '<a class="btn btn-default" id="select-{identifier:s}" row="{identifier:s}">{title:s}</a>'
research_text_fmt = '<div class="row darken-bg-50" id="{identifier:s}">\n{text:s}\n</div>'
for k, v in research.items():
    identifier = k
    # <a href="" class="topic">Star Cluster in Stochastic Regime</a>
    for line in v:
        if "topic" in line:
            break
    title = line.replace('<a href="" class="topic">', '')\
                .replace('</a>\n', '')
    text = '\n'.join(v)
    content = dict(identifier=identifier, title=title, text=text)
    research_menu.append(research_menu_fmt.format(**content))
    research_text.append(research_text_fmt.format(**content))

with open('paperlist/section_publications_articles.html', 'r') as f:
    publist = f.read()

with open('scripts.html', 'r') as f:
    scripts = f.read()

with open('cv/education.html', 'r') as f:
    cv_education = f.read()

with open('cv/current_projects.html', 'r') as f:
    cv_current_projects = f.read()

with open('cv/other_projects.html', 'r') as f:
    cv_other_projects = f.read()

with open('cv/teaching.html', 'r') as f:
    cv_teaching = f.read()

with open('cv/talks.html', 'r') as f:
    cv_talks = f.read()

content = dict(
        ABOUTME=aboutme, 
        RESEARCH_MENU='\n'.join(research_menu),
        RESEARCH_TEXT='\n'.join(research_text),
        PUBLIST_DATE=str(datetime.date.today()),
        PUBLIST=publist,
        CV_EDUCATION=cv_education,
        CV_CURRENT_PROJECTS=cv_current_projects,
        CV_OTHER_PROJECTS=cv_other_projects,
        CV_TEACHING=cv_teaching,
        CV_TALKS=cv_talks,
        SCRIPTS=scripts
        )

with open('index.html', 'w') as fout:
    fout.write(index.format(**content))
