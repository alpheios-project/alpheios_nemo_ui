<!--
    Copyright 2010 Cantus Foundation
    http://alpheios.net

    This file is part of Alpheios.

    Alpheios is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Alpheios is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
--><!--
    Transforms an TEI XML to  XHTML (Alpheios Enhanced Text Display)
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:t="http://www.tei-c.org/ns/1.0" 
    xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
    <xsl:output method="html" indent="yes"/>
    <xsl:param name="doclang"/>

    <xsl:template match="tei:milestone[@unit != 'card']">
        <xsl:variable name="idstring">
            <xsl:if test="@n">
                <xsl:text>m</xsl:text>
                <xsl:value-of select="@n"/>
            </xsl:if>
        </xsl:variable>
        <div class="milestone {@unit}" id="{$idstring}">
            <xsl:value-of select="@n"/>
        </div>
    </xsl:template>
    <xsl:template
        match="//tei:body | //tei:div0 | //tei:div1 | //tei:div2 | //tei:div3 | //tei:div4 | //tei:div5 | //tei:sp | //tei:div">

        <div>
            <xsl:if test="@xml:lang">
                <xsl:attribute name="class">
                    <xsl:value-of select="@type"/>
                    <xsl:text> lang_</xsl:text>
                    <xsl:value-of select="@xml:lang"/>
                </xsl:attribute>
                <xsl:attribute name="data-lang">
                    <xsl:value-of select="./@xml:lang"/>
                </xsl:attribute>
                <xsl:attribute name="lang">
                    <xsl:value-of select="./@xml:lang"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:if test="@xml:lang = 'ar'">
                <xsl:attribute name="dir">
                    <xsl:text>rtl</xsl:text>
                </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
   
    <xsl:template match="tei:head">
        <h3>
            <xsl:apply-templates/>
        </h3>
    </xsl:template>
    <xsl:template match="tei:speaker">
        <div class="speaker">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    <xsl:template match="tei:l">
        <xsl:variable name="rend" select="@rend"/>
        <div class="l {$rend}">
            <xsl:if test="@xml:lang">
                <xsl:attribute name="lang">
                    <xsl:value-of select="@xml:lang"/>
                </xsl:attribute>
            </xsl:if>
            <div class="l-text">
                <xsl:apply-templates/>
            </div>
            <xsl:if test="@n">
                <xsl:variable name="citeshow">
                    <xsl:if test="number(@n) mod 5 != 0">d-none</xsl:if>
                </xsl:variable>
                <div class="l-cite {$citeshow}">
                    <xsl:value-of select="@n"/>
                </div>    
            </xsl:if>
        </div>
    </xsl:template>

    <xsl:template match="tei:p">
        <xsl:variable name="rend" select="@rend"/>
        <div class="p {$rend}">
            <xsl:if test="@xml:lang">
                <xsl:attribute name="lang">
                    <xsl:value-of select="@xml:lang"/>
                </xsl:attribute>
            </xsl:if>
            <div class="p-text">
                <xsl:apply-templates/>
            </div>
            <div class="p-cite">
                <xsl:value-of select="@n"/>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="tei:seg">
        <xsl:variable name="rend" select="@rend"/>
        <div class="seg {$rend}">
            <xsl:if test="@xml:lang">
                <xsl:attribute name="lang">
                    <xsl:value-of select="@xml:lang"/>
                </xsl:attribute>
            </xsl:if>
            <div class="seg-text">
                <xsl:apply-templates/>
            </div>
            <div class="seg-cite">
                <xsl:value-of select="@n"/>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="tei:w">
        <xsl:variable name="wordId">
            <xsl:call-template name="ref_to_id">
                <xsl:with-param name="list" select="@n"/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="nrefList">
            <xsl:call-template name="ref_to_id">
                <xsl:with-param name="list" select="@nrefs"/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:call-template name="separate_words">
            <xsl:with-param name="real_id" select="@id"/>
            <xsl:with-param name="id_list" select="$wordId"/>
            <xsl:with-param name="nrefs" select="$nrefList"/>
            <xsl:with-param name="tbrefs" select="@ana"/>
            <xsl:with-param name="tbref" select="@ana"/>
        </xsl:call-template>
    </xsl:template>

    <!-- from scaife -->
    <!-- glyphs -->
    <!-- <xsl:include href="teig.xsl" /> -->
    <xsl:template match="//t:g">
        <xsl:choose>
            <xsl:when test="@type = 'crux' or @type = 'cross'">
                <xsl:text>†</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'crosses'">
                <xsl:text>††</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'drachma'">
                <xsl:text>₯</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'year'">
                <xsl:text>L</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'stop'">
                <xsl:text>•</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'stauros'">
                <xsl:text>+</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'staurogram'">
                <xsl:text>⳨</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'leaf'">
                <xsl:text>❦</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'dipunct'">
                <xsl:text>:</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'apostrophe'">
                <xsl:text>’</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'check' or @type = 'check-mark'">
                <xsl:text>／</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'chirho'">
                <xsl:text>☧</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'dash'">
                <xsl:text>—</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'dipunct'">
                <xsl:text>∶</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'filled-circle'">
                <xsl:text>⦿</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'filler' and @rend = 'extension'">
                <xsl:text>―</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'latin-interpunct' or @type = 'middot' or @type = 'mid-punctus'">
                <xsl:text>·</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'monogram'">
                <span class="italic">
                    <xsl:text>monogr.</xsl:text>
                </span>
            </xsl:when>
            <xsl:when test="@type = 'upper-brace-opening'">
                <xsl:text>⎧</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'center-brace-opening'">
                <xsl:text>⎨</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'lower-brace-opening'">
                <xsl:text>⎩</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'upper-brace-closing'">
                <xsl:text>⎫</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'center-brace-closing'">
                <xsl:text>⎬</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'lower-brace-closing'">
                <xsl:text>⎭</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'parens-upper-opening'">
                <xsl:text>⎛</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'parens-middle-opening'">
                <xsl:text>⎜</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'parens-lower-opening'">
                <xsl:text>⎝</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'parens-upper-closing'">
                <xsl:text>⎞</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'parens-middle-closing'">
                <xsl:text>⎟</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'parens-lower-closing'">
                <xsl:text>⎠</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'rho-cross'">
                <xsl:text>⳨</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'slanting-stroke'">
                <xsl:text>/</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'stauros'">
                <xsl:text>†</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'tachygraphic marks'">
                <span class="italic">
                    <xsl:text>tachygr. marks</xsl:text>
                </span>
            </xsl:when>
            <xsl:when test="@type = 'tripunct'">
                <xsl:text>⋮</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'double-vertical-bar'">
                <xsl:text>‖</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'long-vertical-bar'">
                <xsl:text>|</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'x'">
                <xsl:text>☓</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'xs'">
                <xsl:text>☓</xsl:text>
                <xsl:text>☓</xsl:text>
                <xsl:text>☓</xsl:text>
                <xsl:text>☓</xsl:text>
                <xsl:text>☓</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'milliaria'">
                <xsl:text>ↀ</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'leaf'">
                <xsl:text>❦</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'palm'">
                <xsl:text>††</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'star'">
                <xsl:text>*</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'interpunct'">
                <xsl:text>·</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'sestertius'">
                <xsl:text>𐆘</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'denarius'">
                <xsl:text>𐆖</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'barless-A'">
                <xsl:text>Λ</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'dot'">
                <xsl:text>.</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'stop'">
                <xsl:text>•</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'crux' or @type = 'cross'">
                <xsl:text>†</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <span class="smaller" style="font-style:italic;">
                    <xsl:text>(symbol: </xsl:text>
                    <xsl:value-of select="@type"/>
                    <xsl:text>)</xsl:text>
                </span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- edition -->


    <xsl:template match="t:phr">
        <xsl:element name="span">
            <xsl:attribute name="class">phr</xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="t:quote">
        <xsl:choose>
            <xsl:when test="@rend='blockquote'">
                <blockquote class="blockquote">
                    <xsl:apply-templates/>    
                </blockquote>
            </xsl:when>
            <xsl:otherwise>
                "<xsl:apply-templates/>"
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    
    <xsl:template match="t:q">
        <xsl:text>"</xsl:text><xsl:apply-templates/><xsl:text>"</xsl:text>
    </xsl:template>
    

    <xsl:template match="t:figure">
        <div>Figure here!
            <!--<figure>
