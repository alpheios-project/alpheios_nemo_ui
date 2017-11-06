<?xml version="1.0" encoding="UTF-8"?>
<!--
This Stylesheets are no replacement for the real and far mor sophisticated Stylsheets, wich you can find unter http://sourceforge.net/p/epidoc/wiki/Stylesheets/.
But they are away to get the Epidoc (currently only the edition and the translation part) rendered in a more or less satisfying way using only XSLT 1.0 and PHP.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:php="http://php.net/xsl"  xmlns:t="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="php">
    
    
 <xsl:output xml:space="default"/>

  <!-- glyphs -->
  <xsl:include href="teig.xsl" />
  
  <!-- edition -->
  <xsl:include href="edition.xsl" />

  <!--
  others: just remove for now
	  <xsl:include href="teiHeader.xsl" />
	  <xsl:include href="facsimile.xsl" />
	  <xsl:include href="text.xsl" />
	-->
</xsl:stylesheet>