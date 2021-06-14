#@+leo-ver=4-thin
#@+node:zoomq.20100902112115.6559:@shadow gen4dot2htm.py
#@@language python
#@@tabwidth -4
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Changelog:
    - 10.9.2 fixed as ZqLib
    - 9.11.03 for KUP++ mapping fixed
    - 9.05.16 for kup.s.kingsoft.net/map as root
    - 9.04.21 for deep dir gen html
    - 9.03.12 for KUP.rdev dot mapping gen html
'''
VERSION = "10.9.4"
#@+others
#@+node:zoomq.20100902112115.6560:declarations
import subprocess
from datetime import datetime
from optparse import OptionParser,OptionGroup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#@-node:zoomq.20100902112115.6560:declarations
#@+node:zoomq.20100908150441.6739:默认值
DODOT = "dot %s.dot -Tpng -o %s.png -Tcmapx -o %s.map"
DOFDP = "fdp %s.dot -Tpng -o %s.png -Tcmapx -o %s.map"
DOTCSS= '''
img {
    border: 0;
    }
#mapping {text-align:center;
    border: 1px solid #eee;
    }

#powerby { text-align:right; 
    border: 1px solid #eee;
    }
#blueprintbutton { float:left; margin-top:3px; margin-right:24px; vertical-align:middle; 
    }

/*usage http://www.cssstickyfooter.com/cn/using-sticky-footer-code.html 
zip hight 150->90px*/
html, body, #wrap {height: 100%;}
body > #wrap {height: auto; min-height: 100%;}
#main {padding-bottom: 90px;}  /* must be same height as the footer */
#footer {position: relative;
	margin-top: -90px; /* negative value of footer height */
	height: 90px;
	clear:both;
	} 
'''
HTMTPL='''<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" >
  <title>%(dotPageTitle)</title>
  <link rel="stylesheet" type="text/css" href="dotmapping.css" />
</head>
<body>
    <center>
    <img src="%(imgame)s"" usemap="%(mapname)s"/>
    %(map4dot)s<br/>
    <img src="idx-zoomquiet-legend.png" usemap=""/>
    </center>
    <hr/>
