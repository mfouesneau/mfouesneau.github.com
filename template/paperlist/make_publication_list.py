# -*- coding: utf-8 -*-
# !pip install -q ads

import os
import inspect
os.environ["ADS_DEV_KEY"] = "okomkAPoHKJKbNvpEVwGsMndPXOMinBGXr1NJEWw"
import ads 
from utf8totex import utf8totex

#directories
__ROOT__ = '/'.join(os.path.abspath(inspect.getfile(inspect.currentframe())).split('/')[:-1])


print("Generating the publication list for author Fouesneau in directory {0:s}".format(__ROOT__))


papers = list(
        ads.SearchQuery(
            author='fouesneau',
            fl=[
                "id",
                "identifier",
                "title",
                "author",
                "year",
                "pub",
                "volume",
                "page",
                "identifier",
                "doctype",
                "citation_count",
                "bibcode",
                "bibtex",
                "url",
            ],
            max_pages=100,
            sort="year"
        )
    )

# add non ads references

ralet2015 = ads.search.Article()
ralet2015.title = ['PRESPEC-AGATA setup: Optimizing the target positions with Bayesian data analysis']
ralet2015.year = '2015'
ralet2015.author = [ 'Ralet, D.' , 'Fouesneau, M.', 'Gerl, J.', 'Pietralla, N.', 'Pietri, S.']
ralet2015.pub = 'GSI Helmholtzzentrum f\"ur Schwerionenforschung'
ralet2015.page = ['157']
ralet2015.volume = '2015.1'
ralet2015.url = "\href{https://repository.gsi.de/record/183914}{issn:0171-4546}"
ralet2015.doctype = 'circular'
ralet2015.citation_count = 0

papers.append(ralet2015)

papers = sorted(papers, reverse=True, key=lambda paper: int(paper.year))

def shortname(name):
    sname = utf8totex(name).split(',')
    fam = sname[0]
    names = []
    for token in sname[1:]:
        if '-' in token.strip():
            tok = '-'.join([k.strip()[0] + '.' for k in token.split("-")])
        else:
            tok = ' '.join([k.strip()[0] + '.' for k in token.split()])
        names.append(tok)
    return fam + ', ' + ', '.join(names)

JOURNAL_MAP = {
    "arXiv e-prints": "ArXiv",
    "Monthly Notices of the Royal Astronomical Society": "\\mnras",
    "The Astrophysical Journal": "\\apj",
    "The Astronomical Journal": "\\aj",
    "Publications of the Astronomical Society of the Pacific": "\\pasp",
    "IAU General Assembly": "IAU",
    "American Astronomical Society Meeting Abstracts": "AAS",
}


def generate_short_author_list_latex(paper, highlight='fouesneau', keep=-1):
    hl = highlight.lower()
    author = ["\\textbf{{{name:s}}}".format(name=name) if hl in name.lower()
              else name  for name in map(shortname, paper.author)]
    if keep > 0:
        return (', '.join(author[:keep]) + ', et al.').replace(', ,', ',')
    return ', '.join(author).replace(', ,', ',')


def generate_short_author_list_html(paper, highlight='fouesneau', keep=-1):
    hl = highlight.lower()
    author = ["<b>{name:s}</b>".format(name=name) if hl in name.lower()
              else name  for name in map(shortname, paper.author)]
    if keep > 0:
        return (', '.join(author[:keep]) + ', et al.').replace(', ,', ',')
    return ', '.join(author).replace(', ,', ',')


def generate_tagyear_latex(year):
    return '\\tagyear{{{year:d}}}'.format(year=year)


def generate_tagyear_html(year):
    return '<li style="color:#77BFF2; border-bottom: 1px solid #77BFF2"><b>{year:d}</b></li>'.format(year=year)


latex_paper_fmt = "\\item {author:s}, {paper.year:s}, \"{title:s}\", {pub}, {paper.page[0]} [{paper.citation_count:,d} citations] {paper.url}"
latex_article_url_fmt = "\href{{https://ui.adsabs.harvard.edu/abs/{paper.bibcode:s}}}{{{bibcode:s}}}"

html_paper_fmt = """<li> <b>{title:s}</b><br>
{author:s}, {paper.year:s}, {pub}, {paper.page[0]} [{paper.citation_count:,d} citations] <br>
{paper.url} </li>
"""
html_article_url_fmt = "<a href=\"https://ui.adsabs.harvard.edu/abs/{paper.bibcode:s}\">{bibcode:s}</a>"

HTML_OUTPUT = True

if HTML_OUTPUT:
    paper_fmt = html_paper_fmt
    article_url_fmt = html_article_url_fmt
    generate_short_author_list = generate_short_author_list_html
    generate_tagyear = generate_tagyear_html
else:
    paper_fmt = latex_paper_fmt
    article_url_fmt = latex_article_url_fmt
    generate_short_author_list = generate_short_author_list_latex
    generate_tagyear = generate_tagyear_latex

