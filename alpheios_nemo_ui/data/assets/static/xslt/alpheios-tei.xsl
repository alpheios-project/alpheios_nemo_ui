<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
    
    <!-- shared functionality for converting TEI documents to Alpheios Enhanced Display -->
    <xsl:param name="htmlTitlePrefix" select="'Alpheios:'"/>
    
    <!-- generates the title for the html document from the teiHeader elements -->
    <xsl:template name="generateAlpheiosTitle">
        <xsl:variable name="myName">
            <xsl:value-of select="local-name(.)"/>
        </xsl:variable>
        <xsl:value-of select="$htmlTitlePrefix"/>
        <xsl:if test="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/text()">
            <xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author"/>
            <xsl:text>, </xsl:text>
        </xsl:if>
        <xsl:if test="//tei:teiheader/tei:filedesc/tei:titlestmt/tei:author/text()">
            <xsl:value-of select="//tei:teiheader/tei:filedesc/tei:titlestmt/tei:author"/>
            <xsl:text>, </xsl:text>
        </xsl:if>
        <xsl:variable name="title">
            <xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
            <xsl:value-of select="//tei:teiheader/tei:filedesc/tei:titlestmt/tei:title"/>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test="contains($title,'.')">
                <xsl:value-of select="substring-before($title,'.')"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$title"/>
                <xsl:if test="$myName='div2' and @n">
                    (<xsl:value-of select="@n"/>)
                </xsl:if>
                <xsl:if test="$myName='div2' and @alpheios-subtitle">
                    - <xsl:value-of select="@alpheios-subtitle"/>
                </xsl:if>
                <xsl:text> </xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- generates the title for display within the page from the teiHeader elements -->
    <xsl:template name="generateAlpheiosTitleHtml">
        <h1>
            <xsl:variable name="author" select="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author"/>
            <xsl:if test="$author">
                <span class="author">
                    <xsl:value-of select="$author"/>, </span>
            </xsl:if>
            <xsl:variable name="myName">
                <xsl:value-of select="local-name(.)"/>
            </xsl:variable>
            <span class="title">
                <xsl:variable name="title">
                    <xsl:value-of select="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/>
                    <xsl:value-of select="//tei:teiheader/tei:filedesc/tei:titlestmt/tei:title"/>
                </xsl:variable>
                <xsl:choose>
                    <xsl:when test="contains($title,'.')">
                        <xsl:value-of select="substring-before($title,'.')"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="$title"/>
                        <xsl:if test="$myName='div2' and @n">
                            <span class="sectionid"> (<xsl:value-of select="@n"/>)</span>
                        </xsl:if>
                        <xsl:if test="$myName='div2' and @alpheios-subtitle">
                            <span class="subtitle"> - <xsl:value-of select="@alpheios-subtitle"/>
                            </span>
                        </xsl:if>
                        <xsl:if test="$myName='div2' and head">
                            <span class="subtitle"> - <xsl:value-of select="head"/>
                            </span>
                        </xsl:if>
                    </xsl:otherwise>
                </xsl:choose>
            </span>
            <xsl:if test="//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/text()">
                <a id="alph-citation-links" href="#citation" title="Citation">
                    <img id="alph-citation-icon" src="../image/citation_static.gif" alt="Citation"/>
                </a>
            </xsl:if>
            <xsl:if test="//tei:teiheader/tei:filedesc/tei:titlestmt/tei:author/text()">
                <a id="alph-citation-links" href="#citation" title="Citation">
                    <img id="alph-citation-icon" src="../image/citation_static.gif" alt="Citation"/>
                </a>
            </xsl:if>
        </h1>
    </xsl:template>
</xsl:stylesheet>