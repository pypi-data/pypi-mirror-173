"""
   File Name：     PyGeoTimes
   Description :
   Author :       abhay
   date：          2022/10/24
   University: Chengdu University of Technology.
"""
import json
import os
_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data_path(path):
    return os.path.join(_ROOT, 'lexion', path)
    # return path

def read_file(filename):
    with open(get_data_path(filename), 'r') as f:
            filename = [i.strip() for i in f.readlines() if i]
            return filename

class GeoTimes(object):
    def __init__(self,sentences,title=None):
        """
        :param sentences:  A text that may contain geologic time
        :param title: A title that may contain geologic time
        """
        self.sentences = sentences
        self.title = title

    def get_geotime(self):
        with open(get_data_path('GTS-format.txt'), 'r') as f:
            ages = json.loads(f.read())

        age_stage_txt = read_file(get_data_path('stage.txt'))
        age_period_txt = read_file(get_data_path('period.txt'))
        age_period = [age for age in age_period_txt if age in self.title]
        if age_period:
            age_period_value = age_period
        else:
            age_period_value = [age for age in age_period_txt if age in self.sentences]
        age_stage_value = [age for age in age_stage_txt if age in self.sentences]

        if age_period_value:
            for i in age_period_value:
                if len(i.split(' ')) == 1:
                    a = [x for x in age_period_value if i in x]
                    if a and len(age_period_value) != 1:
                        age_period_value.remove(i)

        if age_stage_value:
            for i in age_stage_value:
                if len(i.split(' ')) == 1:
                    a = [x for x in age_stage_value if i in x]
                    if a:
                        age_stage_value.remove(i)

        age_stage_values=[]
        if age_period_value:
            for i in age_period_value:
                if len(i.split(' ')) == 2:
                    j = i.split(' ')[-1]
                else:
                    j = i
                match_stage = ages[j]
                for stage in age_stage_value:
                    age_stage_values.extend([stage for l in match_stage if l in stage])
        return age_period_value,age_stage_values



if __name__ == '__main__':
    tilte = 'First Records of Late Triassic Conodont Fauna and δCcarb from the Dengdengqiao Section, Dangchang County, Gansu Province, Northwestern China'
    sentence = 'Based on a study of 49 conodont and 57 geochemical samples from the Upper Triassic, carbonate-dominated Dengdengqiao Formation, Qinling Basin, China, the Carnian conodonts and carbon isotope records are first reported. Two genera and four species have been identified amongst 87 conodont elements: Mosherella praebudaensis, Mo. longnanensis sp. nov., Mo. sp., and “Misikella” longidentata. The presence of Mo. praebudaensis indicates that the lower part (bed 2) of the formation is attributable to the Julian (lower Carnian) substage. A radiolarian fauna identified in a previous study belongs to the upper Carnian, but the sampling horizon is unclear. The δCcarb curve shows a ~1.8‰ negative excursion beginning from upper part of bed 3, but its stratigraphic location is uncertain. The Dengdengqiao Formation is clearly at least partly of Carnian age but could include younger strata. The abundant calcareous algae at the section is probably due to some transport rather than preserved in site. The unusual ecosystem with rare marine organisms may reflect long-term stressful and unfavorable conditions at Dengdengqiao.'
    geo = GeoTimes(sentence,tilte)
    print(geo.get_geotime())