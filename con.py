# -*- coding: UTF-8 -*-

import os
import sys
import codecs
from collections import OrderedDict

input_file = os.path.abspath(sys.argv[1])
output_dir = os.path.abspath(sys.argv[2])
book_name = sys.argv[3]
output_dir_zh = output_dir + "/zh-CN"
index = 0
index_dict = {}
tree = OrderedDict()

if not os.path.exists(output_dir_zh):
    os.makedirs(output_dir_zh)
output_file = codecs.open(output_dir_zh + '/' + book_name + '.xml', 'w', 'utf-8')


def output_prefix(output_file):
    output_file.write("<?xml version='1.0' encoding='utf-8' ?>\n")
    output_file.write("<!DOCTYPE book PUBLIC \"-//OASIS//DTD DocBook XML V4.5//EN\" \"http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd\" [\n")
    output_file.write("<!ENTITY % BOOK_ENTITIES SYSTEM \"" + book_name + ".ent\">\n")
    output_file.write("%BOOK_ENTITIES;\n")
    output_file.write("]>\n")
    output_file.write("<book>\n")
    output_file.write("  <xi:include href=\"Book_Info.xml\" xmlns:xi=\"http://www.w3.org/2001/XInclude\"/>\n")
    output_file.write("  <xi:include href=\"Preface.xml\" xmlns:xi=\"http://www.w3.org/2001/XInclude\"/>\n")
    output_file.write("  <xi:include href=\"Chapter-using-guide.xml\" xmlns:xi=\"http://www.w3.org/2001/XInclude\"/>\n")


def output_suffix(output_file):
    output_file.write("</book>")
    output_file.close()


def proccessSectionTree(output_file, line):
    if len(line.strip()) == 0:
        return
    if line.startswith("#"):
        return
    title = line[line.index("[") + 1:line.rindex("]")]
    title_path = line[line.rindex("(") + 1:line.rindex(")")]
    title_path = title_path[:-len(".md")]
    depth = (len(line) - len(line.lstrip()) + 1)/4
    index_dict[depth] = title + '|' + title_path
    target = tree
    search_depth = 0;
    while(search_depth < depth):
        target = target[index_dict[search_depth]]
        search_depth += 1
    target[index_dict[depth]] = OrderedDict()


def pandocGenerate(title_path, depth):
    command = "pandoc -s -f markdown -t docbook " + title_path.encode('utf-8') + ".md -o " + output_dir_zh.encode('utf-8') + "/" + title_path.encode('utf-8') + ".xml --template " + os.path.dirname(os.path.abspath(sys.argv[0]))
    if depth == 1:
        command += "/chapter.docbook"
    else:
        command += "/default.docbook"
    print command
    if not os.path.exists(title_path.encode('utf-8') + ".md"):
        if not os.path.exists(os.path.dirname(title_path.encode('utf-8'))):
            os.mkdir(os.path.dirname(title_path.encode('utf-8')))
        open(title_path.encode('utf-8') + ".md", 'w').close()
    os.system(command)


def proccessDockbook(tree, depth, p_title, p_title_path, output_file):
    if tree:
        if depth == 1:
            output_file.write("<?xml version='1.0' encoding='utf-8' ?>\n")
            output_file.write("<!DOCTYPE book PUBLIC \"-//OASIS//DTD DocBook XML V4.5//EN\" \"http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd\" [\n")
            output_file.write("<!ENTITY % BOOK_ENTITIES SYSTEM \"" + book_name + ".ent\">\n")
            output_file.write("%BOOK_ENTITIES;\n")
            output_file.write("]>\n")
            output_file.write("<chapter id=\"" + p_title_path.replace('/', '_') + "\">\n")
            output_file.write("  <title>" + p_title + "</title>\n")
        if depth > 1:
            output_file.write("<section>\n")
            output_file.write("<title>" + p_title + "</title>\n")
        for key in tree:
            title, title_path = key.split('|')
            title_path_index = title_path
            if depth > 0:
                title_path_index = title_path[title_path.index('/') + 1:]
            output_file.write("  <xi:include href=\"" + title_path_index + ".xml\" xmlns:xi=\"http://www.w3.org/2001/XInclude\"/>\n")
            if not os.path.exists(os.path.dirname(output_dir_zh + '/' + title_path)):
                os.mkdir(os.path.dirname(output_dir_zh + '/' + title_path))
            new_file = codecs.open(output_dir_zh + '/' + title_path + ".xml", 'w', 'utf-8')
            proccessDockbook(tree[key], depth + 1, title, title_path, new_file)
            new_file.close()
        if depth > 1:
            output_file.write("</section>\n")
        if depth == 1:
            output_file.write("</chapter>\n")
    else:
        pandocGenerate(p_title_path, depth)


