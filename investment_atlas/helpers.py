def get_sectors_label(page):
    sectors_label = ''

    if 'related_sectors' in page:
        related_sectors = [
            sector['related_sector']['title'] for sector in page['related_sectors'] if sector['related_sector']]

        # TODO: For mutliple sector put subsector inside related sector
        # we dont have any relation for sector and subsector in database at the moment
        if 'sub_sectors' in page and page['sub_sectors']:
            sub_sectors = [sub_sector for sub_sector in page['sub_sectors'] if sub_sector]
            if sub_sectors:
                sectors_label += '({})'.format(', '.join(related_sectors + sub_sectors))
            # TODO: following else could be avoided but based on test case data leaving it for time being
            else:
                sectors_label += '{}'.format(', '.join(related_sectors))
        else:
            sectors_label += '{}'.format(', '.join(related_sectors))
    return sectors_label
