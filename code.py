import web

render = web.template.render('templates/')
urls = (
    '/', 'index',
)
app = web.application(urls, globals())
db = web.database(dbn='mysql', user='monitor', pw='passwd', db='monitordb', port=3306)
web.config.debug = False

class index:
    def GET(self):
        cpuInfo = db.select('cpu order by id DESC limit 1')
        memInfo = db.select('mem order by id DESC limit 1')
        diskInfo = db.select('disk order by id DESC limit 1')
        netInfo = db.select('net order by id DESC limit 1')
        times = db.select('boot_time order by id DESC limit 1')
        return render.index(cpuInfo, memInfo, diskInfo, netInfo, times)

    if __name__ == "__main__":
        web.internalerror = web.debugerror
        app.run()
