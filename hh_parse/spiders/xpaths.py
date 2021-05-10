
HH_START_PAGE_SELECTORS = {
    "page": "//div[@data-qa='pager-block']//a[@data-qa='pager-page']/@href",
    "employer": "//div[@class='vacancy-serp-item__row']//a[@data-qa='vacancy-serp__vacancy-employer']/@href",
    "vacancy_employer": "//div[@class='vacancy-company-details']/a[@data-qa='vacancy-company-name']/@href",
    "vacancy": "//div[@class='vacancy-serp-item__info']//a[@data-qa='vacancy-serp__vacancy-title']/@href",
    "employer_vacancies": "//div[@class='employer-sidebar-block']/"
                          "a[@data-qa='employer-page__employer-vacancies-link']/@href"
}

HH_VACANCY_ITEM_SELECTORS = {
    "title": "//div[@class='vacancy-title']/h1/text()",
    "employer_url": "//div[@class='vacancy-company-wrapper']//a[@data-qa='vacancy-company-name']/@href",
    "skills": "//div[@class='bloko-tag-list']//div[@data-qa='bloko-tag bloko-tag_inline skills-element']/span/text()",
    "salary": "//div[@class='vacancy-title']//p/span/text()",
}

HH_EMPLOYER_ITEM_SELECTORS = {
    "business_line": "//div[@class='bloko-text-emphasis']/following-sibling::p/text()",
    "title": "//div[@class='company-header']//*[@data-qa='company-header-title-name']/text()"
             " | //div[@class='tmpl_hh_vacancy_block']/h3/text()",
    "description": "//div[@data-qa='company-description-text']/div/p/text()"
                   " | //div[@class='tmplt_hh-about-text']/p/text()"
                   " | //div[@class='tmpl_hh_about__content']/p/text()"
}
