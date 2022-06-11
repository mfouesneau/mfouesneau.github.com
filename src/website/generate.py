from glob import glob
from .markdown_helpers import Markdown
from .make_publication_list import Paper, main as generate_publication_list
from typing import Sequence
import os
import yaml
import textwrap
import shutil
import re


def _merge_subdicts(root: dict) -> dict:
    """ Merge/flatten nested dictionaries into one. """
    res = root[0].copy()
    for sub in root[1:]:
        res.update(sub)
    return res


def get_icon(which: str) -> str:
    """ Return the icon html code for the given icon name. """
    return f"""<i class="{which:s}"></i>"""


def get_href(url: str, text: str = None, newpage:bool = True) -> str:
    """ Return the href html code for the given url. """
    if text is None:
        text = url
    if newpage:
        return f"""<a href="{url:s}" target="_blank">{text:s}</a>"""
    else:
        return f"""<a href="{url:s}">{text:s}</a>"""


def estimate_reading_time(text: str, WPM: int = 200) -> int:
    total_words = len(re.findall(r'\w+', text))
    time_minute = total_words // WPM + 1
    if time_minute == 0:
        time_minute = 1
    elif time_minute > 60:
        return str(time_minute // 60) + 'h'
    return str(time_minute) + 'min'


def generate_rss(data: Sequence[dict], title: str,
                 description: str,
                 baseurl: str = None) -> str:

    item_template = """
    <item>
        <title>{title}</title>
        <link>{url}</link>
        <description>{desription}</description>
    </item>
    """

    items = []
    for entry in data:
        items.append(item_template.format(
            title=entry['title'],
            url=entry['url'],
            desription=entry['description']))

    items = '\n'.join(items)

    template = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">

    <channel>
    <title>{title}</title>
    <link>{baseurl}</link>
    <description>{description}</description>
    {items}
    </channel>

    </rss>
    """
    return textwrap.dedent(template)


class Content(dict):
    """ Parent class for all widgets. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    @property
    def active(self):
        """ Return True if the widget is active. """
        return self['meta'].get('active', False)

    @property
    def theme_dir(self):
        """ Root directory of the theme."""
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def template_dir(self):
        """ Root directory of the theme."""
        return os.path.join(self.theme_dir, 'theme')

    def build(self, **kwargs: dict):
        """ Build the section. """
        raise NotImplementedError


class Section(Content):
    """ A section of the website. """

    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'section.html')

    def build(self, **kwargs: dict):
        """ Build the section.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        title = self['meta']['title']
        name = self['name']
        section_class = self.get('section_class', '')

        template = template.replace('{{name}}', name)\
                           .replace('{{other-classes}}', section_class)\
                           .replace('{{title}}', title)\
                           .replace('{{description}}', self['content'].to_html())

        # generate menu reference
        if self['meta'].get('icon', None):
            icon = get_icon(self['meta']['icon'])
        else:
            icon = ""
        ref = f"""<li><a class="nav-link scrollto" href="#{name:s}">{icon:s}<span>{title:s}</span></a></li>"""
        return template, ref


class Title(Content):
    pass


class AboutMe(Content):
    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'aboutme.html')

    def build(self, **kwargs: dict):
        """ Build the section.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        # social links
        social_links = []
        for element in self['meta']['social']:
            icon = get_icon(element['icon'])
            url = element['link']
            social_links.append(get_href(url, text=icon, newpage=True))

        # background image on title
        background_image = 'url({0:s})'.format(self['meta']['background_image'])

        # affiliations
        orgs = self['meta']['organizations']
        affiliations = []
        for org in orgs:
            name_ = org['name']
            url_ = org.get('url', None)
            if url_ is not None:
                name_ = get_href(url_, text=name_, newpage=True)
            else:
                name_ = name_
            affiliations.append(name_)

        name = self['name']
        title = "About Me"

        template = template.replace('{{name}}', name)\
                           .replace('{{title}}', self['meta']['title'])\
                           .replace('{{iam}}', self['meta']['iam'])\
                           .replace('{{roles}}', self['meta']['role'])\
                           .replace('{{social-links}}', '\n'.join(social_links))\
                           .replace('{{bg-hero-image}}', background_image)\
                           .replace('{{headshot-image}}', self['meta']['headshot_image'])\
                           .replace('{{affiliations}}', '\n'.join(affiliations))\
                           .replace('{{aboutme-content}}', self['content'].to_html())

        # generate menu reference
        if self['meta'].get('icon', None):
            icon = get_icon(self['meta']['icon'])
        else:
            icon = ""
        ref = f"""<li><a class="nav-link scrollto" href="#{name:s}">{icon:s}<span>{title:s}</span></a></li>"""
        return template, ref


