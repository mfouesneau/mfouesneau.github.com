# -*- coding: utf-8 -*-
# !pip install -q ads
import os
os.environ["ADS_DEV_KEY"] = "okomkAPoHKJKbNvpEVwGsMndPXOMinBGXr1NJEWw"
import ads
from ads.search import Article
from typing import Any
import yaml


def shortname(name: str) -> str:
    """ Generate a  short name from a full name """
    sname = name.split(',')
    fam = sname[0]
    names = []
    for token in sname[1:]:
        if '-' in token.strip():
            tok = '-'.join([k.strip()[0] + '.' for k in token.split("-")])
        else:
            tok = ' '.join([k.strip()[0] + '.' for k in token.split()])
        names.append(tok)
    return fam + ', ' + ', '.join(names)


def generate_short_author_list(paper: Article,
                               highlight: str = 'fouesneau',
                               keep: int = -1) -> str:
    hl = highlight.lower()
    author = ["<strong>{name:s}</strong>".format(name=name) if hl in name.lower()
              else name  for name in map(shortname, paper.author)]
    if keep > 0:
        return (', '.join(author[:keep]) + ', et al.').replace(', ,', ',')
    return ', '.join(author).replace(', ,', ',')


class Paper(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_attributes()

    @classmethod
    def from_article(cls, paper: Article):
        self = cls()
        self['author'] = paper.author
        try:
            self['bibcode'] = paper.bibcode
        except Exception:
            self['bibcode'] = None
        # correcting bug in ads
        # self.bibtex = ads.ExportQuery(bibcodes=paper.bibcode, format="bibtex").execute()
        self['citation_count'] = paper.citation_count
        self['doctype'] = paper.doctype
        try:
            self['identifier'] = paper.identifier
        except Exception:
            self['identifier'] = [None]
        self['page'] = paper.page[0] if paper.page else '-'
        self['pub'] = paper.pub
        self['title'] = paper.title[0]
        self['url'] = paper.url
        self['volume'] = paper.volume
        self['year'] = int(paper.year)
        self['abstract'] = paper.abstract
        self.check_attributes()
        return self

    def check_attributes(self):
        """ Check values in attributes and set defaults """
        if self.get('citation_count', None) is None:
            self['citation_count'] = 0
        if self.get('page') is None:
            self['page'] = '-'
        if self.get('title') is None:
            self['title'] = 'None'
        if 'arxiv' in self['page'].lower():
            self['page'] = '-'
        try:
            self.set_cateogry()
        except KeyError:
            self['category'] = 'Unknown'

    def set_cateogry(self):
        if (('collaboration' in self['author'][0].lower())
            or ('messenger' in self['pub'].lower())
            or ('4MOST' in self['title'])):
            self['category'] = 'collaboration'
        elif 'iau symposium' in self['pub'].lower():
            self['category'] = 'other'
        elif self['doctype'] in ('article', 'inbook', 'eprint'):
            self['category'] = 'article'
        elif self['doctype'].lower() in ('code', 'software', 'inproceedings', 'circular', 'catalog', 'techreport'):
            self['category'] = 'other'
        else:
            self['category'] = 'unknown'

    def get_short_author_list(self,
                              highlight: str = 'fouesneau',
                              keep: int = -1,
                              highlight_format='html') -> str:
        hl = highlight.lower()
        if highlight_format == 'html':
            author = ["<strong>{name:s}</strong>".format(name=name) if hl in name.lower()
                    else name  for name in map(shortname, self['author'])]
        elif highlight_format == 'latex':
            author = ["\\textbf{%s}" % name if hl in name.lower()
                    else name  for name in map(shortname, self['author'])]
        if keep > 0:
            return (', '.join(author[:keep]) + ', et al.').replace(', ,', ',')
        return ', '.join(author).replace(', ,', ',')

    def __str__(self):

        fmt = """ "{title}:"\n {_author_list}:,\n{year:d}, {pub}, {page} [{citation_count:,d} citation\n{url}"""
        return fmt.format(_author_list=', '.join(self['author']), **self)

    def to_html(self):
        """ Return the html representation of the paper """
        paper_fmt = "<li>{{icon}}<strong>\"{title:s}\"</strong><br>{author:s}, {year:d}, {pub:s}, {page} [{citation_count:,d} citations]<br> {url}"
        if self['url'] is None:
            url_fmt = "<a href=https://ui.adsabs.harvard.edu/abs/{bibcode:s}>{bibcode:s}</a>"
            url = url_fmt.format(bibcode=self['bibcode'])
        else:
            url = self['url']
        info = dict(author=self.get_short_author_list(),
                    year=self['year'],
                    title=self['title'],
                    pub=self['pub'],
                    page=self['page'],
                    citation_count=self['citation_count'],
                    url=url)
        return paper_fmt.format(**info)

    def to_tex(self):
        """ Return the tex representation of the paper """
        paper_fmt = "\\item {author:s}, {year:d}, \"{title:s}\", {pub}, {page} [{citation_count:,d} citations] {url}"
        if self['url'] is None:
            url_fmt = "\href{{https://ui.adsabs.harvard.edu/abs/{bibcode:s}}}{{{bibcode:s}}}"
            url = url_fmt.format(bibcode=self['bibcode'])
        else:
            url = self['url']
        info = dict(author=self.get_short_author_list(),
                    year=self['year'],
                    title=self['title'],
                    pub=self['pub'],
                    page=self['page'],
                    citation_count=self['citation_count'],
                    url=url)
        return paper_fmt.format(**info)

    def to_dict(self):
        return dict(**self)


def get_additional_papers():
    """ Non ads references """
    additionals = []

    ralet2015 = Article()
    ralet2015.title = ['PRESPEC-AGATA setup: Optimizing the target positions with Bayesian data analysis']
    ralet2015.year = '2015'
    ralet2015.author = [ 'Ralet, D.' , 'Fouesneau, M.', 'Gerl, J.', 'Pietralla, N.', 'Pietri, S.']
    ralet2015.pub = 'GSI Helmholtzzentrum für Schwerionenforschung'
    ralet2015.page = ['157']
    ralet2015.volume = '2015.1'
    ralet2015.bibcode = 'issn:0171-4546'
    ralet2015.url = "https://repository.gsi.de/record/183914"
    ralet2015.doctype = 'circular'
    ralet2015.citation_count = 0

    additionals.append(ralet2015)

    return additionals


def main(filename='publication_list.md',
         author='fouesneau'):

    print(f"Generating the publication list for author {author}")

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
                    "doctype",
                    "citation_count",
                    "bibcode",
                    "bibtex",
                    "url",
                    "abstract",
                    "keyword"
                ],
                max_pages=100,
                sort="year"
            )
        )

    # papers.extend(get_additional_papers())

    papers = sorted(papers, reverse=True, key=lambda paper: int(paper.year))

    converted = []
    for k in papers:
        try:
            converted.append(Paper.from_article(k).to_dict())
        except Exception as e:
            pass

    from itertools import groupby, chain
    keyfunc = lambda x: x['category']
    grouped = groupby(sorted(converted, key=keyfunc), keyfunc)

    myarticles = {}
    for cat, lst in grouped:
        myarticles[cat] = list(lst)

    bibcodes = []
    for k in converted:
        try:
            bibcodes.append(k['bibcode'])
        except:
            pass
    metrics = ads.MetricsQuery(bibcodes).execute()
    hindex = metrics['indicators']['h']

    ncitations = 0
    for k in converted:
        if k['category'] != 'collaboration':
            ncitations += k['citation_count']

    summary = {
        'articles': {'description': "refereed publications",
                    'number': len(myarticles['article'])},
        'collaboration': {'description': "publications from large collaborations",
                        'number': len(myarticles['collaboration'])},
        'other': {'description': "other publications",
                'number': len(myarticles['other'])},
        'hindex': {'description': "h-index", 'number': hindex},
        'ncite' : {'description': "number of citations (non-collaboration papers)", 'number': ncitations},
    }

    for (k, v) in summary.items():
        print("{0:>50s}: {1:,d}".format(v['description'], v['number']))

    myarticles['summary'] = summary

    with open(os.path.join(filename), 'w') as fout:
        fout.write("---\n")
        fout.write("# Publication list data\n")
        fout.write("type: null\n")
        fout.write("active: false\n")
        yaml.dump(myarticles, fout)
        fout.write("---\n")

    return papers


if __name__ == '__main__':
    papers = main()