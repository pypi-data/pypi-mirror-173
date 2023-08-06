# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hype', 'hype.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2']

setup_kwargs = {
    'name': 'django-hype',
    'version': '1.0.0',
    'description': 'Referral links for Django',
    'long_description': '# Hype\n\nA Django module that implements referral link logic.\n\n\n## Concepts\n\n\nThis library implements two models:\n\n- The `ReferralLink`. This object represents a user\'s referral link, or invitation link.\n  It has a string identifier which allows the user to share their link as `/ref/<refid>/`.\n- The `ReferralHit`. This is an instance of a user (logged in or anonymous) actually following\n  a referral link.\n\n## The Anonymous Cookie\n\nWhen a ReferralLink is followed, a `ReferralHit` object is created. If the link was followed\nby a logged in user, that user will be available on the ReferralHit object as a foreign key.\nIf the link was followed by an anonymous user, a cookie will be set on the user for future\nreference.\n\nThe cookie contains a random UUID which is set on the ReferralHit. At any time, you may get\nthat cookie and, should the user log in, update all ReferralHit objects with that matching\nUUID.\nThe library includes a middleware which will automatically do this for every logged in users,\nsee `hype.middleware.AnonymousReferralMiddleware`.\n\n\n## Confirming Referrals\n\nYou may wish to implement a `SuccessfulReferral` model which is created when a user who\npreviously followed a `ReferralLink` (and thus created a `ReferralHit`) actually completes\nwhichever steps the referral system requires referred users to complete (for example:\nRegister to the website, make their first purchase, post their first comment, ...).\n\nThe `ReferralHit` model also has a `confirmed` DateTimeField which you may use for this purpose.\n\n\n## Supporting Referral Links on Any URL\n\nImplementers may find it useful to allow a referral on any URL. This is implemented in the\n`hype.middleware.ReferralLinkMiddleware` middleware, which looks at all GET requests\nand, should a valid referral link be present in the GET parameters, redirects to that referral\nlink\'s URL with the `next` parameter set to the original URL, without the referral link present.\n\nExample:\n - `/accounts/signup/?ref=abc123def` redirects to...\n - `/ref/abs123def?next=/accounts/signup/` which redirects to...\n - `/accounts/signup/`, after creating a ReferralHit.\n\n\n## Setup and configuration\n\n1. Install via `python -m pip install django-hype`\n2. Add `hype` to your `INSTALLED_APPS`\n3. Include `hype.urls` in your URLs. Example: `url(r"^ref/", include("hype.urls"))`\n4. Add `hype.middleware.AnonymousReferralMiddleware` to your `MIDDLEWARE`.\n   This is required to update referrals for anonymous users when they log in.\n5. (optional) Add `hype.middleware.ReferralLinkMiddleware` to your `MIDDLEWARE`.\n   This is required if you want `?ref=...` to redirect properly.\n\nThese steps are enough to start gathering referral information.\nYou create a referral link, and watch the `ReferralHit` table fill up as users follow it.\n\nIn addition to having that data, you may want to "confirm" referrals. The `ConfirmedReferral`\nmodel is there as a convenience model to allow you to filter down the referral hits in question.\nUpon creating a ConfirmedReferral you may also want to do something else, such as crediting a\nuser some points.\nThe atomicity and idempotency of such events is left as an exercise for the reader.\n\n\n## License\n\nThis project is licensed under the MIT license. The full license text is\navailable in the LICENSE file.\n',
    'author': 'Justin Mayer',
    'author_email': 'entroP@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
