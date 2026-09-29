"""Build-time discoverability index; no copies of scientific data or runtime fetches."""
_navigation = None


def on_nav(nav, **kwargs):
    global _navigation
    _navigation = nav
    return nav


def on_env(env, *, config, files):
    listed = {p.file.src_uri for p in _navigation.pages}
    names = {
        'architecture': 'Architettura — documenti complementari',
        'project': 'Governance — registri e documenti complementari',
        'session-reports': 'Sessioni — report individuali',
        'chapters': 'Manuale tecnico — approfondimenti',
        'ui': 'Interfaccia e navigazione',
        'developer': 'Sviluppo e pubblicazione',
        'releases': 'Note di rilascio',
    }
    groups = {}
    for file in files.documentation_pages():
        if file.src_uri in listed or not file.page:
            continue
        folder = file.src_uri.split('/')[0]
        title = names.get(folder, folder.replace('-', ' ').capitalize())
        groups.setdefault(title, []).append({'title': file.page.title, 'url': file.url})
    config.extra['dsg_directory_extras'] = [
        {'title': title, 'links': sorted(links, key=lambda x: x['title'].casefold())}
        for title, links in sorted(groups.items())
    ]
    config.extra['dsg_directory_count'] = len(list(files.documentation_pages()))
    return env
