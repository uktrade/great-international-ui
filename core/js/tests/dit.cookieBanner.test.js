require('../src/dit.cookieBanner');

describe('cookie banner', () => {
    beforeEach(async () => {
        document.cookie = '';
        document.body.innerHTML = `
            <meta id="privacyCookieDomain" value="localhost" />
            <div id="banner">
                <div id="prompt">
                    <button id="accept-all">Accept all</button>
                </div>
                <div id="thanks" style="display: none;">
                    <button id="dismiss">Dismiss</button>
                </div>
            </div>
        `;
        dit.cookieBanner.init({
            bannerId: 'banner',
            promptId: 'prompt',
            thanksId: 'thanks',
            acceptAllId: 'accept-all',
            dismissId: 'dismiss'
        });
        window.document.dispatchEvent(new Event("DOMContentLoaded", {
            bubbles: true,
            cancelable: true
        }));
    });

    it('sets the preference cookie, removes the prompt, pushes to the GTM dataLayer and shows the thank you message', () => {
        jest.spyOn(dit.cookieBanner, 'buildCookieString');
        const defaultOptions = {
            days: 365,
            domain: 'localhost',
            path: '/',
            secure: false
        };

        document.getElementById('accept-all').click();

        expect(dit.cookieBanner.buildCookieString).toHaveBeenCalledWith(
            'cookie_preferences_set',
            'true',
            defaultOptions
        );
        expect(dit.cookieBanner.buildCookieString).toHaveBeenCalledWith(
            'cookies_policy',
            '{"essential":true,"settings":true,"usage":true,"campaigns":true}',
            defaultOptions
        );
        expect(document.cookie).toMatch('cookie_preferences_set=true');
        expect(document.cookie).toMatch('cookies_policy={"essential":true,"settings":true,"usage":true,"campaigns":true}');

        expect(window.dataLayer).toHaveLength(2);
        expect(window.dataLayer[0].event).toEqual('cookies_policy_accept');
        expect(window.dataLayer[1].event).toEqual('gtm.dom');

        expect(document.getElementById('prompt')).toBe(null);
        expect(document.getElementById('thanks').style.display).toBe('block');
    });

    it('dismisses the whole cookie banner', () => {
        document.getElementById('accept-all').click();
        document.getElementById('dismiss').click();

        expect(document.getElementById('banner')).toBe(null);
    });

    describe('buildCookieString', () => {
        it('creates a cookie with name and value', () => {
            const cookie = dit.cookieBanner.buildCookieString('foo', 'bar');

            expect(cookie).toEqual('foo=bar');
        });

        it('creates a cookie string with path, domain, secure and max age', () => {
            const cookie = dit.cookieBanner.buildCookieString('bar', 'baz', {
                path: '/',
                domain: 'example.org',
                secure: true,
                days: 7
            });

            expect(cookie).toEqual('bar=baz; path=/; domain=example.org; Secure; max-age=60*60*24*7');
        });
    });
})
