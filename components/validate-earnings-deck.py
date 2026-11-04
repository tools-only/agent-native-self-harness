# program: on
# description: Check slide count, figures, citations, caveats, HTML, and navigation.
# tags: presentation, html
import re
s=open('artifacts/presentation.html',encoding='utf-8').read()
slides=re.findall(r'<section class="slide(?:\s[^\"]*)?"',s)
checks={
'exactly_15_slides':len(slides)==15,
'one_active_slide_start':bool(re.search(r'<section class="slide active',s)) and s.count('class="slide active')==1,
'native_html_content':all(x in s for x in ['<table class="table">','<div class="card">','<h2>']),
'keyboard_and_button_navigation':all(x in s for x in ['ArrowRight','ArrowLeft',"getElementById('prev')","getElementById('next')"]),
'citations_and_figures':all(x in s for x in ['Source: Earnings release','Third-Quarter 2021 Results','$11.7B','$3.74','$3.0T','$1.6T','12.9%','13.6%']),
'finance_explanation_and_caveats':all(x in s for x in ['fully taxable-equivalent','not core or recurring profits','excludes Commercial Card','past 90 days','CECL capital transition provisions','does not say whether it is included']),
'self_contained_no_external_assets':not bool(re.search(r'(src|href)=[\"\']https?://',s,re.I)),
}
import json
ok=all(checks.values())
{'ok':ok,'reason':f"{sum(checks.values())}/{len(checks)} checks passed; failed: {[k for k,v in checks.items() if not v]}"}