class CV(Content):
    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'cv.html')

    def build(self, **kwargs: dict):
        """ Build the section.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        name = self['name']
        title = self['meta']['title']

        def parse_cv_category(cvdata, category):
            items = []
            item_template = """
            <div class="resume-item">
                <h5>{date}</h5>
                <h4>{title}</h4>
                <p><em>{where}</em></p>
                {description}
                <p style="font-size:small; color: rgba(85, 85, 85, 0.782);">{keywords}</p>
            </div>
            """
            items = []
            for exp in cvdata[category]:
                title = exp['title']
                where = exp['where']
                date = exp['date']
                description = Markdown(exp['description'])
                keywords = exp['keywords']
                items.append(
                    item_template.format(title=title, where=where,
                                        date=date, description=description.to_html(),
                                        keywords=keywords))
            return '\n'.join(items)

        def parse_cv(cvdata):
            col_template = """
            <div class="col-lg-{columwidth}">
                <h3 class="resume-title">{item_title}</h3>
                {items}
            </div>
            """
            setup = cvdata['setup']
            contents = []
            for entry in setup:
                columnwidth = entry['columnwidth']
                item_title = get_icon(entry['icon']) + " " + entry['title']
                category = entry['category']
                items = parse_cv_category(cvdata, category)

                contents.append(col_template.format(
                    columwidth=columnwidth, items=items, item_title=item_title))

            content = '\n\n'.join(contents)
            cvsum = cvdata['summary']
            if cvsum not in (None, ""):
                cvsum = Markdown(cvsum).to_html()
            return cvsum, content

        cvsum, content = parse_cv(self['meta']['cv'])

        template = template.replace('{{name}}', name)\
                           .replace('{{title}}', title)\
                           .replace('{{cv-summary}}', '\n'.join(cvsum))\
                           .replace('{{cv-content}}', content)

        # generate menu reference
        if self['meta'].get('icon', None):
            icon = get_icon(self['meta']['icon'])
        else:
            icon = ""
        ref = f"""<li><a class="nav-link scrollto" href="#{name:s}">{icon:s}<span>{title:s}</span></a></li>"""
        return template, ref


class Contacts(Content):
    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'contacts.html')

    def build(self, **kwargs: dict):
        """ Build the section.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        name = self['name']
        title = self['meta']['title']

        def parse_contact(contacts):
            contact_template = """
            <div class="phone">
                {icon}
                <h4>{title}</h4>
                {description}
            </div>
            """
            entries = []
            for contact in contacts:
                icon = get_icon(contact['icon'])
                title = contact['title']
                description = Markdown(contact['description'])
                entries.append(
                    contact_template.format(icon=icon, title=title,
                                            description=description.to_html()))
            return '\n'.join(entries)

        template = template.replace('{{name}}', name)\
                           .replace('{{title}}', title)\
                           .replace('{{contact-info}}', parse_contact(self['meta']['contact']))\

        # generate menu reference
        if self['meta'].get('icon', None):
            icon = get_icon(self['meta']['icon'])
        else:
            icon = ""
        ref = f"""<li><a class="nav-link scrollto" href="#{name:s}">{icon:s}<span>{title:s}</span></a></li>"""
        return template, ref


