import zipimport

importer = zipimport.zipimporter('mylibs/turbotopics-py.mod')
#importer = zipimport.zipimporter('nlplibs.mod')

print importer 

gs = importer.load_module('turbotopics')