</body>
</html>
'''

#@-node:zoomq.20100908150441.6739:默认值
#@+node:zoomq.20100907214327.11503:class zqlog
class zqlog():
    '''z quickly logging,export all kinds of log as stderr
    usage:
        log = zqlog()
        log.info
        log.debug
        log.error
        log.warning

        log.info("info!")
        log.debug("debug!")
        log.error("error!")
        log.warning("warning")
    配合CL参数: -Q|V|N|D 过滤不同等级的输出
    mdebug|verbose|mquiet|mnotdo
    '''
    #@    @+others
    #@+node:zoomq.20100907214327.11504:__init__()
    def __init__(self,optionValues):
        '''初始化日志输出句柄
        '''
        self.tformatter = "%y%m%d %H:%M:%S,%f"
        self.lformatter = "%(asctime)s - %(levelname)-8s - %(message)s\n"
        self.hdlr = sys.stderr
        self.ov = optionValues

    #@-node:zoomq.20100907214327.11504:__init__()
    #@+node:zoomq.20100908150441.6730:__logit()
    def __logit(self, levelname,message):
        '''日志输出行动函式
        datetime.datetime.now().strftime("%y%m%d %H:%M:%S,%f")
        '''
        asctime = datetime.now().strftime(self.tformatter)
        levelname = levelname.upper()
        self.hdlr.write(self.lformatter%locals())
    #@-node:zoomq.20100908150441.6730:__logit()
    #@+node:zoomq.20100908091715.7752:__getattr__()
    def __getattr__(self, levelname):
        #print self.ov
        if self.ov.mquiet:
            self.__dict__[levelname] = lambda message:None
        elif self.ov.mnotdo:
            if levelname == "info":
                self.__dict__[levelname] = lambda message:self.__logit(levelname,str(message))
            else:
                self.__dict__[levelname] = lambda message:None
        elif self.ov.verbose:
            if levelname == "debug":
                self.__dict__[levelname] = lambda message:None
            else:
                self.__dict__[levelname] = lambda message:self.__logit(levelname,str(message))
        elif self.ov.mdebug:
            self.__dict__[levelname] = lambda message:self.__logit(levelname,str(message))
        else:
            # 默认情况同 -N
            if levelname == "info":
                self.__dict__[levelname] = lambda message:self.__logit(levelname,str(message))
            else:
                self.__dict__[levelname] = lambda message:None
    #@-node:zoomq.20100908091715.7752:__getattr__()
    #@-others

#@-node:zoomq.20100907214327.11503:class zqlog
#@+node:zoomq.20100906103453.10040:_gen()
def _gen(dotis,tplf,dotf,mapname,wxpf):
    """usage dot exp png+img map,auto usage html tpl writ out idenx page!
    """
    if "dot" in dotis:
        runtpl = DODOT
    else:
        runtpl = DOFDP
    script = VERSION
    gentime = GENTIME
    TPL = tplf
    dotmap = dotf.split(".")[0]
    #mapname = dotmap.split("/")[-1]
    #print dotmap
    #css = open(FOOTCSS).read()
    genmap = runtpl%(dotmap,dotmap,dotmap)
    expath = os.path.dirname(wxpf)
    r, w, e = popen2.popen3(genmap)
    print e.readlines()
    print r.readlines()
    r.close()
    e.close()
    w.close()
    cmapx = open("%s.map"%dotmap).read()#.decode('utf8')
    dotmap = "/%s"%dotmap
    urlroot = ROOTURL
    open(wxpf,"w").write(open(TPL).read() % locals())
    print "%s done gen mapping @%s"%(VERSION,GENTIME)

#@-node:zoomq.20100906103453.10040:_gen()
#@+node:zoomq.20100902112115.6561:gen()
def gen(ov,log):
    """渲染输出包图片含热区的HTML
    """
    pass
#@nonl
#@-node:zoomq.20100902112115.6561:gen()
#@+node:zoomq.20100906103453.10038:_main()
def _main(ov,log):
    '''默认主函式,组合响应各种参数,调用实际行为..
    #{'mdebug': False, 'verbose': True, 'title': '.dot \xe5\x9b\xbe\xe8\xb0\xb1', 'tdd': False, 'mquiet': False, 'expage': './index.html', 'exptpl': './idx.htm', 'mnotdo': False, 'fdp': False}
    #<logging.RootLogger instance at 0x968caac>
    '''
    #@    @+others
    #@-others
    if ov.tdd:
        import doctest
        doctest.testmod()
        #print "TDD?"
    log.error("错误")
    log.info("消息")
    log.debug("调试")
    log.warning("警告")
    log.info("消息2")
    #gen(ov,log)
#@-node:zoomq.20100906103453.10038:_main()
#@-others
if __name__ == '__main__':      # this way the module can be
    #@    <<__main__>>
    #@+node:zoomq.20100902112115.6562:<<__main__>>
    '''usage::
    gen4dot2htm.py -t path/2/模板.htm -o path/2/发布.html -i '标题'
    业务参数:
        -t 页面输出模板
        -o 输出页面
        -i 页面标题
    通用参数:
        -n 测试模式:不作为,测试输出相关参数
        -d 调试模式:打印debug信息到屏幕
        -q 安静模式:不输出任何信息
        -v 运营模式:输出 INFO|WARNING|ERROR 到sys.stderr

        -h 使用帮助
        -version 版本查询
    '''
    #@<<交互参数>>
    #@+node:zoomq.20100903105555.6662:<<交互参数>>
    usage = "$python %prog [-V|N|D|Q][--dot|fdp][-t path/2/templete.htm] [-o /path/2/export.html] [-i 'title of page']"
    parser = OptionParser(usage,version="%s {powered by Zoom.Quiet+Leo}"%VERSION)
    #@<<运营模式组>>
    #@+node:zoomq.20100906103453.10041:<<运营模式组>>
    gRun = OptionGroup(parser, "Group for Running",
        '''DEFAULT::
    -V False    -N False    -D False    -Q False'''
        )
    gRun.add_option("-V","--verbose",metavar="",help="mod_run: export INFO|WARNING|ERROR ->sys.stderr"
        ,dest="verbose",action="store_true"
        ,default=False
        )
    gRun.add_option("-N","--notdo",metavar="",help="mod_try: no realy do,export INFO"
        ,dest="mnotdo",action="store_true"
        ,default=False
        )
    gRun.add_option("-D","--debug",metavar="",help="mod_debug: export DEBUG|INFO|WARNING|ERROR ->sys.stderr"
        ,dest="mdebug",action="store_true"
        ,default=False
        )
    gRun.add_option("-Q","--quiet",metavar="",help="mod_quiet: export NULL"
        ,dest="mquiet",action="store_true"
        ,default=False
        )
    gRun.add_option("--doctest",metavar="",help="mod_test: runnin doctest"
        ,dest="tdd",action="store_true"
        ,default=False
        )
    parser.add_option_group(gRun)

    #@-node:zoomq.20100906103453.10041:<<运营模式组>>
    #@nl
    gIput = OptionGroup(parser, "Group fo Import",
        "them need realy obj.")
    gIput.add_option("-t","--tmplete",metavar="path/2/tpl.htm"
        ,dest="exptpl",nargs=1,type="string"
        ,default="./idx.htm"
        ,help="file name with ppath "
        "e.g: ../tpl/idx.htm"
        "   DEFAULT: ./idx.htm"
        )
    gIput.add_option("-o","--ouyput",metavar="path/2/page.html"
        ,dest="expage",nargs=1,type="string"
        ,default="./index.html"
        ,help="templet file name with ppath "
        "e.g: ../exp/idx.html"
        "   DEFAULT: ./index.html"
        )
    gIput.add_option("-i","--title",metavar=""
        ,dest="title",nargs=1,type="string"
        ,default=".dot mapping"
        ,help="Page Title"
        )
    gIput.add_option("--fdp",metavar=""
        ,dest="fdp",action="store_true"
        ,default=False
        ,help="usahe fdp tool"
        "   DEFAULT:dot"
        )
    parser.add_option_group(gIput)
    #@-node:zoomq.20100903105555.6662:<<交互参数>>
    #@nl
    (options, args) = parser.parse_args()
    #@+others
    #@+node:zoomq.20100907214327.11513:主业务
    #log4all,hdlr = __initlog()
    ov = parser.values
    # 检查是否没有参数
    if 1==len(sys.argv):
        parser.print_help()
    # 切换dot 生成命令
    DOTORDER = DODOT
    if ov.fdp:
        DOTORDER = DOFDP

    log = zqlog(ov)
    log.info
    log.debug
    log.error
    log.warning
    _main(ov,log)
    '''
    log.info("消息")
    log.debug("调试")
    log.error("错误")
    log.warning("警告")
    '''
    #@-node:zoomq.20100907214327.11513:主业务
    #@-others
    #@-node:zoomq.20100902112115.6562:<<__main__>>
    #@nl
#@-node:zoomq.20100902112115.6559:@shadow gen4dot2htm.py
#@-leo