class Gallery(Content):
    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'gallery.html')

    def generate_detail_page(self, detail_data):
        name = self['name']
        directory = self['meta']['content-directory']
        output_dir = os.path.join(self['build_dir'], directory)

        if detail_data['meta']['active'] is False:
            print('Detail page {0:s} ({1:s}) is not active.'.format(name, detail_data['name']))
            return
        else:
            print("Building Detail page {0:s} ({1:s}).".format(name, detail_data['name']))

        image_template = """
        <div class="swiper-slide">
            <img src="{url}" alt="">
            <p> {caption}</p>
        </div>
        """
        slideshow = [image_template.format(url=image['url'], caption=Markdown(image['caption']).to_html())
                        for image in detail_data['meta']['images']]
        slideshow = '\n'.join(slideshow)

        info = Markdown(detail_data['meta']['information']).to_html()
        description = Markdown(detail_data['content']).to_html()

        with open(os.path.join(self.template_dir, 'gallery-details.html')) as f:
            template = f.read()

        template = template.replace('{{slideshow-items}}', slideshow)\
                           .replace('{{information}}', info)\
                           .replace('{{description}}', description)

        # export the detail pages
        if os.path.exists(output_dir) is False:
            os.makedirs(output_dir)
        else:
            if not os.path.isdir(output_dir):
                raise ValueError('{0:s} is not a directory.'.format(output_dir))
        output_name = os.path.join(output_dir, detail_data['name'] + ".html")
        with open(output_name, 'w') as f:
            # print("Writing {0:s}.".format(output_name))
            f.write(template)

    def generate_gallery_item(self, gallery_data):
        item_template = """
            <div class="col-lg-4 col-md-6 portfolio-item {keywords}">
                <div class="portfolio-wrap" style="background:rgba(255,255,255,0);">
                <img src="{preview_image}" class="img-fluid" alt="">
                <div class="portfolio-info">
                    <h4>{title}</h4>
                    <p>{brief}</p>
                    <div class="portfolio-links">
                    <a href="{preview_image}" data-gallery="portfolioGallery" class="portfolio-lightbox" title="{title}"><i class="bx bx-plus"></i></a>
                    <a href="{item_details_htmlfile}" class="portfolio-details-lightbox" data-glightbox="type: external" title="Details"><i class="bx bx-link"></i></a>
                    </div>
                </div>
                </div>
            </div>
            """
        entry = gallery_data['meta']
        title = entry['title']
        brief = Markdown(entry['brief'])
        keywords = ' '.join(["filter-{key}".format(key=key) for key in entry['keywords']])
        preview_image = entry['preview-image']
        url = entry['url']

        directory = self['meta']['content-directory']
        output_name = os.path.join(directory, gallery_data['name'] + ".html")
        item  =item_template.format(title=title, brief=brief.to_html(),
                                    preview_image=preview_image,
                                    keywords=keywords, url=url,
                                    item_details_htmlfile=output_name)
        return item


    def build(self, **kwargs: dict):
        """ Build the section.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        name = self['name']
        title = self['meta']['title']

        # detail_page
        directory = os.path.join(self['source_dir'], self['meta']['content-directory'])
        print("Reading {1:s} content from {0:s}... ".format(directory, name))

        items = []
        for fname in glob(directory + '/*.md'):
            data = content_from_file(fname)
            self.generate_detail_page(data)
            items.append(self.generate_gallery_item(data))

        items = '\n'.join(items)    # parse_items(self['meta']['content'])
        filters = self['meta']['filters']
        filters = '\n'.join(["""<li data-filter=".filter-{k}">{v}</li>""".format(k=k, v=v) for k, v in filters.items()])

        template = template.replace('{{name}}', name)\
                           .replace('{{title}}', title)\
                           .replace('{{summary}}', self['content'].to_html())\
                           .replace('{{portfolio-items}}', items)\
                           .replace('{{filter-keywords}}', filters)

        # generate menu reference
        if self['meta'].get('icon', None):
            icon = get_icon(self['meta']['icon'])
        else:
            icon = ""
        ref = f"""<li><a class="nav-link scrollto" href="#{name:s}">{icon:s}<span>{title:s}</span></a></li>"""
        return template, ref

class Testimonials(Section):
    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'testimonials.html')

class Services(Section):
    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'services.html')

class Publications(Content):
    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'publications.html')

    def build(self, **kwargs: dict):
        """ Build the section.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        indata = os.path.join(self['source_dir'], self['meta']['publication-list']['filename'] + '.md')

        # check if you have to run the publication generator
        if self['meta']['publication-list'].get('regenerate', False):
            print(f"Generating publications... {indata:s}")
            generate_publication_list(
                indata,
                author=self['meta']['publication-list']['author'],
                )

        with open(self.template, 'r') as f:
            template = f.read()

        title = self['meta']['title']
        name = self['name']

        print("   reading data from {0:s}".format(indata))

        _pubs = Markdown.from_file(indata)
        meta = _pubs.meta

        stats = meta['summary']
        nrefereed = stats['articles']['number']
        ncolab = stats['collaboration']['number']
        nother = stats['other']['number']
        hindex = stats['hindex']['number']
        ncite = stats['ncite']['number']

        content = self['content'].to_html()
        paper_lst_fmt = """\n<div class="resume-item">\n<h5>{year:d}</h5>\n<ul style="list-style: none;">\n{lst:s}\n<ul>\n</div>"""
        papers = []
        year = meta['article'][0]['year']
        for k in range(self['meta']['show-nrecent-articles']):
            paper_ = Paper(meta['article'][k])
            papers.append(paper_.to_html()\
                            .replace('{icon}', get_icon("far fa-file-alt pub-icon") + " "))
            if paper_['year'] != year:
                content += paper_lst_fmt.format(year=year, lst='\n'.join(papers))
                year = paper_['year']
                papers = []
        if papers:
            content += paper_lst_fmt.format(year=year, lst='\n'.join(papers))

        social_links = []
        for element in self['meta']['links']:
            icon = get_icon(element['icon'])
            url = element['url']
            desc = element['description']
            social_links.append(get_href(url, text=icon + " " + desc, newpage=True))

        template = template.replace('{{name}}', name)\
                           .replace('{{title}}', title)\
                           .replace('{{description}}', content)\
                           .replace('{{nrefereed}}', f'{nrefereed:,d}')\
                           .replace('{{ncolab}}', f'{ncolab:,d}')\
                           .replace('{{nother}}', f'{nother:d}')\
                           .replace('{{ncite}}', f'{ncite:,d}')\
                           .replace('{{hindex}}', f'{hindex:d}')\
                           .replace('{{links}}', '\n<br>'.join(social_links))\
                           .replace('{{fulllist-url}}', 'publication-list.html')

        with open(os.path.join(self.template_dir, 'publications-full.html')) as f:
            template_full = f.read()

        content = ""

        content += '<h4>Refereed Articles</h4>'
        papers = []
        year = meta['article'][0]['year']
        for paperk in meta['article']:
            paper_ = Paper(paperk)
            papers.append(paper_.to_html()\
                            .replace('{icon}', get_icon("far fa-file-alt pub-icon") + " "))
            if paper_['year'] != year:
                content += paper_lst_fmt.format(year=year, lst='\n'.join(papers))
                year = paper_['year']
                papers = []
        if papers:
            content += paper_lst_fmt.format(year=year, lst='\n'.join(papers))

        content += '<h4>Collaboration Articles</h4>'
        papers = []
        year = meta['collaboration'][0]['year']
        for paperk in meta['collaboration']:
            paper_ = Paper(paperk)
            papers.append(paper_.to_html()\
                            .replace('{icon}', get_icon("far fa-file-alt pub-icon") + " "))
            if paper_['year'] != year:
                content += paper_lst_fmt.format(year=year, lst='\n'.join(papers))
                year = paper_['year']
                papers = []
        if papers:
            content += paper_lst_fmt.format(year=year, lst='\n'.join(papers))

        content += '<h4>Other Articles</h4>'
        papers = []
        year = meta['other'][0]['year']
        for paperk in meta['other']:
            paper_ = Paper(paperk)
            papers.append(paper_.to_html()\
                            .replace('{icon}', get_icon("far fa-file-alt pub-icon") + " "))
            if paper_['year'] != year:
                content += paper_lst_fmt.format(year=year, lst='\n'.join(papers))
                year = paper_['year']
                papers = []
        if papers:
            content += paper_lst_fmt.format(year=year, lst='\n'.join(papers))

        template_full = template_full.replace('{{name}}', name)\
                                     .replace('{{title}}', "Publication List")\
                                     .replace('{{description}}', content)\
                                     .replace('{{nrefereed}}', f'{nrefereed:,d}')\
                                     .replace('{{ncolab}}', f'{ncolab:,d}')\
                                     .replace('{{nother}}', f'{nother:d}')\
                                     .replace('{{ncite}}', f'{ncite:,d}')\
                                     .replace('{{hindex}}', f'{hindex:d}')\
                                     .replace('{{links}}', '\n<br>'.join(social_links))

        with open(os.path.join(self['build_dir'], 'publication-list.html'), 'w') as fout:
            fout.write(template_full)

        # generate menu reference
        if self['meta'].get('icon', None):
            icon = get_icon(self['meta']['icon'])
        else:
            icon = ""
        ref = f"""<li><a class="nav-link scrollto" href="#{name:s}">{icon:s}<span>{title:s}</span></a></li>"""
        return template, ref

