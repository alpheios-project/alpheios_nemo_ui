<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:php="http://php.net/xsl" exclude-result-prefixes="php">
  <xsl:template match="//g">
    <xsl:choose>
      <xsl:when test="@type='crux' or @type='cross'">
        <xsl:text>†</xsl:text>
      </xsl:when>
      <xsl:when test="@type='crosses'">
        <xsl:text>††</xsl:text>
      </xsl:when>
      <xsl:when test="@type='drachma'">
        <xsl:text>₯</xsl:text>
      </xsl:when>
      <xsl:when test="@type='year'">
        <xsl:text>L</xsl:text>
      </xsl:when>
      <xsl:when test="@type='stop'">
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
      <xsl:when test="@type='apostrophe'">
        <xsl:text>’</xsl:text>
      </xsl:when>
      <xsl:when test="@type='check' or @type='check-mark'">
        <xsl:text>／</xsl:text>
      </xsl:when>
      <xsl:when test="@type='chirho'">
        <xsl:text>☧</xsl:text>
      </xsl:when>
      <xsl:when test="@type='dash'">
        <xsl:text>—</xsl:text>
      </xsl:when>
      <xsl:when test="@type='dipunct'">
        <xsl:text>∶</xsl:text>
      </xsl:when>
      <xsl:when test="@type='filled-circle'">
        <xsl:text>⦿</xsl:text>
      </xsl:when>
      <xsl:when test="@type='filler' and @rend='extension'">
        <xsl:text>―</xsl:text>
      </xsl:when>
      <xsl:when test="@type='latin-interpunct' or @type='middot' or @type='mid-punctus'">
        <xsl:text>·</xsl:text>
      </xsl:when>
      <xsl:when test="@type='monogram'">
        <span class="italic">
          <xsl:text>monogr.</xsl:text>
        </span>
      </xsl:when>
      <xsl:when test="@type='upper-brace-opening'">
        <xsl:text>⎧</xsl:text>
      </xsl:when>
      <xsl:when test="@type='center-brace-opening'">
        <xsl:text>⎨</xsl:text>
      </xsl:when>
      <xsl:when test="@type='lower-brace-opening'">
        <xsl:text>⎩</xsl:text>
      </xsl:when>
      <xsl:when test="@type='upper-brace-closing'">
        <xsl:text>⎫</xsl:text>
      </xsl:when>
      <xsl:when test="@type='center-brace-closing'">
        <xsl:text>⎬</xsl:text>
      </xsl:when>
      <xsl:when test="@type='lower-brace-closing'">
        <xsl:text>⎭</xsl:text>
      </xsl:when>
      <xsl:when test="@type='parens-upper-opening'">
        <xsl:text>⎛</xsl:text>
      </xsl:when>
      <xsl:when test="@type='parens-middle-opening'">
        <xsl:text>⎜</xsl:text>
      </xsl:when>
      <xsl:when test="@type='parens-lower-opening'">
        <xsl:text>⎝</xsl:text>
      </xsl:when>
      <xsl:when test="@type='parens-upper-closing'">
        <xsl:text>⎞</xsl:text>
      </xsl:when>
      <xsl:when test="@type='parens-middle-closing'">
        <xsl:text>⎟</xsl:text>
      </xsl:when>
      <xsl:when test="@type='parens-lower-closing'">
        <xsl:text>⎠</xsl:text>
      </xsl:when>
      <xsl:when test="@type = 'rho-cross'">
        <xsl:text>⳨</xsl:text>
      </xsl:when>
      <xsl:when test="@type='slanting-stroke'">
        <xsl:text>/</xsl:text>
      </xsl:when>
      <xsl:when test="@type='stauros'">
        <xsl:text>†</xsl:text>
      </xsl:when>
      <xsl:when test="@type='tachygraphic marks'">
        <span class="italic">
          <xsl:text>tachygr. marks</xsl:text>
        </span>
      </xsl:when>
      <xsl:when test="@type='tripunct'">
        <xsl:text>⋮</xsl:text>
      </xsl:when>
      <xsl:when test="@type='double-vertical-bar'">
        <xsl:text>‖</xsl:text>
      </xsl:when>
      <xsl:when test="@type='long-vertical-bar'">
        <xsl:text>|</xsl:text>
      </xsl:when>
      <xsl:when test="@type='x'">
        <xsl:text>☓</xsl:text>
      </xsl:when>
      <xsl:when test="@type='xs'">
        <xsl:text>☓</xsl:text>
        <xsl:text>☓</xsl:text>
        <xsl:text>☓</xsl:text>
        <xsl:text>☓</xsl:text>
        <xsl:text>☓</xsl:text>
      </xsl:when>
      <xsl:when test="@type='milliaria'">
        <xsl:text>ↀ</xsl:text>
      </xsl:when>
      <xsl:when test="@type='leaf'">
        <xsl:text>❦</xsl:text>
      </xsl:when>
      <xsl:when test="@type='palm'">
        <xsl:text>††</xsl:text>
      </xsl:when>
      <xsl:when test="@type='star'">
        <xsl:text>*</xsl:text>
      </xsl:when>
      <xsl:when test="@type='interpunct'">
        <xsl:text>·</xsl:text>
      </xsl:when>
      <xsl:when test="@type='sestertius'">
        <xsl:text>𐆘</xsl:text>
      </xsl:when>
      <xsl:when test="@type='denarius'">
        <xsl:text>𐆖</xsl:text>
      </xsl:when>
      <xsl:when test="@type='barless-A'">
        <xsl:text>Λ</xsl:text>
      </xsl:when>
      <xsl:when test="@type='dot'">
        <xsl:text>.</xsl:text>
      </xsl:when>
      <xsl:when test="@type='stop'">
        <xsl:text>•</xsl:text>
      </xsl:when>
      <xsl:when test="@type='crux' or @type='cross'">
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
</xsl:stylesheet>