<xsl:element name="img">
      <xsl:attribute name="src"><xsl:value-of select="./graphic/@url"/></xsl:attribute>
      <figcaption><em><xsl:value-of select="./head"/></em></figcaption>
    </xsl:element>
</figure>--></div>
    </xsl:template>

    <xsl:template match="t:lg">
        <div class="lg">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="t:pb">
        <div class="pb">
            <xsl:value-of select="@n"/>
        </div>
    </xsl:template>

    <xsl:template match="t:ab">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <xsl:template match="t:foreign[1]">
        <xsl:choose>
            <xsl:when test="preceding-sibling::t:ref[1][@cRef]">
                <strong>
                    <xsl:value-of select="."/>
                </strong>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>


    <xsl:template match="t:name[not(t:placeName)]">
        <span class="name">
            <xsl:value-of select="."/>
        </span>
    </xsl:template>

    <xsl:template match="t:name[t:placeName]">
        <a>
            <xsl:attribute name="class">placeName</xsl:attribute>
            <xsl:value-of select="t:placeName"/>
        </a>
    </xsl:template>

    <xsl:template match="t:lb"> </xsl:template>

    <xsl:template match="t:ex">
        <span class="ex">
            <xsl:text>(</xsl:text>
            <xsl:value-of select="."/>
            <xsl:text>)</xsl:text>
        </span>
    </xsl:template>

    <xsl:template match="t:abbr">
        <span class="abbr">
            <xsl:text/>
            <xsl:value-of select="."/>
            <xsl:text/>
        </span>
    </xsl:template>

    <xsl:template match="t:bibl">
        <xsl:choose>
            <xsl:when test="t:author"/>
            <xsl:when test="t:title"/>
            <xsl:otherwise>
                <xsl:element name="cite">
                    <xsl:if test="@n">
                        <xsl:attribute name="data-ref">
                            <xsl:value-of select="@n"/>
                        </xsl:attribute>
                    </xsl:if>
                    <xsl:value-of select="."/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="t:gap">
        <span class="gap">
            <xsl:choose>
                <xsl:when test="@quantity and @unit = 'character'">
                    <xsl:value-of select="string(@quantity)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>⋯</xsl:text>
                </xsl:otherwise>
            </xsl:choose>

        </span>
    </xsl:template>

    <xsl:template match="t:head">
        <div class="head">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="t:head/t:title">
        <div class="title">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="t:sp">
        <div class="speak">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="t:said">
        <div class="said">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="t:label">
        <span class="label">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="t:speaker">
        <span class="speaker">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="t:supplied">
        <span>
            <xsl:attribute name="class">supplied supplied_<xsl:value-of select="@cert"
                /></xsl:attribute>
            <xsl:text>[</xsl:text>
            <xsl:apply-templates/>
            <xsl:if test="@cert = 'low'">
                <xsl:text>?</xsl:text>
            </xsl:if>
            <xsl:text>]</xsl:text>
        </span>
    </xsl:template>

    <xsl:template match="t:note">
        <xsl:choose>
            <xsl:when test="ancestor::tei:blockquote or ancestor::tei:quote[@rend='blockquote'] or local-name(*[1]) ='bibl'">
                <footer class="blockquote-footer">
                    <xsl:apply-templates/>
                </footer>
            </xsl:when>
            <xsl:otherwise>
                <span>
                    <xsl:attribute name="class">note</xsl:attribute>
                    <xsl:element name="sup">
                        <xsl:attribute name="data-toggle">popover</xsl:attribute>
                        <xsl:attribute name="data-trigger">hover focus</xsl:attribute>
                        <xsl:text>[*]</xsl:text>
                    </xsl:element>
                    <xsl:element name="span">
                        <xsl:attribute name="class">popover-content note-content</xsl:attribute>
                        <xsl:apply-templates/>
                    </xsl:element>
                </span>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>

    <xsl:template match="t:ab/t:ref[@cRef]">
        <span class="cRef">◉</span>
        <xsl:text> </xsl:text>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="t:ab/t:ref[@target]">
        <xsl:element name="ref-lower">
            <xsl:attribute name="urn">
                <xsl:value-of select="@target"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="t:choice">
        <span class="choice">
            <xsl:attribute name="title">
                <xsl:value-of select="reg"/>
            </xsl:attribute>
            <xsl:value-of select="orig"/>
            <xsl:text> </xsl:text>
        </span>
    </xsl:template>

    <xsl:template match="t:hi">
        <xsl:choose>
            <xsl:when test="@rend = '#bold' or @rend = 'bold'">
                <strong>
                    <xsl:value-of select="."/>
                </strong>
            </xsl:when>
            <xsl:when test="@rend = 'italic' or @rend = 'italics'">
                <em>
                    <xsl:value-of select="."/>
                </em>
            </xsl:when>
            <xsl:when test="@rend = 'underline'">
                <u>
                    <xsl:value-of select="."/>
                </u>
            </xsl:when>
            <xsl:when test="@rend = 'subscript'">
                <sub>
                    <xsl:value-of select="."/>
                </sub>
            </xsl:when>
            <xsl:when test="@rend = 'superscript'">
                <sup>
                    <xsl:value-of select="."/>
                </sup>
            </xsl:when>
            <xsl:when test="@rend = 'smallcaps'">
                <small>
                    <xsl:value-of select="."/>
                </small>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!--<xsl:template match="t:ab>
    <xsl:element name="text-part">
      <xsl:attribute name="class">ab<xsl:attribute>
     <xsl:apply-templates/>
    </xsl:element>
  </xsl:template> -->




    <xsl:template match="t:unclear">
        <span class="unclear">
            <xsl:value-of select="."/>
        </span>
    </xsl:template>

    <!--- functions -->

    <xsl:template name="footer">
        <xsl:param name="style" select="'plain'"/>
        <div class="stdfooter alpheiosignore" id="citation">
            <hr/>
            <address>
                <xsl:call-template name="copyrightStatement"/>
            </address>
        </div>
        <div class="alpheios-ignore">
            <xsl:call-template name="funder"/>
            <xsl:call-template name="publicationStatement"/>
        </div>
    </xsl:template>
    <xsl:template name="funder">
        <xsl:if test="//tei:titleStmt/tei:funder">
            <div class="perseus-funder">
                <xsl:value-of select="//tei:titleStmt/tei:funder"/>
                <xsl:text> provided support for entering this text.</xsl:text>
            </div>
        </xsl:if>
        <xsl:if test="//tei:titlestmt/tei:funder">
            <div class="perseus-funder">
                <xsl:value-of select="//tei:titlestmt/tei:funder"/>
                <xsl:text> provided support for entering this text.</xsl:text>
            </div>
        </xsl:if>
    </xsl:template>
    <xsl:template name="publicationStatement">
        <xsl:if
            test="//tei:publicationStmt/tei:publisher/text() or //tei:publicationStmt/tei:pubPlace/text() or //tei:publicationStmt/tei:authority/text()">
            <div class="perseus-publication">XML for this text provided by <span class="publisher">
                    <xsl:value-of select="//tei:publicationStmt/tei:publisher"/>
                </span>
                <span class="pubPlace">
                    <xsl:value-of select="//tei:publicationStmt/tei:pubPlace"/>
                </span>
                <span class="authority">
                    <xsl:value-of select="//tei:publicationStmt/tei:authority"/>
                </span>
            </div>
        </xsl:if>
        <xsl:if
            test="//tei:publicationstmt/tei:publisher/text() or //tei:publicationstmt/tei:pubplace/text() or //tei:publicationstmt/tei:authority/text()">
            <div class="perseus-publication">XML for this text provided by <span class="publisher">
                    <xsl:value-of select="//tei:publicationstmt/tei:publisher"/>
                </span>
                <span class="pubPlace">
                    <xsl:value-of select="//tei:publicationstmt/tei:pubPlace"/>
                </span>
                <span class="authority">
                    <xsl:value-of select="//tei:publicationstmt/tei:authority"/>
                </span>
            </div>
        </xsl:if>
    </xsl:template>
    <xsl:template name="copyrightStatement">
        <xsl:call-template name="source-desc"/>
        <div class="rights_info">
            <xsl:call-template name="rights_cc"/>
        </div>
    </xsl:template>
    <xsl:template name="rights_cc">
        <p class="cc_rights">
            <xsl:choose>
                <xsl:when test="false()">
                    <xsl:copy-of select="TODO"/>
                </xsl:when>
                <xsl:otherwise>
                    <!--Creative Commons License--> This work is licensed under a <a rel="license"
                        href="http://creativecommons.org/licenses/by-sa/3.0/us/">Creative Commons
                        Attribution-Share Alike 3.0 United States License</a>.
                    <!--/Creative Commons License-->
                </xsl:otherwise>
            </xsl:choose>
        </p>
    </xsl:template>

    <xsl:template name="separate_words">
        <xsl:param name="real_id"/>
        <xsl:param name="id_list"/>
        <xsl:param name="nrefs"/>
        <xsl:param name="tbrefs"/>
        <xsl:param name="tbref"/>
        <xsl:param name="delimiter" select="' '"/>
        <xsl:variable name="newlist">
            <xsl:choose>
                <xsl:when test="contains($id_list, $delimiter)">
                    <xsl:value-of select="normalize-space($id_list)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="concat(normalize-space($id_list), $delimiter)"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:variable name="first" select="substring-before($newlist, $delimiter)"/>
        <xsl:variable name="remaining" select="substring-after($newlist, $delimiter)"/>
        <xsl:variable name="highlightId">
            <xsl:call-template name="ref_to_id">
                <!--xsl:with-param name="list" select="$highlightWord"/-->
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="highlight">
            <!--xsl:if test="$highlightWord  and (($first = $highlightId) or ($highlightWord = $real_id)) ">
             alpheios-highlighted-word
         </xsl:if-->
        </xsl:variable>
        <xsl:element name="span">
            <xsl:attribute name="class">w alpheios-word <xsl:value-of select="$highlight"/>
            </xsl:attribute>
            <xsl:attribute name="id">
                <xsl:value-of select="$first"/>
            </xsl:attribute>
            <xsl:attribute name="nrefs">
                <xsl:value-of select="$nrefs"/>
            </xsl:attribute>
            <xsl:choose>
                <xsl:when test="@tbrefs">
                    <xsl:attribute name="tbrefs">
                        <xsl:value-of select="@tbrefs"/>
                    </xsl:attribute>
                </xsl:when>
                <xsl:when test="@tbref">
                    <xsl:attribute name="tbref">
                        <xsl:value-of select="@tbref"/>
                    </xsl:attribute>
                </xsl:when>
                <xsl:when test="@ana">
                    <xsl:attribute name="tbref">
                        <xsl:value-of select="@ana"/>
                    </xsl:attribute>
                    <xsl:variable name="urn" select="ancestor::tei:body/@n"/>
                    <xsl:variable name="docref">
                        <xsl:choose>
                            <xsl:when test="contains($urn, 'latinLit')">
                                <xsl:value-of select="substring-after($urn, 'urn:cts:latinLit:')"/>
                            </xsl:when>
                            <xsl:when test="contains($urn, 'greekLit')">
                                <xsl:value-of select="substring-after($urn, 'urn:cts:greekLit:')"/>
                            </xsl:when>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:attribute name="data-alpheios_tb_ref">
                        <xsl:value-of select="concat($docref, '#', @ana)"/>
                    </xsl:attribute>
                </xsl:when>
            </xsl:choose>
            <xsl:apply-templates/>
        </xsl:element>
        <xsl:if test="$remaining">
            <xsl:value-of select="$delimiter"/>
            <xsl:call-template name="separate_words">
                <xsl:with-param name="id_list" select="$remaining"/>
                <xsl:with-param name="nrefs" select="$nrefs"/>
                <xsl:with-param name="tbrefs" select="$tbrefs"/>
                <xsl:with-param name="tbref" select="$tbref"/>
                <xsl:with-param name="delimiter">
                    <xsl:value-of select="$delimiter"/>
                </xsl:with-param>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    <xsl:template name="ref_to_id">
        <xsl:param name="list"/>
        <xsl:param name="delimiter" select="' '"/>
        <xsl:if test="$list">
            <xsl:variable name="newlist">
                <xsl:choose>
                    <xsl:when test="contains($list, $delimiter)">
                        <xsl:value-of select="normalize-space($list)"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="concat(normalize-space($list), $delimiter)"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="first" select="substring-before($newlist, $delimiter)"/>
            <xsl:variable name="remaining" select="substring-after($newlist, $delimiter)"/>
            <xsl:variable name="sentence" select="substring-before($first, '-')"/>
            <xsl:variable name="word" select="substring-after($first, '-')"/>
            <xsl:text>s</xsl:text>
            <xsl:value-of select="$sentence"/>
            <xsl:text>_w</xsl:text>
            <xsl:value-of select="$word"/>
            <xsl:if test="$remaining">
                <xsl:value-of select="$delimiter"/>
                <xsl:call-template name="ref_to_id">
                    <xsl:with-param name="list" select="$remaining"/>
                    <xsl:with-param name="delimiter">
                        <xsl:value-of select="$delimiter"/>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:if>
        </xsl:if>
    </xsl:template>

    <!-- taken from perseus'  tei2p4.xsl -->
    <xsl:template name="source-desc">
        <xsl:variable name="sourceText">
            <xsl:for-each select="//tei:sourceDesc/descendant::*[name(.) != 'author']/text()">
                <xsl:variable name="normalized" select="normalize-space(.)"/>
                <xsl:value-of select="$normalized"/>
                <!-- Print a period after each text node, unless the current node
                    ends in a period -->
                <xsl:if
                    test="$normalized != '' and not(contains(substring($normalized, string-length($normalized)), '.'))">
                    <xsl:text>.</xsl:text>
                </xsl:if>
                <xsl:if test="position() != last()">
                    <xsl:text> </xsl:text>
                </xsl:if>
            </xsl:for-each>
            <xsl:for-each select="//tei:sourcedesc/descendant::*[name(.) != 'author']/text()">
                <xsl:variable name="normalized" select="normalize-space(.)"/>
                <xsl:value-of select="$normalized"/>
                <!-- Print a period after each text node, unless the current node
                    ends in a period -->
                <xsl:if
                    test="$normalized != '' and not(contains(substring($normalized, string-length($normalized)), '.'))">
                    <xsl:text>.</xsl:text>
                </xsl:if>
                <xsl:if test="position() != last()">
                    <xsl:text> </xsl:text>
                </xsl:if>
            </xsl:for-each>
        </xsl:variable>
        <xsl:if test="string-length(normalize-space($sourceText)) &gt; 0">
            <span class="source-desc">
                <xsl:value-of select="$sourceText"/>
            </span>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>
