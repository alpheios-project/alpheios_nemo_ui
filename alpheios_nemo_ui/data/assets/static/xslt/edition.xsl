<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:t="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="t">
    
    <!-- glyphs -->
    <xsl:template name="split-refs">
        <xsl:param name="pText"/>
        <xsl:if test="string-length($pText)">
            <xsl:if test="not($pText=.)">
                <xsl:text> </xsl:text>
            </xsl:if>
            <xsl:element name="a">
                <xsl:attribute name="href">
                    <xsl:value-of select="concat('http://cts.perseids.org/api/cts/?request=GetPassage', '&#38;', 'urn=', substring-before(concat($pText,','),','))"/>
                </xsl:attribute>
                <xsl:attribute name="target">_blank</xsl:attribute>
                <xsl:value-of select="substring-before(concat($pText,','),',')" />
            </xsl:element>
            <xsl:call-template name="split-refs">
                <xsl:with-param name="pText" select=
                    "substring-after($pText, ',')"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>

    <xsl:template match="//t:div[@type = 'translation']">
    <div>
      <xsl:attribute name="id">
        <xsl:text>translation</xsl:text>
        <xsl:if test="@xml:lang"><xsl:text>_</xsl:text></xsl:if>
        <xsl:value-of select="@xml:lang"/>
      </xsl:attribute>
      
      <xsl:attribute name="class">
        <xsl:text>translation lang_</xsl:text>
        <xsl:value-of select="@xml:lang"/>
      </xsl:attribute>
      
      
      <xsl:apply-templates/>
    
    </div>
  </xsl:template>
    
    <xsl:template match="t:w">
        <xsl:element name="span">
            <xsl:attribute name="class">w</xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="t:pc">
        <xsl:element name="span">
            <xsl:attribute name="class">
                <xsl:text>pc_</xsl:text>
                <xsl:value-of select="@unit|@type"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="//t:div[@type = 'commentary']">
    <div>
      <xsl:attribute name="id">
        <xsl:text>commentary</xsl:text>
        <xsl:if test="@xml:lang"><xsl:text>_</xsl:text></xsl:if>
        <xsl:value-of select="@xml:lang"/>
      </xsl:attribute>
      
      <xsl:attribute name="class">
        <xsl:text>commentary lang_</xsl:text>
        <xsl:value-of select="@xml:lang"/>
      </xsl:attribute>
      
      
      <xsl:apply-templates/>
    
    </div>
  </xsl:template>
    
    <xsl:template match="t:div[@type = 'edition']">
        <div id="edition">
            <xsl:attribute name="class">
                <xsl:text>edition lang_</xsl:text>
                <xsl:value-of select="@xml:lang"/>
            </xsl:attribute>
            <xsl:attribute name="data-lang"><xsl:value-of select="./@xml:lang"/></xsl:attribute>
            <xsl:if test="@xml:lang = 'heb'">
                <xsl:attribute name="dir">
                    <xsl:text>rtl</xsl:text>
                </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <xsl:template match="t:div[@type = 'textpart']">
        <xsl:element name="div">
            <xsl:attribute name="class">
                <xsl:value-of select="@subtype" />
            </xsl:attribute>
            <xsl:apply-templates select="@urn" />
            <xsl:if test="./@sameAs">
               <xsl:element name="p">
                   <xsl:element name="small">
                       <xsl:text>Sources </xsl:text>
                       <xsl:choose>
                           <xsl:when test="@cert = 'low'">
                               <xsl:text>(D'après)</xsl:text>
                           </xsl:when>
                       </xsl:choose>
                       <xsl:text> : </xsl:text>
                       <xsl:call-template name="split-refs">
                           <xsl:with-param name="pText" select="./@sameAs"/>
                       </xsl:call-template>
                   </xsl:element>
               </xsl:element>
            </xsl:if>
            <xsl:choose>
                <xsl:when test="child::t:l">
                    <ol><xsl:apply-templates /></ol>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="t:l">
        <xsl:element name="li">
            <xsl:apply-templates select="@urn" />
            <xsl:attribute name="value"><xsl:value-of select="@n"/></xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="t:lg">
        <xsl:element name="ol">
            <xsl:apply-templates select="@urn" />
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="t:pb">
        <div class='pb'><xsl:value-of select="@n"/></div>
    </xsl:template>
    
    <xsl:template match="t:ab/text()">
        <xsl:value-of select="." />
    </xsl:template>
    
    
    <xsl:template match="t:p">
        <p>
            <xsl:apply-templates select="@urn" />
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    
    <xsl:template match="t:lb" />
    
    
    <xsl:template match="t:ex">
        <span class="ex">
            <xsl:text>(</xsl:text><xsl:value-of select="." /><xsl:text>)</xsl:text>
        </span>
    </xsl:template>
    
    <xsl:template match="t:abbr">
        <span class="abbr">
            <xsl:text></xsl:text><xsl:value-of select="." /><xsl:text></xsl:text>
        </span>
    </xsl:template>  
    
    <xsl:template match="t:gap">
        <span class="gap">
            <xsl:choose>
                <xsl:when test="@quantity and @unit='character'">
                    <xsl:value-of select="string(@quantity)" />
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>---</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            
        </span>
    </xsl:template>
    
    <xsl:template match="t:head">
        <h3 class="head"><xsl:apply-templates />
            <xsl:apply-templates select="@urn" /></h3>
    </xsl:template>
    
    <xsl:template match="@urn">
        <xsl:attribute name="data-urn"><xsl:value-of select="."/>/></xsl:attribute>
    </xsl:template>
    
    <xsl:template match="t:sp">
        <section class="speak">
            <xsl:if test="./t:speaker">
                <em><xsl:value-of select="./t:speaker/text()" /></em>
            </xsl:if>
            <xsl:choose>
                <xsl:when test="./t:lg">
                    <xsl:apply-templates select="./t:lg" />
                </xsl:when>
                <xsl:when test="./t:p">
                    <xsl:apply-templates select="./t:p" />
                </xsl:when>
                <xsl:otherwise>
                    <ol>
                        <xsl:apply-templates select="./t:l"/>
                    </ol>
                </xsl:otherwise>
            </xsl:choose>
        </section>
    </xsl:template>
    
    <xsl:template match="t:supplied">
        <span>
            <xsl:attribute name="class">supplied supplied_<xsl:value-of select='@cert' /></xsl:attribute>
            <xsl:text>[</xsl:text>
            <xsl:apply-templates/><xsl:if test="@cert = 'low'"><xsl:text>?</xsl:text></xsl:if>
            <xsl:text>]</xsl:text>
        </span>
    </xsl:template>  
    
    <xsl:template match="t:note">
        <span class="note"><a href="#">[*]</a><span class="note-content"><xsl:text>(</xsl:text><xsl:value-of select="." /><xsl:text>)</xsl:text></span></span>
    </xsl:template>
    
    <xsl:template match="t:ref">
        <a class="urn">
            <xsl:attribute name="href">
                <xsl:value-of select="@target"/>
            </xsl:attribute>
            <xsl:value-of select="." />
            [*]
        </a>
    </xsl:template>
    
    <xsl:template match="t:choice">
        <span class="choice">
            <xsl:attribute name="title">
                <xsl:value-of select="reg" />
            </xsl:attribute>
            <xsl:value-of select="orig" /><xsl:text> </xsl:text>
        </span>
    </xsl:template>
    
    <xsl:template match="t:unclear">
        <span class="unclear"><xsl:value-of select="." /></span>
    </xsl:template>
    
    
</xsl:stylesheet>
