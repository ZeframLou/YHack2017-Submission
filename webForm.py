#import declarations
import web
from web import form
import importlib

#this is what allows us to render the HTML files
render = web.template.render('templates/')

#global variables
finished = False

#sets URL for homepage
urls = ('/home', 'index')
app = web.application(urls, globals())

#creates form
myform = form.Form(
    #form fields
    form.Textbox("interest",
        form.notnull, description="Technology of interest:"))
        #name of field, form validation, description and name on website

#START funct method
def funct(stringVal):
    print "Entered into funct" #for testing
    print "the value that was passed in was: " + stringVal #for testing
    print "Starting Imports" #for testing
    import trends as trendObj
    import redditTest as reddittestObj
    print "Imports completed" #for testing
    print "Starting Google trends" #for testing
    testArr = trendObj.googleTrends(stringVal)
    print "Completed Google trends" #for testing
    print testArr
    try:
        print "Starting Reddit test" #for testing
        hits = reddittestObj.popularity(stringVal, testArr[0], testArr[1])
        print "hits are: " + hits #for testing
        print "Finished Reddit test" #for testing

        finished = True
        return hits

    except:
        finished = True
        return 0
#END of funct method

#START of index class
class index:
    #GET function sets the webpage with the created form and the HTML
    def GET(self):
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.formtest(form, finished)

    #POST function begins when input has been entered into the form
    def POST(self):
        #generates new form and variable with input
        user_data = web.input()
        form = myform()

        if not form.validates():
            return render.formtest(form, finished)

        #This is what executes when the code is correct
        else:
            render.formtest(form, finished)
            hits = funct(user_data.interest)
            return render.resultsHTML(hits)



if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
