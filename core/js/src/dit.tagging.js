if (!Element.prototype.matches) {
    Element.prototype.matches =
        Element.prototype.msMatchesSelector ||
        Element.prototype.webkitMatchesSelector;
}

if (!Element.prototype.closest) {
    Element.prototype.closest = function (s) {
        var el = this;

        do {
            if (Element.prototype.matches.call(el, s)) return el;
            el = el.parentElement || el.parentNode;
        } while (el !== null && el.nodeType === 1);
        return null;
    };
}

dit = window.dit || {}
dit.tagging = dit.tagging || {};

dit.tagging.base = new function () {
    this.init = function (debug_mode) {
        window.addEventListener('DOMContentLoaded', () => {
            // addTaggingForVideos();
            // addTaggingForForms();

            document.addEventListener('click', addTaggingForLinks);
        });

        function addTaggingForLinks(event) {
            if (event.target.tagName === 'A') {
                if (event.type === 'click') {
                    sendLinkEvent(event.target);
                }
                if (event.type === 'keydown' && event.key === 'Enter') {
                    sendLinkEvent(event.target);
                }
            }
        }

        function addTaggingForVideos() {
            $("#hero-campaign-section-watch-video-button").click(function () {
                sendVideoEvent($(this), 'play')
            });
            $('video')
                .on('play', function () {
                    sendVideoEvent($(this), 'play')
                })
                .on('pause', function () {
                    sendVideoEvent($(this), 'pause')
                })
                .on('ended', function () {
                    sendVideoEvent($(this), 'ended')
                })
        }

        function addTaggingForForms() {
            $('form').on('submit', function () {
                sendFormEvent($(this))
            })
        }

        function sendLinkEvent(link) {
            var action = link.getAttribute('data-ga-action') || 'clickLink';
            var type = link.getAttribute('data-ga-type') || inferLinkType(link);
            var element = link.getAttribute('data-ga-element') || inferElement(link);
            var value = link.getAttribute('data-ga-value') || inferLinkValue(link);
            var destination = link.getAttribute('href');

            sendEvent(linkEvent(action, type, element, value, destination));
        }

        function sendVideoEvent(video, action) {
            var type = video.data('ga-type') || 'video';
            var element = video.data('ga-element') || inferElement(video);
            var value = video.data('ga-value') || inferVideoValue(video);

            sendEvent(event(action, type, element, value));
        }

        function sendFormEvent(form) {
            var action = form.data('ga-action') || 'submit';
            var type = form.data('ga-type') || 'form';
            var element = form.data('ga-element') || inferElement(form);
            var value = form.data('ga-value') || inferFormValue(form);

            var includeFormData = form.data('ga-include-form-data');
            var formData = includeFormData && includeFormData.toLowerCase() === "true" ? form.serialize() : null;

            sendEvent(formEvent(action, type, element, value, formData));
        }

        function inferLinkType(link) {
            if (isCta(link)) {
                return 'CTA';
            }

            if (isCard(link)) {
                return 'Card';
            }

            return 'PageLink';
        }

        function inferElement(domObject) {
            var titleSection = domObject.closest('[data-ga-section]');
            var title = titleSection && titleSection.getAttribute('data-ga-section');
            if (title) {
                return title;
            }

            var idSection = domObject.closest('[id]')
            var id = id && idSection.getAttribute('id');
            if (id) {
                return id;
            }

            return '';
        }

        function inferLinkValue(link) {
            var title = guessTitleFromLinkContents(link);
            if (title) {
                return title;
            }
            return link.textContent.trim();
        }

        function inferVideoValue(video) {
            return video.find('source').attr('src');
        }

        function inferFormValue(form) {
            return form.attr('action') || '';
        }

        function isCta(link) {
            var ctaClasses = ['button', 'cta'];
            var linkClasses = link.getAttribute('class') || '';
            for (var index = 0; index < ctaClasses.length; index++) {
                if (linkClasses.includes(ctaClasses[index])) {
                    return true;
                }
            }
            return false;
        }

        function isCard(link) {
            if (link.textContent) {
                return false;
            }

            var cardClasses = ['card'];
            var linkClasses = link.css();
            for (var index = 0; index < cardClasses.length; index++) {
                if (linkClasses.includes(cardClasses[index])) {
                    return true;
                }
            }
            return false;
        }

        function guessTitleFromLinkContents(link) {
            var titleElements = ['h1', 'h2', 'h3', 'h4', 'h5', 'span', 'p'];

            for (var index = 0; index < titleElements.length; index++) {
                var titleElement = link.querySelector(titleElements[index]);
                if (titleElement) {
                    return titleElement.textContent.trim();
                }
            }
            return null;
        }

        function event(action, type, element, value) {
            return {
                'event': 'gaEvent',
                'action': action,
                'type': type,
                'element': element,
                'value': value
            }
        }

        function linkEvent(action, type, element, value, destination) {
            var linkEvent = event(action, type, element, value);
            linkEvent['destination'] = destination;

            return linkEvent;
        }

        function formEvent(action, type, element, value, data) {
            var formEvent = event(action, type, element, value);

            if (data) {
                formEvent['formData'] = data;
            }

            return formEvent;
        }

        function sendEvent(event) {
            if (debug_mode) {
                console.log(event);
            }

            window.dataLayer.push(event);
        }
    }

};

