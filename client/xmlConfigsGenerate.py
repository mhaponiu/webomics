from xml.dom.minidom import Document
import re
import sys
import os
from symbol import parameters



## Pomocnicza klasa do generowania pliku XML
class XmlBuilder:
    ## Konstruktor
    def __init__(self):
        self.doc = Document()
    
    ## Funkcja tworzaca nowego node'a
    #  @param node_name: Nazwa tworzonego node'a
    #  @param parent_node: Rodzic tworzonego node'a - parametr nieobowiazkowy
    #  @param value: Wartosc tworzonego node'a - parametr nieobowiazkowy
    #  @param with_attribs: Slownik atrybutow tworzonego node'a - parametr nieobowiazkowy
    #  @return: 
    def createNode(self, node_name, parent_node = '', value = '', with_attribs = {}):
        node = self.doc.createElement(node_name)
        if parent_node == '':   # Utworzenie rodzica
            created_node = self.doc.appendChild(node)
        else:                  # Utworzenie dziecka
            created_node = parent_node.appendChild(node)
        if value != '':
            text_node = self.doc.createTextNode(value)
            node.appendChild(text_node)
        if with_attribs != {}:
            for key, value in with_attribs.items():
                self.setAttribute(created_node, key, value)
        return created_node
    
    ## Funkcja dodajaca atrybut do zadanego node'a
    #  @param node: Node, do ktorego ma zostac dodany atrybut
    #  @param key: Nazwa atrybutu
    #  @param value: Wartosc atrybutu
    def setAttribute(self, node, key, value):
        node.setAttribute(key, value)
    
    ## Funkcja zwracajaca aktualnie wygenerowanego XMLa
    #  @return: Aktualnie zbudowany plik XML w postaci tekstowej
    def getXML(self):
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
        pretty_XML = text_re.sub('>\g<1></', self.doc.toprettyxml(encoding="utf-8", indent="  "))
        pretty_XML = pretty_XML.replace("&quot;", "\"")
        return pretty_XML
    
    ## Funkcja zapisuje aktualnie wygenerowanego XMLa do podanego sciazka pliku
    #  @param file_name: Sciezka do pliku, gdzie ma zostac zapisany plik XML
    def saveXML(self, file_name):
        xml_file = open(file_name, "w")
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
        pretty_XML = text_re.sub('>\g<1></', self.doc.toprettyxml(encoding="utf-8", indent="  "))
        pretty_XML = pretty_XML.replace("&quot;", "\"")
        xml_file.write(str(pretty_XML))
        xml_file.close()