def proccessSUMMARYmd():
    output_prefix(output_file)
    with codecs.open(input_file, 'r', 'utf-8') as f:
        for line in f:
            proccessSectionTree(output_file, line)
    proccessDockbook(tree, 0, None, None, output_file)
    output_suffix(output_file)
    output_file.close()


def proccessMiscPublicanFiles():
    ent = open(output_dir_zh + '/' + book_name + '.ent', 'w')
    ent.write("<!ENTITY PRODUCT \"Documents\">\n")
    ent.write("<!ENTITY BOOKID \"" + book_name + "\">\n")
    ent.write("""\
<!ENTITY YEAR "2015">
<!ENTITY HOLDER "| 易云捷讯技术有限公司 |">
<!ENTITY OVIRT " Eayun 企业级虚拟化 ">
<!ENTITY OVIRT_STORAGE " Eayun 企业级虚拟化存储 ">
<!ENTITY MANAGER "Eayun 企业级虚拟化管理中心">
<!ENTITY NODE "Eayun 企业级虚拟化宿主机">
<!ENTITY DEFAULT_LOGICAL_NETWORK "管理网络">
""")
    ent.close()

    author_group = open(output_dir_zh + '/Author_Group.xml', 'w')
    author_group.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE authorgroup PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN" "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" [
""")
    author_group.write("<!ENTITY % BOOK_ENTITIES SYSTEM \"" + book_name + ".ent\">\n")
    author_group.write("""\
%BOOK_ENTITIES;
]>
<authorgroup>
    <author>
      <firstname>哲</firstname>
      <surname>马</surname>
      <affiliation>
        <orgname>易云捷讯</orgname>
        <orgdiv>虚拟化文档组</orgdiv>
      </affiliation>
      <email>zhe.ma@eayun.com</email>
    </author>
    <author>
      <firstname>礼洋</firstname>
      <surname>潘</surname>
      <affiliation>
        <orgname>易云捷讯</orgname>
        <orgdiv>虚拟化文档组</orgdiv>
      </affiliation>
      <email>liyang.pan@eayun.com</email>
    </author>
    <author>
      <firstname>媛媛</firstname>
      <surname>相</surname>
      <affiliation>
        <orgname>易云捷讯</orgname>
        <orgdiv>虚拟化文档组</orgdiv>
      </affiliation>
      <email>yuanyuan.xiang@eayun.com</email>
    </author>
    <author>
      <firstname>亚琪</firstname>
      <surname>张</surname>
      <affiliation>
        <orgname>易云捷讯</orgname>
        <orgdiv>虚拟化文档组</orgdiv>
      </affiliation>
      <email>yaqi.zhang@eayun.com</email>
    </author>
    <author>
      <firstname>超</firstname>
      <surname>赵</surname>
      <affiliation>
        <orgname>易云捷讯</orgname>
        <orgdiv>虚拟化文档组</orgdiv>
      </affiliation>
      <email>chao.zhao@eayun.com</email>
    </author>
    <author>
      <firstname>嫣然</firstname>
      <surname>周</surname>
      <affiliation>
        <orgname>易云捷讯</orgname>
        <orgdiv>虚拟化文档组</orgdiv>
      </affiliation>
      <email>yanran.zhou@eayun.com</email>
    </author>
</authorgroup>
""")
    author_group.close()

    book_info = open(output_dir_zh + '/Book_Info.xml', 'w')
    book_info.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE bookinfo PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN" "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" [
""")
    book_info.write("<!ENTITY % BOOK_ENTITIES SYSTEM \"" + book_name + ".ent\">")
    book_info.write("""\
%BOOK_ENTITIES;
]>
<bookinfo id="book-Documents-Book_info">
""")
    book_info.write("<title>" + book_name + "</title>")
    book_info.write("""\
    <productname>EayunOS</productname>
    <productnumber>4.1</productnumber>
    <edition>0</edition>
    <pubsnumber>0</pubsnumber>
    <corpauthor>
        <inlinemediaobject>
            <imageobject>
                <imagedata fileref="Common_Content/images/title_logo.svg" format="SVG" />
            </imageobject>
        </inlinemediaobject>
    </corpauthor>
    <xi:include href="Common_Content/Legal_Notice.xml" xmlns:xi="http://www.w3.org/2001/XInclude" />
    <xi:include href="Author_Group.xml" xmlns:xi="http://www.w3.org/2001/XInclude" />
</bookinfo>
""")
    book_info.close()


    revision_his = open(output_dir_zh + '/Revision_History.xml', 'w')
    revision_his.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE appendix PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN" "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" [
