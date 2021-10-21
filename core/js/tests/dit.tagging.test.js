require('../src/dit.tagging');

describe('dit tagging replacement', () => {
    beforeEach(async () => {
        document.body.innerHTML = `
            <a href="#link-basic">Basic link</a>
            <a href="#link-cta-button" class="button">CTA link with \`button\` class</a>
            <a href="#link-cta-cta" class="cta">CTA link with \`cta\` class</a>
            <section data-ga-section="Section name">
                <a href="#link-named-section">Link from named section</a>
            </section>
            <section id="section-id">
                <a href="#link-section-with-id">Link from a section with id</a>
            </section>
            <a href="#link-with-inferred-title-h1"><h1>Title in h1 </h1></a>
            <a href="#link-with-inferred-title-h2"><h2>  Title in h2</h2></a>
            <a href="#link-with-inferred-title-h3"><h3>  Title in h3  </h3></a>
            <a href="#link-with-inferred-title-h4"><h4>Title in h4 </h4></a>
            <a href="#link-with-inferred-title-h5"><h5>Title in h5  </h5></a>
            <a href="#link-with-inferred-title-span"><span>Title in span  </span></a>
            <a href="#link-with-inferred-title-p"><p>   Title in p</p></a>
        `;
        window.dataLayer = [];
        dit.tagging.base.init();
        window.document.dispatchEvent(new Event("DOMContentLoaded", {
            bubbles: true,
            cancelable: true
        }));
    });

    it('pushes to data layer on clicking a link', () => {
        // Original dit.tagging.js use the `mouseup` event here, probably hoping to include clicks
        // using the middle mouse button.
        // This isn't very useful, for several reasons, hence we move to using `click` instead:
        // - Tap events on touch devices do not trigger a `mouseup` event
        // - `mouseup` can be initiated by clicking outside of the element, then moving the mouse
        //   and releasing the button over the target.
        // - There was no distinction in the resulting GA event between left and middle button anyway.

        document.querySelector('[href="#link-basic"]').click()

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': '',
            'value': 'Basic link',
            'destination': '#link-basic'
        })
    })

    it('pushes to data layer on pressing return on a link', () => {
        document.querySelector('[href="#link-basic"]').dispatchEvent(new KeyboardEvent('keydown', {
            bubbles: true,
            cancellable: true,
            key: 'Enter'
        }));

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': '',
            'value': 'Basic link',
            'destination': '#link-basic'
        })
    })

    it.each([
        ['CTA link with `button` class', '#link-cta-button'],
        ['CTA link with `cta` class', '#link-cta-cta'],
    ])('pushes to data layer on clicking a %s', (text, href) => {
        document.querySelector(`[href="${href}"]`).click()

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'CTA',
            'element': '',
            'value': text,
            'destination': href
        })
    })

    it('pushes to data layer on clicking a link from a named section', () => {
        document.querySelector('[href="#link-named-section"]').click()

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': 'Section name',
            'value': 'Link from named section',
            'destination': '#link-named-section'
        })
    })

    it('pushes to data layer on clicking a link from a section with id', () => {
        document.querySelector('[href="#link-section-with-id"]').click()

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': 'section-id',
            'value': 'Link from a section with id',
            'destination': '#link-section-with-id'
        })
    })

    it.each(['h1', 'h2', 'h3', 'h4', 'h5', 'span', 'p'])('pushes to data layer on clicking a link with inferred title from %s', (titleElement) => {
        document.querySelector(`[href="#link-with-inferred-title-${titleElement}"]`).click()

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': '',
            'value': `Title in ${titleElement}`,
            'destination': `#link-with-inferred-title-${titleElement}`
        })
    })
})
