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

        function addTaggingForFeaturedCards(element) {
            // Find any link within the featured card (as the card content is just editor defined markdown)
            $("[data-ga-class='large-feature']").find('a').on("click", function () {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'LargeFeature',
                    'element': element,
                    'value': $(this).text()
                });
            });

            $("[data-ga-class='small-feature']").find('a').on('click', function () {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'SmallFeature',
                    'element': element,
                    'value': $(this).text()
                });
            })
        }

        function addTaggingForGuideLinks() {
            $("[data-ga-class='guide-card']").find('a').on('click', function () {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'SetupGuideLink',
                    'element': 'SetupGuidePage',
                    'value': $(this).text()
                });
            });
        }

        function addTaggingForArticleHyperlinks() {
            $("[data-ga-class='article-content']").find('a').on('click', function () {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'ArticleContentLink',
                    'element': 'ArticlePage',
                    'value': $(this).text()
                });
            })
        }

        function addTaggingForRelatedArticles() {
            $("[data-ga-class='related-content-card']").find('a').on('click', function () {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'RelatedContent',
                    'element': 'ArticlePage',
                    'value': $(this).text()
                });
            });
        }

        function addTaggingForRelatedPages() {
            $("[data-ga-class='related-pages']").find('a').on('click', function () {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'RelatedContent',
                    'element': 'IndustryPage',
                    'value': $(this).text()
                });
            });
        }

        function addTaggingForNextSteps() {
            $("[data-ga-class='next-steps-links']").find('a').on('click', function () {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'NextSteps',
                    'element': 'IndustryPage',
                    'value': $(this).text()
                });
            });
        }

        function addTaggingForCaseStudies() {
            $("[data-ga-class='case-study-link']").on('click', function () {
                window.dataLayer.push({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'CaseStudy',
                    'element': 'IndustryPage',
                    'value': $(this).text()
                });
            })
        }
    }
};
