def get_sectors_label(page):
    sectors_label = ''

    if 'related_sectors' in page and len(page['related_sectors']) > 0:
        sectors_label = page['related_sectors'][0]['related_sector']['title']

        if 'sub_sectors' in page and len(page['sub_sectors']) > 0:
            sectors_label += ' ({})'.format(', '.join(page['sub_sectors']))

    return sectors_label
