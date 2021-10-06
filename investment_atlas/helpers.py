def get_sectors_label(page):
    sectors_label = ''

    if 'related_sectors' in page:
        related_sectors = [sector for sector in page['related_sectors'] if sector['related_sector']]
        if related_sectors:
            sectors_label = related_sectors[0]['related_sector']['title']

            if 'sub_sectors' in page:
                sub_sectors = [sub_sector for sub_sector in page['sub_sectors'] if sub_sector]
                if sub_sectors:
                    sectors_label += ' ({})'.format(', '.join(sub_sectors))

    return sectors_label
