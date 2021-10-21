require('../src/dit.tagging');

describe('dit tagging replacement', () => {
    beforeEach(async () => {
        document.body.innerHTML = `
            <a href="#link-basic">Basic link</a>
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
})
