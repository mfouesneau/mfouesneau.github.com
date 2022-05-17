---
type: section
active: true

date: 2022-04-07

# Display name
title: MPIA Arxiv Display

brief: I spent a significant amount of time to update the way we show ArXiv papers at the institute. I decided to completely outsource the process to GitHub using the GitHub Actions.

keywords:
    - data-driven
    - astrophysical parameters

preview-image: ""

---

[arxiv_display](https://github.com/mpi-astronomy/arxiv_display) is a hack born during a science coffee at MPIA between [Iskren Georgiev (@iskreng-y-g)](https://github.com/iskren-y-g) and [Morgan Fouesneau (@mfouesneau)](https://github.com/mfouesneau). This repository generates the screen content for the corridors of the institute. It is a sort of Arxiver for institutes or groups.

This repository "only" hosts a website that supports the institute's displays.

The main goal is to provide summaries of daily papers authored or co-authored by MPIA members. Only for those, the summary contains the title, authors, abstract, and figures (with captions).

This evolution heavily relies on [arXiv on deck 2](https://mfouesneau.github.io/arxiv_on_deck_2), a package that searches for new articles on [ArXiv](https://arxiv.org/) and renders their summary as Markdown documents. It does not compile the original LaTeX documents and only extracts the relevant information into Markdown files.