class XmlConfigs():
    WINDOWS_ = "Windows"
    LINUX_ = "Linux"
    
    def __init__(self, type, flex_path, project_path):
        if type == self.WINDOWS_:
            self.flex_path = str(flex_path).replace("/", "\\")
            self.project_path = str(project_path).replace("/", "\\")
        else:
            self.flex_path = str(flex_path).replace("\\", "/")
            self.project_path = str(project_path).replace("\\", "/")
    
    def generate(self, output_file):
        config_string = self.generateConfig()
        
        xml_file = open(output_file, "w")
        xml_file.write(str(config_string))
        xml_file.close()
        
        return config_string
    
    def generateConfig(self):
        #print "\t\tSPARKSKINS:", os.path.join(self.flex_path, 'frameworks', 'libs', 'sparkskins.swc')
        return '''<flex-config>
   <compiler>
      <accessible>true</accessible>
      <allow-source-path-overlap>false</allow-source-path-overlap>
      <as3>true</as3>
      <debug>true</debug>
      <es>false</es>
      <external-library-path>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'player', '11.1', 'playerglobal.swc') + '''</path-element>
      </external-library-path>
      <fonts>
         <advanced-anti-aliasing>true</advanced-anti-aliasing>
         <local-fonts-snapshot>${flexlib}/localFonts.ser</local-fonts-snapshot>
         <managers>
            <manager-class>flash.fonts.JREFontManager</manager-class>
            <manager-class>flash.fonts.BatikFontManager</manager-class>
            <manager-class>flash.fonts.AFEFontManager</manager-class>
            <manager-class>flash.fonts.CFFFontManager</manager-class>
         </managers>
         <max-cached-fonts>20</max-cached-fonts>
         <max-glyphs-per-face>1000</max-glyphs-per-face>
      </fonts>
      <keep-generated-actionscript>false</keep-generated-actionscript>
      <library-path>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'authoringsupport.swc') + '''</path-element>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'locale', '{locale}') + '''</path-element>
         <path-element>''' + os.path.join(self.project_path, 'client', 'libs') + '''</path-element>
      </library-path>
      <locale>
         <locale-element>en_US</locale-element>
      </locale>
      <mobile>false</mobile>
      <mxml>
      </mxml>
      <namespaces>
         <namespace>
            <uri>http://ns.adobe.com/mxml/2009</uri>
            <manifest>''' + os.path.join(self.flex_path, 'frameworks', 'mxml-2009-manifest.xml') + '''</manifest>
         </namespace>
         <namespace>
            <uri>library://ns.adobe.com/flex/spark</uri>
            <manifest>''' + os.path.join(self.flex_path, 'frameworks', 'spark-manifest.xml') + '''</manifest>
         </namespace>
         <namespace>
            <uri>library://ns.adobe.com/flex/mx</uri>
            <manifest>''' + os.path.join(self.flex_path, 'frameworks', 'mx-manifest.xml') + '''</manifest>
         </namespace>
         <namespace>
            <uri>http://www.adobe.com/2006/mxml</uri>
            <manifest>''' + os.path.join(self.flex_path, 'frameworks', 'mxml-manifest.xml') + '''</manifest>
         </namespace>
      </namespaces>
      <omit-trace-statements>true</omit-trace-statements>
      <optimize>true</optimize>
      <show-actionscript-warnings>true</show-actionscript-warnings>
      <show-binding-warnings>true</show-binding-warnings>
      <show-shadowed-device-font-warnings>false</show-shadowed-device-font-warnings>
      <show-unused-type-selector-warnings>true</show-unused-type-selector-warnings>
      <source-path>
         <path-element>''' + os.path.join(self.project_path, 'client', 'src') + '''</path-element>
      </source-path>
      <strict>true</strict>
      <theme>
         <filename>''' + os.path.join(self.flex_path, 'frameworks', 'themes', 'Spark', 'spark.css') + '''</filename>
      </theme>
      <use-resource-bundle-metadata>true</use-resource-bundle-metadata>
      <verbose-stacktraces>false</verbose-stacktraces>
      <warn-array-tostring-changes>false</warn-array-tostring-changes>
      <warn-assignment-within-conditional>true</warn-assignment-within-conditional>
      <warn-bad-array-cast>true</warn-bad-array-cast>
      <warn-bad-bool-assignment>true</warn-bad-bool-assignment>
      <warn-bad-date-cast>true</warn-bad-date-cast>
      <warn-bad-es3-type-method>true</warn-bad-es3-type-method>
      <warn-bad-es3-type-prop>true</warn-bad-es3-type-prop>
      <warn-bad-nan-comparison>true</warn-bad-nan-comparison>
      <warn-bad-null-assignment>true</warn-bad-null-assignment>
      <warn-bad-null-comparison>true</warn-bad-null-comparison>
      <warn-bad-undefined-comparison>true</warn-bad-undefined-comparison>
      <warn-boolean-constructor-with-no-args>false</warn-boolean-constructor-with-no-args>
      <warn-changes-in-resolve>false</warn-changes-in-resolve>
      <warn-class-is-sealed>true</warn-class-is-sealed>
      <warn-const-not-initialized>true</warn-const-not-initialized>
      <warn-constructor-returns-value>false</warn-constructor-returns-value>
      <warn-deprecated-event-handler-error>false</warn-deprecated-event-handler-error>
      <warn-deprecated-function-error>true</warn-deprecated-function-error>
      <warn-deprecated-property-error>true</warn-deprecated-property-error>
      <warn-duplicate-argument-names>true</warn-duplicate-argument-names>
      <warn-duplicate-variable-def>true</warn-duplicate-variable-def>
      <warn-for-var-in-changes>false</warn-for-var-in-changes>
      <warn-import-hides-class>true</warn-import-hides-class>
      <warn-instance-of-changes>true</warn-instance-of-changes>
      <warn-internal-error>true</warn-internal-error>
      <warn-level-not-supported>true</warn-level-not-supported>
      <warn-missing-namespace-decl>true</warn-missing-namespace-decl>
      <warn-negative-uint-literal>true</warn-negative-uint-literal>
      <warn-no-constructor>false</warn-no-constructor>
      <warn-no-explicit-super-call-in-constructor>false</warn-no-explicit-super-call-in-constructor>
      <warn-no-type-decl>true</warn-no-type-decl>
      <warn-number-from-string-changes>false</warn-number-from-string-changes>
      <warn-scoping-change-in-this>false</warn-scoping-change-in-this>
      <warn-slow-text-field-addition>true</warn-slow-text-field-addition>
      <warn-unlikely-function-value>true</warn-unlikely-function-value>
      <warn-xml-class-has-changed>false</warn-xml-class-has-changed>
   </compiler>
   <default-background-color>0xFFFFFF</default-background-color>
   <default-frame-rate>24</default-frame-rate>
   <default-script-limits>
      <max-recursion-depth>1000</max-recursion-depth>
      <max-execution-time>60</max-execution-time>
   </default-script-limits>
   <default-size>
      <width>500</width>
      <height>375</height>
   </default-size>
   <frames>
   </frames>
   <framework>halo</framework>
   <load-config>${flexlib}/${configname}-config.xml</load-config>
   <metadata>
      <creator>unknown</creator>
      <description>http://www.adobe.com/products/flex</description>
      <language>EN</language>
      <publisher>unknown</publisher>
      <title>Adobe Flex 4 Application</title>
   </metadata>
   <remove-unused-rsls>true</remove-unused-rsls>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'textLayout.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/tlf/2.0.0.232/textLayout_2.0.0.232.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>textLayout_2.0.0.232.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'osmf.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/flex/4.6.0.23201/osmf_1.0.0.16316.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>osmf_1.0.0.16316.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'framework.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/flex/4.6.0.23201/framework_4.6.0.23201.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>framework_4.6.0.23201.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'mx', 'mx.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/flex/4.6.0.23201/mx_4.6.0.23201.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>mx_4.6.0.23201.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'rpc.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/flex/4.6.0.23201/rpc_4.6.0.23201.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>rpc_4.6.0.23201.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'charts.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/flex/4.6.0.23201/charts_4.6.0.23201.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>charts_4.6.0.23201.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'spark.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/flex/4.6.0.23201/spark_4.6.0.23201.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>spark_4.6.0.23201.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'advancedgrids.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/flex/4.6.0.23201/advancedgrids_4.6.0.23201.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>advancedgrids_4.6.0.23201.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'sparkskins.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/flex/4.6.0.23201/sparkskins_4.6.0.23201.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>sparkskins_4.6.0.23201.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-path>
      <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'spark_dmv.swc') + '''</path-element>
      <rsl-url>http://fpdownload.adobe.com/pub/swz/flex/4.6.0.23201/spark_dmv_4.6.0.23201.swz</rsl-url>
      <policy-file-url>http://fpdownload.adobe.com/pub/swz/crossdomain.xml</policy-file-url>
      <rsl-url>spark_dmv_4.6.0.23201.swz</rsl-url>
   </runtime-shared-library-path>
   <runtime-shared-library-settings>
      <application-domain>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'textLayout.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'osmf.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'framework.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'mx', 'mx.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'rpc.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'charts.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'spark.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'advancedgrids.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'sparkskins.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
         <path-element>''' + os.path.join(self.flex_path, 'frameworks', 'libs', 'spark_dmv.swc') + '''</path-element>
         <application-domain-target>default</application-domain-target>
      </application-domain>
   </runtime-shared-library-settings>
   <static-link-runtime-shared-libraries>false</static-link-runtime-shared-libraries>
   <swf-version>14</swf-version>
   <target-player>11.1.0</target-player>
   <use-network>true</use-network>
   <verify-digests>true</verify-digests>
</flex-config>
        '''


#xml_conf = XmlConfigs(XmlConfigs.LINUX_, "/home/proz/flex_sdk_4.6", "/home/proz/Projekty/GenomeBrowser/trunk/implementation")
#xml_conf.generate()

#xml_conf = XmlConfigs(XmlConfigs.WINDOWS_, "E:\\Adobe\\Adobe Flash Builder 4.6\\sdks\\4.6.0", "D:\\Uczelnia\\PracaMagisterska\\GenomeBrowser\\trunk\\implementation")
#xml_conf.generate()