""")
    revision_his.write("<!ENTITY % BOOK_ENTITIES SYSTEM \"" + book_name + ".ent\">")
    revision_his.write("""\
%BOOK_ENTITIES;
]>
<appendix id="appe-Documents-Revision_History">
    <title>修订历史</title>
    <simpara>
        <revhistory>
            <revision>
                <revnumber>0.0-0</revnumber>
                <date>Mon Jun 9 2014</date>
                <author>
                    <firstname>firstname</firstname>
                    <surname>surname</surname>
                    <email>user@mail.com</email>
                </author>
                <revdescription>
                    <simplelist>
                        <member>revdescription</member>
                    </simplelist>
                </revdescription>
            </revision>
        </revhistory>
    </simpara>
</appendix>
""")
    revision_his.close()

    publican = open(output_dir + '/publican.cfg', 'w')
    publican.write("""\
# Config::Simple 4.59
# Wed Feb 12 18:43:21 2014

brand: eayun
type: Book
xml_lang: "zh-CN"
""")
    publican.close()

    publican = open(output_dir_zh + '/Preface.xml', 'w')
    publican.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE preface PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN" "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" [
""")
    publican.write("<!ENTITY % BOOK_ENTITIES SYSTEM \"" + book_name + ".ent\">")
    publican.write("""\
%BOOK_ENTITIES;
]>
<preface id="pref-Documents-Preface">
    <title>Preface</title>
    <xi:include href="Common_Content/Conventions.xml" xmlns:xi="http://www.w3.org/2001/XInclude" />
    <xi:include href="Feedback.xml" xmlns:xi="http://www.w3.org/2001/XInclude"><xi:fallback xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include href="Common_Content/Feedback.xml" xmlns:xi="http://www.w3.org/2001/XInclude" />
    </xi:fallback>
    </xi:include>
</preface>
""")
    publican.close()

    publican = open(output_dir_zh + '/Chapter-using-guide.xml', 'w')
    publican.write("""\
<?xml version='1.0' encoding='utf-8' ?>
<!DOCTYPE chapter PUBLIC "-//OASIS//DTD DocBook XML V4.5//EN" "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" [
""")
    publican.write("<!ENTITY % BOOK_ENTITIES SYSTEM \"" + book_name + ".ent\">")
    publican.write("""\
%BOOK_ENTITIES;
]>
<chapter id="chap-Documents-Chapter-using-guide">
    <title>手册使用向导</title>
    <para>
        This is a test paragraph
    </para>
    <section id="sect-Documents-Chapter-using-guide-Section_1">
        <title>阅读管理员手册前的准备</title>
        <para>
            This is a test paragraph in a section
        </para>
    </section>

    <section id="sect-Documents-Chapter-using-guide-Section_2">
        <title>本手册的层次结构</title>
        <para>
            This is a test paragraph in Section 2
            <orderedlist>
                <listitem>
                    <para>
                        This is a test listitem.
                    </para>
                </listitem>
            </orderedlist>
        </para>
    </section>

    <section id="sect-Documents-Chapter-using-guide-Section_3">
        <title>流程实例</title>
        <para>
        </para>
           <section id="sect-Documents-Chapter-using-guide-Section_3-1">
                <title>概览</title>
                <para>
                </para>
           </section>
           <section id="sect-Documents-Chapter-using-guide-Section_3-2">
                <title>流程示例之创建iscsi数据中心</title>
                <para>
                </para>
           </section>
           <section id="sect-Documents-Chapter-using-guide-Section_3-3">
                <title>流程示例之负载</title>
                <para>
                </para>
           </section>
           <section id="sect-Documents-Chapter-using-guide-Section_3-4">
                <title>流程示例之供用户组使用的模板</title>
                <para>
                </para>
           </section>
    </section>
</chapter>
""")
    publican.close()

proccessSUMMARYmd()
proccessMiscPublicanFiles()
