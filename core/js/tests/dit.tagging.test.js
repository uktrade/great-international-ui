require('../src/dit.tagging');

describe('links event tracking', () => {
    beforeEach(async () => {
        document.body.innerHTML = `
            <a href="#link-basic">Basic link</a>
            <a href="#link-nested"><span>Nested link</span></a>
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
            <a 
                href="#link-with-ga-attributes"
                data-ga-action="ga-action"
                data-ga-type="ga-type"
                data-ga-element="ga-element"
                data-ga-value="ga-value"
            >Basic link</a>
        `;
        window.dataLayer = [];
        dit.tagging.base.init();
        window.document.dispatchEvent(new Event("DOMContentLoaded", {
            bubbles: true,
            cancelable: true
        }));
    });

    it('pushes to data layer on clicking a link', () => {
        // Original dit.tagging.js uses the `mouseup` event here, probably hoping to include clicks
        // using the middle mouse button.
        // This isn't very useful, for several reasons, hence we move to using `click` instead:
        // - Tap events on touch devices do not trigger a `mouseup` event
        // - `mouseup` can be initiated by clicking outside of the element, then moving the mouse
        //   and releasing the button over the target.
        // - There was no distinction in the resulting GA event between left and middle button anyway.

        document.querySelector('[href="#link-basic"]').click();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': '',
            'value': 'Basic link',
            'destination': '#link-basic'
        });
    });

    it('pushes to data layer on clicking descendants of a link', () => {
        document.querySelector('[href="#link-nested"] span').click();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': '',
            'value': 'Nested link',
            'destination': '#link-nested'
        });
    });

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
        });
    })

    it.each([
        ['CTA link with `button` class', '#link-cta-button'],
        ['CTA link with `cta` class', '#link-cta-cta'],
    ])('pushes to data layer on clicking a %s', (text, href) => {
        document.querySelector(`[href="${href}"]`).click();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'CTA',
            'element': '',
            'value': text,
            'destination': href
        });
    })

    it('pushes to data layer on clicking a link from a named section', () => {
        document.querySelector('[href="#link-named-section"]').click();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': 'Section name',
            'value': 'Link from named section',
            'destination': '#link-named-section'
        });
    })

    it('pushes to data layer on clicking a link from a section with id', () => {
        document.querySelector('[href="#link-section-with-id"]').click();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': 'section-id',
            'value': 'Link from a section with id',
            'destination': '#link-section-with-id'
        });
    })

    it.each(
        ['h1', 'h2', 'h3', 'h4', 'h5', 'span', 'p']
    )('pushes to data layer on clicking a link with inferred title from %s', (titleElement) => {
        document.querySelector(`[href="#link-with-inferred-title-${titleElement}"]`).click();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': '',
            'value': `Title in ${titleElement}`,
            'destination': `#link-with-inferred-title-${titleElement}`
        });
    })

    it('pushes to data layer on clicking a link with ga attributes', () => {
        document.querySelector('[href="#link-with-ga-attributes"]').click();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'ga-action',
            'type': 'ga-type',
            'element': 'ga-element',
            'value': 'ga-value',
            'destination': '#link-with-ga-attributes'
        });
    })

    it('does not push to data layer on clicking something else than a link', () => {
        document.querySelector('#section-id').click();

        expect(window.dataLayer.length).toEqual(0);
    })
})

describe('video events tracking', () => {
    beforeEach(async () => {
        document.body.innerHTML = `
            <video>
                <source src="foo.mp4">
            </video>
            <video data-ga-type="ga-video" data-ga-element="ga-element" data-ga-value="ga-value">
                <source src="foo-ga.mp4">
            </video>
        `;
        window.dataLayer = [];
        dit.tagging.base.init();
        window.document.dispatchEvent(new Event("DOMContentLoaded", {
            bubbles: true,
            cancelable: true
        }));
    });

    it.each(
        ['play', 'pause', 'ended']
    )('pushes to data layer on a video %s event', (event) => {
        document.querySelector('video').dispatchEvent(new Event(event));

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': event,
            'type': 'video',
            'element': '',
            'value': 'foo.mp4'
        });
    })

    it.each(
        ['play', 'pause', 'ended']
    )('pushes to data layer on a video %s event with ga attributes', (event) => {
        document.querySelector('video[data-ga-type]').dispatchEvent(new Event(event));

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': event,
            'type': 'ga-video',
            'element': 'ga-element',
            'value': 'ga-value'
        });
    })
})

describe('form events tracking', () => {
    beforeEach(async () => {
        // Returning false as submit isn't implemented in jsdom
        document.body.innerHTML = `
            <form action="/foo" onsubmit="return false;"></form>
            <form 
                action="/bar" 
                data-ga-action="ga-action"
                data-ga-type="ga-type"
                data-ga-element="ga-element"
                data-ga-value="ga-value"
                onsubmit="return false;"
            ></form>
            <form data-ga-include-form-data="true" action="/foo-bar" onsubmit="return false;">
                <input type="hidden" name="foo" value="1">
                <input type="hidden" name="bar" value="baz">
            </form>
            <form id="no-action" onsubmit="return false;"></form>
        `;
        window.dataLayer = [];
        dit.tagging.base.init();
        window.document.dispatchEvent(new Event("DOMContentLoaded", {
            bubbles: true,
            cancelable: true
        }));
    });

    it('pushes to data layer on form submit', () => {
        document.querySelector('form').submit();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'submit',
            'type': 'form',
            'element': '',
            'value': '/foo'
        });
    });

    it('pushes to data layer on form submit with no action', () => {
        document.querySelector('form#no-action').submit();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'submit',
            'type': 'form',
            'element': 'no-action',
            'value': ''
        });
    });

    it('pushes to data layer on form submit with ga attributes', () => {
        document.querySelector('form[data-ga-action]').submit();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'ga-action',
            'type': 'ga-type',
            'element': 'ga-element',
            'value': 'ga-value'
        });
    });

    it('pushes to data layer on form submit and includes data', () => {
        document.querySelector('form[data-ga-include-form-data]').submit();

        expect(window.dataLayer[0]).toEqual({
            'event': 'gaEvent',
            'action': 'submit',
            'type': 'form',
            'element': '',
            'value': '/foo-bar',
            'formData': 'foo=1&bar=baz'
        });
    });
})

describe('in debug mode', () => {
    beforeEach(async () => {
        document.body.innerHTML = `
            <a href="#link-basic">Basic link</a>
        `;
        window.dataLayer = [];
        dit.tagging.base.init(true);
        window.document.dispatchEvent(new Event("DOMContentLoaded", {
            bubbles: true,
            cancelable: true
        }));
        window.console.log = jest.fn();
    });

    it('logs to console on clicking a link', () => {
        document.querySelector('[href="#link-basic"]').click();

        expect(window.console.log).toHaveBeenCalledWith({
            'event': 'gaEvent',
            'action': 'clickLink',
            'type': 'PageLink',
            'element': '',
            'value': 'Basic link',
            'destination': '#link-basic'
        });
    });
})
