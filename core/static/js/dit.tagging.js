dit.tagging = dit.tagging || {};
dit.tagging.international = new function() {

    this.init = function(page) {
        $(document).ready(function () {
            switch (page) {
                case ("InternationalHomePage"):
                    addTaggingForFeaturedCards('International Landing Page');
                    break;

                case ("CuratedLandingPage"):
                    addTaggingForFeaturedCards('Doing Business in the UK');
                    break;

                case ("GuideLandingPage"):
                    addTaggingForGuideLinks();
                    break;

                case ("ArticlePage"):
                    addTaggingForArticleHyperlinks();
                    addTaggingForRelatedArticles('Article Page');
                    break;

                case ("SectorPage"):
                    addTaggingForRelatedPages();
                    addTaggingForNextSteps();
                    addTaggingForCaseStudies();
                    break;

                default:
                // do nothing.
            }
        });

        function addTaggingForFeaturedCards(label) {
            // Find any link within the featured card (as the card content is just editor defined markdown)
            $("[data-ga-class='large-feature']").find('a').on("click", function () {
                window.dataLayer.push({
                    'eventAction': 'Link',
                    'eventCategory': 'Large Feature',
                    'eventLabel': label,
                    'eventValue': $(this).text()
                });
            });

            $("[data-ga-class='small-feature']").find('a').on('click', function () {
                window.dataLayer.push({
                    'eventAction': 'Link',
                    'eventCategory': 'Small Feature',
                    'eventLabel': label,
                    'eventValue': $(this).text()
                });
            })
        }

        function addTaggingForGuideLinks() {
            $("[data-ga-class='guide-card']").find('a').on('click', function () {
                window.dataLayer.push({
                    'eventAction': 'Link',
                    'eventCategory': 'Setup Guide Link',
                    'eventLabel': 'Setup Guide Page',
                    'eventValue': $(this).text()
                });
            });
        }

        function addTaggingForArticleHyperlinks() {
            $("[data-ga-class='article-content']").find('a').on('click', function () {
                window.dataLayer.push({
                    'eventAction': 'Link',
                    'eventCategory': 'Article Content Link',
                    'eventLabel': 'Article Page',
                    'eventValue': $(this).text()
                });
            })
        }

        function addTaggingForRelatedArticles() {
            $("[data-ga-class='related-content-card']").find('a').on('click', function () {
                window.dataLayer.push({
                    'eventAction': 'Link',
                    'eventCategory': 'Related Content',
                    'eventLabel': 'Article Page',
                    'eventValue': $(this).text()
                });
            });
        }

        function addTaggingForRelatedPages() {
            $("[data-ga-class='related-pages']").find('a').on('click', function () {
                window.dataLayer.push({
                    'eventAction': 'Link',
                    'eventCategory': 'Related Content',
                    'eventLabel': 'Industry Page',
                    'eventValue': $(this).text()
                });
            });
        }

        function addTaggingForNextSteps() {
            $("[data-ga-class='next-steps-links']").find('a').on('click', function () {
                window.dataLayer.push({
                    'eventAction': 'Link',
                    'eventCategory': 'Next Steps',
                    'eventLabel': 'Industry Page',
                    'eventValue': $(this).text()
                });
            });
        }

        function addTaggingForCaseStudies() {
            $("[data-ga-class='case-study-link']").on('click', function () {
                window.dataLayer.push({
                    'eventAction': 'Link',
                    'eventCategory': 'Case Study',
                    'eventLabel': 'Industry Page',
                    'eventValue': $(this).text()
                });
            })
        }
    }
};