article_year = 0
code_year = 0
collab_year = 0
articles = []
codes = []
collabs = []
for paper in papers:
    if paper.citation_count is None:
        paper.citation_count = 0
    if paper.page is None:
        paper.page = ['-']
    if paper.title is None:
        paper.title = 'None'
    if 'arxiv' in paper.page[0].lower():
        paper.page[0] = '-'
    author = generate_short_author_list(paper)
    title = utf8totex(paper.title[0])
    # pub = JOURNAL_MAP.get(paper.pub, paper.pub)
    pub = paper.pub

    if paper.url is None:
        bibcode = utf8totex(paper.bibcode)
        paper.url = article_url_fmt.format(paper=paper, bibcode=bibcode)

    if ('collaboration' in paper.author[0].lower()):
        if int(paper.year) != collab_year:
            collab_year = int(paper.year)
            collabs.append(generate_tagyear(collab_year))
        author = generate_short_author_list(paper, keep=2) 
        collabs.append(paper_fmt.format(author=author, paper=paper, 
                                         title=title, pub=pub))
    elif ('messenger' in paper.pub.lower()):
        if int(paper.year) != collab_year:
            collab_year = int(paper.year)
            collabs.append(generate_tagyear(collab_year))
        author = generate_short_author_list(paper, keep=1) 
        if '4MOST' in title:
            author = '4MOST collaboration, ' + author
        collabs.append(paper_fmt.format(author=author, paper=paper, 
                                         title=title, pub=pub))
    elif ('iau symposium' in paper.pub.lower()):
        if int(paper.year) != code_year:
            code_year = int(paper.year)
            codes.append(generate_tagyear(code_year))
        codes.append(paper_fmt.format(author=author, paper=paper, 
                                         title=title, pub=pub))
    elif paper.doctype in ('article', 'inbook', 'eprint'):
        if int(paper.year) != article_year:
            article_year = int(paper.year)
            articles.append(generate_tagyear(article_year))
        articles.append(paper_fmt.format(author=author, paper=paper, 
                                         title=title, pub=pub))
    elif paper.doctype.lower() in ('code', 'software', 'inproceedings', 'circular'):
        if int(paper.year) != code_year:
            code_year = int(paper.year)
            codes.append(generate_tagyear(code_year))
        codes.append(paper_fmt.format(author=author, paper=paper, 
                                         title=title, pub=pub))
    else:
        # print(paper.doctype, paper.bibcode, paper.author[0], paper.title, paper.pub, paper.citation_count)
        pass

if HTML_OUTPUT:
    with open(__ROOT__ + '/section_publications_articles.html', 'w') as fout:
        fout.write('\n'.join(articles))
    with open(__ROOT__ + '/section_publications_collabs.html', 'w') as fout:
        fout.write('\n'.join(collabs))
    with open(__ROOT__ + '/section_publications_other.html', 'w') as fout:
        fout.write('\n'.join(codes))
else:
    with open(__ROOT__ + '/section_publications_articles.tex', 'w') as fout:
        fout.write('\n'.join(articles))
    with open(__ROOT__ + '/section_publications_collabs.tex', 'w') as fout:
        fout.write('\n'.join(collabs))
    with open(__ROOT__ + '/section_publications_other.tex', 'w') as fout:
        fout.write('\n'.join(codes))

# Acknowlegements
print("Generating the publications acknowledging contributions")
ack_papers = list(
        ads.SearchQuery(
            ack='fouesneau',
            fl=[
                "id",
                "identifier",
                "title",
                "author",
                "year",
                "pub",
                "volume",
                "page",
                "identifier",
                "doctype",
                "citation_count",
                "bibcode",
                "bibtex",
                "url",
            ],
            max_pages=100,
            sort="year"
        )
    )

article_year = 0
ack_articles = []
for paper in ack_papers:
    if paper.citation_count is None:
        paper.citation_count = 0
    if paper.page is None:
        paper.page = ['-']
    if paper.title is None:
        paper.title = 'None'
    if 'arxiv' in paper.page[0].lower():
        paper.page[0] = '-'
    author = generate_short_author_list(paper)
    title = utf8totex(paper.title[0])
    # pub = JOURNAL_MAP.get(paper.pub, paper.pub)
    pub = paper.pub

    if paper.url is None:
        bibcode = utf8totex(paper.bibcode)
        paper.url = article_url_fmt.format(paper=paper, bibcode=bibcode)

        if int(paper.year) != article_year:
            article_year = int(paper.year)
            ack_articles.append('\\tagyear{{{year:d}}}'.format(year=article_year)) 
            ack_articles.append(generate_tagyear(article_year)) 
        ack_articles.append(paper_fmt.format(author=author, paper=paper, 
                                             title=title, pub=pub))

if HTML_OUTPUT:
    with open(__ROOT__ + '/section_publications_ack.html', 'w') as fout:
        fout.write('\n'.join(ack_articles))
else:
    with open(__ROOT__ + '/section_publications_ack.tex', 'w') as fout:
        fout.write('\n'.join(ack_articles))

summary = """
number of articles: {0:,d}
number of collaboration articles: {1:,d}
number of other publications: {2:,d}
number of Acknowleged contributions: {3:,d}
""".format(len([k for k in articles if 'tagyear' not in k]), 
           len([k for k in collabs if 'tagyear' not in k]), 
           len([k for k in codes if 'tagyear' not in k]),
           len([k for k in ack_articles if 'tagyear' not in k]))

print(summary)

if HTML_OUTPUT:
    print(""" updated 
    'section_publications_articles.html'
    'section_publications_collabs.html'
    'section_publications_other.html'
    'section_publications_ack.html'
    'section_publications_summary.html'
    """)
    with open(__ROOT__ + '/section_publications_summary.html', 'w') as fout:
        fout.write(summary)
else:
    print(""" updated 
    'section_publications_articles.tex'
    'section_publications_collabs.tex'
    'section_publications_other.tex'
    'section_publications_ack.tex'
    'section_publications_summary.tex'
    """)
    with open(__ROOT__ + '/section_publications_summary.tex', 'w') as fout:
        fout.write(summary)
