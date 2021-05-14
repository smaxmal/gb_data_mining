
AVITO_START_PAGE_SELECTORS = {
    "apartments_cat": "//div[starts-with(@class, 'category-with-counters-item')]/a[text()='Недвижимость']/@href",
    "apartment_list": "//ul[starts-with(@class, 'rubricator-list-item-submenu')]"
                      "//a[starts-with(@class,'rubricator-list-item-link') and @title='Все квартиры']/@href",
    "apartment_page": "//div[starts-with(@class, 'iva-item-titleStep')]/a[@data-marker='item-title']/@href",
    "pagination": "//div[contains(@class, 'pagination-hidden')]//a[@class='pagination-page']/@href",
}

AVITO_FLAT_ITEM_SELECTORS = {
    "title": "//div[contains(@class,'item-view-title-info')]//h1/span[@class='title-info-title-text']/text()",
    "price": "//div[@id='price-value']//span[@itemprop='price']/@content",
    "address": "//div[@class='item-address']//div[@itemprop='address']/span/text()",
    "seller_url": "//div[@class='seller-info-value']//a/@href",
    "properties": "//ul[@class='item-params-list']//li[@class='item-params-list-item']/text() | "
                  "//ul[@class='item-params-list']//li[@class='item-params-list-item']/*/text()",
}

AVITO_FLAT_ITEM_COMPLEX_SELECTORS = {
    "keys": "//ul[@class='item-params-list']//li[@class='item-params-list-item']/span/text()",
    "values": "//ul[@class='item-params-list']//li[@class='item-params-list-item']/text()",
}