
class service_analysis(object):
    def func():
        print ('this is analysis')
        
    def flowrate(duration, weight_powder):
        print('flowrate')
        flowrate = duration / weight_powder
        return flowrate

    def apparent_density(weight_scrapecup, weight_powder):
        print('apparent density')
        apparent_density = weight_scrapecup / weight_powder
        return apparent_density
    
if __name__ == "__main__":
    print('analysis main')