class Post(Content):
    @property
    def template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'posts.html')

    def generate_detail_page(self, detail_data):
        name = self['name']
        if detail_data['meta']['active'] is False:
            print('Detail page {0:s} ({1:s}) is not active.'.format(name, detail_data['name']))
            return
        else:
            print("Building Detail page {0:s} ({1:s}).".format(name, detail_data['name']))

        entry = detail_data['meta']
        directory = self['meta']['content-directory']
        output_dir = os.path.join(self['build_dir'], directory)
        brief = Markdown(entry['brief'])
        keywordlist = ', '.join(entry['keywords'])
        date = entry['date']
        readtime = estimate_reading_time(entry['brief'] + detail_data['content'])


        with open(os.path.join(self.template_dir, 'post-details.html')) as f:
            template = f.read()

        template = template.replace('{{title}}', detail_data['meta']['title'])\
                           .replace('{{content}}', Markdown(detail_data['content']).to_html())\
                           .replace('{{date}}', str(date))\
                           .replace('{{brief}}', brief.to_html())\
                           .replace('{{keywordlist}}', keywordlist)\
                           .replace('{{readtime}}', readtime)

        # export the detail pages
        if os.path.exists(output_dir) is False:
            os.makedirs(output_dir)
        else:
            if not os.path.isdir(output_dir):
                raise ValueError('{0:s} is not a directory.'.format(output_dir))
        output_name = os.path.join(output_dir, detail_data['name'] + ".html")
        with open(output_name, 'w') as f:
            # print("Writing {0:s}.".format(output_name))
            f.write(template)

    def generate_gallery_item(self, gallery_data, rss: bool = False):
        item_template = """
            <div style="display:flex;flex-direction: row;align-items: center;flex-wrap: nowrap; justify-content: space-between;" class="{keywords}">
                <div>
                    <h4 style="color:#0563bb;font-weight: bold;">
                    <a href="{item_details_htmlfile}" class="portfolio-details-lightbox" data-glightbox="type: external" title="Details">
                    {title}
                    </a>
                    </h4>
                    <p>{brief}</p>
                    <p style="font-size: 14px; letter-spacing: .03em; color: rgba(0,0,0,.54);">
                        Last updated on {date} &#183; {readtime} read &#183; <i class="fas fa-folder mr-1"></i> {keywordlist}</p>
                </div>
                <div class="post image-preview" style="padding:1rem;">
                    <img src="{preview_image}" class="img-fluid" alt="" style="max-width: 200px; object-fit: cover; height:auto;">
                </div>
            </div>
            """
        entry = gallery_data['meta']
        title = entry['title']
        brief = Markdown(entry['brief'])
        keywords = ' '.join(["filter-{key}".format(key=key) for key in entry['keywords']])
        keywordlist = ', '.join(entry['keywords'])
        preview_image = entry['preview-image']
        date = entry['date']
        readtime = estimate_reading_time(entry['brief'] + gallery_data['content'])

        directory = self['meta']['content-directory']
        output_name = os.path.join(directory, gallery_data['name'] + ".html")
        item = item_template.format(title=title, brief=brief.to_html(),
                                    preview_image=preview_image, date=date,
                                    keywords=keywords, keywordlist=keywordlist,
                                    item_details_htmlfile=output_name,
                                    readtime=readtime)
        if rss:
            rss_item = dict(title=title,
                            url=self['baseURL'] + output_name,
                            description=brief.to_html() + '\n' + gallery_data['content'].to_html())
        else:
            rss_item = {}
        return date, item, rss_item

    def build(self, **kwargs: dict):
        """ Build the section.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        # no need to bother if not active
        if self.active is False:
            print('Section {0:s} ({1:s}) is not active.'.format(self.name, self.filename))
            return '', ''
        print('Building Section {0:s} ({1:s}).'.format(self.name, self.filename))

        self.update(**kwargs)

        with open(self.template, 'r') as f:
            template = f.read()

        title = self['meta']['title']
        name = self['name']

        # detail_page
        directory = os.path.join(self['source_dir'], self['meta']['content-directory'])
        print("Reading {1:s} content from {0:s}... ".format(directory, name))

        # generate items
        rss = self['meta']['generate-rss']
        items = []
        for fname in glob(directory + '/*.md'):
            data = content_from_file(fname)
            self.generate_detail_page(data)
            items.append(self.generate_gallery_item(data, rss=rss))


        # sort items
        items.sort(key=lambda x: x[0], reverse=True)

        summary = self['content'].to_html()

        if rss:
            rssfile = os.path.join(self['build_dir'], 'rss-post.xml')
            print("Generating {1:s} rss content to {0:s}... ".format(rssfile, name))
            rss_content = generate_rss([k[-1] for k in items],
                                        "Posts", "New posts", baseurl=self['baseURL'])
            with open(rssfile, 'w') as f:
                f.write(rss_content)
            summary += '<p><a href="{0:s}"><i class="fa-solid fa-rss"></i></a></p>'.format('rss-post.xml')

        filters = self['meta']['filters']
        filters = '\n'.join(["""<li data-filter=".filter-{k}">{v}</li>""".format(k=k, v=v) for k, v in filters.items()])

        nrecent = min(len(items), self['meta']['show-nrecent-articles'])
        template = template.replace('{{name}}', name)\
                           .replace('{{title}}', title)\
                           .replace('{{summary}}', summary)\
                           .replace('{{post-items}}', '\n'.join([k[1] for k in items[:nrecent]]))\
                           .replace('{{filter-keywords}}', filters)\
                           .replace('{{fulllist-url}}', 'posts-list.html')

        with open(os.path.join(self.template_dir, 'posts-full.html')) as f:
            template_full = f.read()

        template_full = template_full.replace('{{name}}', name)\
                                     .replace('{{title}}', "Post List")\
                                     .replace('{{description}}', '\n'.join([k[1] for k in items]))


        with open(os.path.join(self['build_dir'], 'posts-list.html'), 'w') as fout:
            fout.write(template_full)

        # generate menu reference
        if self['meta'].get('icon', None):
            icon = get_icon(self['meta']['icon'])
        else:
            icon = ""
        ref = f"""<li><a class="nav-link scrollto" href="#{name:s}">{icon:s}<span>{title:s}</span></a></li>"""
        return template, ref



def content_from_file(filename: str,
                      **kwargs) -> "Content":
    """
    Parameters
    ----------
    filename : str
        The name of the program file to write.
    template_dir : str
        The name of the template files to use.

    Returns
    -------
    content: Content
        The content object to be used in the website.
    """
    content = Markdown.from_file(filename)
    content_type = content.meta.get('type', 'section')
    name = filename.split('/')[-1].split('.')[0]

    # add relevant categories
    type_mapping = {'section': Section,
                    'aboutme': AboutMe,
                    'contacts': Contacts,
                    'cv': CV,
                    'publications': Publications,
                    'gallery': Gallery,
                    'posts': Post}

    return type_mapping.get(content_type, Content)(
        filename = filename,
        name = name,
        content=content,
        meta=content.meta,
        type=content_type,
        **kwargs)


class Generator(dict):
    """ Main page generator. """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    @classmethod
    def from_file(cls, path: str) -> 'Generator':
        with open(path, 'r') as f:
            return cls(**yaml.load(f, yaml.FullLoader))

    def build(self, fname: str, **kwargs):
        """ Generates the content of a markdown file.

        Parameters
        ----------
        fname : str
            The name of the markdown file to read.

        Returns
        -------
        markdown_content : str
            The content of the markdown file as a string.
        header : dict
            The header of the markdown file as a dictionary (yaml output).
        """
        content = content_from_file(fname, **kwargs)
        return content.build(**kwargs)

    @property
    def theme_dir(self):
        """ Root directory of the theme."""
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def template_dir(self):
        """ Root directory of the theme."""
        return os.path.join(self.theme_dir, 'theme')

    @property
    def index_template(self):
        """ Path to the index template. """
        return os.path.join(self.template_dir, 'index.html')

    def generate(self):
        root_dir = self['sourcedir']
        build_dir = self['builddir']
        static_dir = self['staticdir']
        index = Markdown.from_file(os.path.join(root_dir, 'index.md'))
        header = index.meta

        print(textwrap.dedent(f"""
        Generating website...
        ----------------------
        configuration:
            * content directory: {root_dir}
            * static content directory: {static_dir}
            * building directory: {build_dir}
            * theme directory: {self.theme_dir}
            * template directory: {self.template_dir}
        """))

        # construct the output folder
        if os.path.exists(build_dir):
            # remove if exists
            shutil.rmtree(build_dir)

        # copy theme resource files

        shutil.copytree(os.path.join(self.template_dir, 'assets'), os.path.join(build_dir, "assets"))

        # copy static files
        shutil.copytree(self['staticdir'],
                        os.path.join(build_dir, "static"))

        with open(self.index_template, 'r') as f:
            print('Reading index template...', self.index_template)
            template = f.read()

        # Some global information about self
        fname = f'{root_dir}/aboutme.md'
        data = content_from_file(fname)

        # social links
        social_links = []
        for element in data['meta']['social']:
            icon = get_icon(element['icon'])
            url = element['link']
            social_links.append(get_href(url, text=icon, newpage=True))

        email = [k['email'] for k in data['meta']['contact'] if 'email' in k][0]

        # background image on title
        background_image = 'url({0:s})'.format(data['meta']['background_image'])

        # keep various sections
        sections = []
        # Navigation bar
        nav = []

        for section in header['content']:
            fname = os.path.join(root_dir, section + '.md')
            txt, reference = self.build(fname,
                                        source_dir=root_dir,
                                        build_dir=build_dir,
                                        baseURL=self['baseURL'],)
            sections.append(txt)
            nav.append(reference)

        template = template.replace('{{sections}}', '\n'.join(sections))\
                           .replace('{{nav-content}}', '\n'.join(nav))\
                           .replace('{{title}}', data['meta']['title'])\
                           .replace('{{iam}}', data['meta']['iam'])\
                           .replace('{{social-links}}', '\n'.join(social_links))\
                           .replace('{{bg-hero-image}}', background_image)\
                           .replace('{{email}}', email)\
                           .replace('{{site-title}}', header['site-title'])

        # export the index.html
        with open(os.path.join(build_dir, "index.html"), 'w') as f:
            f.write(template)

        print("\nWebsite generated into {}".format(build_dir))



def generate_index(path: str = None):
    """ Generates the index.html file. """
    if path is None:
        path = os.path.join(os.getcwd(), 'config.yml')
    generator = Generator.from_file(path)
    generator.generate()


def generate(cfgfile: str = None):
    """ Generates the website from a given configuration file. """
    import importlib

    if cfgfile is None:
        cfgfile = os.path.join(os.getcwd(), 'config.yml')

    if not os.path.isfile(cfgfile):
        raise FileNotFoundError(f"{cfgfile} does not exist.")

    import yaml

    generator = Generator.from_file(cfgfile)
    generator.generate()