dit.tagging = dit.tagging || {};
dit.tagging.international = new function() {

    this.init = function(page) {
        $(document).ready(function () {
            addTaggingForCTAs();
            addTaggingForBreadcrumbs();
            addTaggingForFeedback();
            switch (page) {
                case ("InternationalHomePage"):
                    addTaggingForHeroCTAs();
                    addTaggingForMarkdownLinksWithinFeaturedCard();
                    addTaggingForFeaturedArticles();
                    break;

                case ("InternationalCuratedTopicLandingPage"):
                    addTaggingForMarkdownLinksWithinFeaturedCard();
                    addTaggingForContactLinks();
                    break;

                case ("GuideLandingPage"):
                    addTaggingForGuideLinks();
                    break;

                case ("InternationalArticlePage"):
                    addTaggingForArticleHyperlinks();
                    addTaggingForRelatedPageLinks();
                    addTaggingForRelatedPageCards();
                    addTaggingForSocialShareLinks();
                    addTaggingForArticleTags();
                    break;

                case ("SectorPage"):
                    addTaggingForRelatedPageCards();
                    addTaggingForNextSteps();
                    addTaggingForCaseStudies();
                    addTaggingForRelatedPageLinks();
                    break;

                case("InternationalCapitalInvestLandingPage"):
                    addTaggingForHeroCTAs();
                    addTaggingForRegionCards();
                    break;

                case("InternationalGuideLandingPage"):
                    addTaggingForGuideLinks();
                    break;

                case("InternationalCampaignPage"):
                    addTaggingForRelatedPageLinks();
                    break;

                case("CapitalInvestOpportunityPage"):
                    addTaggingForCaseStudies();
                    addTaggingForRelatedPageCards();
                    break;

                case("InternationalContactPage"):
                    addTaggingForContactLinks();
                    break;

                case("InternationalTopicLandingPage"):
                    addTaggingForRelatedPageCards();
                    break;

                default:
                // do nothing.
            }
        });

        function addTaggingForBreadcrumbs() {
            $("[data-ga-class='breadcrumbs']").on('click', function () {
                sendEvent({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'Breadcrumb',
                    'value': $(this).text()
                });
            });
        }

        function addTaggingForFeedback() {
            $("[data-ga-class='feedback-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'Feedback'))
            });
        }

        function addTaggingForRegionCards() {
            $("[data-ga-class='region-card']").on('click', function () {
                sendEvent(ctaEvent($(this).data('ga-value'),'Regions'));
            });
        }

        function addTaggingForMarkdownLinksWithinFeaturedCard() {
            // Find any link within the featured card (as the card content is just editor defined markdown)
            $("[data-ga-class='featured-card']").on("click", function () {
                sendEvent(ctaEvent($(this).text()));
            });
        }

        function addTaggingForGuideLinks() {
            $("[data-ga-class='guide-card']").on('click', function () {
                sendEvent(ctaEvent($(this).data('ga-value'),'SetupGuide'));
            });
        }

        function addTaggingForArticleHyperlinks() {
            $("[data-ga-class='article-content']").on('click', function () {
                sendEvent({
                    'event': 'gaEvent',
                    'action': 'Link',
                    'type': 'ArticleContentLink',
                    'element': 'ArticlePage',
                    'value': $(this).text()
                });
            })
        }

        function addTaggingForRelatedPageLinks() {
            $("[data-ga-class='related-page-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'RelatedPages'));
            });
        }

        function addTaggingForRelatedPageCards() {
            $("[data-ga-class='related-page-card']").on('click', function () {
                sendEvent(ctaEvent($(this).data("ga-value"), 'RelatedPages'));
            });
        }

        function addTaggingForFeaturedArticles() {
            $("[data-ga-class='featured-article']").on('click', function () {
                sendEvent(ctaEvent($(this).data("ga-value"), 'FeaturedArticles'));
            });
        }

        function addTaggingForNextSteps() {
            $("[data-ga-class='next-steps-links']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'NextSteps'));
            });
        }

        function addTaggingForCaseStudies() {
            $("[data-ga-class='case-study-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'CaseStudy'));
            })
        }

        function addTaggingForSocialShareLinks() {
            $("[data-ga-class='social-share-link']").on('click', function () {
                sendEvent(shareEvent($(this).data('ga-value')));
            });
        }

        function addTaggingForArticleTags() {
            $("[data-ga-class='article-tag-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'ArticleTag'));
            })
        }

        function addTaggingForHeroCTAs() {
            $("[data-ga-class='hero-cta']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'Hero'));
            })
        }

        function addTaggingForCTAs() {
            $("[data-ga-class='cta']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), null));
            })
        }

        function addTaggingForContactLinks() {
            $("[data-ga-class='contact-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'Contact'))
            })
        }

        function ctaEvent(linkText, element) {
            var event = {
                'event': 'gaEvent',
                'action': 'Link',
                'type': 'CTA',
                'value': linkText
            };

            if (element) {
                event.element = element;
            }

            return event;
        }

        function shareEvent(site) {
            return {
                'event': 'gaEvent',
                'action': 'Link',
                'type': 'Share',
                'element': 'ArticlePage',
                'value': site
            }
        }
        
        function sendEvent(event) {
            window.dataLayer.push(event);
        }
    }
};
