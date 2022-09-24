#coding=utf-8

class PriceInfo:

    def __init__(self):

        self.productId = ''
        self.publishedState = 'published'
        self.purchaseType = 'managed_by_android'
        self.AutoTranslate = 'false'
        self.AutoFillPrices = 'false'
        self.PricingTemplateID = ''

        self.local_title_des = ''
        self.price_info = ''

    # def toInfoArray(self):
    #     a = []
    #     a.append(self.productId)
    #     a.append(self.publishedState)
    #     a.append(self.purchaseType)
    #     # a = [self.productId, self.publishedState, self.purchaseType,self.AutoTranslate,self.local_title_des,self.AutoFillPrices,self.price_info,self.PricingTemplateID]
    #     return a

